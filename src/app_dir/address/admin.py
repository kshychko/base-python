from django.contrib import admin

from app_dir.address.models import Suburb, State, Country

admin.site.register(Suburb)
admin.site.register(State)
admin.site.register(Country)
