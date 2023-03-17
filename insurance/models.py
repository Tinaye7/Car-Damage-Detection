from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer

status=(
            ('Approved','APPROVED'),
            ('Rejected','REJECTED'),
            ('Pending','PENDING'),
        )
class Category(models.Model):
    category_name =models.CharField(max_length=20)
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.category_name

class Policy(models.Model):
    category= models.ForeignKey('Category', on_delete=models.CASCADE)
    policy_name=models.CharField(max_length=200)
    sum_assurance=models.PositiveIntegerField()
    premium=models.PositiveIntegerField()
    tenure=models.PositiveIntegerField()
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.policy_name

class PolicyRecord(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    Policy= models.ForeignKey(Policy, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,default='Pending')
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.policy

class Question(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    description =models.CharField(max_length=500)
    admin_comment=models.CharField(max_length=200,default='Nothing')
    asked_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.description

class claims(models.Model) :
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    phone= models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    national=models.CharField(max_length=255)
    dob= models.DateField()
    gender=models.CharField(max_length=255)
    driver= models.CharField(max_length=255)
    ownership=models.CharField(max_length=255)
    authorized=models.CharField(max_length=255)
    licenced=models.CharField(max_length=255)
    purpose=models.CharField(max_length=255)
    vehicle= models.CharField(max_length=255)
    make= models.CharField(max_length=255)
    reg=models.CharField(max_length=255)
    address_where_it_occured= models.CharField(max_length=255)
    time=models.TimeField()
    date=models.DateField()
    how_it_happened= models.CharField(max_length=255)
    weather= models.CharField(max_length=255)
    road_surface= models.CharField(max_length=255)
    extent_of_damage= models.CharField(max_length=255)
    estimate_repair_cost= models.CharField(max_length=255)
    details_of_injuries= models.CharField(max_length=255)
    passengers= models.CharField(max_length=255)
    damaged_property= models.CharField(max_length=255)
    names_of_third_parties= models.CharField(max_length=255)
    Status=models.CharField(max_length=300,choices=status, default='Pending')
    Remarks=models.CharField(max_length=500, default='Pending Assessment')
    objects=models.Manager()
    
   

class PoliceReports(models.Model):
    id=models.AutoField(primary_key=True)
    claim=models.ForeignKey(claims,on_delete=models.CASCADE)
    image=models.FileField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    def __str__(self):
        return self.image

class Licence(models.Model):
    id=models.AutoField(primary_key=True)
    claim=models.ForeignKey(claims,on_delete=models.CASCADE)
    image=models.FileField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)

    def __str__(self):
        return self.image

class Quotations(models.Model):
    id=models.AutoField(primary_key=True)
    claim=models.ForeignKey(claims,on_delete=models.CASCADE)
    image=models.FileField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    def __str__(self):
        return self.image

class Damages(models.Model):
    id=models.AutoField(primary_key=True)
    claim=models.ForeignKey(claims,on_delete=models.CASCADE)
    image=models.FileField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    def __str__(self):
        return self.image