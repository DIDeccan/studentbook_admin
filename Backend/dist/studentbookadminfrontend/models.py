from datetime import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Class(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "studentbookfrontend_class"
 
 
 
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone_number:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone_number=self.normalize_email(phone_number),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone_number,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USER_TYPE_CHOICES = [  
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin')
    ]

    email = models.EmailField(
       
        max_length=255,
        null=True,
        blank=True
        
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to="profile",blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=50,unique=True, verbose_name="phone number",)
    address=models.CharField(max_length=300,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=200,null=True,blank=True)
    zip_code = models.CharField(max_length=50,null=True,blank=True)
    otp = models.CharField(max_length=50,null=True,blank=True)
    user_type = models.CharField(max_length=20, null=True,choices=USER_TYPE_CHOICES)
    login_time = models.DateTimeField(null=True)
    otp_verified = models.BooleanField(default=False)
    registered_date = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
    def update_login_time(self):
        self.login_time = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if self.is_superuser and not self.user_type:
            self.user_type = 'admin'
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    class Meta:
        db_table = 'studentbookfrontend_user'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


class Student(User):
    school = models.CharField(max_length=255, null=True, blank=True)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="main_students")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number
    class Meta:
        managed = False
        db_table = 'studentbookfrontend_student'
    
