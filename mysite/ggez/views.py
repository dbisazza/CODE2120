from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from .models import *
import os,sys
import requests


# Create your views here.

def example_get(request, var_a, var_b):
	try:
		returnob = {
		"dis what u want?": "hi %s: %s" %(var_a, var_b), "n":"o"
		}
		return JsonResponse(returnob)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		other = sys.exc_info()[0].__name__
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		errorType = str(exc_type)
		return JsonResponse({"isError": True, "error":str(e), "errorType":errorType, "function":fname, "line":exc_tb.tb_lineno, "log":log})

@csrf_exempt
def example_post(request):
	log = []
	if request.method == "POST":
		try:
			
			data = request.POST["data"]
			jsob = json.loads(data)
			print(jsob)
			print(type(jsob))
			index = 0

			for i in jsob['demo']:
				index += 1
			s = int(jsob['n1']) + int(jsob['n2'])
			m = int(jsob['n1']) * int(jsob['n2'])
			count = 0
			num1 = 0
			num2 = 1
			fib = [num2]
			while (int(jsob['limit'])) > count:
				nextNum = num1 + num2
				num1 = num2
				num2 = nextNum
				fib.append(nextNum)
				count += 1



			results = {'sum': s, 'multiplcation':m, 'fib': fib}


			return JsonResponse(results)
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			other = sys.exc_info()[0].__name__
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			errorType = str(exc_type)
			return JsonResponse({"isError": True, "error":str(e), "errorType":errorType, "function":fname, "line":exc_tb.tb_lineno, "log":log})
	else:
		return HttpResponse("<h1>ONLY POST REQUESTS</h1>")

@csrf_exempt
def fib(request):
	log = []
	jsob = {"startNumber": 0, "length": 10} #DEFAULTS
	if request.method == "POST":
		try:
			
			data = request.POST["data"]
			recieved = json.loads(data)
			jsob.update(recieved)
			
			
			startNumber = int(jsob['startNumber'])
			length = int(jsob['length'])
			loop = range(length)

			numarray = []

			fibno = startNumber
			addno = 1


			for l in loop:
				numarray.append(fibno)
				fibno = fibno + addno
				addno = fibno - addno




			return JsonResponse({'fib': numarray})
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			other = sys.exc_info()[0].__name__
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			errorType = str(exc_type)
			return JsonResponse({"isError": True, "error":str(e), "errorType":errorType, "function":fname, "line":exc_tb.tb_lineno, "log":log})
	else:
		return JsonResponse(jsob)
		
@csrf_exempt
def image(request):
	log = []
	jsob = {"clusters": 5,"path": 0}
	if request.method == "POST":
		try: 
			data = request.POST["data"]
			print(data)
			received = json.loads(str(data))
			jsob.update(received)
			path = jsob.get("path")
			tmp_file = 'tmp.jpg'
			urllib.request.urlretrieve(path,filename=tmp_file)
			execution_path = os.getcwd()
			print ('exe:     ' + str(execution_path)+ "\example/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
			prediction = ImagePrediction()
			prediction.setModelTypeAsResNet()
			print ('exe:     ' + str(execution_path) + "\example/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
			prediction.setModelPath( execution_path + "/example/resnet50_weights_tf_dim_ordering_tf_kernels.h5")

			prediction.loadModel()

			path = jsob.get("path")
			predictions, percentage_probabilities = prediction.predictImage(tmp_file, result_count=5)
			results = {}
			for index in range(len(predictions)):
				idk = (predictions[index] , " : " , percentage_probabilities[index])
				results[predictions[index]] =  percentage_probabilities[index]

			return JsonResponse(results)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			other = sys.exc_info()[0].__name__
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			errorType = str(exc_type)
			return JsonResponse({"isError": True, "error":str(e), "errorType":errorType, "function":fname, "line":exc_tb.tb_lineno, "log":log})
	else:
		 	return JsonResponse(jsob)
