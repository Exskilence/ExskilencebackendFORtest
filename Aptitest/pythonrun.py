from django.http import HttpResponse, JsonResponse
import json
from rest_framework.decorators import api_view
from .sqlviews import addAttempt

@api_view(['POST'])
def run_python(request):
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body)
            code=jsondata.get('Code')
            callfunc=jsondata.get('CallFunction')
            code_data=str(code+'\n'+callfunc).split('\n')
            result=jsondata.get('Result')
            TestCases=jsondata.get('TestCases')
            Attempt = jsondata.get('Attempt')
            Subject = jsondata.get ('Subject')
            studentId = jsondata.get('UID')
            Qn = jsondata.get('Qn')
            Day_no = jsondata.get('Day_no')
            bol=True
            main=[]
            i=0
            for tc in TestCases:
                if i==0:
                    tc=tc.get('Testcase')
                    boll=[]
                    for t in tc:
                        for c in code_data:
                            if str(c).replace(' ','').startswith('#') or str(c).replace(' ','').startswith('"""') or str(c).replace(' ','').startswith("'''"):
                                code_data.remove(c)
                                continue
                            if str(c).replace(' ','').startswith(str(t).replace(' ','')):
                                boll.append({t:code_data.index(c),"val": str(c)})
                                break 
                    unique_in_tc = [item for item in tc if item not in {key for d in boll for key in d.keys()}]
                    for u in unique_in_tc:
                        if str(code_data).__contains__(u):
                            boll.append({u:True,"val": str(u)})
                    if len(boll)==len(tc):
                        t={"TestCase"+str(i+1) :"Passed"}
                        main.append(t)
                    else:
                        t={"TestCase"+str(i+1) :"Failed"}
                        bol=False
                        main.append(t)
                if i>0:
                    tc=tc['Testcase']
                    Values=tc['Value']
                    Output=tc['Output']
                    def slashNreplace(string):
                        if string=='':
                            return string
                        if string[-1]=='\n':
                            string=slashNreplace(string[:-1])
                        return string
                    for val in Values:
                        for b in boll :
                            key=str(b.keys()).split("'")[1]
                            if str(val).replace(' ','').split('=')[0] in str(b.keys()): 
                                newvalue=str(b['val'])[0:str(b['val']).index(key[0])]+val
                                if str(val).startswith(key):
                                    if str(val).replace(' ','').split('=')[0]==code_data[b[key]].replace(' ','').split('=')[0]:
                                        code_data[b[key]]=newvalue
                                    else:
                                        for c in code_data:
                                            if str(c).replace(' ','').split('=')[0]==(str(val).replace(' ','').split('=')[0]):
                                                newvalue = str(c)[0:str(c).index(key[0])]+val
                                                code_data[code_data.index(c)]= newvalue
                                                break
                                                
                    newcode=""
                    for c in code_data:
                        newcode=newcode+str(c)+'\n' 

                    t = {'TestCase'+str(i+1) :
                    {'Code':newcode,'Output':str(Output)}}

                    main.append(t)
                i=i+1
            data={'Result' : {
                'Code':code+'\n'+callfunc,
                'Output':str(result)}}

            main.append(data)
            addAttempts = addAttempt(studentId,Subject,Qn,Attempt,str(code+'\n'+callfunc))
            Output={'TestCases':main,
                    'Attempt':addAttempts
                    }
            # return JsonResponse(Output)
            return HttpResponse(json.dumps(Output), content_type="application/json")
        except Exception as e:
            # return JsonResponse({"Error": str(e)}, safe=False)
            return HttpResponse('Error! User does not exist', status=404)

@api_view(['POST'])
def run_pythonDSA(request):
        try:
            jsondata = json.loads(request.body)
            code=jsondata.get('Code')
            callfunc=jsondata.get('CallFunction')
            code_data=str(code+'\n'+callfunc).split('\n')
            result=jsondata.get('Result')
            TestCases=jsondata.get('TestCases')
            Attempt = jsondata.get('Attempt')
            Subject = jsondata.get ('Subject')
            studentId = jsondata.get('studentId')
            Qn = jsondata.get('Qn')
            Day_no = jsondata.get('Day_no')
            bol=True
            main=[]
            i=0
            for tc in TestCases:
                if i==0:
                    tc=tc.get('Testcase')
                    boll=[]
                    for t in tc:
                        for c in code_data:
                            if str(c).replace(' ','').startswith('#') or str(c).replace(' ','').startswith('"""') or str(c).replace(' ','').startswith("'''"):
                                code_data.remove(c)
                                continue
                            if str(c).replace(' ','').startswith(str(t).replace(' ','')):
                                boll.append({t:code_data.index(c),"val": str(c)})
                                break 
                    unique_in_tc = [item for item in tc if item not in {key for d in boll for key in d.keys()}]
                    for u in unique_in_tc:
                        if str(code_data).__contains__(u):
                            boll.append({u:True,"val": str(u)})
                    if len(boll)==len(tc):
                        t={"TestCase"+str(i+1) :"Passed"}
                        main.append(t)
                    else:
                        t={"TestCase"+str(i+1) :"Failed"}
                        bol=False
                        main.append(t)
                if i>0:
                    tc=tc['Testcase']
                    Values=tc['Value']
                    Output=tc['Output']
                    if jsondata.get('ClassTypeValidation','False') == 'True':
                        # print('ClassTypeValidation')
                        
                        # print(code+'\n'+Values[0])
                        # print(Output)
                        t = {'TestCase'+str(i+1) :
                        {'Code':code+'\n'+Values[0],'Output':str(Output)}}

                        main.append(t)
                                            
                    else:
                        # def slashNreplace(string):
                        #     if string=='':
                        #         return string
                        #     if string[-1]=='\n':
                        #         string=slashNreplace(string[:-1])
                        #     return string
                        for val in Values:
                            for b in boll :
                                key=str(b.keys()).split("'")[1]
                                if str(val).replace(' ','').split('=')[0] in str(b.keys()): 
                                    newvalue=str(b['val'])[0:str(b['val']).index(key[0])]+val
                                    if str(val).startswith(key):
                                        if str(val).replace(' ','').split('=')[0]==code_data[b[key]].replace(' ','').split('=')[0]:
                                            code_data[b[key]]=newvalue
                                        else:
                                            for c in code_data:
                                                if str(c).replace(' ','').split('=')[0]==(str(val).replace(' ','').split('=')[0]):
                                                    newvalue = str(c)[0:str(c).index(key[0])]+val
                                                    code_data[code_data.index(c)]= newvalue
                                                    break
                                                    
                        newcode=""
                        for c in code_data:
                            newcode=newcode+str(c)+'\n' 

                        t = {'TestCase'+str(i+1) :
                        {'Code':newcode,'Output':str(Output)}}

                        main.append(t)
                i=i+1
            data={'Result' : {
                'Code':code+'\n'+callfunc,
                'Output':str(result)}}

            main.append(data)
            addAttempts = addAttempt(studentId,Subject,Qn,Attempt,Day_no)
            Output={'TestCases':main,
                    'Attempt':addAttempts
                    }
            return HttpResponse(json.dumps(Output), content_type="application/json")
        except Exception as e:
            return HttpResponse('Error! User does not exist', status=404)
