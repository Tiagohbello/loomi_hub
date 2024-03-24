import io
import uuid

from PIL import Image
from django.core.exceptions import ValidationError
from django.db import models
from django.core.files.base import ContentFile

from loomi_hub.post.utils.image_resize import resize_image
from loomi_hub.user.models import User


def upload_to(instance, filename):
    return "images/{filename}".format(filename=filename)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=upload_to, null=True, blank=True)

    content = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.image and not self.content:
            raise ValidationError("You must include an image or a content")

    def save(self, *args, **kwargs):

        if self.image:

            resized_image = resize_image(self.image, (1080, 1080), 100)
            self.image.save(
                self.image.name, ContentFile(resized_image.read()), save=False
            )
            resized_image.close()

            thumbnail = resize_image(self.image, (128, 128), quality=100)
            self.thumbnail.save(
                "thumb_" + self.image.name, ContentFile(thumbnail.read()), save=False
            )
            thumbnail.close()
        return super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "post")
