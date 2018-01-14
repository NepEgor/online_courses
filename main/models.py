from django.db import models
from django.urls import reverse
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=512, null=True)
    picture = models.ImageField(upload_to='pictures', default='pictures/nopic.png', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('course', args=[str(self.id)])


class Subscription(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed = models.DateTimeField(auto_now_add=True)
