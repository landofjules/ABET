from __future__ import unicode_literals
from django.db import models

class performanceLevels(models.Model):
    achievementLevel = models.IntegerField(default=0)
    description = models.CharField(max_length=512)

class performanceIndicators(models.Model):
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.CharField(max_length=512)


class outcomeData(models.Model):

    SEMESTERS = (
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('spring', 'Spring'),
    )

    outcomeLetter = models.CharField(max_length=3)
    courseName = models.CharField(max_length=48)
    achievementLevel = models.IntegerField(default=0)
    yr = models.IntegerField(default=0)
    numberAchieved = models.IntegerField(default=0)
    semester = models.CharField(max_length=6, choices=SEMESTERS, default='fall')

class studentOutcomes(models.Model):
    outcomeLetter = models.CharField(max_length=3)
    description = models.CharField(max_length=512)

class courseOutcomeMap(models.Model):
    courseName = models.CharField(max_length=48)
    outcomeLetter = models.CharField(max_length=3)

class rubrics(models.Model):
    achievementLevel = models.IntegerField(default=0)
    gradeRange = models.IntegerField(default=0)
    description = models.CharField(max_length=512)

class piData(models.Model):

    SEMESTERS = (
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('spring', 'Spring'),
    )

    studentStrengths = models.CharField(max_length=512)
    studentWeaknesses = models.CharField(max_length=512)
    numberAchieved = models.IntegerField(default=0)
    achievementLevel = models.IntegerField(default=0)
    numberAchieved = models.IntegerField(default=0)
    yr = models.IntegerField(default=0)
    semester = models.CharField(max_length=6, choices=SEMESTERS, default='fall')
