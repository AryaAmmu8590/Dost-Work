from django.shortcuts import render
from.models import*

# Create your views here.




def home(request):
    data=User_reg.objects.all()

    return render(request,"bengali/index.html",context={"data":data})
