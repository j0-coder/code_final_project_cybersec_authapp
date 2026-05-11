from django.shortcuts import render
import random; from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import User, OTP

OTPStorage = {}

# def OTPGenerator(request):
#     userID = "TestUser"
#     OTPNum = str(random.randint(100000,999999))
#     OTPStorage[userID] = {"OTPCode" : OTPNum, "Attempts" : 0}
#     return JsonResponse({"OTPCode" : OTPNum})

@csrf_exempt
def OTPValidate(request):
    user_email = request.POST.get('email')
    enteredCode = request.POST["OTPCode"]
    try:
        user = User.objects.get(user_email = user_email)
        otp = OTP.objects.filter(user = user).latest('otp_expiry')
        if enteredCode == otp.otp_code and otp.otp_expiry > datetime.now():
            user.verified_status = True
            user.save()
            return JsonResponse({"valid": True, "message": "OTP is valid"})
        else:
            return JsonResponse({"valid": False, "message": "Invalid OTP"})
    except User.DoesNotExist:
        return JsonResponse({"valid": False, "message": "User does not exist"})

# Create your views here.
def webHomePage(request):
    return render(request, 'toc.html')

def loginPage(request):
    return render(request, 'login.html')

def dashBoardPage(request):
    return render(request, 'dashboard.html')

def signupPage(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_name = request.POST.get('name')
        user_phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password2')

        if password != password_confirmation:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        else:
            user = User.objects.create(
                user_email=user_email,
                user_name=user_name,
                user_phone=user_phone,
                password=password
            ); otp_code = str(random.randint(100000,999999))
            OTP.objects.create(
                user = user,
                otp_code = otp_code,
                otp_expiry = datetime.now() + timedelta(minutes = 5)
            ); 
            print(f"OTP: {otp_code}")
            return render(request, 'otp.html', {'user': user, 'otp_code': otp_code, 'email': user_email})
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
