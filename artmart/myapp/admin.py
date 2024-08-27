# from django.contrib import admin

# Register your models here.
# myapp/admin.py
from django.contrib import admin
from myapp.models import *
admin.site.register(UserProfile)
admin.site.register(ArtistProfile)
admin.site.register(Artwork)
admin.site.register(Order)
admin.site.register(Review)

