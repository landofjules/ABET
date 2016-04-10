from __future__ import unicode_literals
from django.db import models

# ---------- TOP LEVEL [no forign keys] ---------- #

class professor(models.Model):
    netID = models.CharField(max_length=512, default='')
    isAdmin = models.BooleanField()
    
    def __str__(self):
        return self.netID

class course(models.Model):
    name = models.CharField(max_length=512, default='')
    description = models.CharField(max_length=512, default='')
    
    def __str__(self):
        return self.name
     

class studentOutcome(models.Model):
    outcomeLetter = models.CharField(max_length=3)
    description = models.CharField(max_length=512, default='')
    
    def __str__(self):
        return self.outcomeLetter

class performanceLevel(models.Model):
    achievementLevel = models.IntegerField(default=0)
    description = models.CharField(max_length=512, default='')
    
    def __str__(self):
        return self.description
    

# --------- SPLIT VERSIONS OF COURSE AND OUTCOME ---------- #
    
class section(models.Model):
    
    SEMESTERS = (
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('spring', 'Spring'),
    )
    year = models.IntegerField(default=0)
    semester = models.CharField(max_length=6, choices=SEMESTERS, default='fall')
    
    main = models.ForeignKey(course,on_delete=models.CASCADE, null=True)
    professor = models.ForeignKey(professor, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return "%s - %s - %s%d" % (self.professor.netID , self.course.name , self.semester , self.year)
    
class courseOutcome(models.Model):
    narrativeSummary = models.CharField(max_length=512, default='')
    
    main = models.ForeignKey(studentOutcome, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(section, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.main.outcomeLetter + ": " + str(self.section)
    
class performanceIndicator(models.Model):
    name = models.CharField(max_length=512, default='')
    # section number to section
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.CharField(max_length=512, default='')
    
    outcome = models.ForeignKey(courseOutcome, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name


# ---------- SPLIT BY PERFORMACE LEVEL ---------- # 

class outcomeData(models.Model):
    numberAchieved = models.IntegerField(default=0)
    
    course = models.ForeignKey(course, on_delete=models.CASCADE, null=True)
    performanceLevel = models.ForeignKey(performanceLevel, on_delete=models.CASCADE, null=True)
    outcome = models.ForeignKey(courseOutcome, on_delete=models.CASCADE, null=True)

    
class rubric(models.Model):
    gradeTopBound = models.IntegerField(default=0)
    gradeLowerBound = models.IntegerField(default=0)
    description = models.CharField(max_length=512, default='')
    numStudents = models.IntegerField(default=0)
    
    performanceLevel = models.ForeignKey(performanceLevel, on_delete=models.CASCADE, null=True)
    performanceIndicator = models.ForeignKey(performanceIndicator, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.description


