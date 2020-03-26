from django.db import models
from datetime import datetime,date
from django.utils import timezone
#mydate= "2020-02-01"
#defecto_fecha= datetime.strptime(mydate, "%Y-%m-%d")
# Create your models here.
class Datos(models.Model):
    identificativo= models.AutoField(primary_key=True)
    id= models.CharField(default=0,max_length=40 )  
    #identificativo del material, puede tener texto 
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
    
    

    imagen=models.ImageField(upload_to = 'imagenes/', default = 'imagenes/None/no-img.jpg')



    def __str__(self):
        """
        Para el nombre en el admin de Django
        """
        return self.nombre + self.apellido  