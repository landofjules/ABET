from __future__ import unicode_literals
from django.db import models

# ---------- TOP LEVEL [no forign keys] ---------- #

class professor(models.Model):
    netID = models.CharField(max_length=512, default='', verbose_name='Net ID')
    fn = models.CharField(max_length=512, default='', verbose_name='First Name')
    ln = models.CharField(max_length=512, default='', verbose_name='Last Name')
    
    def __str__(self):
        return self.ln + ', ' + self.fn

class course(models.Model):
    name = models.CharField(max_length=512, default='', verbose_name='Course Name')
    description = models.CharField(max_length=512, default='')
    
    def __str__(self):
        return self.name
     

class studentOutcome(models.Model):
    outcomeLetter = models.CharField(max_length=3, verbose_name='Outcome Letter')
    description = models.CharField(max_length=512, default='')
    
    def __str__(self):
        return self.outcomeLetter


class performanceLevel(models.Model):
    achievementLevel = models.IntegerField(default=0, verbose_name='Achievement Level')
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
    
    course = models.ForeignKey(course,on_delete=models.CASCADE, null=True)
    professor = models.ForeignKey(professor, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return "%s - %s - %s%d" % (self.professor.netID , self.course.name , self.semester , self.year)
    
    
class courseOutcome(models.Model):
    narrativeSummary = models.CharField(max_length=512, default='')
    
    studentOutcome = models.ForeignKey(studentOutcome, on_delete=models.CASCADE, null=True, verbose_name='Outcome')
    section = models.ForeignKey(section, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.studentOutcome.outcomeLetter + ": " + str(self.section)
    
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
    numberAchieved = models.IntegerField(default=0, verbose_name='Number Achieved')
    
    course = models.ForeignKey(course, on_delete=models.CASCADE, null=True)
    performanceLevel = models.ForeignKey(performanceLevel, on_delete=models.CASCADE, null=True, verbose_name='Performance Level')
    outcome = models.ForeignKey(courseOutcome, on_delete=models.CASCADE, null=True, verbose_name='Outcome')

    
class rubric(models.Model):
    gradeTopBound = models.IntegerField(default=0, verbose_name='Upper Grade Bound')
    gradeLowerBound = models.IntegerField(default=0, verbose_name='Lower Grade Bound')
    description = models.CharField(max_length=512, default='')
    numStudents = models.IntegerField(default=0, verbose_name='Number of Students')
    
    performanceLevel = models.ForeignKey(performanceLevel, on_delete=models.CASCADE, null=True, verbose_name='Performance Level')
    performanceIndicator = models.ForeignKey(performanceIndicator, on_delete=models.CASCADE, null=True, verbose_name='Performance Indicator')
    
    def __str__(self):
        return self.description


