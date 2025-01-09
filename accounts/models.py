from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    mpassword = models.CharField(verbose_name='密码', blank=True, null=True, default='0', max_length=100)
    mobile = models.CharField(verbose_name='手机', blank=True, null=True, default='', max_length=100)
    email = models.CharField(verbose_name='邮箱', blank=True, null=True, default='', max_length=100)
    header_image = models.ImageField(upload_to = 'img',verbose_name='头像', blank=True, null=True, default='default.jpg')
    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
