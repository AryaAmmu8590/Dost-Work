from django import forms
from .models import  UserDetails,WorkersDetails,AgencyDetails,UserComplaints





class  UserDetailsForm(forms.ModelForm):
    class Meta:
        model =  UserDetails
        fields = ['profile','address','age','sex']

class WorkersDetailsForm(forms.ModelForm):
    class Meta:
        model= WorkersDetails
        fields=['profile','id_no','image','address']


class AgencyDetailsForm(forms.ModelForm):
    class Meta:
        model = AgencyDetails
        fields =['profile','agency_name','licence_id','address']
        
        
class UserComplaintsForm(forms.ModelForm):
    class Meta:
        model = UserComplaints
        fields =['complaints','name','email']
        



from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'card_number', 'amount']


from .models import UserComplaintReply 
class ReplyForm(forms.ModelForm):
    class Meta:
        model = UserComplaintReply
        fields ='__all__'





