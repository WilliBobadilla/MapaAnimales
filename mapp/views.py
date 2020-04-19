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
from django.core.files.storage import FileSystemStorage
# lo que sigue extraemos de flask del proyecto ganaderia
from mapanimales import settings
from PIL import Image   #para manejar imagenes

import platform 

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
        #link= "file://"+settings.BASE_DIR +"/media/" + str(item.imagen)
        link= item.imagen.url   
        print(link)
        cada_dato={ "id":item.identificativo  , "nombre": item.nombre, "apellido": item.apellido,"url":link,
                    "sexo": item.sexo, "animal": item.animal,"descripcion": item.descripcion,
                      "ubicacion": {"latitud": item.latitud,
                                     "longitud": item.longitud
                                    }}
        lista.append(cada_dato) # agregamos a la lista

    data = {"data": lista} # al final enviamos esto 
    
    return render(request, "muestra.html", data) 





def solicitud(request):
    """
    solicitud ajax para verificar id
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
        myfile = request.FILES['imagen']
        fs = FileSystemStorage()
        extension_archivo= str(myfile.name).split(".")[1]
        print("extension",extension_archivo)
        nombre_archivo=str(ultimo_id)+"."+extension_archivo
        filename = fs.save(nombre_archivo, myfile)
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
        datos_a_guardar.imagen=nombre_archivo # le ponemos para relacionar el nombre con el id  
        datos_a_guardar.save() # guardamos los valores 
        data = {
        }
        data['message'] = 'Agregado correctamente'
    else:
        data['message']="Error, no me enviaste nada"
    return render(request,"mensaje.html",data )# respondemos con un mensaje


def consulta_datos():
    todos= Datos.objects.all()
    return todos

def cantidad_total_adoptados():
    cant= len(consulta_datos()  ) # devuelve la longitud de la lista
    return cant 