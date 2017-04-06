from models import *
from django.contrib import admin

class RegistrationAdmin(admin.ModelAdmin):
    pass

class HorarioAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Horario, HorarioAdmin)
