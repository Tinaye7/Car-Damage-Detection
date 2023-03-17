from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Category
        fields=['category_name']

class PolicyForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=models.Category.objects.all(),empty_label="Category Name", to_field_name="id")
    class Meta:
        model=models.Policy
        fields=['policy_name','sum_assurance','premium','tenure']

class QuestionForm(forms.ModelForm):
    class Meta:
        model=models.Question
        fields=['description']
        widgets = {
        'description': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }

class ClaimsForm(forms.ModelForm):
    class Meta:
        model= models.claims
        
        fields=['name','phone','email','address','national','dob','gender','driver','ownership','authorized',
               'licenced','purpose','vehicle','make','reg','address_where_it_occured','time','date','how_it_happened',
               'weather','road_surface','extent_of_damage','estimate_repair_cost',
               'details_of_injuries','passengers','damaged_property','names_of_third_parties','Status','Remarks']
      

class LicenceForm(forms.ModelForm):
    class Meta:
        model=models.Licence
        fields=['image']

class PoliceForm(forms.ModelForm):
    class Meta:
        model=models.PoliceReports
        fields=['image']

class QuotationForm(forms.ModelForm):
    class Meta:
        model=models.Quotations
        fields=['image']

class DamageForm(forms.ModelForm):
    class Meta:
        model=models.Damages
        fields=['image']

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password',]
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['profile_pic','mobile','address']

