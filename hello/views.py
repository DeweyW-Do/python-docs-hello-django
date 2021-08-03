from django.http import HttpResponse
from django.shortcuts import render

# def hello(request):
#     return HttpResponse("Hello, World!")

import urllib.request # rest api 호출용 모듈 전부 입력
import json
import pkg_resources
import subprocess
import sys
import os
import ssl
 
def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
 
def index(request):
# api에서 데이터를 받아오는 구문
    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
    data = {'param':{'bld':1}}
    body = str.encode(json.dumps(data))
    url = 'http://52.141.0.146:80/api/v1/service/tsop-skt-ahu-economizer/score' # 엔드포인트 > tsop-skt-ahu-economizer > REST 엔드포인트 값
    api_key = 'UrAzVhOgxF0xvmYeWHN48CqaVf42Fx5L' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)
 
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        result = json.loads(result.decode("utf-8"))
 
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
 
# 결과물을 values라는 json에 올림
# values에 원하는 수치를 올리고, tables/table1.html를 랜더링
    values = json.loads(result['table'])
    values['time'] = result['time']
    values['out_enthalpy'] = result['out_enthalpy']
    values['out_Temperature'] = result['out_Temperature']
    values['out_Humidity'] = result['out_Humidity']
    values['now_time'] = result['now_time']
    values['fine_dust'] = result['fine_dust']
    values['fine_particulate_matter'] = result['fine_particulate_matter']
 
    return render(request, "tables/table1.html", context = values)
