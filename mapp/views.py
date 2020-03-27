from django.shortcuts import render,HttpResponseRedirect
import json
from django.http import JsonResponse,FileResponse
from django.urls import reverse
# Create your views here.
from .models import Datos
from django.views.decorators.csrf import csrf_exempt
import os 
from django.contrib.auth import authenticate, login,logout

from .forms import ImageUploadForm

from mapanimales.settings import MEDIA_URL

# lo que sigue extraemos de flask del proyecto ganaderia

from PIL import Image   #para manejar imagenes

import platform 

# total de horas trabajadas hasta el momento: 18 hs
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


def inicio(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    datos_adopciones=consulta_datos()
    print(datos_adopciones)
    print('informacino el SO' )
    print(platform.platform()  )
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

def muestra_datos(request):
    # para ver el mapa de los adoptados no hace falta que estees logueado
    datos_adopciones=consulta_datos()
    print(datos_adopciones)
    lista=[ ]
    for item in datos_adopciones:
        cada_dato={ "id":item.identificativo  , "nombre": item.nombre, "apellido": item.apellido,
                    "sexo": item.sexo, "animal": item.animal,"descripcion": item.descripcion,
                      "ubicacion": {"latitud": item.latitud,
                                     "longitud": item.longitud
                                    }}
        lista.append(cada_dato) # agregamos a la lista

    data = {"data": lista} # al final enviamos esto 
    
    return render(request, "muestra.html", data) 





@csrf_exempt
def solicitud(request):
    """
    solicitud ajax para verificar id
    """
    if not request.user.is_authenticated:
        return render(request,'login.html')
    if request.method == 'POST':
        datos_a_guardar= Datos() # instanciamos la clase Datos
        #procesamos la imagen aca

        #form = ImageUploadForm(request.POST, request.FILES)
        #if form.is_valid():
            #print('formulario valido')
        
        #datos_a_guardar.imagen = form.cleaned_data.get('imagen') 
        #

        #f = request.FILES['imagen'] #solicitamos al post el archivo
        #filename = 'nombre'   #lo llamamos a la imagen con el nombre de la id para poder relacionar
                # Guardamos el archivo en el directorio "Archivos"
        #print ("El nombre del archivo es ", filename)
        #ruta=os.path.join(MEDIA_URL, filename)
        #f.save(ruta)
        datos= request.POST
        print("datos del post: ")
        print(datos)
        datos.id=Datos.identificativo 
        nombre = datos.get('nombre')
        apellido=datos.get('apellido')
        edad=datos.get('edad')
        fecha= datos.get('fecha')
        descripcion= datos.get('descripcion')
        edad_animal=  datos.get('edad_animal')
        animal=datos.get('animal')
        sexo=datos.get('sexo')
        cant_animales=datos.get('cant_animales')
        latitud= datos.get('latitud')
        longitud= datos.get('longitud')
        imagen=datos.get('imagen')
        print("+++++++++++++++++++++++")
        print(nombre,apellido,edad,sexo,animal,cant_animales, latitud,longitud)
        #una vez obtenidos los datos, debemos de guardarlos, 
        # creo que hay una forma de guardar directamente un 
        # pero es lo mas rapido que se me ocurrio 
         #instanciamos la clase datos para luego crear el objeto datos_a_guardar
        datos_a_guardar.nombre=nombre
        datos_a_guardar.apellido=apellido
        datos_a_guardar.edad=edad
        datos_a_guardar.fecha= fecha
        datos_a_guardar.descripcion=descripcion
        datos_a_guardar.animal=animal
        datos_a_guardar.sexo=sexo
        datos_a_guardar.edad_animal=edad_animal
        datos_a_guardar.cant_animales=cant_animales
        datos_a_guardar.latitud=latitud
        datos_a_guardar.longitud=longitud
        datos_a_guardar.imagen=request.FILES
        datos_a_guardar.save() # guardamos los valores 
        data = {
        }
        data['message'] = 'Agregado correctamente'
    else:
        data['message']="Error, no me enviaste nada"
    return JsonResponse(data)# respondemos con un mensaje


def consulta_datos():
    todos= Datos.objects.all()
    return todos

def cantidad_total_adoptados():
    cant= len(consulta_datos()  ) # devuelve la longitud de la lista
    return cant 