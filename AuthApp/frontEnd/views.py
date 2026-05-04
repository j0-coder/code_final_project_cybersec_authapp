from django.shortcuts import render
import random; from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

OTPStorage = {}

def OTPGenerator(request):
    userID = "TestUser"
    OTPNum = str(random.randint(100000,999999))
    OTPStorage[userID] = {"OTPCode" : OTPNum, "Attempts" : 0}
    return JsonResponse({"OTPCode" : OTPNum})

@csrf_exempt
def OTPValidate(request):
    userID = "TestUser"
    enteredCode = request.POST["OTPCode"]
    OTPData = OTPStorage.get(userID)

    if not OTPData:
        return JsonResponse({"valid": False, "message": "No OTP found"})
    OTPData["Attempts"] += 1
    if enteredCode == OTPData["OTPCode"]:
        return JsonResponse({"valid": True, "message": "OTP is valid"})
    else:
        return JsonResponse({"valid": False, "message": "Invalid OTP"})

# Create your views here.
def webHomePage(request):
    return render(request, 'toc.html')

def loginPage(request):
    return render(request, 'login.html')

def dashBoardPage(request):
    return render(request, 'dashboard.html')

def signupPage(request):
    return render(request, 'signup.html')

def OTPPage(request):
    return render(request, 'otp.html')

def forgotPage(request):
    return render(request, 'forgot.html')

def successPage(request):
    return render(request, 'success.html')

def failedPage(request):
    return render(request, 'failed.html')

def lockedPage(request):
    return render(request, 'locked.html')

def appKeyPage(request):
    return render(request, 'appkey.html')

def termsAndConditionsPage(request):
    return render(request, 'tc.html')
