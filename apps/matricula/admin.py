from models import *
from django.contrib import admin

class MatriculaAdmin(admin.ModelAdmin):
    search_fields = (['nombre'])


admin.site.register(Matricula, MatriculaAdmin)
