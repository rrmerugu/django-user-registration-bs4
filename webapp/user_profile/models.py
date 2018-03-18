from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import BytesIO
import logging
from django.core.files.base import ContentFile
from placeholder_pics.placeholder import PlaceholderPic
from django_thumbs.fields import ImageThumbsField

import os
from django.utils import timezone

logger = logging.getLogger(__name__)


# Create your models here.
def upload_avatar_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'userprofile/%s%s' % (
        timezone.now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),
    )


class UserProfile(models.Model):
    SIZES = (
        {'code': '60x60', 'wxh': '60x60', 'resize': 'crop'},  #
        {'code': '100x100', 'wxh': '100x100', 'resize': 'crop'},
        {'code': '200x200', 'wxh': '200x200', 'resize': 'crop'},  # 'resize' defaults to 'scale'
        {'code': '400x400', 'wxh': '400x400', 'resize': 'crop'},  # 'resize' defaults to 'scale'
    )

    THUMBNAIL_ALIASES = {
        '': {
            'avatar': {'size': (50, 50), 'crop': True},
        },
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    image = ImageThumbsField(default=None, verbose_name="profile image",
                             sizes=SIZES,
                             upload_to=upload_avatar_to, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True, default=None, verbose_name="Write about your self")
    location = models.CharField(max_length=30, blank=True, null=True, default=None)
    birth_date = models.DateField(null=True, blank=True)

    def generate_img(self):
        f = BytesIO()
        logger.debug("generating image")
        if self.user.first_name:
            img_name = self.user.first_name[:2].capitalize()
        else:
            img_name = self.user.email[:2].capitalize()
        placeholder = PlaceholderPic(img_name)
        placeholder.image.save(f, format='png')
        s = f.getvalue()

        self.image.save("%s.png" % self.user.id,
                        ContentFile(s))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        if not profile.image:
            profile.generate_img()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()
