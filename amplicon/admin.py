from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Amplicon)
class AmpliconAdmin(admin.ModelAdmin):
    list_display = ('id','run','host','geo_loc_name_country')
