from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings



# sender: the model who will send this function
# instance: the instance of the model/object who treggered this function
# created: (true, false value) to let us know if this (user-model)/profile/user is already exist in DB (if true), or if newly created profile/user (if it false)
# @reciver(post_save,sender=Profile)
def profileCreated(sender, instance, created, **kwarg):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )

        subject = 'Welcome to DevSearch'
        message = 'We glad you are here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender,instance,**kwarg):
    user = instance.user
    user.delete()


post_save.connect(profileCreated,sender=User)
post_save.connect(updateUser,sender=Profile)
post_delete.connect(deleteUser,sender=Profile)