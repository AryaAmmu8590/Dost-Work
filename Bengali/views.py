from django.shortcuts import render
from.models import*
from django.contrib import messages
from .form import UserDetailsForm
from .form import WorkersDetailsForm
from.form import WorkersDetailsForm
from.form import AgencyDetailsForm
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
        user_details_form = UserDetailsForm(request.POST)
        
        password=request.POST.get('password')
        email=request.POST.get('email')
       
        try:
            user=Profile.objects.create_user(username=email,password=password,email=email,role=RoleChoices.USER)
        except Exception as e:
            print(e)
            return redirect('user_registration')
            
          

        if user_details_form.is_valid():
            user_details = user_details_form.save(commit=False)
            user_details.profile = user
            user_details.save()

            messages.success(request, 'User registered successfully!')
            return redirect('login')
        else:
            print(user_details_form.errors ,user_details_form.errors)

    else:
        user_details_form = UserDetailsForm()

    return render(request, 'user_registration.html', {
        'user_details_form':UserDetailsForm ,
    })


def worker_registration(request):
    if request.method == 'POST':
        worker_details_form = WorkersDetailsForm(request.POST)
        
        password=request.POST.get('password')
        email=request.POST.get('email')
        
        
        try:
            worker=Profile.objects.create_user(username=email,password=password,email=email,role=RoleChoices.WORKERS)
        except Exception as e:
            print(e)
            return redirect('worker-registration')
            
          

        if worker_details_form.is_valid():
            worker_details = worker_details_form.save(commit=False)
            worker_details.profile =worker
            worker_details.save()

            messages.success(request, 'Worker registered successfully!')
            return redirect('login')
        else:
            print(worker_details_form.errors ,worker_details_form.errors)

    else:
        worker_details_form = UserDetailsForm()

    return render(request, 'worker_reg.html', {
        'worker_details_form':WorkersDetailsForm ,
    })
    
    
    
def agency_registration(request):
    if request.method == 'POST':
        agency_details_form = AgencyDetailsForm(request.POST)
       
        agency_name=request.POST.get('agency_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        id=request.POST.get('id')
        
        try:
            agency=Profile.objects.create_user(username=email,agency_name=agency_name,email=email,phone=phone,address=address,id=id,role=RoleChoices.AGENCY)
        except Exception as e:
            print(e)
            return redirect('agency_registration')
            
          

        if agency_details_form.is_valid():
            agency_details = agency_details_form.save(commit=False)
            agency_details.profile = agency
            agency_details.save()

            messages.success(request, 'Agency registered successfully!')
            return redirect('login')
        else:
            print(agency_details_form.errors ,agency_details_form.errors)

    else:
        agency_details_form = AgencyDetailsForm()

    return render(request, 'agency-reg.html', {
        'agency_details_form':AgencyDetailsForm ,
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

def navbar(request):
    return render(request,"navbar.html")






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


    