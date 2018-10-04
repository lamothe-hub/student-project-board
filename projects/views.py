from django.shortcuts import render
from projects.models import Project
import datetime

# Create your views here.



def projectPage(request):
    return render (request, 'projects/projectPage.html')

def addProject(request):
    return render (request, 'projects/addProject.html')

def projectAdded(request):
    title = request.GET['title']
    body = request.GET['body']
    skills = request.GET['skills']
    university = request.GET['university']
    data = {'title':title, 'body':body, 'skills':skills, 'university':university}
    newProject = Project(title=title, pub_date=datetime.datetime.now(), body=body, skills=skills, university=university)
    newProject.save()
    return render(request, 'projects/projectAdded.html',data)

def home(request):
    objects = Project.objects.order_by('pub_date')
    return render(request, 'projects/home.html', {'projects':objects})

def projectDetails(request, projectId):
    if projectId[-1] == '/':
        projectId = projectId[:-1]
    project = Project.objects.get(pk=projectId)
    return render(request, 'projects/projectDetails.html', {'project': project})
