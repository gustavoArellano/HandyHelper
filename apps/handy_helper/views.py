from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import User
from .models import Job
import datetime
from time import strftime
import bcrypt


def index(request):
    return render(request, "handy_helper/index.html")


def registration_process(request):
    errors = User.objects.reg_validation(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)

    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(
            first_name= request.POST['first_name'], 
            last_name= request.POST['last_name'], 
            email= request.POST['email'], 
            password = hash_pw
            )
        user = User.objects.last() 
        request.session['logged_in'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        return redirect('/welcome')
    return redirect('/')


def login(request):
    errors = User.objects.login_validation(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
    else:
        user = User.objects.get(email = request.POST['login_email'])
        request.session['logged_in'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        return redirect('/welcome')
    return redirect('/')



def logout(request):
    request.session.clear()
    return redirect('/logout_complete')

def logout_complete(request):
    request.session.clear()
    return redirect('/')


def welcome(request):
    context = {
        'jobs': Job.objects.all(),
        'jobs_available': Job.objects.all().exclude(users_doing_job = request.session['logged_in']),
        'jobs_assigned': Job.objects.filter(users_doing_job = User.objects.get(id = request.session['logged_in']))
    }
    return render(request, 'handy_helper/welcome.html', context)



   
    
def delete_job(request, id):
    if request.method == "POST":
        this_job= Job.objects.get(id = request.POST['delete'])
        this_job.delete()
        return redirect('/welcome')



def show_job_info(request, id):
    if request.method == "POST":
        this_job = Job.objects.get(id = request.POST['show_job_info'])  
        
        context = {
            'show_job_info': this_job 
        }
        return render(request, 'handy_helper/info.html', context)



def edit_job(request, id):
    if request.method == "POST":
        
        this_job = Job.objects.get(id = request.POST['edit'])  
        
        context = {
            'display_info': this_job 
        }
    return render(request, 'handy_helper/edit.html', context)


def update(request, id):
    errors = Job.objects.update_validation(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)

    else: 
        
        job_values = { 
            'name': request.POST['name'],
            'description': request.POST['description'],
            'location': request.POST['location']
        } 
        Job.objects.filter(id=id).update(**job_values)
        return redirect('/welcome')
    print('****************')
    return redirect('request.edit_job')
  

def create_job(request):
    return render(request, 'handy_helper/add.html')

def create_job_process(request):
    errors = Job.objects.job_validation(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
       
    else:
        
        this_user = User.objects.get(id = request.session['logged_in'])

        creation = Job.objects.create(
            created_by_user = this_user,
            name = request.POST['name'],
            description = request.POST['description'],
            location = request.POST['location'],
        )
        return redirect('/welcome')
    return redirect('/create_job')

def add_job_to_user(request, id):
    if request.method == "POST":
        this_user = User.objects.get(id = request.session['logged_in'])
        this_job = Job.objects.get(id = request.POST['add_job_to_user'])

       
        this_job.users_doing_job = this_user
        this_job.save()
        print('************************')
        
# def add_job_to_user(request):
#     if request.method == 'POST':
#         this_user = User.objects.get(id = request.session['logged_in'])
#         this_job = Job.objects.get(id = request.POST['add_job_to_user'])
#         this_job.users_doing_job.add(this_user)
#     return redirect('/welcome')
        
    return redirect('/welcome')