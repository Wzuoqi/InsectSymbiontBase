from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Symbiont)
class articleAdmin(admin.ModelAdmin):
    list_display = ('id','record_type','host_species','symbiont_name')
