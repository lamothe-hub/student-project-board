from django.contrib import admin
from django.conf.urls import url
from projects import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^projectPage/', views.projectPage, name='projectPage'),
    url(r'^addProject/', views.addProject, name='addProject'),
    url(r'^projectAdded/', views.projectAdded, name='projectAdded'),
    url(r'^signUp/', views.signUp, name='signUp'),
    url(r'^signedUp/', views.signedUp, name='signedUp'),
    url(r'^login/', views.login, name='login'),
    url(r'^loggedIn/', views.loggedIn, name='loggedIn'),
    url(r'^logUserOut/', views.logUserOut, name='logUserOut'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^userHome/', views.userHome, name='userHome'),
    url(r'^clearProjects/', views.clearProjects, name='clearProjects'),
    url(r'^filterProjects/', views.filterProjects, name='filterProjects'),
    url(r'^projects/(?P<projectId>[0-9]+/$)', views.projectDetails),
    url(r'^projects/edit/(?P<projectId>[0-9]+/$)', views.editProject),
    url(r'^projects/projectEdited/(?P<projectId>[0-9]+/$)', views.projectEdited),
    url(r'^projects/delete/(?P<projectId>[0-9]+/$)', views.deleteProject),
    url(r'^sendMail/', views.sendMail, name='sendMail'),
    url(r'^editProfile/', views.editProfile, name='editProfile'),
    url(r'^profileEdited/', views.profileEdited, name='profileEdited'),
    url(r'^editProject/', views.editProject, name='editProject'),
    url(r'^deleteProject/', views.deleteProject, name='deleteProject'),



]
