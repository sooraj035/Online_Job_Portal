from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ApplicantUser(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    phone=models.IntegerField(null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=10,null=True)
    type=models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.user.username


class Recruiter(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    phone=models.IntegerField(null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=10,null=True)
    company=models.CharField(null=True)
    type=models.CharField(max_length=10,null=True)
    status=models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.user.username


class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    title = models.CharField()
    start_date = models.DateField()
    end_date = models.DateField()
    salary = models.FloatField(max_length=30)
    image = models.FileField()
    description = models.CharField()
    experience = models.CharField()
    location = models.CharField(max_length=20)
    skills = models.CharField(max_length=20)
    creation_date = models.DateField()
    def __str__(self):
        return self.title


class Appliedjob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(ApplicantUser, on_delete=models.CASCADE)
    resume = models.FileField()
    applied_date = models.DateField()

    def __str__(self):
        return str(self.id)



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
