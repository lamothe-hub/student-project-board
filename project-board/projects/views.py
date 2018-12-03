from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from projects.models import Project, Person
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from projects.forms import NameForm
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils import timezone
import json

import datetime

# Create your views here.
# Creating Forms: https://docs.djangoproject.com/en/2.1/topics/forms/


def sendMail(request):
    subject = 'Test Email'
    message = 'Hello, this is my test email!'
    sender = 'jeffreylamothe@gmail.com'
    recipients = ['jeffreylamothe@hotmail.com']


    send_mail(subject, message, sender, recipients)
    return HttpResponse('Message sent')

def projectPage(request):
    return render (request, 'projects/projectPage.html')

def addProject(request):
    return render (request, 'projects/addProject.html')

def formSkillsDictFromRequest(request):
    skills = {
        'c': request.GET.get(('c'), "False"),
        'cSharp': request.GET.get(('cSharp'), "False"),
        'cpp': request.GET.get(('cpp'), "False"),
        'dataScience': request.GET.get(('dataScience'), "False"),
        'desktopApplication': request.GET.get(('desktopApplication'), "False"),
        'java': request.GET.get(('java'), "False"),
        'javaScript': request.GET.get(('javaScript'), "False"),
        'nodeJs': request.GET.get(('nodeJs'), "False"),
        'php': request.GET.get(('php'), "False"),
        'python': request.GET.get(('python'), "False"),
        'ruby': request.GET.get(('ruby'), "False"),
        'sql': request.GET.get(('sql'), "False"),
        'swift': request.GET.get(('swift'), "False"),
        'webDevelopment': request.GET.get(('webDevelopment'), "False"),
    }
    return skills
def parseSkillsStringIntoArray(skillsString):
        skillDict = eval(skillsString)

        skillsList = []
        for key in skillDict:
            if skillDict[key] == 'True':
                skillsList.append(key)
        return skillsList


def projectAdded(request):

    if request.user.is_authenticated:
        title = request.GET['title']
        body = request.GET['body']
        #c = request.GET['c']
        #cSharp = request.GET['cSharp']
        skills = formSkillsDictFromRequest(request)
        skillsString = str(skills)
        university = request.GET['university']

        data = {'title':title, 'body':body, 'skills':str(parseSkillsStringIntoArray(skillsString)), 'university':university}
        newProject = Project(title=title, pub_date=datetime.datetime.now(), body=body, skills=skillsString, university=university, owner=request.user)
        newProject.save()
        return render(request, 'projects/projectAdded.html',data)
    else:
        return render(request, 'projects/createProjectError.html')



def home(request):
    username = None
    message = ""
    if request.user.is_authenticated:
        username = request.user.username
        message = "Hello " + username + ", "
    objects = Project.objects.order_by('-pub_date')
    data = {'projects':objects, 'message':message, 'userAuthenticated':request.user.is_authenticated}

    return render(request, 'projects/home.html', data)

def getTimeInDays(time):
    if time == "week":
        return 7
    elif time =="month":
        return 30
    else:
        return 9999

def filterProjects(request):
    university = ''
    # skillsArray contains the skills that we are searching for...
    searchSkillsArray = parseSkillsStringIntoArray(str(formSkillsDictFromRequest(request)))
    timeSincePosting = ''
    skills = ''
    universitySet = Project.objects.none()
    skillSet = Project.objects.none()
    timeSet = Project.objects.none()
    objects = Project.objects.order_by('-pub_date')
    validObjects = [] # list containing the objects that meet both the university and the skills requirements
    if 'university' in request.GET.keys():
        university = request.GET['university']
        universitySet = Project.objects.filter(university=university)
        objects = universitySet
    if len(searchSkillsArray) > 0:
        # Find the set with any of the skills contained in the array
        for object in objects:
            # Loop through the objects that meet the university criteria to see if they also meet skill criteria
            objectSkills = parseSkillsStringIntoArray(object.skills)
            for objectSkill in objectSkills:
                # For each skill in the project we check to see if it matches any of the search criteria
                if objectSkill in searchSkillsArray:
                    # If one of the project's skills was earched for, add it to the array
                    validObjects.append(object)
        validUniversityAndSkillsSet = (set(objects) & set(validObjects))
        objects = validUniversityAndSkillsSet

    objectList = list(objects)

    if 'timeSincePosting' in request.GET.keys():
        timeSincePosting = request.GET['timeSincePosting']
        timeInDays = getTimeInDays(timeSincePosting)
        print("Time since posting: " + timeSincePosting)

        now = timezone.now()
        compareDate = now - timedelta(days=timeInDays)

        for object in objectList:
            print(object)
            now = timezone.now()
            compareDate = now - timedelta(days=timeInDays)
            if object.pub_date < compareDate:
                objectList.remove(object)
    data = {'userAuthenticated':request.user.is_authenticated, 'projects':objectList, 'university':university, 'skills':skills, 'timeSincePosting':timeSincePosting}

    return render(request, 'projects/filteredHome.html', data)

def projectDetails(request, projectId):
    if projectId[-1] == '/':
        projectId = projectId[:-1]
    project = Project.objects.get(pk=projectId)
    owner = project.owner
    return render(request, 'projects/projectDetails.html', {'project': project, 'owner': owner})

def signUp(request):
    return render(request, 'projects/signUp.html')

def signedUp(request):
    username = request.GET['username']
    email = request.GET['email']
    password = request.GET['password']
    university = request.GET['university']
    skills = request.GET['skills']
    user = User.objects.create_user(username, email, password)
    person = Person(user=user, skills=skills, university=university)
    person.save()
    return render(request, 'projects/signedUp.html', {'username': username, 'email':email})

def login(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('home')
    else:
        return render(request, 'projects/login.html', {'message': ''})

def loggedIn(request):
    inputUsername = request.GET['username']
    inputPassword = request.GET['password']
    user = authenticate(username=inputUsername, password=inputPassword)
    if user is not None:
        auth_login(request, user)
        return redirect('home')

    else:
        print("We did not find a user")
        return render(request, 'projects/login.html', {'message': 'That is not a valid username/password'})

def logUserOut(request):
    message = ""


def userHome(request):
    inputUsername = request.GET['username']
    message = "Hello " + inputUsername + ", "
    inputPassword = request.GET['password']
    user = authenticate(username=inputUsername, password=inputPassword)
    objects = Project.objects.order_by('pub_date')
    if user is not None:
        print("We found a user")
        auth_login(request, user)
        return render(request, 'projects/home.html', {'message': message, 'projects':objects})

    else:
        print("We did not find a user")
        return render(request, 'projects/login.html', {'message': 'That is not a valid username/password'})

def profile(request):
        username = request.user.username
        objects = Person.objects.filter(user__username=username)
        currentUser = objects[0]
        userObject = {
            'username': username,
            'skills': currentUser.skills,
            'university': currentUser.university,
            'email': request.user.email
        }
        projects = Project.objects.filter(owner=request.user)
        return render(request, 'projects/profile.html', {'user': userObject, 'projects': projects})

def editProfile(request):
        username = request.user.username
        objects = Person.objects.filter(user__username=username)
        currentUser = objects[0]
        userObject = {
            'username': username,
            'skills': currentUser.skills,
            'university': currentUser.university,
            'email': request.user.email
        }
        return render(request, 'projects/editProfile.html', {'user': userObject})

def profileEdited(request):
        user = request.user
        user.username = request.GET["username"]
        user.save()

        username = request.user.username
        objects = Person.objects.filter(user__username=username)
        currentUser = objects[0]
        userObject = {
            'username': username,
            'skills': currentUser.skills,
            'university': currentUser.university,
            'email': request.user.email
        }
        projects = Project.objects.filter(owner=request.user)
        return profile(request)

def clearProjects(request):
    for project in Project.objects.all():
        project.delete()
    return HttpResponse('All projects have been removed from the database.')

def editProject(request, projectId):
    if projectId[-1] == '/':
        projectId = projectId[:-1]
    project = Project.objects.get(pk=projectId)
    return render(request, 'projects/editProject.html', {'project': project})

def projectEdited(request, projectId):
    return render(request, 'proejcts/projectEdited.html')

def deleteProject(request, projectId):
    if projectId[-1] == '/':
        projectId = projectId[:-1]
    project = Project.objects.get(pk=projectId)
    name = project.title
    project.delete()
    return render(request, 'projects/deleteProject.html',{'name': name})
