from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField



class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female'), ('non-binary', 'Non-binary'), ('other', 'Other')])
    nationality = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    # Add any other fields you need
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class WorkExperience(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    current_job = models.BooleanField(default=False)  # If this is the current job

    def __str__(self):
        return f"{self.role} at {self.company_name}"

class Education(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='educations')
    university_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    major = models.TextField()
    level = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.degree} in {self.major} from {self.university_name}"
    
class UserRole(models.Model):
    ROLE_CHOICES = [
        ('ideator', 'Ideator'),
        ('executor', 'Executor'),
        ('funder', 'Funder'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'role')  # Ensure one role per user

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"


class Executor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skills = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    industries_of_interest = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    type_of_work = models.CharField(
        max_length=50,
        choices=[
            ('side-project', 'Side Project'),
            ('part-time', 'Part-Time'),
            ('full-time', 'Full-Time'),
        ]
    )

    def __str__(self):
        return f"Executor: {self.user.first_name} {self.user.last_name}"

class Ideator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # The list of ideas will be stored in a separate Idea model linked to Ideator
    # So no need to store ideas directly here

    def __str__(self):
        return f"Ideator: {self.user.first_name} {self.user.last_name}"

class Funder(models.Model):
    INVESTMENT_TYPE_CHOICES = [
        ('debt', 'Debt'),
        ('equity', 'Equity'),
        ('other', 'Other'),
    ]

    INVESTMENT_SIZE_CHOICES = [
        ('spare-change', 'Some Spare Change'),
        ('solid-cash', 'Solid Cash'),
        ('angel-mode', 'Angel Mode'),
        ('lets-talk-numbers', 'Lets Talk Numbers'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ideas_supported = models.ManyToManyField('ideas.Idea', blank=True)  # links to Idea model in 'ideas' app
    industries_of_interest = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPE_CHOICES)
    investment_size = models.CharField(max_length=20, choices=INVESTMENT_SIZE_CHOICES)

    def __str__(self):
        return f"Funder: {self.user.first_name} {self.user.last_name}"