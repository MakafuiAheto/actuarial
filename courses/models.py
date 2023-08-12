from __future__ import unicode_literals

import uuid

from django.contrib.gis.db import models
from django.db import transaction
from .utility import (AreaOfSpecialization, Gender, Permissions,
                      AuthorPermissionExceptions, StudentPermissionExceptions)
from django.core import validators
from .Exceptions.Exceptions import IncorrectEmailError, SaveUserError

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

GENDER = ((gender.title, gender.gender) for gender in Gender)
INDUSTRY = ((area.title, area.industry) for area in AreaOfSpecialization)

# Author permissions and exceptions
AUTHOR_EXCEPTIONS = [exception.value for exception in AuthorPermissionExceptions]
AUTHOR_PERMISSIONS = [(permission.key, permission.result) for permission in Permissions
                      if (permission.key, permission.result) not in AUTHOR_EXCEPTIONS]

# Student permissions and exceptions
STUDENT_EXCEPTIONS = [exception.value for exception in StudentPermissionExceptions]
STUDENT_PERMISSIONS = [(permission.key, permission.result) for permission in Permissions
                       if (permission.key, permission.result) not in STUDENT_EXCEPTIONS]


# Create your models here..3
class CommonFields(models.Model):
    created_On = models.DateTimeField(auto_now_add=True)
    modified_On = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise IncorrectEmailError('The given email must be set')

        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except Exception as e:
            raise SaveUserError(str(e))

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, CommonFields):
    email = models.EmailField(max_length=254, blank=True,
                              validators=[validators.EmailValidator(message="Invalid Email")], unique=True)
    first_Name = models.CharField(max_length=254, verbose_name="First Name")
    last_Name = models.CharField(max_length=254, verbose_name="last Name")
    user_Name = models.CharField(max_length=254, verbose_name="User Name")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_Name', 'last_Name']

    objects = UserManager()


class Author(User):
    author_ID = models.UUIDField(primary_key=True, default=uuid.uuid4(), auto_created=True, editable=False)
    image = models.ImageField(upload_to="Users/makafuiaheto/Desktop/Felicia/author_images", default="img.png")
    gender = models.CharField(default='', choices=GENDER)
    author_Bio = models.TextField(default='')

    class Meta:
        verbose_name = "Authors"

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)
        self.age = ''

    def save(self, *args, **kwargs):
        super(Author, self).save(*args, **kwargs)
        return self


class Student(User):
    student_ID = models.UUIDField(primary_key=True, default=uuid.uuid4(), auto_created=True, editable=False)
    image = models.ImageField(upload_to="upload/images", default="img.png")
    gender = models.CharField(default='', choices=GENDER)
    next_Subscription_Payment_Date = models.DateTimeField()

    class Meta:
        verbose_name = 'Students'


class Course(CommonFields):
    course_ID = models.UUIDField(primary_key=True, default=uuid.uuid4(), auto_created=True, editable=False)
    course_Name = models.CharField(default='', max_length=200, null=False)
    description = models.TextField(max_length=5000, editable=True)
    specialist_area = models.TextField(default='', choices=INDUSTRY)
    upload_Location = models.PointField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_rel')

    class Meta:
        verbose_name = "Courses"
        ordering = ["created_On"]


class Video(CommonFields):
    video_ID = models.UUIDField(primary_key=True, default=uuid.uuid4(), auto_created=True, editable=False)
    title = models.CharField(max_length=254)

    video_URL = models.URLField()
    video_Description = models.TextField(max_length=500)
    video_ThumbNail = models.ImageField(upload_to="Users/makafuiaheto/Desktop/Felicia/thumbNail_images",
                                        default="img.ing")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_rel")

    class Meta:
        verbose_name = "Videos"


class Comments(CommonFields):
    comment_ID = models.UUIDField(primary_key=True, default=uuid.uuid4(), auto_created=True, editable=False)
    comment = models.TextField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_rel')

    class Meta:
        verbose_name = "Comments"
