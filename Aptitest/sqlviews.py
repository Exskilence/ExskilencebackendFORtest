import json
import re
from django.http import HttpResponse, JsonResponse
from ExskilenceTest.settings import *
from rest_framework.decorators import api_view
from datetime import  datetime, timedelta
from .models import *
from .sqlrun import *

from django.core.cache import cache
CONTAINER ="internship"
# Create your views here.

def addAttempt (studentId,Subject,Qn,Attempt,ans):
    try :
            mainuser  = Test_UserDetails.objects.get(UID = studentId)
            stat = mainuser.Coding_Questions_status.get(Qn)
            if stat < 2 :
                user = QuestionDetails_Days.objects.filter(Student_id=str( studentId),Subject=str( Subject ),Qn=str( Qn )).first()
                if user is not None :
                    user.Attempts=user.Attempts+1
                    user.EndTime=datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
                    user.Ans=ans
                    user.save()
                    return user.Attempts
                else:
                    q = QuestionDetails_Days(
                    Student_id=str(studentId),
                    Subject=str( Subject),
                    Score=0,
                    Attempts=1,
                    StartTime =datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
                    EndTime =datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
                    Qn = str(Qn),
                    Ans = ans
                    )
                    q.save()
                    return 1
            else:
                return 0
    except Exception as e:
        return 'False'
@api_view(['POST'])
def sql_query(req):
    if req.method == 'POST':
        try:
            current_time=datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
            data = req.body
            data = json.loads(data)
            query = str(data.get('query')).strip()
            Attempt = data.get('Attempt')
            Subject = data.get ('Subject')
            studentId = data.get('UID')
            Qn = data.get('Qn')
            addAttempts = addAttempt(studentId,Subject,Qn,Attempt,query)
            out = local(query)
            result= out
            ExpectedOutput=data.get('ExpectedOutput')
            TestCases=data.get('TestCases')
            main ={
                'TestCases':list(testcase_validation(query,result,ExpectedOutput,TestCases))
                ,'data':out
                ,'Time':[{"Execution_Time":str((datetime.utcnow().__add__(timedelta(hours=5,minutes=30))-current_time).total_seconds())[0:-2]+" s"}],
                'Attempt':addAttempts
 
            }
            return HttpResponse(json.dumps(main), content_type='application/json')
            # return JsonResponse(main)
        # except Exception as e:
        #     ErrorLog(req,e)
        #     attendance_update(data.get('StudentId'))
        #     return JsonResponse({"Error": str(e)}, safe=False)
        except Exception as e:  
            return HttpResponse(f"An error occurred: {e}", status=500)
        
def removespace(query_list):
    sl=re.compile(r'[*=,]')
    query=[]
    for s in query_list:
        if sl.search(s):
            equal_index = query_list.index(s)
            if s=='=' or s=='*':#sl.search(s):
                data=query_list[equal_index-1]+query_list[equal_index]+query_list[equal_index+1]
                query_list.remove(query_list[equal_index+1]) 
                query.pop()
                query.append(data)
            elif s.startswith('=') or s.startswith('*') :# or s.endswith('=' or'*'):
                data=query_list[equal_index-1]+query_list[equal_index]
                query.pop()
                query.append(data)
            elif s.endswith('=')or s.endswith('*') :
                data=query_list[equal_index]+query_list[equal_index+1]
                query_list.remove(query_list[equal_index+1]) 
                query.append(data)        
            elif s.endswith(','):
                query.append(query_list[equal_index][0:-1])        
            elif s.startswith(','):
                query.append(query_list[equal_index][1:]) 
            elif s.count(',')  :
                data=query_list[equal_index].split(',')
                query.append(data[0])
                query.append(data[1])       
            else:
                query.append(s)
        else:
            query.append(s)
    return query

def testcase_validation(query,result,ExpectedOutput,TestCases):
    try:
            bol=True
            main=[]
            i=0
            bol=True
            for t in TestCases:
                if i==1:
                    t=t["Testcase"].replace('##',' ').split()[0].split(',')
                    key=str(result[0].keys())

                    key = key.replace('dict_keys(', '')[0:-1]
                    t=str(key).lower()==str(t).lower()
                    if t:
                        t={"TestCase"+str(i) :"Passed"}
                    else:
                        t={"TestCase"+str(i) :"Failed"}
                        bol=False
                    main.append(t)
                if i==2:
                    t=t["Testcase"]
                    if str(result).lower().replace('.0','')==str(t).lower().replace('.0',''):#======================================
                        t={"TestCase"+str(i) :"Passed"}
                    else:
                        t={"TestCase"+str(i) :"Failed"}
                        bol=False
                    main.append(t)
                if i>=3:
                    t=t['Testcase']
                    q = str(re.sub(r"([^\w\s])", r" \1 ", query)).lower().split()
                    t2 = str(re.sub(r"([^\w\s])", r" \1 ", t)).lower().split()
                    if str(q).__contains__(str(t2)[1:-1]):#len(list(common))==len(t2):
                        t={"TestCase"+str(i) :"Passed"}
                    else:
                        t={"TestCase"+str(i) :"Failed"}
                        bol=False
                    main.append(t)
                i=i+1
            if bol:
                t={"TestCase"+str(i) :"Passed"}
                main.append(t)
                result_json = json.dumps(str(result).lower().replace('.0',''), sort_keys=True)
                result_json = json.loads(result_json)
            
                ExpectedOutput_json = json.dumps(str(ExpectedOutput).lower().replace('.0',''), sort_keys=True)
                ExpectedOutput_json = json.loads(ExpectedOutput_json)
                if result_json == ExpectedOutput_json:
                    data={"Result" :"True"}
                else:
                    data=   {"Result" :"False"}
            else:
                t=TestCases[0]["Testcase"]#.split()
                # t=removespace(t)
                t=str(t).lower()
                queryt=str(query).lower()
                if queryt==t:
                    t={"TestCase"+str(i) :"Passed"}
                else:
                    t={"TestCase"+str(i) :"Failed"}
                    
                main.append(t)
                data={"Result" :"False"}
                bol=False

            main.append(data)
            return main
    except Exception as e:
        return False

