from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.db.models.fields.related import manytomanyfield

class AuditTimestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    updated_by = models.IntegerField(blank=True,null=True)
    class Meta:
        abstract = True


""" Role Model """
class Role(AuditTimestamp):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    class Meta:
        db_table = "user_roles"

    def __str__(self):
        return self.name


""" User Model """
class User(AuditTimestamp):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    password = models.CharField(
        max_length=128,
        validators=[
            RegexValidator(
                regex=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
                message="Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        ]
    )
    phone = models.CharField(
                    max_length=10,
                    validators=[
                      RegexValidator(
                        regex=r"^[6-9]\d{9}$", 
                        message="Enter a valid 10-digit Indian phone number starting with 6, 7, 8, or 9."
                        )
                    ],
                    unique=True
                )
    is_active = models.BooleanField(default=True)
    is_register_complete = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False) 
    # is_employer = models.BooleanField(default=False)
    role_id = manytomanyfield(Role, related_name="roles")

    Required_fields = ['email', 'password', 'phone','role_id']
    
    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

""" OTP Model """
class Otp(AuditTimestamp):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=45)
    phone = models.CharField(max_length=10)
    otp = models.CharField(max_length=7,blank=False,null=True)
    expire_at = models.DateTimeField(blank=False,null=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = "user_otp"


""" User Token Model """
class UserToken(AuditTimestamp):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expire_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "user_tokens"
    
