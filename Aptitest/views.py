from datetime import timedelta
import json
import random
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from Aptitest.models import *
from ExskilenceTest.Blob_service import *
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
                    Collage = user.get('Collage'),
                    Branch = user.get('Branch'),
                )
            except Exception as e:
                notadded.append(user.get('Email'))
        return HttpResponse(json.dumps({
            'status': 'success',
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
            return HttpResponse(json.dumps({
                'status': 'success'
                }), content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'User not found'}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'User not found', 'error':str(e)}), content_type='application/json')
JSONDATA = download_list_blob('test_InterviewQuestion/','')
@api_view(['POST'])      
def get_questions(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        try:
            user = Test_UserDetails.objects.get(Email = email)
        except Exception as e:
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'User not found', 'error':str(e)}), content_type='application/json')
        qnsdata =  JSONDATA
        if user.Questions == []:
            Qns = [j.get('Qn_name') for j in qnsdata]
            Qnslist = random.sample(Qns, len(Qns))
            user.Questions = Qnslist  if len(Qnslist) > 30 else Qnslist
            user.Questions_status = { j:0 for j in user.Questions}
            user.save()
            
        userOn = None
        for Qn in user.Questions:
            if user.Questions_status.get(Qn)== 0:
                userOn = user.Questions.index(Qn) 
                break
        if userOn >=0:
            created = UpdateStatus(user.UID,user.Questions[userOn]) if user.Questions_status.get(user.Questions[userOn])==0 else 'success'
        else:
            created =''
        arranged_list = sorted(qnsdata, key=lambda x: user.Questions.index(x['Qn_name']))
        return HttpResponse(json.dumps({
            'status': 'success',
            'created': created,
            'user_on' :userOn if userOn is not None else "completed",
            'data': arranged_list}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': str(e)}), content_type='application/json')

def UpdateStatus(user_UID,next_Qn):
    try:
         nextqn,created = Test_Attendance.objects.get_or_create(UID = user_UID,QnID = next_Qn,
                defaults={
                    'UID' : user_UID,
                    'QnID' : next_Qn,
                    'Competency' : str(next_Qn)[-4],
                    'CorrectAnswer' : '',
                    'EnteredAnswer' : '',
                    'StartTime' : datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
                    'EndTime' : None,
                    })
         return 'success'
    except Exception as e:
        return 'Error  :'+str(e)
@api_view(['POST'])      
def submit_answer(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        try:
            user = Test_UserDetails.objects.get(Email = email)
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'error','data': 'User not found', 'error':str(e)}), content_type='application/json')
        Qn_ID = data.get('Qn')
        if user.Questions_status.get(Qn_ID) > 0:
            return HttpResponse(json.dumps({'status': 'Already Submited'}), content_type='application/json')
        Correct_ans = data.get('CorrectAnswer')
        Entered_ans = data.get('EnteredAnswer')
        userlastans  = Test_Attendance.objects.get(UID = user.UID,QnID =Qn_ID)
        userlastans.CorrectAnswer= Correct_ans
        userlastans.EnteredAnswer= Entered_ans
        userlastans.EndTime = datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
        userlastans.save()
        user.Questions_status.update({Qn_ID:2})
        if Entered_ans == Correct_ans :
            user.Score = int(user.Score) + 1
        user.save()
        QNLIST = user.Questions
        next_Qn_index =  QNLIST.index(Qn_ID)+1
        if next_Qn_index >= len(QNLIST):
            return HttpResponse(json.dumps({'status': 'success','data': 'success'}), content_type='application/json')
        next_Qn = QNLIST[next_Qn_index]
        created = UpdateStatus(user.UID,next_Qn)
        
        return HttpResponse(json.dumps({
            'status': 'success',
            'data': 'success'}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': str(e)}), content_type='application/json')
        