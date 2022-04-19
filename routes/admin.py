from django.contrib import admin
from .models import Profile
from .models import Hotels
from .models import Room, Booking


# Register your models here.
admin.site.register(Profile)
admin.site.register(Hotels)
admin.site.register(Room)
admin.site.register(Booking)


