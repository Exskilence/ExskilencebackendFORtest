import json
import re
from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import cssutils
from ExskilenceTest.Blob_service import download_blob
from .Coding_test import add_daysQN_db
from .models import *
# from .frontend_views import add_daysQN_db
  

def css_to_tuples(css_code,KEYS):
    parser = cssutils.CSSParser()
    if KEYS :
        tuple_format_css = []

        for style in KEYS:
            if "media_query" in style:
                media_query = style["media_query"]
                rules = style["rules"]
                media_rules = [(rule["selector"], [(prop["property"], prop["value"]) for prop in rule["properties"]]) for rule in rules]
                tuple_format_css.append((media_query, media_rules))
            elif "keyframes_name" in style:
                keyframes_name = style["keyframes_name"]
                keyframes_steps = style["keyframes_steps"]
                keyframes = [(step["selector"], [(prop["property"], prop["value"]) for prop in step["properties"]]) for step in keyframes_steps]
                tuple_format_css.append((keyframes_name, keyframes))
            else:
                    selector = style["selector"]
                    properties = style["properties"]
                    prop_list = [(prop["property"], prop["value"]) for prop in properties]
                    tuple_format_css.append((selector, prop_list))
        tuple_format_css=[(i[0].lower().replace(" ", "").replace(" =", "=").replace("= ", "=").replace(" ,", ",").replace(", ", ","),[(j[0].lower().replace(" ", "").replace(" =", "=").replace("= ", "=").replace(" ,", ",").replace(", ", ","),j[1]) for j in i[1]]) for i in tuple_format_css]
        return tuple_format_css
    else:
        stylesheet = parser.parseString(css_code)
        css_tuples = []

        for rule in stylesheet:
            if rule.type == rule.STYLE_RULE:
                selector = rule.selectorText
                properties = []
                for property in rule.style:
                        if str(property.value).__contains__('#') == True :
                            values = property.value.split()
                            for i in range(len(values)):
                                if str(values[i]).startswith('#') and len(str(values[i]).replace(',','')) == 4:
                                    exc = str(values[i])
                                    if str(values[i]).__contains__(','):

                                        exc2 = '#' + exc[1]+exc[1]+exc[2]+exc[2]+exc[3]+exc[3]+','
                                    else:
                                        exc2 = '#' + exc[1]+exc[1]+exc[2]+exc[2]+exc[3]+exc[3]
                                    values[i] = exc2
                            newvalues = ' '.join(values)
                            properties.append((property.name, newvalues))
                        else:
                            properties.append((property.name, property.value))
                css_tuples.append((selector, properties))
            elif rule.type == rule.MEDIA_RULE:
                media_query = rule.media.mediaText.strip()
                media_rules = []

                for media_rule in rule.cssRules:
                    if media_rule.type == media_rule.STYLE_RULE:
                        selector = media_rule.selectorText
                        properties = [(property.name, property.value) for property in media_rule.style]
                        media_rules.append((selector, properties))

                css_tuples.append((media_query, media_rules))
            elif rule.type == rule.KEYFRAMES_RULE:
                keyframes_name = rule.name.strip()
                keyframes_steps = []

                for keyframe in rule.cssRules:
                    if keyframe.type == keyframe.KEYFRAME_RULE:
                        keyframe_selector = keyframe.keyText.strip()
                        keyframe_properties = [(property.name, property.value) for property in keyframe.style]
                        keyframes_steps.append((keyframe_selector, keyframe_properties))

                css_tuples.append((keyframes_name, keyframes_steps))
    css_tuples=[(i[0].lower().replace(" ", "").replace(" =", "=").replace("= ", "=").replace(" ,", ",").replace(", ", ","),[(j[0].lower().replace(" ", "").replace(" =", "=").replace("= ", "=").replace(" ,", ",").replace(", ", ","),j[1]) for j in i[1]]) for i in css_tuples]
    
    return css_tuples
def tupletolist(css_tuples,tupleKeys):
 try:
    anskey =[]
    tupleKey =[]
    ansvalue=[]
    tupleValue=[]
    out =[]
    for i in range(len(css_tuples)):
        css_tuples[i]=list(css_tuples[i])
        anskey.append(css_tuples[i][0])
        ansvalue.append(css_tuples[i][1])
    for i in range(len(tupleKeys)):
        tupleKeys[i]=list(tupleKeys[i])
        tupleKey.append(tupleKeys[i][0])
        tupleValue.append(tupleKeys[i][1])
    for i in  anskey:
        if i in tupleKey:
            ansv = ansvalue[anskey.index(i)]
            tuplev = tupleValue[tupleKey.index(i)]
            com = [i1 for i1 in ansv if i1 in tuplev]
            if len(com) == len(tuplev):
                out.append([i,com])
    return out
 except:
    return [i for i in tupleKeys if i in css_tuples]
@api_view(['POST'])
def css_compare(req    ):
    try:
        data = json.loads(req.body)
        # css_code = data['Ans']
        # keys=data['KEYS']
        # css_tuples_a = css_to_tuples("",keys)
        # css_tuples_b = css_to_tuples(css_code,'')
        # # print('key',css_tuples_a)
        # # print('***********')
        # # print('code',css_tuples_b)
        # common_keywords = tupletolist(css_tuples_b,css_tuples_a)
        # # print('***********')
        # # print(common_keywords)
        output={}
        # if len(common_keywords) == len(css_tuples_a):
        output.update({"valid": True,"message": "CSS code is valid."})
        # else:
        #     output.update({"valid": False,"message": "CSS code is Not valid."})
        score = f'0/0'
        data.update({"Score": f'0/0' ,"Result":'-/-'})
        if data.get('UID') == 'trainer':
            res = 'No data'
        else:
            res= add_daysQN_db(data)
        if str(res).__contains__("An error occurred"):
            resStatuses = "No"
        else:
            resStatuses = "Yes"
        output.update({"score": '-/-',"Res":"-/-", "CSSStatuses":resStatuses})
        return HttpResponse(json.dumps(output), content_type='application/json')
        # return JsonResponse(output)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
        # return JsonResponse({"valid": False,"message": f"An error occurred: {e}"})

def jsonToTuple(code):
    tuple_format = []
    for element in code:
        tag = element["tag"]
        attrs = element["attributes"]
        
        if attrs:
            for attr_name, attr_value in attrs.items():
                tuple_format.append((tag, attr_name, attr_value))
        else:
            tuple_format.append((tag, None, None))
    tuple_format=[
                (tag.lower().replace(" ", "").replace(" =", "=").replace("= ", "=").replace(" ,", ",").replace(", ", ","), attr.lower().replace(" ", "").replace(" =", "=").replace("= ", "=").replace(" ,", ",").replace(", ", ",") if isinstance(attr, str) else attr, 
                 [value.lower().replace(" ", "").replace(" =", "=").replace("= ", "=").replace(" ,", ",").replace(", ", ",") if isinstance(value, str) else value for value in (value if isinstance(value, list) else [value])])
                for tag, attr, value in tuple_format
                ]
    tuple_format=[
                        (tag, attr, value) 
                        for tag, attr, values in tuple_format 
                        for value in (values if isinstance(values, list) else [values])
                    ]
    return tuple_format
def alltags(data,allowedtags,BODY):
    try:
        tags = r'<([a-zA-Z0-9]+)(\s*[^>]*)?>'
        ctags = r'</([a-zA-Z0-9]+)(\s*[^>]*)?>'
        self_closing_pattern = r'<([a-zA-Z][a-zA-Z0-9]*)\s*[^>]*\/?>'
        selfClosingTags = [
          "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
          "meta", "param", "source", "track", "wbr"
        ]
        t=re.findall(tags ,  data)
        t2=re.findall(ctags ,  data)
        sct=re.findall(self_closing_pattern ,  data)
        
        filtered_tags = [tag for tag in sct if tag in selfClosingTags    ]
        alltags       = [tag for tag in t if tag not in selfClosingTags  ]
        closing       = [tag for tag in t2 if tag not in selfClosingTags ]
        ot=[]
        ct=[]
        
        for tag in alltags:
            if tag[0] not in selfClosingTags:
                ot.append(tag[0])
        for tag in closing:
            if tag[0] not in selfClosingTags:
                ct.append(tag[0])
        if BODY:
            for tag in ot:
                if tag  in allowedtags:
                    print('Invalid HTML BODY ********** tag',tag)
                    return 0
            for tag in ct:
                if tag  in allowedtags:
                    print('Invalid HTML BODY ********** tag',tag)
                    return 0
            out = (len(ot)-len(ct)) if (len(ot)-len(ct)) > 0 else (len(ot)-len(ct)) * -1
            if out > 0:
                return out
            else:
                return -1                
        else:
            for tag in ot:
                if tag not in allowedtags:
                    print('Invalid HTML ********** tag',tag)
                    return False
            for tag in ct:
                if tag not in allowedtags:
                    print('Invalid HTML ********** tag',tag)
                    return False
        valid = True
        for tag in alltags:
            if tag[0] not in selfClosingTags and tag[0] not in ct:
                valid = False
                print('Invalid HTML ********** tag',tag[0])
                break
            else:
                if tag[0] not in selfClosingTags:
                    ct.remove(tag[0])
                    ot.remove(tag[0])
                    valid = True
        if valid is False:
            print('Invalid HTML')
            print('ot',ot)
            print('ct',ct)
            return False
        if len(ot) != len(ct):
            print('Invalid HTML')
            print('ot',ot)
            print('ct',ct)
            return False
        return True
    except Exception as e:
        print(e)
        return False
def extract_tag_content(data, tags):
            contents = {}
            for tag in tags:
                pattern = rf"<{tag}.*?>(.*?)</{tag}>"
                match = re.search(pattern, data, re.DOTALL)
                if match:
                    contents[tag] = match.group(1).strip()
            return contents
def HTMLStructure(codedata):
    try:
        ot = codedata.replace(' ','').replace('>',' > '). count('<html')
        ct = codedata.replace(' ','').replace('>',' > '). count('</html >')
        if ot != ct:
            return False
        data = BeautifulSoup((codedata), 'html.parser')
        htmltag =data.html.contents
        htmlvalid = ['head', 'body']
        hot = codedata.replace(' ','').replace('>',' > '). count('<head ')
        hct = codedata.replace(' ','').replace('>',' > '). count('</head >')

        bct = codedata.replace(' ','').replace('>',' > '). count('</body >')
        bot = codedata.replace(' ','').replace('>',' > '). count('<body')

        if hot != hct or hot != 1 or hct != 1:
            return False
        if bot != bct or bot != 1 or bct != 1:
            return False
        for tag in htmltag:
            if tag.name is not None and tag.name not in htmlvalid:
                return False    
        headvalid = data.head.contents
        HTMLdata = extract_tag_content(codedata, htmlvalid)
        htmlstrucHead = ['title', 'meta', 'link', 'style', 'script']
        htmlstrucbbody = ['title', 'meta', 'link', 'style', 'script','head','html']
        Headdatavalid = alltags(HTMLdata.get('head'), htmlstrucHead, False)
        if Headdatavalid == False :
            return False

        for tag in headvalid:
            if tag.name is not None and tag.name not in htmlstrucHead:
                return False
        if not data.body:
            return False
        codebody = data.body.contents
        for tag in codebody:
            if tag.name is not None and tag.name in htmlstrucbbody and tag.name in htmlvalid and tag.name in ['html']:
                return False
        return True
            
    except Exception as e:
        print(e)
        return f"An error occurred: {e}"
    
@api_view(['POST'])
def html_page(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            output = {}
            output.update({"valid": True,"message": "HTML code is valid."})
            data.update({"Score": '0/0' ,"Result":'-/-'})
            if data.get('StudentId') == 'trainer':
                res= 'No data'
            else:
                res= add_daysQN_db(data)
            if str(res).__contains__("An error occurred"):
                resStatuses = "No"
            else:
                resStatuses = "Yes"
            output.update({"score": '-/-',"Res":'-/-', "HTMLStatuses":resStatuses})
            return HttpResponse(json.dumps(output), content_type='application/json')
            # return JsonResponse(output, safe=False)

        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
            # return JsonResponse({"Error": str(e)}, safe=False)
    else:
        return HttpResponse("Method Not Allowed", status=405)
        # return JsonResponse({"Error": "Method Not Allowed"}, safe=False)
   
def scoring_logic(Score,QN):
        if str(QN)[-4]=='E':
            return Score*5
        elif str(QN)[-4]=='M':
            return Score*10
        elif str(QN)[-4]=='H':
            return Score*15
        else:
            return Score 