from __future__ import unicode_literals
from django.db import models

# ---------- TOP LEVEL [no forign keys] ---------- #

class professors(models.Model):
    netID = models.CharField(max_length=512, default='', verbose_name='Net ID')
    fn = models.CharField(max_length=512, default='', verbose_name='First Name')
    ln = models.CharField(max_length=512, default='', verbose_name='Last Name')
    
    def __str__(self):
        return self.ln + ', ' + self.fn


class courses(models.Model):
    name = models.CharField(max_length=512, default='', verbose_name='Course Name')
    description = models.CharField(max_length=512, default='')
    
    def __str__(self):
        return self.name
     

class studentOutcomes(models.Model):
    outcomeLetter = models.CharField(max_length=3, verbose_name='Outcome Letter')
    description = models.CharField(max_length=512, default='')
    
    def __str__(self):
        return self.outcomeLetter


class performanceLevels(models.Model):
    achievementLevel = models.IntegerField(default=0, verbose_name='Achievement Level')
    description = models.CharField(max_length=512, default='')
    
    def __str__(self):
        return self.description
    

# --------- SPLIT VERSIONS OF COURSE AND OUTCOME ---------- #
    
class sections(models.Model):
    
    SEMESTERS = (
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('spring', 'Spring'),
    )
    year = models.IntegerField(default=0)
    semester = models.CharField(max_length=6, choices=SEMESTERS, default='fall') 
    
    course = models.ForeignKey(courses,on_delete=models.CASCADE, null=True)
    professor = models.ForeignKey(professors, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return "%s - %s - %s%d" % (self.professor.netID , self.course.name, self.semester , self.year)
    
    
class courseOutcomes(models.Model):
    narrativeSummary = models.CharField(max_length=512, default='')
    
    studentOutcome = models.ForeignKey(studentOutcomes, on_delete=models.CASCADE, null=True, verbose_name='Outcome')
    section = models.ForeignKey(sections, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.studentOutcome.outcomeLetter + ": " + str(self.section)
    
    
class performanceIndicators(models.Model):
    name = models.CharField(max_length=512, default='')
    # section number to section
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.CharField(max_length=512, default='')
    
    outcome = models.ForeignKey(courseOutcomes, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name


# ---------- SPLIT BY PERFORMACE LEVEL ---------- # 

class outcomeData(models.Model):
    numberAchieved = models.IntegerField(default=0, verbose_name='Number Achieved')
    
    performanceLevel = models.ForeignKey(performanceLevels, on_delete=models.CASCADE, null=True, verbose_name='Performance Level')
    outcome = models.ForeignKey(courseOutcomes, on_delete=models.CASCADE, null=True, verbose_name='Outcome')

    
class rubrics(models.Model):
    gradeTopBound = models.IntegerField(default=0, verbose_name='Upper Grade Bound')
    gradeLowerBound = models.IntegerField(default=0, verbose_name='Lower Grade Bound')
    description = models.CharField(max_length=512, default='')
    numStudents = models.IntegerField(default=0, verbose_name='Number of Students')
    
    performanceLevel = models.ForeignKey(performanceLevels, on_delete=models.CASCADE, null=True, verbose_name='Performance Level')
    performanceIndicator = models.ForeignKey(performanceIndicators, on_delete=models.CASCADE, null=True, verbose_name='Performance Indicator')
    
    def __str__(self):
        return self.description


