from datetime import timedelta, timezone
import random
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from Aptitest.models import *
from ExskilenceTest.Blob_service import *


@api_view(['POST']) 
def Trainer_login (request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        user = Trainer_details.objects.get(Email = email)
        if user:
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
def AddTrainer(request):
    try:
        data = json.loads(request.body)
        notadded = []
        userslist = data.get('users')
        for user in userslist:
            try:
                u = Trainer_details.objects.create(
                    Name = user.get('Name'),
                    Email = user.get('Email'),
                    Created_on = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=5, minutes=30)
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
def Delete_users(request):
    try:
        data = json.loads(request.body)
        emails = data.get('emails')
        users = Test_UserDetails.objects.filter(Email__in = emails)
        for user in users:
            if user:
                Qns_details = QuestionDetails_Days.objects.filter(Student_id=user.UID).delete()
                apti_ans = Test_Attendance.objects.filter(UID = user.UID).delete()
                user.delete()
        return HttpResponse(json.dumps({
            'status': 'success',
            'data': 'Users deleted'}), content_type='application/json')
        
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'User not found', 'error':str(e)}), content_type='application/json')

@api_view(['GET'])
def get_all_students(request):
    try:
        users = list(Test_UserDetails.objects.values('Name', 'Email', 'College', 'Branch', 'Score', 'Test_status','Questions').order_by("-Score"))
        return HttpResponse(json.dumps({
            'status': 'success',
            'data': users}), content_type='application/json')
        
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'User not found', 'error':str(e)}), content_type='application/json')