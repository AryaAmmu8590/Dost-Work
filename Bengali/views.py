from django.shortcuts import render,redirect
from.models import*
from django.contrib import messages
from .form import UserDetailsForm
from .form import WorkersDetailsForm
from.form import WorkersDetailsForm
from.form import AgencyDetailsForm
from .models import RoleChoices
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login,logout



def home(request):
    return render(request,"bengali/home.html")




def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')



def user_complaints(request):
    from django.shortcuts import render, redirect
from .models import UserComplaints
from .forms import UserComplaintForm  # Assuming you have a form for UserComplaints
from django.contrib import messages

def user_complaints(request):
    if request.method == "POST":
        form = UserComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your complaint has been submitted successfully.")
            return redirect("user_complaints")
        else:
            messages.error(request, "There was an error submitting your complaint. Please try again.")
    else:
        form = UserComplaintForm()

    complaints = UserComplaints.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "complaints": complaints,
        "form": form,
    }
    return render(request, "user_complaints.html", context)

   
   




def user_list_workers(request):
    workers=WorkersDetails.objects.all()
    return render(request,"user_list_workers.html",{'workers':workers})


def user_profile(request):
    userdetails = get_object_or_404(UserDetails, profile=request.user)

    if request.method == 'POST':
        user_details_form = UserDetailsForm(request.POST, instance=userdetails)

        profile_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
        }
        if user_details_form.is_valid():
            user_d=user_details_form.save(commit=False)
            user_d.profile=request.user
            user_d.save()

            for field, value in profile_data.items():
                setattr(request.user, field, value)
            
            request.user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')

    if userdetails.profile is None:
        messages.error(request, 'User profile does not exist.')
        return redirect('user_dashboard')  

    user_details_form = UserDetailsForm(instance=userdetails)  
    return render(request, "user_profile.html", {"userdetails": userdetails, "user_details_form": user_details_form})


def view_worker_details(request,worker_id):
    worker=get_object_or_404(WorkersDetails,id=worker_id)
    return render(request,"worker_details_view.html",{'worker':worker})

def review_list_worker(request,worker_id):
    rev=Review.objects.filter(worker__id=worker_id)
    print(rev)
    return render(request,"review_worker_list.html",{'reviews':rev,'worker_id':worker_id})


def submit_review(request, worker_id):
    if request.method == 'POST':
        review_text = request.POST.get('review')
        if review_text:
            try:
                review = Review(worker_id=worker_id, user=request.user, comment=review_text)
                review.save()
                messages.success(request, 'Your review has been submitted successfully.')
            except Exception as e:
                print(e)
        else:
            messages.error(request, 'Please provide both a review and a rating.')
    return redirect('review_worker_list', worker_id=worker_id)





def book_worker(request,worker_id):
    if request.method == 'POST':
        book_worker_text = request.POST.get('book_worker')
        if book_worker_text:
            try:
                book_worker = BookWorker(worker_id=worker_id, user=request.user, comment=book_worker_text)
                book_worker.save()
                messages.success(request, 'Your booking has been submitted successfully.')
            except Exception as e:
                print(e)
        else:
            messages.error(request, 'Please provide both a review and a rating.')
    return render(request,"book_worker.html",{'worker_id':worker_id})










def login_view(request):
    if request.method == 'POST':
        # Get username and password from the form
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email,password)
        user = authenticate(request, username=email, password=password)
        print(user)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            if user.role == RoleChoices.USER:
                return redirect('user_dashboard') 
            elif user.role == RoleChoices.AGENCY:
                return redirect('agency_dashboard') 
            elif user.role == RoleChoices.WORKERS:
                return redirect('worker') 
            elif user.role == RoleChoices.ADMIN or user.is_superuser:
                return redirect('admin_dashboard') 
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def table(request):
    return render(request,"table.html")


def user_registration(request):
    if request.method == 'POST':
        user_details_form = UserDetailsForm(request.POST)
        
        password=request.POST.get('password')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
       
        try:
            user=Profile.objects.create_user(first_name= first_name,last_name=last_name, username=email,password=password,email=email,role=RoleChoices.USER)
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
        print(request.POST)
       
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        
        try:
            agency=Profile.objects.create_user(username=email,email=email,phone=phone,role=RoleChoices.AGENCY,password=password)
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







from .models import BookWorker
def worker_view(request):
    booking=BookWorker.objects.filter(worker__user=request.user)
    print(booking,request.user)
    
    return render(request,"worker_view.html",{'booking':booking})

def user_view(request):
     booking=BookWorker.objects.filter(user=request.user)
     print(booking,request.user)
     return render(request,"user_view.html",{'booking':booking})
 
 
 
def admin_booking(request):
     booking=BookWorker.objects.all()
    
     return render(request,"admin_booking.html",{'booking':booking})
 
 


 
 
 
 



 
 
 
