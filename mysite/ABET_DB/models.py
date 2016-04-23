from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

def current():
    now = timezone.now()
    semNow = str()
    if now.month <= 5:
        semNow = "spring"
    elif now.month >= 7:
        semNow = "fall"
    else:
        semNow = "summer"
   
    return (semNow, now.year)

# ---------- TOP LEVEL [no forign keys] ---------- #

class professors(models.Model):
    netID = models.CharField(max_length=512, default='', verbose_name='Net ID')
    fn = models.CharField(max_length=512, default='', verbose_name='First Name')
    ln = models.CharField(max_length=512, default='', verbose_name='Last Name')
    
    class Meta:
        verbose_name = 'Professors'
        verbose_name_plural = 'Professors'
    
    def __str__(self):
        return self.netID


class courses(models.Model):
    name = models.CharField(max_length=512, default='', verbose_name='Course Name')
    description = models.CharField(max_length=512, default='')
    
    class Meta:
        verbose_name = 'Courses'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return self.name
     

class studentOutcomes(models.Model):
    outcomeLetter = models.CharField(max_length=3, verbose_name='Outcome Letter')
    description = models.CharField(max_length=512, default='')
    
    class Meta:
        verbose_name = 'Outcomes'
        verbose_name_plural = 'Outcomes'
    
    def __str__(self):
        return self.outcomeLetter


class performanceLevels(models.Model):
    achievementLevel = models.IntegerField(default=0, verbose_name='Achievement Level')
    description = models.CharField(max_length=512, default='')
    
    class Meta:
        verbose_name = 'Performance Levels'
        verbose_name_plural = 'Performance Levels'
    
    def __str__(self):
        return self.description
    

# --------- SPLIT VERSIONS OF COURSE AND OUTCOME ---------- #
    
class sections(models.Model):
    
    SEMESTERS = (
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('spring', 'Spring'),
    )
    
    sem, yr = current()
    
    year = models.IntegerField(default=yr)
    semester = models.CharField(max_length=6, choices=SEMESTERS, default=sem) 
    
    course = models.ForeignKey(courses,on_delete=models.CASCADE, null=True)
    professor = models.ForeignKey(professors, on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = 'Sections'
        verbose_name_plural = 'Sections'
    
    def __str__(self):
        return "%d, %s, %s   %s, %s" % (self.year , self.semester, self.course.name, self.professor.ln, self.professor.fn)
        
    
class courseOutcomes(models.Model):
    narrativeSummary = models.CharField(max_length=512, default='', verbose_name='Narrative Summary')
    studentOutcome = models.ForeignKey(studentOutcomes, on_delete=models.CASCADE, null=True, verbose_name='Outcome')
    section = models.ForeignKey(sections, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Outcome-Section Mappings'
        verbose_name_plural = 'Outcome-Section Mappings'

    def __str__(self):
        return self.studentOutcome.outcomeLetter + ": " + str(self.section)
    
    
class performanceIndicators(models.Model):
    name = models.CharField(max_length=512, default='')
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.CharField(max_length=512, default='')
    
    outcome = models.ForeignKey(courseOutcomes, on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = 'Performance Indicators'
        verbose_name_plural = 'Performance Indicators'
    
    def __str__(self):
        return self.name


# ---------- SPLIT BY PERFORMACE LEVEL ---------- # 

class outcomeData(models.Model):
    numberAchieved = models.IntegerField(default=0, verbose_name='Number Achieved')
    performanceLevel = models.ForeignKey(performanceLevels, on_delete=models.CASCADE, null=True, verbose_name='Performance Level')
    outcome = models.ForeignKey(courseOutcomes, on_delete=models.CASCADE, null=True, verbose_name='Outcome')

    class Meta:
        verbose_name = 'Outcome Data'
        verbose_name_plural = 'Outcome Data'
    
    
class rubrics(models.Model):
    gradeTopBound = models.IntegerField(verbose_name='Upper Grade Bound',null=True)
    gradeLowerBound = models.IntegerField( verbose_name='Lower Grade Bound',null=True)
    numStudents = models.IntegerField(verbose_name='Number of Students',null=True)
    description = models.CharField(max_length=512,null=True)
    
    performanceLevel = models.ForeignKey(performanceLevels, on_delete=models.CASCADE, verbose_name='Performance Level')
    performanceIndicator = models.ForeignKey(performanceIndicators, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Rubrics'
        verbose_name_plural = 'Rubrics'
    
    def __str__(self):
        return self.description


