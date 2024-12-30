from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Projects(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length = 200, blank = True, null = True)
    description = models.TextField(blank = True, null = True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.name)

class ProjectMembers(models.Model):
    _id = models.AutoField(primary_key=True, editable = False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    choices = [('Admin', 'Admin'), ('Member', 'Member')]
    role = models.CharField(max_length=10, choices=choices, null=True, blank=True)

    def __str__(self):
        return str(self.role)

class Tasks(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length = 200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    choices = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done')
    ]
    status = models.CharField(max_length=20, choices=choices, blank=True, null=True)
    priority_choices = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]
    priority = models.CharField(max_length=10, choices=priority_choices, blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.title)

class Comments(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.content[:50])


