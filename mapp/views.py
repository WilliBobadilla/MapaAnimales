from django.shortcuts import render,HttpResponseRedirect
import json
from django.http import JsonResponse,FileResponse
from django.urls import reverse
# Create your views here.
from .models import Datos,Datos_adopcion,Datos_extravio
from django.views.decorators.csrf import csrf_exempt
import os 
from django.contrib.auth import authenticate, login,logout

from .forms import UploadImageForm

from mapanimales.settings import MEDIA_URL
from django.core.files.storage import FileSystemStorage
# lo que sigue extraemos de flask del proyecto ganaderia
from mapanimales import settings

import platform 
from ipware import get_client_ip  # para manejar las ips, ante la solicitud de un animal perdido
# total de horas trabajadas hasta el momento: 24 hs
def solcitud_login(request):
    """
    Aca se manejan las solicitudes de login 
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    print("el usuario es: ", user )
    if user is not None and user.is_active: 
        login(request,user)
        return HttpResponseRedirect(reverse("inicio"))
    return render(request,'login.html',{'mensaje':"Credenciales invalidas  "})

def index(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    else:
        return HttpResponseRedirect(reverse("inicio"))

def logout_request(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

def home(request):
    """
    is not necesary to be loged
    """
    datos=Datos_adopcion.objects.all()# de todo esto solo selecionamos los primeros 6 
    if len(datos)>6: 
        datos= datos[0:6] # solo los primeros 6
    dic= {
        "data":datos
    }
    print(dic)
    return render( request, 'index.html',dic)

def inicio_mapa(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    datos_adopciones=consulta_datos()

    lista=[ ]
    for item in datos_adopciones:
        cada_dato={"id":item.identificativo ,"nombre": item.nombre, "apellido": item.apellido,
                    "sexo": item.sexo, "animal": item.animal,"descripcion": item.descripcion,
                      "ubicacion": {"latitud": item.latitud,
                                     "longitud": item.longitud
                                    }}
        lista.append(cada_dato) # agregamos a la lista

    data = {"data": lista} # al final enviamos esto 
    
    return render(request, "mapanuevo.html", data)

def perdidos_mapa(request):
    """
    Vista donde se renderizan en un mapa los animalitos perdidos
    """
    datos_adopciones=Datos_extravio.objects.all()
    lista=[ ]
    cantidad_encontrados= len(Datos_extravio.objects.filter(encontrado=True))
    for item in datos_adopciones:
        cada_dato={"id":item.identificativo ,"fecha": str(item.fecha), "nombre": item.nombre_animal,
                    "sexo": item.sexo, "animal": item.animal,"descripcion": item.descripcion,
                    "link":item.imagen.url ,"extraviado":str(item.encontrado),
                    "telefono":item.numero_telefono_persona,  
                    "nombre":item.nombre_publicador,
                    "apellido":item.apellido_publicador,              
                    "ubicacion": {"latitud": item.latitud_perdido,
                                    "longitud": item.longitud_perdido
                                    }}
        lista.append(cada_dato) # agregamos a la lista
    data = {"data": lista,"cant_encontrados":cantidad_encontrados} # al final enviamos esto 
    return render(request, "perdidos.html", data)


def perdidos_form(request):
    """
    vista donde se maneja el post, se debe estar logueado
    """
    if not request.user.is_authenticated:
        return render(request,'login.html')
    if request.method=='POST':
        posteo=request.POST #cargamos primero aca 
        datos_a_guardar= Datos_extravio(fecha=posteo.get('fecha'),descripcion=posteo.get('descripcion'),nombre_animal=posteo.get('nombre'), animal=posteo.get('tipo'),sexo=posteo.get('select_sexo'),
        edad_animal=posteo.get('edad_animal'),numero_telefono_persona=int(posteo.get('numero_telefono')),
        latitud_perdido=float(posteo.get('latitud')),longitud_perdido=float(posteo.get('longitud')),
         encontrado=False,nombre_publicador=request.user.first_name,
         apellido_publicador= request.user.last_name) #  instanciamos la clase Datos_extravio
        imagen=UploadImageForm(request.POST, request.FILES)
        if imagen.is_valid():
            datos_a_guardar.imagen=imagen.cleaned_data['imagen']
            datos_a_guardar.save()
        return render(request, "formulario_perdidos.html")
    else: 
        return render(request, "formulario_perdidos.html")



def muestra_datos(request):
    # para ver el mapa de los adoptados no hace falta que estees logueado
    datos_adopciones=consulta_datos()
    print(datos_adopciones)
    lista=[ ]
    for item in datos_adopciones:
        link= item.imagen.url   
        print(link)
        cada_dato={ "id":item.identificativo, "nombre": item.nombre, "apellido": item.apellido,"url":link,
                    "sexo": item.sexo, "animal": item.animal,"descripcion": item.descripcion,
                      "ubicacion": {"latitud": item.latitud,
                                     "longitud": item.longitud
                                    }}
        lista.append(cada_dato) # agregamos a la lista

    data = {"data": lista,"cantidad_adoptados":len(datos_adopciones)} # al final enviamos esto 
    
    return render(request, "muestra.html", data) 



def formulario_posteo(request):
    """
    Utilizado para publicar nuevos animales \n
    en la pagina principal 
    """
    if not request.user.is_authenticated:
        return render(request,'login.html')
    if request.method=='POST':
        posteo=request.POST #caragamos primero aca 
        print(posteo.get('numero_telefono'))
        datos_a_guardar= Datos_adopcion(descripcion=posteo.get('descripcion'),animal=posteo.get('select_animal'),sexo=posteo.get('select_sexo'),
        edad_animal=int(posteo.get('edad_animal')),numero_telefono_persona=str(posteo.get('numero_telefono')),
        latitud_persona=float(posteo.get('latitud')),longitud_persona=float(posteo.get('longitud'))) # instanciamos la clase Datos
        
        imagen=UploadImageForm(request.POST, request.FILES)
        if imagen.is_valid():
            datos_a_guardar.imagen=imagen.cleaned_data['imagen']
            datos_a_guardar.save()
        return render(request,"formulario_posteo.html")
    else: 
        return render(request,"formulario_posteo.html")

def solicitud(request):
    """
    vista donde se procesa datos de un nuevo animal adoptado
    """
    if not request.user.is_authenticated:
        return render(request,'login.html')
    if request.method == 'POST':
        datos_a_guardar= Datos() # instanciamos la clase Datos
        datos= request.POST
        todos=consulta_datos() # para tener el ultimo id
        print("todos los datos", todos)
        try:
            ultimo_id= cantidad_total_adoptados() +1 
            print("ultimo id", ultimo_id)
        except:
            ultimo_id=1
        datos.id=ultimo_id  # le asignamos este id 
        #imagenes tratamiento
        #nombre_archivo= datos.get('identificativo') 
        imagen=UploadImageForm(request.POST, request.FILES)
        if imagen.is_valid():
            datos_a_guardar.imagen=imagen.cleaned_data['imagen']
        #una vez obtenidos los datos, debemos de guardarlos, 
        # creo que hay una forma de guardar directamente un 
        # pero es lo mas rapido que se me ocurrio 
         #instanciamos la clase datos para luego crear el objeto datos_a_guardar
        datos_a_guardar.nombre=datos.get('nombre')
        datos_a_guardar.apellido= datos.get('apellido')
        datos_a_guardar.edad=datos.get('edad')
        datos_a_guardar.fecha= datos.get('fecha')
        datos_a_guardar.descripcion=datos.get('descripcion')
        datos_a_guardar.animal=datos.get('select_animal')
        datos_a_guardar.sexo=datos.get('select_sexo')
        datos_a_guardar.edad_animal=datos.get('edad_animal')
        datos_a_guardar.cant_animales=datos.get('cant_animales')
        datos_a_guardar.latitud=float(datos.get('latitud')) # conversion a flotante 
        datos_a_guardar.longitud=float(datos.get('longitud'))
        
        datos_a_guardar.save() # guardamos los valores 
        data = {
        }
        data['message'] = 'Agregado correctamente'
    else:
        data['message']="Error, no me enviaste nada"
    return render(request,"mensaje.html",data )# respondemos con un mensaje


def publicar_animal(requests):
    """
    Utilizado para publicar nuevos animales \n
    en la pagina principal 
    """
    pass


def consulta_datos():
    todos= Datos.objects.all()
    return todos

def cantidad_total_adoptados():
    cant= len(consulta_datos()  ) # devuelve la longitud de la lista
    return cant 