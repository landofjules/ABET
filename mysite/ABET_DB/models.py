from __future__ import unicode_literals
from django.db import models


class performanceLevels(models.Model):
    achievementLevel = models.IntegerField(default=0)
    description = models.CharField(max_length=512)


class performanceIndicators(models.Model):
    name = models.CharField(max_length=512)
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.CharField(max_length=512)
    studentStrengths = models.CharField(max_length=512)
    studentWeaknesses = models.CharField(max_length=512)


class studentOutcomes(models.Model):
    outcomeLetter = models.CharField(max_length=3)
    description = models.CharField(max_length=512)


class courses(models.Model):

    SEMESTERS = (
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('spring', 'Spring'),
    )

    crnNumber = models.IntegerField(default=0)
    courseName = models.CharField(max_length=512)
    description = models.CharField(max_length=512)
    yr = models.IntegerField(default=0)
    semester = models.CharField(max_length=6, choices=SEMESTERS, default='fall')
    
    
class professors(models.Model):
    netID = models.CharField(max_length=512)
    isAdmin = models.BooleanField(initial=False)

    
class outcomeData(models.Model):
   
    numberAchieved = models.IntegerField(default=0)
    studentOutcome = models.ForeignKey(studentOutcomes, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(courses, on_delete=models.CASCADE, null=True)
    performanceLevel = models.ForeignKey(performanceLevels, on_delete=models.CASCADE, null=True)


class courseOutcomeMap(models.Model):
    course = models.ForeignKey(courses, on_delete=models.CASCADE, null=True)
    studentOutcome = models.ForeignKey(studentOutcomes, on_delete=models.CASCADE, null=True)
    performanceIndicator = models.ForeignKey(performanceIndicators, on_delete=models.CASCADE, null=True)


class rubrics(models.Model):
    gradeTopBound = models.IntegerField(default=0)
    gradeLowerBound = models.IntegerField(default=0)
    description = models.CharField(max_length=512)
    numberAchieved = models.IntegerField(default=0)

    performanceLevel = models.ForeignKey(performanceLevels, on_delete=models.CASCADE, null=True)
    performanceIndicator = models.ForeignKey(performanceIndicators, on_delete=models.CASCADE, null=True)


