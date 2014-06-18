from django.contrib import admin
from models import *

class UnitAdmin(admin.ModelAdmin):
    
    list_display = (
        'vclan',
        'vclanID',
        'unitaID',
        'gruppoID',
        'quartier',
        'storeroom',
        'stock',
    )

    list_filter = ('quartier__number', 'storeroom__number', 'stock__letter')
    list_order = ('quartier__number', 'storeroom__number', 'stock__letter')

admin.site.register(Stock)
admin.site.register(Quartier)
admin.site.register(Storeroom)
admin.site.register(Person)
admin.site.register(VirtualPerson)

admin.site.register(Unit, UnitAdmin)
admin.site.register(CamstControl)
admin.site.register(StockAssignement)
