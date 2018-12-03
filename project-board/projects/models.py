from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone


# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    body = models.TextField()
    skills = models.TextField()
    university = models.CharField(max_length = 100)

    def __str__(self):
        return self.title

    def printDate(self):

        now = timezone.now()
        difference = int(str((now - self.pub_date).days))
        returnMessage = ""
        if difference > 0:
            returnMessage = "Posted " + str((now - self.pub_date).days) + " days ago"
        else:
            returnMessage = "Posted today"
        return returnMessage


        """
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
                        """


    def parseIntoList(self):
        skillDict = eval(self.skills)

        skillsList = []
        for key in skillDict:
            if skillDict[key] == 'True':
                skillsList.append(key)
        return skillsList

    def skillsToString(self):
        skillsList = self.parseIntoList()
        skillsString = ""
        for item in skillsList:
            skillsString += str(item) + ", "
        return skillsString[:-2]

    def summary(self):
        summary = 'Title: ' + self.title + ' | Summary: ' + self.body + ' | Skills: ' + self.skillsToString() + ' | University: ' + self.university
        return summary

    def get_owner(self):
        return self.owner


    def printableSkillsString(self):
        def mapping(skill):
            if skill == "c":
                return "C"
            if skill == "cSharp":
                return "C#"
            if skill == "cpp":
                return "C++"
            if skill == "dataScience":
                return "Data Science"
            if skill == "desktopApplication":
                return "Desktop Application"
            if skill == "java":
                return "Java"
            if skill == "javascript":
                return "Javascript"
            if skill == "nodeJs":
                return "Node.js"
            if skill == "php":
                return "PHP"
            if skill == "python":
                return "Python"
            if skill == "ruby":
                return "Ruby"
            if skill == "sql":
                return "SQL"
            if skill == "swift":
                return "Swift"
            if skill == "webDevelopment":
                return "Web Development"

        listOfSkills = self.parseIntoList()
        printableVersion = []
        for skill in listOfSkills:
            printableVersion.append(mapping(skill))

        skillsString = ""
        for item in printableVersion:
            skillsString += str(item) + ", "
        return skillsString[:-2]


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    skills = models.TextField()
    university = models.CharField(max_length=100)
