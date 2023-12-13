from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
import datetime
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Максимальный размер файла %sMB" % str(megabyte_limit))


class CustomAccountManager(BaseUserManager):
    def create_user(self, username, fullname, email, password):
        user = self.model(email=email, username=username, fullname=fullname, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, fullname, email, password):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not fullname:
            raise ValueError("User must have a full name")
        user = self.model(email=email, username=username, fullname=fullname, password=password)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username_):
        return self.get(username=username_)


class AdvUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=200, unique=True, verbose_name='Логин')
    fullname = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=200)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'password', 'email',]

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.username

    def natural_key(self):
        return self.username

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Введите категорию заявки', verbose_name='Название')

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=200, help_text='Введите название заявки', verbose_name='Название')
    summary = models.CharField(max_length=1000, help_text='Введите описание заявки', verbose_name='Описание')
    category = models.ForeignKey('Category', help_text='Выберите категория для заявки', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    timestamp = models.DateTimeField(default=timezone.now())
    image = models.ImageField(upload_to='images/', validators=[validate_image], help_text='Максимальный размер '
                                                                                          'изображения 2MB', verbose_name='Дизайн(фото)')

    application_status = (
        ('Новая', 'Новая',),
        ('Принято в работу', 'Принято в работу',),
        ('Выполнено', 'Выполнено',)
    )

    status = models.CharField(max_length=50, choices=application_status, blank=True, default='Новая', verbose_name='Статус')
    client = models.ForeignKey(AdvUser, on_delete=models.SET_NULL, null=True, blank=True, to_field='id')
    comment = models.TextField(max_length=500, blank=True)
    design = models.ImageField(upload_to='images/',
                               help_text="Максимальный размер изображения 2MB",
                               blank=True,
                               null=True,
                               validators=[validate_image])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profile')
