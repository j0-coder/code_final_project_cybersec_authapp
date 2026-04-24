from django.shortcuts import render

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
