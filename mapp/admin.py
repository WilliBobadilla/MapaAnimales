from django.contrib import admin
from .models import Datos,Datos_adopcion

admin.site.register(Datos) # para que aparezca en el panel de admin 
admin.site.register(Datos_adopcion)