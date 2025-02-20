from datetime import timedelta
import json
import random
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from Aptitest.models import *
from .views import UpdateStatus
from ExskilenceTest.Blob_service import *

# def get_coding_test_questions():
#     try:
# added = {
#     'SQL':[],'JS':[],'HTML':[],'Python':[]
# }
# JSONDATA_SQL = download_list_blob2('Coding_Test_Qns/SQL/','','internship')
# JSONDATA_HTML = download_list_blob2('Coding_Test_Qns/HTML/','','internship')
# JSONDATA_JS = download_list_blob2('Coding_Test_Qns/JS/','','internship')
# JSONDATA_PY = download_list_blob2('Coding_Test_Qns/Python/','','internship')

# @api_view(['PUT']) 
# def add_coding_test_questions(request):
#     try:
#         data = json.loads(request.body)
#         list_of_users = data.get('users_ids')
#         users = Test_UserDetails.objects.filter(UID__in = list_of_users)
#         for u in users:
#              # HTML
#              HTMLQN= U_Qns('HTML')
#              u.Coding_Questions.append(HTMLQN)
#              # JS
#              JSQN= U_Qns('JS')
#              u.Coding_Questions.append(JSQN)
#              # SQL
#              qn= sql_Qns()
#              u.Coding_Questions.append(qn)
#              # Python
#              PYQN= U_Qns('Python')
#              u.Coding_Questions.append(PYQN)
#              u.Coding_Questions_status.update({ j:0 for j in u.Coding_Questions})
#              u.save()
#              print('user:',u.UID,u.Coding_Questions)
 
#         return HttpResponse(json.dumps({
#             'status': 'success',
#             }), content_type='application/json')
#     except Exception as e:
#         return HttpResponse(json.dumps({
#             'status': 'error',
#             'data': str(e)}), content_type='application/json')
    
# def sql_Qns():
#         Qnslist = random.sample(JSONDATA_SQL, len(JSONDATA_SQL))
#         l2=[j.get('Qn_name')for j in Qnslist]
#         if len(added.get('SQL'))==len(Qnslist):
#             added.update({'SQL':[]})
#         while l2[0] in added.get('SQL'):
#             l2 = random.sample(l2, len(l2))
#         added.get('SQL').append(l2[0])
#         qn= l2[0]
#         return qn

# def U_Qns(sub):
#      if sub == 'HTML':
#         data =  JSONDATA_HTML
#      elif sub == 'JS':
#         data =  JSONDATA_JS
#      elif sub == 'Python':
#         data =  JSONDATA_PY
#      Qnslist = random.sample(data, len(data))
#      l2=[j.get('Qn_name')for j in Qnslist]
#      while l2[0] in added.get(sub):
#             l2 = random.sample(l2, len(l2))
#      added.get(sub).append(l2[0])
#      qn= l2[0]
#      return qn

@api_view(['POST']) 
def get_Questions(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')      
        try:
            user = Test_UserDetails.objects.get(Email = email)
        except Exception as e:
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'User not found', 'error':str(e)}), content_type='application/json')
        # userOn = None
        # for Qn in user.Coding_Questions:
        #     if user.Coding_Questions_status.get(Qn)== 0:
        #         userOn = user.Coding_Questions.index(Qn) 
        #         break
        # if userOn >=0:
        #     created = UpdateStatus(user.UID,user.Questions[userOn]) if user.Questions_status.get(user.Questions[userOn])==0 else 'success'
        # else:
        #     created =''
        AllQns =[]
        for qn in user.Coding_Questions:
            if str(qn).startswith('QSQ'):
                key = 'SQL'
            elif str(qn).startswith('QHC'):
                key = 'HTML'
            elif str(qn).startswith('QJS'):
                key = 'JS'
            elif str(qn).startswith('QPY'):
                key = 'Python'
            AllQns.append(json.loads(download_blob2('Coding_Test_Qns/'+key+'/'+qn+'.json','internship')))
        print('ss')
        return HttpResponse(json.dumps({
            'status': 'success',
            # 'duration': duration(user.UID),
            # 'created': created,
            # 'user_on' :userOn if userOn is not None else "completed",
            'data': AllQns}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': str(e)}), content_type='application/json')