from django.urls import path
from . import views 
from .views import RoomListView, BookingListView, RoomDetailView, CancelBookingView

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('hotels/', views.hotels, name='hotels'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('change_pass/', views.change_pass, name="change_pass"),
    path('room_list/', RoomListView, name='RoomListView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),

]