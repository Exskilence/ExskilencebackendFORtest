from datetime import timedelta, timezone
import random
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from Aptitest.models import *
from ExskilenceTest.Blob_service import *
from .MCQ_views import upjson

ONTIME = ONTIME = datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
@api_view(['GET'])   
def home(request):
    # data = {
    #     'JSONDATA_SQL' : download_list_blob2('Coding_Test_Qns/SQL/','','internship'),
    #     'JSONDATA_HTML' :download_list_blob2('Coding_Test_Qns/HTML/','','internship'),
    #     'JSONDATA_JS' : download_list_blob2('Coding_Test_Qns/JS/','','internship'),
    #     'JSONDATA_PY' : download_list_blob2('Coding_Test_Qns/Python/','','internship')
    # }
    # res = {'MCQ':upjson(download_list_blob('test_InterviewQuestion/NEWQns/','')),
    #         'Coding':upjson(download_list_blob('test_InterviewQuestion/NEWQns/',''))
    # }

    return HttpResponse(json.dumps({'Message': 'Welcome to the Home Page of thoughtprocess online test By RK :--'+str(ONTIME)}), content_type='application/json')
@api_view(['POST'])
def AddUsers(request):
    try:
        data = json.loads(request.body)
        notadded = []
        userslist = data.get('users')
        for user in userslist:
            try:
                u = Test_UserDetails.objects.create(
                    Name = user.get('Name'),
                    Email = user.get('Email'),
                    College = user.get('College'),
                    Branch = user.get('Branch'),
                    batch = user.get('Batch'),
                    Year = str(datetime.utcnow().year),
                    Created_on = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=5, minutes=30)
                )
            except Exception as e:
                notadded.append(user.get('Email'))
        return HttpResponse(json.dumps({
            'status': 'success',
            'saved': len(userslist)-len(notadded),
            'notadded': len(notadded),
            'data': notadded}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': str(e)}), content_type='application/json')
@api_view(['POST']) 
def login (request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        user = Test_UserDetails.objects.get(Email = email)
        if user:
            if user.Name != 'TEST':
                return HttpResponse(json.dumps({
                    'status': 'error',
                    'data': 'User not found'
                }), content_type='application/json')
            if user.Coding_Test_status=='Completed':
                return HttpResponse(json.dumps({
                'status': 'Test Completed'
                }), content_type='application/json')
            return HttpResponse(json.dumps({
                'status': 'success',
                'UID':  user.UID
                }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'User not found'}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'User not found', 'error':str(e)}), content_type='application/json')
    

@api_view(['POST'])
def Test_duration(req):
    try:
        data = json.loads(req.body)
        email = data.get('email')  
        type = data.get('type')    
        try:
            user = Test_UserDetails.objects.get(Email = email)
        except Exception as e:
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'User not found', 'error':str(e)}), content_type='application/json')
        if user.Last_update is None:
            user.Last_update= datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=5, minutes=30)
        now = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=5, minutes=30)
        if type == 'mcq': 
            user.MCQ_duration += (now-user.Last_update).total_seconds()
            Duration = user.MCQ_duration
        else:
            user.Coding_duration += (now-user.Last_update).total_seconds()
            Duration = user.Coding_duration
        user.Last_update = datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
        user.save()
        return HttpResponse(json.dumps({
            'status': 'success',
            'duration':Duration}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({'Error':str(e)}), content_type='application/json')
    

# JSONDATA = download_list_blob('test_InterviewQuestion/','')
# JSONDATA = []

# @api_view(['GET'])
# def updateJson(request):
#     global JSONDATA
#     # JSONDATA = download_list_blob('test_InterviewQuestion/','')
#     JSONDATA = download_list_blob('test_InterviewQuestion/NEWQns/','')
#     return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json') 
# @api_view(['POST'])      
# def get_questions(request):
#     try:
#         data = json.loads(request.body)
#         email = data.get('email')
#         try:
#             user = Test_UserDetails.objects.get(Email = email)
#         except Exception as e:
#             return HttpResponse(json.dumps({
#                 'status': 'error',
#                 'data': 'User not found', 'error':str(e)}), content_type='application/json')
#         qnsdata =  JSONDATA
#         if user.Test_status == 'Completed':
#             return HttpResponse(json.dumps({
#                 'status': 'error',
#                 'data': 'Test Already Completed'}), content_type='application/json')
#         if user.Questions == []:
#             Qns = [j.get('Qn_name') for j in qnsdata]
#             Qnslist = random.sample(Qns, len(Qns))
#             user.Questions = Qnslist  if len(Qnslist) > 30 else Qnslist
#             user.Questions_status = { j:0 for j in user.Questions}
#             user.Test_status = 'Started'
#             user.save()
            
#         userOn = None
#         for Qn in user.Questions:
#             if user.Questions_status.get(Qn)== 0:
#                 userOn = user.Questions.index(Qn) 
#                 break
#         if userOn >=0:
#             created = UpdateStatus(user.UID,user.Questions[userOn]) if user.Questions_status.get(user.Questions[userOn])==0 else 'success'
#         else:
#             created =''
#         arranged_list = sorted(qnsdata, key=lambda x: user.Questions.index(x['Qn_name']))
#         # print(duration(user.UID))
#         return HttpResponse(json.dumps({
#             'status': 'success',
#             'duration': duration(user.UID),
#             'created': created,
#             'user_on' :userOn if userOn is not None else "completed",
#             'data': arranged_list}), content_type='application/json')
#     except Exception as e:
#         return HttpResponse(json.dumps({
#             'status': 'error',
#             'data': str(e)}), content_type='application/json')

# def UpdateStatus(user_UID,next_Qn):
#     try:
#          nextqn,created = Test_Attendance.objects.get_or_create(UID = user_UID,QnID = next_Qn,
#                 defaults={
#                     'UID' : user_UID,
#                     'QnID' : next_Qn,
#                     'Competency' : str(next_Qn)[-4],
#                     'CorrectAnswer' : '',
#                     'EnteredAnswer' : '',
#                     'StartTime' : datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#                     'EndTime' : datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#                     })
#          return 'success'
#     except Exception as e:
#         return 'Error  :'+str(e)
# @api_view(['POST'])      
# def submit_answer(request):
#     try:
#         data = json.loads(request.body)
#         email = data.get('email')
#         try:
#             user = Test_UserDetails.objects.get(Email = email)
#         except Exception as e:
#             return HttpResponse(json.dumps({'status': 'error','data': 'User not found', 'error':str(e)}), content_type='application/json')
#         Qn_ID = data.get('Qn')
#         if user.Questions_status.get(Qn_ID) > 0:
#             return HttpResponse(json.dumps({'status': 'Already Submited'}), content_type='application/json')
#         Correct_ans = data.get('CorrectAnswer')
#         Entered_ans = data.get('EnteredAnswer')
#         userlastans  = Test_Attendance.objects.get(UID = user.UID,QnID =Qn_ID)
#         userlastans.CorrectAnswer= Correct_ans
#         userlastans.EnteredAnswer= Entered_ans
#         userlastans.EndTime = datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
#         userlastans.save()
#         user.Questions_status.update({Qn_ID:2})
#         if Entered_ans == Correct_ans :
#             user.Score = int(user.Score) + 1
#         user.save()
#         QNLIST = user.Questions
#         next_Qn_index =  QNLIST.index(Qn_ID)+1
#         if next_Qn_index >= len(QNLIST):
#             return HttpResponse(json.dumps({'status': 'success','data': 'success'}), content_type='application/json')
#         next_Qn = QNLIST[next_Qn_index]
#         created = UpdateStatus(user.UID,next_Qn)
        
#         return HttpResponse(json.dumps({
#             'status': 'success',
#             'duration': duration(user.UID),
#             'data': 'success'}), content_type='application/json')
#     except Exception as e:
#         return HttpResponse(json.dumps({
#             'status': 'error',
#             'data': str(e)}), content_type='application/json')
# from django.db.models import Min, Max      
# def duration(UID):
#     try:
#         answers = Test_Attendance.objects.filter(UID = UID)
#         # print("1",len(answers))
#         if len(answers) > 0:
#             agg = answers.aggregate(low=Min('StartTime'), high=Max('EndTime'))
#             # print('2')
#             low = agg['low']
#             high = agg['high']
#         else:
#             now = datetime.utcnow() + timedelta(hours=5, minutes=30)
#             low = high = now
#         # print("3")
#         duration = (high - low).total_seconds()
#         print('high',high,'low',low,'duration',duration/60)
#         return duration
#     except Exception as e:
#         return 0
# @api_view(['POST'])
# def logout(request):
#     try:
#         data = json.loads(request.body)
#         email = data.get('email')
#         user = Test_UserDetails.objects.get(Email = email)
#         # user.Test_status = 'Completed'
#         user.Coding_Test_status = "Completed"
#         user.save()
#         return HttpResponse(json.dumps({
#             'status': 'success' }), content_type='application/json')
#     except Exception as e:
#         return HttpResponse(json.dumps({
#             'status': 'error',
#             'data': str(e)}), content_type='application/json')
  
# @api_view(['GET'])
# def report(requrst):
#     try:
#         users = list(Test_UserDetails.objects.exclude(Name="TEST").values('Name', 'Email', 'College', 'Branch', 'Score', 'Test_status').order_by("-Score"))
#         for u in users:
#             if u.get('Test_status') =='Not_Started':
#                 u.update({'Test_status':"No","Score":'-',"Total_Score":30,'Percentage': '0%'})
#             else:
#                 u.update({'Test_status':"Yes","Total_Score":30,'Percentage': str(round((u.get('Score') / 30) * 100, 2))+'%'})
#         return HttpResponse(json.dumps({
#             'data':  users}), content_type='application/json')
#     except Exception as e:
#         return HttpResponse(json.dumps({
#             'status': 'error',
#             'data': str(e)}), content_type='application/json')