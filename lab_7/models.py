from django.db import models

class Friend(models.Model):
    friend_name = models.CharField(max_length=400)
    npm = models.CharField(max_length=250)
    address = models.CharField(max_length=400, default=" ")
    mail_code = models.CharField(max_length=100, default=" ")
    hometown = models.CharField(max_length=250, default=" ")
    birthday = models.CharField(max_length=250, default=" ")
    program = models.CharField(max_length=250, default=" ")
    angkatan = models.CharField(max_length=250, default=" ")
    added_at = models.DateField(auto_now_add=True)
