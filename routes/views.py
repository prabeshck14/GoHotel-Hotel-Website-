from django.shortcuts import render , redirect , HttpResponseRedirect , HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .forms import CreateUserForm
from django.views.generic import ListView, FormView, View, DeleteView
from .models import Hotels, Room, Booking, Contact
from .forms import AvailabilityForm
from routes.booking_functions.availability import check_availability


# Create your views here.
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('BookingListView')



@login_required
def RoomListView(request):
    if 'q' in request.GET:
        q = request.GET['q']
        ROOM_CATEGORIES = Room.objects.filter(capacity__icontains=q)
    else:
        ROOM_CATEGORIES = Room.objects.all()


    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    room_values = room_categories.values()
    room_list=[]

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('RoomDetailView',kwargs={'category':room_category})
        room_list.append((room,room_url))
    context = {
        "room_list":room_list,
    }
    return render(request, 'room_list_view.html', context)


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "booking_list.html"
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')

# @login_required
# class BookingView(FormView):
#     form_class = AvailabilityForm
#     template_name = 'availability_form.html'

#     def form_valid(self, form):
#         data = form.cleaned_data
#         room_list = Room.objects.filter(category=data['room_category'])
#         available_rooms = []
#         for room in room_list:
#             if check_availability(room, data['check_in'], data['check_out']):
#                 available_rooms.append(room)

#         if len(available_rooms) > 0:
#             room = available_rooms[0]
#             booking = Booking.objects.create(
#                 user=self.request.user,
#                 room=room,
#                 check_in=data['check_in'],
#                 check_out=data['check_out']
#             )
#             booking.save()
#             return HttpResponse(booking)
#         else:
#             return HttpResponse('All of this category of rooms are booked!! Try another one')

def index(request):
    
    return render(request, "index.html")

def about(request):

    return render(request, "about.html")


def hotels(request):
    if 'q' in request.GET:
        q = request.GET['q']
        hotel = Hotels.objects.filter(name__icontains=q)
    else:
        hotel = Hotels.objects.all()
    
    return render(request, "hotels.html",{'hotel': hotel})

    

def contact(request):
    if request.method=="POST":
        print(request)
        name = request.POST.get('name' , '')
        email = request.POST.get('email' , '')
        message = request.POST.get('message' , '')
        print(name, email, message)
        contact = Contact(name=name,email=email,message=message)
        contact.save()
        
    return render(request, "contact.html")
@login_required
def profile(request):
    return render(request, "profile.html")

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


#change password 
def change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request,'Password Changed Successfully')
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request,'change_pass.html', {'form':fm})
    else:
        return HttpResponseRedirect('/login/')

