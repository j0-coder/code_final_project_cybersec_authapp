# from django.utils import timezone
# from datetime import datetime
# from django.shortcuts import redirect

# class SessionTimeout:
#     def __init__(self, getResponse):
#         self.getResponse = getResponse 
#         self.timeout = 900

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             lastActive = request.session.get('last_active')
#             now = timezone.now()

#             if lastActive:
#                 elapsedTime = (now - timezone.make_aware(datetime.fromisoformat(lastActive))).total_seconds()
#                 if elapsedTime > self.timeout:
#                     request.session.flush()
#                     return redirect('login')
#             else:
#                 request.session['last_active'] = now.isoformat()
#         return self.getResponse(request)