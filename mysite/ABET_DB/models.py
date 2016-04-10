from __future__ import unicode_literals
from django.db import models


class performanceLevels(models.Model):
    achievementLevel = models.IntegerField(default=0)
    description = models.CharField(max_length=512, default='')
    
    def __str__(self):
        return self.description


class professors(models.Model):
    netID = models.CharField(max_length=512, default='')
    isAdmin = models.BooleanField()
    
    def __str__(self):
        return self.netID
    

class courses(models.Model):

    SEMESTERS = (
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('spring', 'Spring'),
    )

    courseName = models.CharField(max_length=512, default='')
    description = models.CharField(max_length=512, default='')
    yr = models.IntegerField(default=0)
    semester = models.CharField(max_length=6, choices=SEMESTERS, default='fall')
    professor = models.ForeignKey(professors, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.courseName
    
    
class studentOutcomes(models.Model):
    outcomeLetter = models.CharField(max_length=3)
    description = models.CharField(max_length=512, default='')
    course = models.ForeignKey(courses, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.outcomeLetter
    

class performanceIndicators(models.Model):
    name = models.CharField(max_length=512, default='')
    # section number to section
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.CharField(max_length=512, default='')
    outcome = models.ForeignKey(studentOutcomes, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name


class outcomeData(models.Model):
    numberAchieved = models.IntegerField(default=0)
    # point only to courseOutcome by section number and letter
    course = models.ForeignKey(courses, on_delete=models.CASCADE, null=True)
    performanceLevel = models.ForeignKey(performanceLevels, on_delete=models.CASCADE, null=True)
    studentOutcome = models.ForeignKey(studentOutcomes, on_delete=models.CASCADE, null=True)

    
class rubrics(models.Model):
    gradeTopBound = models.IntegerField(default=0)
    gradeLowerBound = models.IntegerField(default=0)
    description = models.CharField(max_length=512, default='')
    numStudents = models.IntegerField(default=0)
    performanceLevel = models.ForeignKey(performanceLevels, on_delete=models.CASCADE, null=True)
    performanceIndicator = models.ForeignKey(performanceIndicators, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.description


