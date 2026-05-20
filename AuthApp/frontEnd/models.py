from django.db import models
from django.utils import timezone
from datetime import timedelta

# HELPER FUNCTIONS

def isExpired(creationTime, minutes= 5):
    if creationTime.tzinfo is None: 
        creationTime = timezone.make_aware(creationTime)
        
    expiryCountdown = creationTime + timedelta(minutes = minutes)
    timeLeft = ((expiryCountdown - timezone.now()).total_seconds())
    return {
        "expired" : timeLeft <= 0,
        "remainingTime" : max(0, int(timeLeft))
    }

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    user_phone = models.CharField(max_length=100, null=True, blank=True)
    password = models.TextField()
    verified_status = models.BooleanField(default=False)
    account_registration = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = 'user_table'

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_active = models.DateTimeField(auto_now=True)
    session_expiry = models.DateTimeField()
    ip_address = models.GenericIPAddressField()
    access_revoked = models.BooleanField(default=False)

    class Meta: 
        db_table = 'session_table'
        indexes = [
            models.Index(fields=['user']), 
            models.Index(fields=['session_expiry'])
        ]

class OTP(models.Model):
    otp_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.TextField()
    code_status = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now)
    
    class Meta: 
        db_table = 'otp_table'
        indexes = [
            models.Index(fields=['user']), 
            models.Index(fields=['otp_code'])
        ]

class Appkey(models.Model):
    appkeyID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appkey = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    revoked_status = models.BooleanField(default=False)

    class Meta: 
        db_table = 'appkey_table'