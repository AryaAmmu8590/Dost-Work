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




from django.shortcuts import render, redirect
from .models import UserComplaints
from .form import UserComplaintsForm  # Assuming you have a form for UserComplaints
from django.contrib import messages

def user_complaints(request):
   
    worker_id=request.GET.get('id')
    if worker_id and worker_id !='':
        worker=get_object_or_404(WorkersDetails,id_no=worker_id)
    else:
        worker=''
    if request.method == "POST":
        form = UserComplaintsForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.status='Open'
            obj.save()
            messages.success(request, "Your complaint has been submitted successfully.")
            return redirect("user_dashboard")
        else:
            print(form.errors)
            messages.error(request, "There was an error submitting your complaint. Please try again.")
    else:
        form = UserComplaintsForm()

    complaints = UserComplaints.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "complaints": complaints,
        'worker':worker,
        "form": form,
    
    }
    print(worker,worker_id)
    return render(request, "user_complaints.html", context)

   
from django.shortcuts import render
from .models import AgencyDetails

def agency_details(request):
    agencies = AgencyDetails.objects.all()
    return render(request, 'agency_details.html', {'agencies': agencies})


from django.shortcuts import render
from .models import WorkersDetails

def workers_details(request):
    workers = WorkersDetails.objects.all()  # Fetch all workers data
    return render(request, 'workers_details.html', {'workers': workers})






from django.shortcuts import render
from .models import WorkersDetails

def user_list_workers(request):
    workers = WorkersDetails.objects.all() 
    query = request.GET.get('query')  

    if query and query != '':
        workers = workers.filter(
            models.Q(profile__first_name__icontains=query) | models.Q(category__icontains=query)
        )
    
    return render(request, "user_list_workers.html", {'workers': workers})


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
        book_worker_text = request.POST.get('additional_notes')
        time=request.POST.get('available_time')
        place=request.POST.get('place')
        try:
            book_worker = BookWorker(worker_id=worker_id, user=request.user, additionalnotes=book_worker_text,  time=time, place=place)
            book_worker.save()
              # Create a notification for the worker
            notification_message = f'You have a new booking from {request.user.email} at {place} on {time}.'

            worker = WorkersDetails.objects.get(id=worker_id)
            Notification.objects.create(
                recipient=worker.profile,
                sender=request.user,
                message=f'Your have a booking request with {request.user.email} .'    
            )

            messages.success(request, 'Your booking has been submitted successfully.')
        except Exception as e:
            print(e)
       
    return render(request,"book_worker.html",{'worker_id':worker_id})


from django.shortcuts import render
from .models import Notification

def admin_noty(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, "admin_noty.html", {'notifications': notifications})


def worker_notification(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, "worker_notification.html", {'notifications': notifications})







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
        age=request.POST.get('age')
       
        try:
            user=Profile.objects.create_user(first_name= first_name,last_name=last_name, username=email,password=password,email=email,age=age,role=RoleChoices.USER)
        except Exception as e:
            print(e)
            return redirect('user_registration')
            
        if user_details_form.is_valid():
            user_details = user_details_form.save(commit=False)
            user_details.profile = user
            user_details.save()

            messages.success(request, 'User registered successfully!')
            request.session['user_id'] = user.id
            return redirect('payment')
        else:
            user.delete()
            print(user_details_form.errors ,user_details_form.errors)

    else:
        user_details_form = UserDetailsForm()

    return render(request, 'user_registration.html', {
        'user_details_form':UserDetailsForm ,
    })



def worker_registration(request):
    agencies=AgencyDetails.objects.all()
    if request.method == 'POST':
        worker_details_form = WorkersDetailsForm(request.POST)
        password=request.POST.get('password')
        email=request.POST.get('email')
        agency_id=request.POST.get('agency')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        agency_id=request.POST.get('agency')
        agency=get_object_or_404(AgencyDetails,id=agency_id)
        
        try:
            worker=Profile.objects.create_user(username=email,password=password,email=email,role=RoleChoices.WORKERS,first_name=first_name,last_name=last_name)
        except Exception as e:
            print(e)
            return redirect('worker-registration')
            
        if worker_details_form.is_valid():
            worker_details = worker_details_form.save(commit=False)
            worker_details.profile =worker
            worker_details.agency=agency
            worker_details.save()

            messages.success(request, 'Worker registered successfully!')
            request.session['user_id'] = worker.id
            return redirect('payment')

        else:
            print(worker_details_form.errors ,worker_details_form.errors)

    else:
        worker_details_form = UserDetailsForm()

    return render(request, 'worker_reg.html', {
        'worker_details_form':WorkersDetailsForm ,
        'agencies':agencies,
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
            request.session['user_id'] = agency.id
            return redirect('payment')
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
    workers=WorkersDetails.objects.filter(agency__profile=request.user,approved_by_agency=True)
    query=request.GET.get('query',None)
    if query:
        workers = workers.filter(profile__first_name__icontains=query)  
    return render(request,"agency_dashboard.html",{'workers':workers})


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
    booking=BookWorker.objects.filter(worker__profile=request.user)
    print(booking,request.user)
    
    return render(request,"worker_view.html",{'booking':booking})

def user_view(request):
     booking=BookWorker.objects.filter(user=request.user)
     print(booking,request.user)
     return render(request,"user_view.html",{'booking':booking})
 
 
 
def admin_booking(request):
     booking=BookWorker.objects.all()
    
     return render(request,"admin_booking.html",{'booking':booking})
 
 
 
 
def user_details(request):
    user_details = UserDetails.objects.all()
    return render(request,"user_details.html",{'user_details': user_details})

def reports(request):
    complaints = UserComplaints.objects.all()  # Fetch all complaints from the database
    return render(request, 'reports.html', {'complaints': complaints})






def worker_profile(request):
    userdetails = get_object_or_404(WorkersDetails, profile=request.user)

    if request.method == 'POST':
        worker_details_form = WorkersDetailsForm(request.POST, instance=userdetails)

        profile_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
        }
        if worker_details_form.is_valid():
            worker_d=worker_details_form.save(commit=False)
            worker_d.profile=request.user
            worker_d.save()

            for field, value in profile_data.items():
                setattr(request.user, field, value)
            
            request.user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('worker_profile')

    if userdetails.profile is None:
        messages.error(request, 'worker profile does not exist.')
        return redirect('worker_dashboard')  

    worker_details_form =WorkersDetailsForm(instance=userdetails)  
    return render(request, "worker_profile.html", {"userdetails": userdetails, "worker_details_form": worker_details_form})





def complaints_replay(request):
    return render(request,"complaints_replay.html")


def agency_profile(request):
    agencydetails = get_object_or_404(AgencyDetails, profile=request.user)

    if request.method == 'POST':
        agency_details_form = AgencyDetailsForm(request.POST, instance=agencydetails)

        profile_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
        }
        if agency_details_form.is_valid():
            agency_d=agency_details_form.save(commit=False)
            agency_d.profile=request.user
            agency_d.save()

            for field, value in profile_data.items():
                setattr(request.user, field, value)
            
            request.user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('agency_profile')

    if agencydetails.profile is None:
        messages.error(request, 'Agency profile does not exist.')
        return redirect('agency_dashboard')  

    agency_details_form = AgencyDetailsForm(instance=agencydetails)  
    return render(request, "agency_profile.html", {"agencydetails": agencydetails, "agency_details_form": agency_details_form})
 

def agency_workers(request):
    workers=WorkersDetails.objects.filter(agency__profile=request.user,approved_by_agency=False)
    print(workers)
    return render(request,"agency_workers.html",{'workers':workers})
 

def approve_worker(request,worker_id):
    worker=WorkersDetails.objects.get(id=worker_id)
    worker.approved_by_agency=True
    worker.save()
    return redirect('agency_workers')
 
def reject_worker(request,worker_id):
    worker=WorkersDetails.objects.get(id=worker_id)
    worker.delete()
    return redirect('agency_workers')




def new_reg(request):
    reg=WorkersDetails.objects.filter(agency__profile=request.user,approved_by_agency=True)
    return render(request,"new_reg.html",{'users':reg})



def user_complaint(request):
    profiles = UserDetails.objects.all().values_list('profile', flat=True)
    complaints = UserComplaints.objects.filter(user__in=profiles)
    return render(request, "user_complaint.html", {'complaints': complaints})


def worker_complaint(request):
    profiles = WorkersDetails.objects.all().values_list('profile', flat=True)
    complaints = UserComplaints.objects.filter(user__in=profiles)
    return render(request,"worker_complaint.html" ,{'complaints': complaints} )
   


def worker_dash_com(request):

    if request.method == "POST":
        form = UserComplaintsForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user 
            complaint.save()
            messages.success(request, "Complaint added successfully!")
            return redirect("worker_dash_com") 

    else:
        form = UserComplaintsForm()

    return render(request, "worker_dash_com.html", { "form": form})




from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import BookWorker

def worker_weekly_reports(request):
    today = timezone.now().date()

    start_of_week = today - timedelta(days=today.weekday()) 
    end_of_week = start_of_week + timedelta(days=6) 
    worker_bookings = (
        BookWorker.objects.filter(worker__agency__profile=request.user,created_at__range=(start_of_week, end_of_week))
        .values("worker__profile__email") 
        .annotate(total_bookings=Count("id"))
        .order_by("-total_bookings")
    )

    return render(request, "worker_weekly_reports.html", {"worker_bookings": worker_bookings})




def worker_report(request):
    bookings = BookWorker.objects.filter(worker__agency__profile=request.user)
    return render(request,"worker_reports.html", {'bookings': bookings})





    




from django.db.models import Count


def weekly_worker_reports(request):
    today = timezone.now().date()

    start_of_week = today - timedelta(days=today.weekday())  # Start from Monday
    end_of_week = start_of_week + timedelta(days=6)  # End on Sunday

    user_bookings = (
        BookWorker.objects.filter(created_at__range=(start_of_week, end_of_week))
        .values("user__email")  # Group by user email
        .annotate(total_bookings=Count("id"))  # Count bookings per user
        .order_by("-total_bookings")  # Sort by most bookings
    )
    booking = BookWorker.objects.filter(worker__profile=request.user)
    print(booking   )
    return render(request, "weekly_worker_reports.html", {"all_bookings": booking})





from django.shortcuts import render, get_object_or_404, redirect
from .models import UserComplaintReply ,UserComplaints
from .form import ReplyForm

def agency_user_replay(request, complaint_id):  
    complaint = get_object_or_404(UserComplaints, id=complaint_id)  
    form = ReplyForm(data=request.POST or None)
    if form.is_valid():
        replay = form.save(commit=False)
        replay.complaint = complaint
        replay.save()
        return redirect('user_complaints')
    else:
        print(form.errors)
    return render(request, "agency_user_replay.html", {"complaint": complaint})  



def agency_worker_replay(request):
    return render(request,"agency_worker_replay.html"  )
   
   
   
   
   
def admin_user_report(request):
    complaints = UserComplaints.objects.all()
    return render(request, "admin_user_report.html", {'complaints': complaints})



def admin_worker_report(request):
    complaints = UserComplaints.objects.all()
    return render(request, "admin_worker_report.html", {'complaints': complaints})


from django.shortcuts import render, redirect
from .models import Payment
from .form import PaymentForm

# Payment view to handle payment submission
def payment(request):
    if request.method == 'POST':
        user = get_object_or_404(Profile, id=request.session.get('user_id'))   
        form = PaymentForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=user
            obj.save() 
            return redirect('success') 
        else:
            print(form.errors)
            user.delete()
            
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'form': form})




def success(request):
    return render(request, "success.html")



def admin_pay(request):
    payments=Payment.objects.all()
    return render(request, "admin_pay.html",{'payments':payments})



from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_email):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            fail_silently=False,  # Set to True to avoid exceptions
        )
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_admin_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_email = request.POST.get('recipient_email')
        result = send_email(subject, message, recipient_email)
        if result.get('success'):
            messages.success(request, 'Email sent successfully.')
        else:
            messages.error(request, 'Failed to send email. Please try again.')
    return render(request, 'sendmail.html')


 
 
 
