import json
import re
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
import jsbeautifier
from ExskilenceTest.Blob_service import  get_blob_container_client
from .Coding_test import add_daysQN_db
from .models import *
# from .frontend_views import add_daysQN_db

@api_view(['POST'])
def run_test_js(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        js_code = data['Ans']
        # beautified_js1 = jsbeautifier.beautify(js_code)
        # d1 = beautified_js1.split('\n')
        # # print(d1)
        # for i in d1:
        #       print(i)
        # sam = data['KEYS']
        # print(sam)
        # ans = [a.replace(' ','').replace('"',"'") for key in sam for a in d1 if str(a.replace(' ','').replace('"',"'")).__contains__(key.replace(' ','').replace('"',"'"))]
        # print(ans)
        # common_keywords = [i for i in sam if any(str(j).__contains__(str(i).replace(' ','').replace('"',"'")) for j in ans)]
        # print(common_keywords)
        output = {
            "valid": '-/-',
            "message": "JS code is valid." ,
            "common":'-/-',
            'Failed': '-/-', #[{'keyword':i} for i in sam if not any(str(j).__contains__(str(i).replace(' ','').replace('"',"'")) for j in ans)]
        }
        score = f'-/-'
        data.update({"Score": score,"Result":score})
        res= add_daysQN_db(data)
        # print('database',res)
        if str(res).__contains__("An error occurred"):
                resStatuses = "No"
        else:
                resStatuses = "Yes"
        output.update({"score": score,"Res":res, "JSStatuses":resStatuses})
        # output.update({"score": score,"Res":res})
        return HttpResponse(json.dumps(output), content_type='application/json')
    
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    

@api_view(['POST'])
def  js_Score(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        data.update({"Score": '-/-' ,"Result":'-/-'})
        res= add_daysQN_db(data)
        if str(res).__contains__("An error occurred"):
                resStatuses = "No"
        else:
                resStatuses = "Yes"
        output = {
            "valid": '-/-',
            "message": "JS code is valid." ,
            "score": '-/-',
            "Res":res,
            "JSStatuses":resStatuses
        }
        return HttpResponse(json.dumps(output), content_type='application/json')
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
       

