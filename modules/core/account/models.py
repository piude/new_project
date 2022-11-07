import uuid
import pytz
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


# Create your models here.
class AppUserManager(BaseUserManager):
	def _create_user(self, email, first_name, last_name, password, **extra_fields):
		if not email:
			raise ValueError('User must have an email address.')
		email = self.normalize_email(email)
		first_name = self.normalize_firstname(first_name)
		last_name = self.normalize_lastname(last_name)
		user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
		user.set_password(password)
		user.save(self._db)
		return user

	def create_user(self,email=None, first_name=None, last_name=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff',False)
		extra_fields.setdefault('is_superuser',False)
		return _create_user(email,first_name,last_name,password,**extra_fields)

	def create_superuser(self, email, first_name, last_name, password, **extra_fields):
		extra_fields.setdefault('is_staff',True)
		extra_fields.setdefault('is_superuser',True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

	@classmethod
	def normalize_firstname(cls,first_name):
		return unicodedata.normalize('NFKC',force_text(first_name))

	@classmethod
	def normalize_lastname(cls,last_name):
		return unicodedata.normalize('NFKC',force_text(last_name))

class User(AbstractBaseUser):
	first_name = models.CharField(max_length=500, blank=True)
	last_name = models.CharField(max_length=500, blank=True)
	email = models.EmailField(blank=True, unique=True)
	username = models.UUIDField(default=uuid.uuid4, editable=False)
	date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name','last_name']
	objects = AppUserManager()

	class Meta:
		verbose_name =_('user')
		verbose_name_plural =_('users')

	def __str__(self):
		full_name = '%S %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

def user_avatar_dir(instance, filename):
	return 'uploads/user_{0}/avatar/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
	MALE ='M'
	FEMALE ='F'
	OTHERS ='Others'
	Gender_choice = (
		(MALE,'male'),
		(FEMALE,'female'),
		)
	TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to=user_avatar_dir)
	bio = models.TextField(max_length=1000, blank=True)
	location = models.CharField(max_length=1000, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
	gender = models.CharField(max_length=61, choices=Gender_choice, blank=True)
	email_verified = models.BooleanField(default=False)
	facebook_url = models.URLField(blank=True)
	twitter_url = models.URLField(blank=True)
	google_url = models.URLField(blank=True)
	linkedin_url = models.URLField(blank=True)













