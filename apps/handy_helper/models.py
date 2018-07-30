from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from time import strftime
from django import forms
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validation(self, postData):
        errors = {}
        if User.objects.filter(email = postData['email']):
            errors['email_exists'] = "An account has already been created with this email!"

        if len(postData['first_name']) < 1: 
                errors['first_name'] = "First name cannot be blank!"
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First name must contain 2 letters minimum!"
        elif not postData['first_name'].isalpha():
            errors['first_name'] = "First name must contain letter ONLY!"

        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last name cannot be blank!"
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must contain 2 letters minimum!"
        elif not postData['last_name'].isalpha():
            errors['last_name'] = "Last name must contain letter ONLY!"

        if EMAIL_REGEX.match(postData['email']) == None:
            errors['email_format'] = "Invalid email format!"
        elif len(postData['email']) < 1:
            errors['email'] = "email name cannot be blank"

        if len(postData['password']) < 1:
            errors['password'] = "Password cannot be blank"
        elif len(postData['password']) < 8:
            errors['pw_length'] = "Password must be at least 8 characters minimum!"

        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match!"
        return errors



    def login_validation(self, postData):
        user = User.objects.filter(email = postData['login_email'])
        errors = {}
        if not user:
            errors['email'] = "Invalid email or password!"

        if user and not bcrypt.checkpw(postData['login_password'].encode('utf8'), user[0].password.encode('utf8')):
            errors['password'] = "Invalid email or password!"
        return errors



class JobManager(models.Manager):
    def job_validation(self, postData):
        errors = {}

        if len(postData['name']) < 1: 
                errors['name'] = "Title cannot be blank!"
        elif len(postData['name']) < 3:
            errors['name'] = "Title must contain 3 letters minimum!"

        if len(postData['description']) < 1: 
                errors['description'] = "Description cannot be blank!"
        elif len(postData['description']) < 3:
            errors['description'] = "Description must contain 3 letters minimum!"
        
        if len(postData['location']) < 1: 
                errors['location'] = "Location cannot be blank!"
        elif len(postData['location']) < 3:
            errors['location'] = "location must contain 3 letters minimum!"

        return errors

    def update_validation(self, postData):
        errors = {}
        
        if len(postData['name']) < 1: 
                errors['name'] = "Title cannot be blank!"
        elif len(postData['name']) < 3:
            errors['name'] = "Title must contain 3 letters minimum!"

        if len(postData['description']) < 1: 
                errors['description'] = "Description cannot be blank!"
        elif len(postData['description']) < 3:
            errors['description'] = "Description must contain 3 letters minimum!"
        
        if len(postData['location']) < 1: 
                errors['location'] = "Location cannot be blank!"
        elif len(postData['location']) < 3:
            errors['location'] = "location must contain 3 letters minimum!"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Job(models.Model):
    users_doing_job = models.ForeignKey(User, blank=True, null=True, related_name = "users_task")
    name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey(User, related_name = "created_by_user")
    objects = JobManager()
