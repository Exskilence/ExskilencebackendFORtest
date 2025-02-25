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
    College = models.CharField(max_length=25)
    Branch = models.CharField(max_length=25)
    Questions = models.JSONField(default=list)
    Questions_status = models.JSONField(default=dict)
    Coding_Questions = models.JSONField(default=list)
    Coding_Questions_status = models.JSONField(default=dict)
    Score = models.IntegerField(default=0)
    Coding_Score = models.FloatField(default=0)
    Test_status = models.CharField(max_length=25,default='Not_Started')
    Coding_Test_status = models.CharField(max_length=25,default='Not_Started')
    Duration = models.IntegerField(default=0)
    Last_update = models.DateTimeField(default=None)

    class meta:
        db_table = 'Test_UserDetails'

class QuestionDetails_Days(models.Model):
    sl_no           = models.AutoField(primary_key=True)
    Student_id      = models.CharField(max_length=25)
    Subject         = models.CharField(max_length=25)
    Attempts        = models.IntegerField()
    StartTime       = models.DateTimeField()
    EndTime         = models.DateTimeField()
    Score           = models.FloatField()
    Qn              = models.TextField(max_length=25)
    Ans             = models.TextField()
    Result          = models.JSONField(default=dict)

    class meta:
        db_table = 'Test_Coding_details'