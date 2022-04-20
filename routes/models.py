from email.mime import image
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Profile (models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    
    
    def __str__(self):
        return f'{self.user.username} Profile'

class Hotels(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    location = models.TextField(max_length=50,default="")
    rating = models.CharField(max_length=10,default="")
    desc = models.TextField()

    def __str__(self):
         return self.name

class Room(models.Model):
    ROOM_CATEGORIES=(
        ('YAC','AC'),
        ('NAC','NON-AC'),
        ('DEL','DELUXE'),
        ('KIN','KING'),
        ('QUE','QUEEN'),
    )
    image = models.ImageField(upload_to='pics',default="")
    number= models.IntegerField()
    category = models.CharField(max_length=15, choices=ROOM_CATEGORIES)
    beds = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.number}. {self.category} with {self.beds} beds for {self.capacity}people'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f' Hey, {self.user} You have booked room no. {self.room} from {self.check_in} to {self.check_out}'

    def get_room_category(self):
        room_categories = dict(self.room.ROOM_CATEGORIES)
        room_category = room_categories.get(self.room.category)
        return room_category

    def get_cancel_booking_url(self):
        return reverse('CancelBookingView', args=[self.pk, ])

class Contact(models.Model):
    Msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default="")
    message = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name
        
     