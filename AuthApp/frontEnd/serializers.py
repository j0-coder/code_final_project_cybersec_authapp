# from datetime import datetime, timedelta
# import random
# from django.conf import settings
# from rest_framework import serializers
# from frontEnd.models import UserModel

# print(settings.MAX_OTP_ATTEMPTS)

# class UserSerializer(serializers.ModelSerializer):
#     userPassword = serializers.CharField(write_only=True, min_length = settings.MIN_PASSWORD_LENGTH, error_messages = {"min_length" : f"Password must be atleast {settings.MIN_PASSWORD_LENGTH} characters long."})

#     userPasswordConfirmation = serializers.CharField(write_only=True, min_length = settings.MIN_PASSWORD_LENGTH, error_messages = {"min_length" : f"Password must be atleast {settings.MIN_PASSWORD_LENGTH} characters long."})

#     class Meta:
#         model = UserModel
#         fields = ['phoneNumber', 'email', 'userPassword', 'userPasswordConfirmation']
#         extra_kwargs = {
#             'userPassword': {'write_only': True},
#             'userPasswordConfirmation': {'write_only': True}
#         }
#     def validate(self, userData):
#         if userData['userPassword'] != userData['userPasswordConfirmation']:
#             raise serializers.ValidationError({"password": "Password and Password Confirmation do not match."})
#         return userData
    
#     def create(self, validatedData):
#         OTPNum = random.randint(1000,9999); OTPExpiry = datetime.now() + timedelta(minutes = 5)
#         user = UserModel(phoneNumber = validatedData['phoneNumber'], email = validatedData['email'],OTPNum = OTPNum, OTPExpiry = OTPExpiry, OTPAttempts = settings.MAX_OTP_ATTEMPTS)
#         user.set_password(validatedData['userPassword'])
#         user.save()
#         return user