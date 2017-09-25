from django.db import models
from django.utils import timezone
import pytz

class Message(models.Model):
	def converTime():
		return timezone.now() + timezone.timedelta(hours=7)

	name = models.CharField(max_length=27)
	email = models.EmailField()
	message = models.TextField()
	created_date = models.DateTimeField(default=converTime)

	def __str__(self):
	    return self.message



