from django.contrib import admin
from models import *

class UnitAdmin(admin.ModelAdmin):
    
    list_display = (
        'vclan',
        'vclanID',
        'unitaID',
        'gruppoID',
        'quartier',
        'storeroom'
    )

    list_filter = ('quartier__number', 'storeroom__number' )
    list_order = ('quartier__number', 'storeroom__number')

admin.site.register(Stock)
admin.site.register(Quartier)
admin.site.register(Storeroom)
admin.site.register(Person)
admin.site.register(VirtualPerson)

admin.site.register(Unit, UnitAdmin)
admin.site.register(CamstControl)
admin.site.register(StockAssignement)
