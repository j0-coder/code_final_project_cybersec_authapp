from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
import random; from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import User, OTP
from AuthApp.settings import EMAIL_HOST_USER



# This function should later be refactored to enable resending of OTPs
# def OTPGenerator(request):
#     userID = "TestUser"
#     OTPNum = str(random.randint(100000,999999))
#     OTPStorage[userID] = {"OTPCode" : OTPNum, "Attempts" : 0}
#     return JsonResponse({"OTPCode" : OTPNum})

def SendAutomatedMail(userEmail, OTPCode):
    send_mail(
        f'{'AuthApp Verification Code':}',
        f'Your OTP is: {OTPCode}\nDo not share this OTP with anyone.\nOTPs are valid for only 5 minutes.',
        EMAIL_HOST_USER,
        [userEmail],
        fail_silently=False,
    )

@csrf_exempt
def OTPValidate(request):
    userEmail = request.POST.get('email'); enteredCode = request.POST["OTPCode"]

    pendingConfirmation = request.session.get('pendingUser')
    expirationTimeOTP = request.session.get('otpExpiry')

    if not pendingConfirmation or pendingConfirmation['user_email'] != userEmail:
        return JsonResponse({"valid": False, "message": "No ongoing sessions found"})
    if enteredCode == pendingConfirmation['otp_code'] and datetime.fromisoformat(expirationTimeOTP) > datetime.now():
        userAccount = User.objects.create(
            user_email = pendingConfirmation['user_email'],
            user_name = pendingConfirmation['user_name'],
            user_phone = pendingConfirmation['user_phone'],
            password = pendingConfirmation['password'],
            verified_status = True
        )
        otpCode = OTP.objects.create(
            user = userAccount,
            otp_code = make_password(pendingConfirmation['otp_code']),
            code_status = True,
            creation_date = datetime.now().replace(microsecond=0),
        )
        del request.session['pendingUser']; del request.session['otpExpiry']
        return JsonResponse({"valid": True, "message": "OTP is valid"})
    else:
        return JsonResponse({"valid": False, "message": "Invalid OTP"})
    # try:
    #     user = User.objects.get(user_email = user_email)
    #     otp = OTP.objects.filter(user = user).latest('otp_expiry')
    #     if enteredCode == otp.otp_code and otp.otp_expiry > datetime.now():
    #         user.verified_status = True
    #         user.save()
    # #         return JsonResponse({"valid": True, "message": "OTP is valid"})
    # #     else:
    # #         return JsonResponse({"valid": False, "message": "Invalid OTP"})
    # except User.DoesNotExist:
    #     return JsonResponse({"valid": False, "message": "User does not exist"})

# Create your views here.
def webHomePage(request):
    return render(request, 'toc.html')

def loginPage(request):
    if request.method == 'POST':
        userEmail = request.POST.get('email')
        userPassword = request.POST.get('password')
        try:
            userAccount = User.objects.get(user_email = userEmail)
            if userAccount.verified_status:
                if check_password(userPassword, userAccount.password):
                    return render(request, 'success.html', {'user': userAccount})
                else: return JsonResponse({"valid": False, "message": "Incorrect Password"})
            else: return JsonResponse({"valid": False, "message": "User is not verified"})
        except User.DoesNotExist:
            return JsonResponse({"valid": False, "message": "User does not exist"})
    return render(request, 'login.html')

def dashBoardPage(request):
    return render(request, 'dashboard.html')

def signupPage(request):
    if request.method == 'POST':
        userEmail = request.POST.get('email')
        userName = request.POST.get('name')
        userPhone = request.POST.get('phone')
        userPassword = request.POST.get('password')
        passwordConfirmation = request.POST.get('password2')

        if userPassword != passwordConfirmation:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        # else:
        #     user = User.objects.create(
        #         user_email=user_email,
        #         user_name=user_name,
        #         user_phone=user_phone,
        #         password=password
        #     ); otp_code = str(random.randint(100000,999999))
        #     OTP.objects.create(
        #         user = user,
        #         otp_code = otp_code,
        #         otp_expiry = datetime.now() + timedelta(seconds = 5)
        #     ); 
        #     print(f"OTP: {otp_code}")
        #     return render(request, 'otp.html', {'user': user, 'otp_code': otp_code, 'email': user_email})
        otpCode = str(random.randint(100000,999999))
        request.session['pendingUser'] = {
            'user_email': userEmail,
            'user_name': userName,
            'user_phone': userPhone,
            'password': make_password(userPassword),
            'otp_code': otpCode
            }
        request.session['otpExpiry'] = (datetime.now() + timedelta(minutes = 5)).isoformat()
        SendAutomatedMail(userEmail, otpCode)
        print(f'OTP: {otpCode}')
        return render(request, 'otp.html', {'otp_code': otpCode, 'email': userEmail})
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
