# import json
# import math
# import random
# from datetime import date, datetime, time, timedelta
# from django.http import HttpResponse, JsonResponse
# from .models import *
# from rest_framework.decorators import api_view
# from ExskilenceTest.Blob_service import download_blob2,download_list_blob2
# from .views import Scoring_logic
# CONTAINER ="internship"


# def add_daysQN_db(data):
#     try:
#         res = data.get("Result")
#         if data.get("Subject") == 'HTML' or data.get("Subject") == 'CSS' or data.get("Subject") == 'Java Script' or data.get("Subject") == 'Java_Script':
#                 requirements = int(str(data.get("Score")).split('/')[0])/int(str(data.get("Score")).split('/')[1])
#                 score = Scoring_logic(requirements,{ "Attempt":1, "Qn":data.get("Qn") })
#                 result = res
#                 attempt = 1
#         user = QuestionDetails_Days.objects.filter(Student_id=str(data.get("StudentId")),Subject=str(data.get("Subject")),Qn=str(data.get("Qn"))).first()
#         mainuser = StudentDetails_Days_Questions.objects.filter(Student_id=str(data.get("StudentId"))).first()
#         if mainuser is None:
#             mainuser = StudentDetails_Days_Questions(
#                 Student_id=str(data.get("StudentId")),   
#                 Days_completed = {data.get("Subject"):0},
#                 Qns_lists = {data.get("Subject"):[]},
#                 Qns_status = {data.get("Subject"):{}},
#                 Ans_lists = {data.get("Subject"):[]},
#                 Score_lists = {data.get("Subject")+'Score':"0/0"},
#             )   
#             mainuser.save()
#         if user is  None:
#             q = QuestionDetails_Days(
#                 Student_id=str(data.get("StudentId")),
#                 Subject=str(data.get("Subject")),
#                 Score=score,
#                 Attempts=attempt,
#                 DateAndTime=datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#                 Qn = str(data.get("Qn")),
#                 Ans = str(data.get("Ans")),
#                 Result = {"TestCases":{'Testcase':result,
#                           "Result":str(str(result).split('/')[0] == str(result).split('/')[1])}}
#                 )
#             q.save()
#             if str(data.get("Qn") )[-4] == 'E':
#                 outoff = 5
#             elif str(data.get("Qn") )[-4] == 'M':
#                 outoff = 10
#             elif str(data.get("Qn") )[-4] == 'H':
#                 outoff = 15
#             if mainuser.Qns_status.get(data.get('Subject') ) is None:
#                 mainuser.Qns_status.update({data.get('Subject') :{}})
#             if mainuser.Ans_lists.get(data.get("Subject")) is None:
#                 mainuser.Ans_lists.update({data.get("Subject"):[]}) #mainuser.Ans_lists[data.get("Subject")]=[]
#             if mainuser.Score_lists.get(data.get("Subject")+'Score') is None or mainuser.Score_lists.get(data.get("Subject")+'Score')==[]:
#                 mainuser.Score_lists.update({data.get("Subject")+'Score':"0/0"}) #mainuser.Score_lists[data.get("Subject")+'Score']=0
#             oldscore =  mainuser.Score_lists.get(data.get("Subject")+'Score',"0/0").split('/')[0]
#             totaloff = mainuser.Score_lists.get(data.get("Subject")+'Score',"0/0").split('/')[1]
#             if data.get("Qn") not in mainuser.Ans_lists.get(data.get("Subject")):
#                 mainuser.Score_lists.update({data.get("Subject")+'Score':str(float(oldscore)+float(score))+'/'+str(float(totaloff)+float(outoff))})
#                 mainuser.Ans_lists[data.get("Subject")].append(data.get("Qn"))
#                 if str(result).split('/')[0] == str(result).split('/')[1]:
#                     mainuser.Qns_status.get(data.get("Subject")).update({data.get("Qn"):3}) 
#                 else:
#                     mainuser.Qns_status.get(data.get("Subject")).update({data.get("Qn"):2})
#                 if mainuser.End_Course is None:
#                     mainuser.End_Course = {}
#                 mainuser.End_Course.update({data.get("Subject"):datetime.utcnow().__add__(timedelta(hours=5,minutes=30))})
#                 mainuser.save() 
#         # print(data.get('Subject'))
#         if data.get('Subject') == 'HTML' or data.get('Subject') == 'CSS':
#             ln_htmlcss = len(mainuser.Qns_lists.get("HTMLCSS",[]))
#             ln_htmlAns = len(mainuser.Ans_lists.get("HTML",[]))
#             ln_cssAns = len(mainuser.Ans_lists.get("CSS",[]))
#             # print(ln_htmlcss,ln_htmlAns,ln_cssAns)
#             if( ln_htmlcss == ln_htmlAns or ln_htmlcss == ln_cssAns) and ln_htmlcss > 0:
#                 # print('UPDATING RANKS...')
#         else:
#             if len(mainuser.Qns_lists.get(data.get("Subject"),[])) == len(mainuser.Ans_lists.get(data.get("Subject"),[])) and len(mainuser.Qns_lists.get(data.get("Subject"),[])) > 0:
#                 # print('UPDATING RANKS...')
#         return {'Result':"Answer has been submitted successfully"}
#     except Exception as e:
#         print(e)
#         return 'An error occurred'+str(e)
    
