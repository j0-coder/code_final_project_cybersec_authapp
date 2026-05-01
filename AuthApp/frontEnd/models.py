from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator

# Create your models here.

phoneRegex = RegexValidator(regex=r'^\+639?1?\d{12}$', message="Phone number must be entered in the format: '+639999999999'.")
validateEmail = RegexValidator(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', message="Invalid email address")

class UserTypeManager(BaseUserManager):
    def createUser(self, phoneNumber, password=None):
        if not phoneNumber:
            raise ValueError('Users must have a phone number')
        user = self.model(phoneNumber=phoneNumber)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def createAdminUser(self, phoneNumber, password):
        user = self.createUser(phoneNumber, password)
        user.isAdmin = True; user.isActive = True; 
        user.save(using=self._db)
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(validators=[validateEmail], max_length=255, blank=True, null=True, unique=True)
    phoneNumber = models.CharField(validators=[phoneRegex], max_length=12, blank=False, null=False, unique=True)
    OTPNum = models.CharField(max_length=6)
    OTPAttempts = models.CharField(default=settings.maxOTPAttempts, max_length=2)
    OTPExpiry = models.DateTimeField(blank=True, null=True); OTPCooldown = models.DateTimeField(blank=True, null=True)

    isActive = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    userRegisterTime = models.DateTimeField(auto_now_add=True)


    objects = UserTypeManager()
    USERNAME_FIELD = 'phoneNumber'
    REQUIRED_FIELDS = ['phoneNumber']

    def __str__(self):
        return self.phoneNumber