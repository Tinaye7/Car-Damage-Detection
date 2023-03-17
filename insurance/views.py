from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from customer import models as CMODEL
from customer import forms 
from django.contrib import messages
from insurance.models import claims
from insurance.models import Damages,PoliceReports,Licence,Quotations
from insurance import forms

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'insurance/index.html')


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):      
        return redirect('customer/customer-dashboard')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
        'total_user':CMODEL.Customer.objects.all().count(),
        'claims':models.claims.objects.all().count(),
        'total_category':models.Category.objects.all().count(),
        'total_question':models.Question.objects.all().count(),
        'total_policy_holder':models.PolicyRecord.objects.all().count(),
        'approved_claims':models.claims.objects.all().filter(Status='Approved').count(),
        'disapproved_claims':models.claims.objects.all().filter(Status='Rejected').count(),
        'waiting_claims':models.claims.objects.all().filter(Status='Pending').count(),
    }
    return render(request,'insurance/admin_dashboard.html',context=dict)



@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers= CMODEL.Customer.objects.all()
    return render(request,'insurance/admin_view_customer.html',{'customers':customers})



@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'insurance/update_customer.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')



def admin_category_view(request):
    return render(request,'insurance/admin_category.html')

def admin_add_category_view(request):
    categoryForm=forms.CategoryForm() 
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-view-category')
    return render(request,'insurance/admin_add_category.html',{'categoryForm':categoryForm})

def admin_view_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_view_category.html',{'categories':categories})

def admin_delete_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_delete_category.html',{'categories':categories})
    
def delete_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    category.delete()
    return redirect('admin-delete-category')

def admin_update_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_update_category.html',{'categories':categories})

@login_required(login_url='adminlogin')
def update_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    categoryForm=forms.CategoryForm(instance=category)
    
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST,instance=category)
        
        if categoryForm.is_valid():

            categoryForm.save()
            return redirect('admin-update-category')
    return render(request,'insurance/update_category.html',{'categoryForm':categoryForm})
  
  

def admin_policy_view(request):
    return render(request,'insurance/admin_policy.html')


def admin_add_policy_view(request):
    policyForm=forms.PolicyForm() 
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST)
        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
            return redirect('admin-view-policy')
    return render(request,'insurance/admin_add_policy.html',{'policyForm':policyForm})

def admin_view_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_view_policy.html',{'policies':policies})



def admin_update_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_update_policy.html',{'policies':policies})

@login_required(login_url='adminlogin')
def update_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policyForm=forms.PolicyForm(instance=policy)
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST,instance=policy)
        
        if policyForm.is_valid():

            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
           
            return redirect('admin-update-policy')
    return render(request,'insurance/update_policy.html',{'policyForm':policyForm})
  
  
def admin_delete_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_delete_policy.html',{'policies':policies})
    
def delete_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policy.delete()
    return redirect('admin-delete-policy')

def admin_view_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all()
    return render(request,'insurance/admin_view_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_approved_claims_view(request):
    claims = models.claims.objects.all().filter(Status='Approved')
    damages = models.Damages.objects.all()
    police = models.PoliceReports.objects.all()
    quote = models.Quotations.objects.all()
    license = models.Licence.objects.all()
    return render(request,'insurance/admin_view_approved_claims.html',{'claims':claims,'damages':damages,'policereports':police,'quotations':quote,'licence':license})

def admin_view_disapproved_claims_view(request):
    claims = models.claims.objects.all().filter(Status='Rejected')
    damages = models.Damages.objects.all()
    police = models.PoliceReports.objects.all()
    quote = models.Quotations.objects.all()
    license = models.Licence.objects.all()
    return render(request,'insurance/admin_view_disapproved_claims.html',{'claims':claims,'damages':damages,'policereports':police,'quotations':quote,'licence':license})

def admin_view_waiting_claims_view(request):
    claims = models.claims.objects.all().filter(Status='Pending')
    damages = models.Damages.objects.all()
    police = models.PoliceReports.objects.all()
    quote = models.Quotations.objects.all()
    license = models.Licence.objects.all()
    return render(request,'insurance/admin_view_waiting_claims.html',{'claims':claims,'damages':damages,'policereports':police,'quotations':quote,'licence':license})

def approve_request_view(request,pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Approved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')

def disapprove_request_view(request,pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Disapproved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')


def admin_question_view(request):
    questions = models.Question.objects.all()
    return render(request,'insurance/admin_question.html',{'questions':questions})

def update_question_view(request,pk):
    question = models.Question.objects.get(id=pk)
    questionForm=forms.QuestionForm(instance=question)
    
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            admin_comment = request.POST.get('admin_comment')
            
            
            question = questionForm.save(commit=False)
            question.admin_comment=admin_comment
            question.save()
           
            return redirect('admin-question')
    return render(request,'insurance/update_question.html',{'questionForm':questionForm})

def aboutus_view(request):
    return render(request,'insurance/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'insurance/contactussuccess.html')
    return render(request, 'insurance/contactus.html', {'form':sub})
def multipleform(request):
    
    return render(request,"customer/multipleform.html")

def multipleform_save(request):
    
    if request.method!="POST":
        return HttpResponseRedirect(reverse("multipleform"))
    else:
        name= request.POST.get("name")
        phone= request.POST.get("phone")
        email=request.POST.get("email")
        address=request.POST.get("address")
        national=request.POST.get("national")
        dob= request.POST.get("dob")
        gender=request.POST.get("gender")
        driver= request.POST.get("driver")
        ownership=request.POST.get("owner")
        authorized=request.POST.get("auth")
        licenced=request.POST.get("licence")
        purpose=request.POST.get("purpose")
        vehicle= request.POST.get("vehicle")
        make= request.POST.get("make")
        reg=request.POST.get("reg")
        address_where_it_occured= request.POST.get("add")
        time=request.POST.get("time")
        date=request.POST.get("date")
        how_it_happened= request.POST.get("how")
        weather= request.POST.get("weather")
        road_surface=request.POST.get("road")
        extent_of_damage= request.POST.get("extent")
        estimate_repair_cost= request.POST.get("estimate")
        details_of_injuries= request.POST.get("injury")
        passengers= request.POST.get("passenger")
        damaged_property= request.POST.get("damage")
        names_of_third_parties= request.POST.get("third")
        if name=="":
            messages.error(request,"fill out blanks")
            return HttpResponseRedirect(reverse('multipleform'))

        try:
            claim=claims(name=name,phone=phone,email=email,address=address,national=national,dob=dob,gender=gender,
            driver=driver,ownership=ownership,authorized=authorized,licenced=licenced,purpose=purpose,vehicle=vehicle,make=make,
            reg=reg,address_where_it_occured=address_where_it_occured,time=time,date=date,how_it_happened=how_it_happened,
            weather=weather,road_surface=road_surface,extent_of_damage=extent_of_damage,estimate_repair_cost=estimate_repair_cost,
            details_of_injuries=details_of_injuries,passengers=passengers,damaged_property=damaged_property,names_of_third_parties=names_of_third_parties)
            claim.save()
            messages.success(request,"Data Save Successfully")
            return HttpResponseRedirect(reverse('multipleform'))
        except:
            messages.error(request,"Error in Saving Data")
            return HttpResponseRedirect(reverse('multipleform'))


def claims(request):
    claims = models.claims.objects.all()
    damages = models.Damages.objects.all()
    police = models.PoliceReports.objects.all()
    quote = models.Quotations.objects.all()
    license = models.Licence.objects.all()
    return render(request,'insurance/claims.html',{'claims':claims,'damages':damages,'policereports':police,'quotations':quote,'licence':license})

@login_required(login_url='adminlogin')
def assess_claim(request,pk):
    customer=models.claims.objects.get(id=pk)
    claims = models.claims.objects.get(id=pk)
    user=models.Licence.objects.get(id=customer.id)
    licence = models.Licence.objects.all().filter(claim_id=customer.id).all()
    police = models.PoliceReports.objects.filter(claim_id=customer.id).all()
    quotation = models.Quotations.objects.filter(claim_id=customer.id).all()
    damage = models.Damages.objects.filter(claim_id=customer.id).all()
    ClaimsForm=forms.ClaimsForm(instance=customer)
    mydict={'ClaimsForm':ClaimsForm,'licence':licence,'claims':claims,'police':police,'quotation':quotation,
           'damage':damage}
    if request.method=='POST':
        licence=models.Licence(request.POST,request.FILES)
        police=models.PoliceReports(request.POST,request.FILES)
        quotation=models.Quotations(request.POST,request.FILES)
        damage=models.Damages(request.POST,request.FILES)
        ClaimsForm=forms.ClaimsForm(request.POST,instance=customer)
        if  ClaimsForm.is_valid():
            #user=userForm.save()
            #user.set_password(user.password)
            #user.save()
            ClaimsForm.save()
            return redirect('claims')
    return render(request,'insurance/assess_claim.html',context=mydict)

def claim_details(request,pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    claims = models.claims.objects.get(id=pk)
    user=models.Licence.objects.get(id=customer.id)
    licence = models.Licence.objects.all().filter(claim_id=customer.id).all()
    police = models.PoliceReports.objects.filter(claim_id=customer.id).all()
    quotation = models.Quotations.objects.filter(claim_id=customer.id).all()
    damage = models.Damages.objects.filter(claim_id=customer.id).all()
    ClaimsForm=forms.ClaimsForm(instance=claims)
    mydict={'ClaimsForm':ClaimsForm,'licence':licence,'claims':claims,'police':police,'quotation':quotation,
           'damage':damage,'customer':customer}
    if request.method=='POST':
        licence=models.Licence(request.POST,request.FILES)
        police=models.PoliceReports(request.POST,request.FILES)
        quotation=models.Quotations(request.POST,request.FILES)
        damage=models.Damages(request.POST,request.FILES)
        ClaimsForm=forms.ClaimsForm(request.POST,instance=customer)
        if  ClaimsForm.is_valid():
            #user=userForm.save()
            #user.set_password(user.password)
            #user.save()
            ClaimsForm.save()
            return redirect('customer/history')
    return render(request,'customer/claim_details.html',context=mydict)