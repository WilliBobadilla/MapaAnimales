from django.db import models
from datetime import datetime,date
from django.utils import timezone

class Datos(models.Model):
    identificativo= models.AutoField(primary_key=True)
    id= models.CharField(default=0,max_length=40)  
    nombre=models.CharField(max_length=40)
    apellido=models.CharField (max_length=40)
    edad=models.IntegerField()
    fecha= models.DateField(default= timezone.now() )
    descripcion=models.TextField(max_length=400,default='Sin descripcion')
    animal= models.CharField(max_length=20)
    sexo=models.CharField(max_length=20)
    edad_animal=models.IntegerField(default=1)
    cant_animales= models.IntegerField()# cantidad de mascotas actuales 
    latitud= models.FloatField()
    longitud= models.FloatField()
    imagen=models.ImageField(upload_to = 'images/', default = 'imagenes/None/no-img.jpg')

    def __str__(self):
        """
        Para el nombre en el admin de Django
        """
        return self.nombre + self.apellido  


class Datos_adopcion(models.Model):
    """
    Tabla donde se pone los datos de los animales \n
    para la adopcion disponibles 
    """
    identificativo= models.AutoField(primary_key=True)
    fecha= models.DateField(default=timezone.now())
    descripcion=models.TextField(max_length=400,default='Sin descripcion')
    animal= models.CharField(max_length=20)# si es gato, perro etc 
    sexo=models.CharField(max_length=20)
    edad_animal=models.IntegerField(default=1)
    numero_telefono_persona= models.IntegerField(default='0975209464')
    latitud_persona=models.FloatField() 
    longitud_persona=models.FloatField()
    imagen=models.ImageField(upload_to = 'images/', default = 'imagenes/None/no-img.jpg')


    def __str__(self):
        """
        Para el nombre en el admin de Django
        """
        return str(self.identificativo) + " ----- "+ str(self.fecha) 
    

class Datos_extravio(models.Model):
    """
    Tabla donde se pone los datos de los animales \n
    para la adopcion disponibles 
    """
    identificativo= models.AutoField(primary_key=True)
    fecha= models.DateField(default=timezone.now())
    descripcion=models.TextField(max_length=400,default='Sin descripcion')
    nombre_animal= models.CharField(max_length=20)
    animal= models.CharField(max_length=20)# si es gato, perro etc 
    sexo=models.CharField(max_length=20)
    edad_animal=models.CharField(max_length=20) #puede poner en meses o años,etc
    numero_telefono_persona= models.IntegerField(default=' ')
    latitud_perdido=models.FloatField()  #datos de la ubicacion aproximada de la perdida del animal
    longitud_perdido=models.FloatField()
    imagen=models.ImageField(upload_to = 'images/', default = 'imagenes/None/no-img.jpg')
    ip_dispositivo=models.CharField(max_length=20)#para saber si es la misma persona que habia subido
    encontrado=models.BooleanField()#para indicar si se encontro o no 


    def __str__(self):
        """
        Para el nombre en el admin de Django
        """
        return str(self.identificativo) + " ----- "+ str(self.fecha)+"----encontrado: "+ str(self.encontrado) 