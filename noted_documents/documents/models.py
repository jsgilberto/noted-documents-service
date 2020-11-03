from django.db import models
from django.utils.text import slugify
import uuid


class TimeStampMixin(models.Model):
    """ Base 'Abstract' model with fields for recording creation and updating times
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Document(TimeStampMixin):
    """ Document model used to represent documents in database
    """
    user_id = models.UUIDField(null=False, blank=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True, max_length=255, blank=True)


    def save(self, *args, **kwargs):
        """ Save method called before instance is saved in db
        """
        if not self.slug:
            title_slugified = slugify(self.title)
            unique_id = uuid.uuid4()
            # Create a slug using uuid4
            self.slug = "{title_slugified}-{unique_id}"
        return super().save(*args, **kwargs)
    
