from django.shortcuts import render
from.models import*
from django.contrib import messages
from .form import UserDetailsForm
from .form import WorkersDetailsForm
from django.contrib.auth.forms import UserCreationForm
from.form import WorkersDetailsForm
from .models import RoleChoices
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



from django.shortcuts import render, redirect




# Create your views here.



def home(request):
    return render(request,"bengali/home.html")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        # Get username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')  # Redirect to the home page or desired location
        else:
            # Invalid credentials
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def table(request):

    return render(request,"table.html")

def user_registration(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        user_details_form = UserDetailsForm(request.POST)

        if user_form.is_valid() and user_details_form.is_valid():
            user = user_form.save(commit=False)
            user.role = RoleChoices.USER
            user.save()

            user_details = user_details_form.save(commit=False)
            user_details.profile = user
            user_details.save()

            messages.success(request, 'User registered successfully!')
            return redirect('login')

    else:
        user_form = UserCreationForm()
        user_details_form = UserDetailsForm()

    return render(request, 'user_registration.html', {
        'user_form': user_form,
        'user_details_form':UserDetailsForm ,
    })


def agency_registration(request):
    return render(request,"agency_reg.html")

def worker_registration(request):
    
    if request.method == 'POST':
        worker_form =  WorkersDetailsForm(request.POST)
        worker_details_form = WorkersDetailsForm(request.POST)

        if worker_form.is_valid() and worker_details_form.is_valid():
            worker = worker_form.save(commit=False)
            worker.role = RoleChoices.USER
            worker.save()

            worker_details = worker_details_form.save(commit=False)
            worker_details.profile = worker
            worker_details.save()

            messages.success(request, 'worker registered successfully!')
            return redirect('login')

    else:
        worker_form = WorkerCreationForm()
        worker_details_form = WorkersDetailsForm()

    return render(request, 'worker_reg.html', {
        'worker_form': worker_form,
        'worker_details_form': WorkersDetailsForm ,
    })

def signup(request):
    return render(request,"signup.html")

def about(request):
    return render(request,"bengali/about.html")

def blog(request):
    return render(request,"bengali/blog.html")

def contact(request):
    return render(request,"bengali/contact.html")

def service(request):
    return render(request,"bengali/service.html")


def user_deatails_view(request):
    return render(request,"table2.html")

def admin_dashboard(request):
    return render(request,"admin_dashboard.html")

def user_dashboard(request):
    return render(request,"user_dashboard.html")

def agency_dashboard(request):
    return render(request,"agency_dashboard.html")

def worker(request):
    return render(request,"worker.html")





from django.shortcuts import render

# Create your views here.
def map(request):
    context = {
        'latitude': 11.2588,
        'longitude': 75.7804
    }
    return render(request, 'map.html', context)





@csrf_exempt 
def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        print(f"Received coordinates: Latitude={latitude}, Longitude={longitude}")

        return JsonResponse({'status': 'success', 'latitude': latitude, 'longitude': longitude})
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)


    