from statistics import mode
from types import CoroutineType
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import pre_save 
from django.dispatch import receiver
from django.core.mail import send_mail

# Create Token When Is Created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user = instance
        )

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

        



# Create your models here.
class AddCity2 (models.Model):
    user= models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='AddCityField2')
    city = models.CharField(max_length=20,blank=True, null=True)
    temperatuer = models.DecimalField(max_digits=12,decimal_places=2,blank=True, null=True)
    description = models.CharField(max_length=200,blank=True, null=True)
    alertAbove = models.IntegerField(blank=True, null=True)
    alertBelow = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.city        


# Send Alert When Alert Field Is Updated
@receiver(post_save,sender=AddCity2)   
def update_cities(sender,instance,  **kwargs):
        old_city = sender.objects.get(pk=instance.pk)
        print(old_city.alertAbove)
        
        if not old_city.alertAbove == instance.alertAbove  or not old_city.alertBelow == instance.alertBelow: 
            user_ = instance.user.user.email
            print(instance.user.user.email)
            print(f'Alert Email Sent!!!!!')
            print(f'to: {instance.user.user.email}')
            print(f'{instance.city} new temperatuer:{instance.temperatuer}')
           
            # Need To Set Up Email Settings in The settings.py
            # send_mail(
            # 'Subject here',
            # 'Here is the message.',
            # 'from@example.com',
            # ['to@example.com'],
            # fail_silently=False,)

