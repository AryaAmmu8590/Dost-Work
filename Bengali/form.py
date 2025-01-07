from django import forms
from .models import  UserDetails,WorkersDetails,AgencyDetails





class  UserDetailsForm(forms.ModelForm):
    class Meta:
        model =  UserDetails
        fields = ['profile','address','age','sex']

class WorkersDetailsForm(forms.ModelForm):
    class Meta:
        model= WorkersDetails
        fields=['profile','id_no','image','time','amount','address']


class AgencyDetailsForm(forms.ModelForm):
    class Meta:
        model = AgencyDetails
        fields =['profile','Agency_Name','licence_id']






