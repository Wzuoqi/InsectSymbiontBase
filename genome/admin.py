from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Genome)
class articleAdmin(admin.ModelAdmin):
    list_display = ('genome_id','source','host','gtdb_classification')
