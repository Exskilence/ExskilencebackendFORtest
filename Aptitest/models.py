from djongo import models

# Create your models here.
class Test_Attendance (models.Model):
    SLID = models.AutoField(primary_key=True)
    UID = models.CharField(max_length=10000)
    QnID = models.CharField(max_length=25)
    Competency = models.CharField(max_length=25)
    EnteredAnswer = models.CharField(max_length=25)
    CorrectAnswer = models.CharField(max_length=25)
    StartTime = models.DateTimeField()
    EndTime     = models.DateTimeField()

    class meta:
        db_table = 'Test_Attendance'
class Test_UserDetails (models.Model):
    UID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=25)
    Email = models.CharField(max_length=25,unique=True)
    Collage = models.CharField(max_length=25)
    Branch = models.CharField(max_length=25)
    Questions = models.JSONField(default=list)
    Questions_status = models.JSONField(default=dict)
    Score = models.IntegerField(default=0)
    Test_status = models.CharField(max_length=25,default='Not_Started')

    class meta:
        db_table = 'Test_UserDetails'