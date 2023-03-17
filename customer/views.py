from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail,EmailMessage
from insurance import models as CMODEL
from insurance import forms as CFORM
from django.contrib.auth.models import User
from django.contrib import messages
from insurance.models import claims,PoliceReports,Licence,Quotations,Damages
from django.core.files.storage import FileSystemStorage
from insurancemanagement import settings
from insurance.models import claims




def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'customer/customerclick.html')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'customer/customersignup.html',context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    dict={
        'customer':models.Customer.objects.get(user_id=request.user.id),
        'multipleform':CMODEL.claims.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),
        'applied_policy':CMODEL.PolicyRecord.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),
        'total_category':CMODEL.Category.objects.all().count(),
        'total_question':CMODEL.Question.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),

    }
    return render(request,'customer/customer_dashboard.html',context=dict)

def apply_policy_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.Policy.objects.all()
    return render(request,'customer/apply_policy.html',{'policies':policies,'customer':customer})

def apply_view(request,pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policy = CMODEL.Policy.objects.get(id=pk)
    policyrecord = CMODEL.PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('history')

def history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    claims = CMODEL.claims.objects.all().filter(customer=customer)
    return render(request,'customer/history.html',{'claims':claims,'customer':customer})

def ask_question_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questionForm=CFORM.QuestionForm() 
    
    if request.method=='POST':
        questionForm=CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            
            question = questionForm.save(commit=False)
            question.customer=customer
            question.save()
            return redirect('question-history')
    return render(request,'customer/ask_question.html',{'questionForm':questionForm,'customer':customer})

def question_history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(customer=customer)
    return render(request,'customer/question_history.html',{'questions':questions,'customer':customer})

def multipleform(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    return render(request,'customer/multipleform.html',{'customer':customer})

def multipleform_save(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    if request.method!="POST":
        return render(request,'customer/multipleform.html',{'customer':customer})
    else:
        customer = models.Customer.objects.get(user_id=request.user.id)
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
        
        images=request.FILES.getlist("file[]")
        print(images)
        images2=request.FILES.getlist("file2[]")
        print(images2)
        images3=request.FILES.getlist("file3[]")
        print(images3)
        images4=request.FILES.getlist("file4[]")
        print(images4)
        
        if name=="":
            messages.error(request,"Confirm Password Doesn't Match")
            return render(request,'customer/multipleform.html',{'customer':customer})
        try:
            claim=claims(customer=customer,name=name,phone=phone,email=email,address=address,national=national,dob=dob,gender=gender,
            driver=driver,ownership=ownership,authorized=authorized,licenced=licenced,purpose=purpose,vehicle=vehicle,make=make,
            reg=reg,address_where_it_occured=address_where_it_occured,time=time,date=date,how_it_happened=how_it_happened,
            weather=weather,road_surface=road_surface,extent_of_damage=extent_of_damage,estimate_repair_cost=estimate_repair_cost,
            details_of_injuries=details_of_injuries,passengers=passengers,damaged_property=damaged_property,names_of_third_parties=names_of_third_parties)
            claim.save()

            
            for img in images:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)

                pimage=PoliceReports(claim=claim,image=file_path,customer=customer)
                pimage.save()

            for img in images2:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)

                pimage=Licence(claim=claim,image=file_path,customer=customer)
                pimage.save()
            for img in images3:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)

                pimage=Quotations(claim=claim,image=file_path,customer=customer)
                pimage.save()

            for img in images4:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)

                pimage=Damages(claim=claim,image=file_path,customer=customer)
                pimage.save()   
            messages.success(request,"Data Save Successfully")
            return render(request,'customer/multipleform.html',{'customer':customer})

        except:
            messages.error(request,"Error in Saving Data")
            return render(request,'customer/multipleform.html',{'customer':customer})
        

