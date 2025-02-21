from datetime import timedelta, timezone
import json
import random
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from Aptitest.models import *
from .sqlrun import get_tables
from .views import UpdateStatus
from ExskilenceTest.Blob_service import *


added = {
    'SQL':[],'JS':[],'HTML':[],'Python':[]
}
JSONDATA_SQL = download_list_blob2('Coding_Test_Qns/SQL/','','internship')
JSONDATA_HTML = download_list_blob2('Coding_Test_Qns/HTML/','','internship')
JSONDATA_JS = download_list_blob2('Coding_Test_Qns/JS/','','internship')
JSONDATA_PY = download_list_blob2('Coding_Test_Qns/Python/','','internship')

@api_view(['PUT']) 
def add_coding_test_questions(request):
    try:
        data = json.loads(request.body)
        list_of_users = data.get('users_ids')
        users = Test_UserDetails.objects.filter(UID__in = list_of_users)
        for u in users:
             # HTML
             HTMLQN= U_Qns('HTML')
             u.Coding_Questions.append(HTMLQN)
             # JS
             JSQN= U_Qns('JS')
             u.Coding_Questions.append(JSQN)
             # SQL
             qn= sql_Qns()
             u.Coding_Questions.append(qn)
             # Python
             PYQN= U_Qns('Python')
             u.Coding_Questions.append(PYQN)
             u.Coding_Questions_status.update({ j:0 for j in u.Coding_Questions})
             u.save()
             print('user:',u.UID,u.Coding_Questions)
 
        return HttpResponse(json.dumps({
            'status': 'success',
            }), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': str(e)}), content_type='application/json')
    
def sql_Qns():
        Qnslist = random.sample(JSONDATA_SQL, len(JSONDATA_SQL))
        l2=[j.get('Qn_name')for j in Qnslist]
        if len(added.get('SQL'))==len(Qnslist):
            added.update({'SQL':[]})
        while l2[0] in added.get('SQL'):
            l2 = random.sample(l2, len(l2))
        added.get('SQL').append(l2[0])
        qn= l2[0]
        return qn

def U_Qns(sub):
     if sub == 'HTML':
        data =  JSONDATA_HTML
     elif sub == 'JS':
        data =  JSONDATA_JS
     elif sub == 'Python':
        data =  JSONDATA_PY
     Qnslist = random.sample(data, len(data))
     l2=[j.get('Qn_name')for j in Qnslist]
     while l2[0] in added.get(sub):
            l2 = random.sample(l2, len(l2))
     added.get(sub).append(l2[0])
     qn= l2[0]
     return qn

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
        userOn = None
        for Qn in user.Coding_Questions:
            if user.Coding_Questions_status.get(Qn)== 0:
                userOn = user.Coding_Questions.index(Qn) 
                break
        # if userOn >=0:
        #     created = UpdateStatus(user.UID,user.Questions[userOn]) if user.Questions_status.get(user.Questions[userOn])==0 else 'success'
        # else:
        #     created =''
        AllQns =[]
        useranss = list(QuestionDetails_Days.objects.filter(Student_id=user.UID).values("Subject","Ans"))
        useranss = {u.get('Subject'):u.get('Ans') for u in useranss}
        for qn in user.Coding_Questions:
            if str(qn).startswith('QSQ'):
                key = 'SQL'
            elif str(qn).startswith('QHC'):
                key = 'HTML'
            elif str(qn).startswith('QJS'):
                key = 'JS'
            elif str(qn).startswith('QPY'):
                key = 'Python'
            jsonData = json.loads(download_blob2('Coding_Test_Qns/'+key+'/'+qn+'.json','internship'))
            if key == 'HTML':
                jsonData.update({'User_HTML_ans':useranss.get('HTML'),'User_CSS_ans':useranss.get('CSS')})
            elif key == 'SQL':
                tabs =  get_tables(jsonData.get('Table'))
                jsonData.update({'User_SQL_ans':useranss.get('SQL'),'Qn_Tables':tabs })
            else:
                jsonData.update({'User_ans':useranss.get(key)})
            jsonData.update({ "Qn_name": qn})
            AllQns.append(jsonData)
        print('ss')
        user.Coding_Test_status='Started'
        if user.Last_update is None:
            user.Last_update= datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=5, minutes=30)
        user.Duration +=( datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=5, minutes=30)-user.Last_update).total_seconds()
        user.Last_update=datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
        user.save()
        return HttpResponse(json.dumps({
            'status': 'success',
            'duration': user.Duration,
            # 'created': created,
            'user_on' :userOn if userOn is not None else "completed",
            'data': AllQns}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': str(e)}), content_type='application/json')
    

@api_view(['POST'])
def submit(request)  :
    jsondata = json.loads(request.body)
    try:
        result = add_daysQN_db(jsondata)
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({'Error':str(e)}), content_type='application/json')
def Scoring_logic(passedcases,data):
    attempt = data.get("Attempt")
    if data.get("Subject") == "Python":
        user = QuestionDetails_Days.objects.filter(Student_id=str(data.get("UID")),Subject=str(data.get("Subject")),Qn=str(data.get("Qn"))).first()

        if user :

            attempt = user.Attempts

        else:

            attempt = 1
    attempt_scores = {
    "E": {1: 5, 2: 5, 3: 3, 4: 2},
    "M": {1: 10, 2: 10, 3: 10,  4: 8, 5: 6, 6: 4, 7: 2},
    "H": {1: 15, 2: 15, 3: 15, 4: 15 ,5: 15, 6: 12, 7: 12, 8: 10, 9: 8, 10: 6, 11: 4, 12: 2},
    }
    qn_type = str(data.get('Qn'))[-4]
    score = attempt_scores.get(qn_type, {}).get(attempt, 0)
    # #(score)
    return   round(score*passedcases ,2)
def add_daysQN_db(data):
    try:
        res = data.get("Result")
        attempt = data.get("Attempt")
        i = 0
        passedcases = 0
        totalcases = 0
        result = {}
        if data.get("Subject") == 'HTML' or data.get("Subject") == 'CSS' or data.get("Subject") == 'Java Script'or data.get("Subject") == 'JS':
                requirements = int(str(data.get("Score")).split('/')[0])/int(str(data.get("Score")).split('/')[1])
                score = Scoring_logic(requirements,{ "Attempt":1, "Qn":data.get("Qn") })
                result = res
                attempt = 1
        else:
            for r in res:
                i += 1
                if r.get("TestCase" + str(i)) == 'Passed' or r.get("TestCase" + str(i)) == 'Failed':
                    totalcases += 1
                    if r.get("TestCase" + str(i)) == 'Passed':
                        passedcases += 1
                    result.update(r)
                if r.get("Result") == 'True' or r.get("Result") == 'False':
                    result.update(r)
            if passedcases == totalcases and passedcases ==0:
                score = 0
            else:
                score = Scoring_logic(passedcases/totalcases,data)
        user = QuestionDetails_Days.objects.filter(Student_id=str(data.get("UID")),Subject=str(data.get("Subject")),Qn=str(data.get("Qn"))).first()
       
        mainuser  = Test_UserDetails.objects.get(UID = data.get('UID'))
        if user is  None:
            q = QuestionDetails_Days(
                Student_id=str(data.get("UID")),
                Subject=str(data.get("Subject")),
                Score=score,
                Attempts=attempt,
                StartTime =datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
                EndTime =datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
                Qn = str(data.get("Qn")),
                Ans = str(data.get("Ans")),
                Result = {"TestCases":result}
                )
            q.save()
        else:
            user.Score = score
            user.EndTime = datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
            user.Ans = str(data.get("Ans"))
            user.Result = {"TestCases":result}
            user.save()
        
        if mainuser.Coding_Questions_status.get(data.get("Qn")) <2:
                mainuser.Coding_Score  = mainuser.Coding_Score + score
                mainuser.Coding_Questions_status.update({data.get("Qn"):2})
        mainuser.Duration +=( datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=5, minutes=30)-mainuser.Last_update).total_seconds()
        mainuser.Last_update=datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
        mainuser.save()
        mainuser.save()
        return ({"status": "success"})
    except Exception as e:
        return ({"status": "error", "message": str(e)})
    
@api_view(['POST'])
def Coding_duration(req):
    try:
        data = json.loads(req.body)
        email = data.get('email')      
        try:
            user = Test_UserDetails.objects.get(Email = email)
        except Exception as e:
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'User not found', 'error':str(e)}), content_type='application/json')
        if user.Last_update is None:
            user.Last_update= datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
        now = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=5, minutes=30)
        user.Duration += (now-user.Last_update).total_seconds()
        user.Last_update = datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
        user.save()
        return HttpResponse(json.dumps({
            'status': 'success',}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({'Error':str(e)}), content_type='application/json')
   