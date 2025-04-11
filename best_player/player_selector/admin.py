from django.contrib import admin
from .models import Field, Time, Place, BestHomo, Vote

admin.site.register(Field)
admin.site.register(Time)
admin.site.register(Place)
admin.site.register(Vote)

@admin.register(BestHomo)
class BestAdmin(admin.ModelAdmin):
    raw_id_fields = ('time', 'field', 'place')