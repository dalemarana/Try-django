from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone

from .utils import slugify_instance_title

# Create your models here.
class Article(models.Model):
    # https://docs.djangoproject.com/en/5.0/topics/db/models/
    # Django model-field-types
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # obj = Article.objects.get(id=1)
        # set something
        # if self.slug is None:
        #     self.slug = slugify(self.title)


        # if self.slug is None:
        #     slugify_instance_title(self)
        super().save(*args, **kwargs)
        # obj.save()
        # do another something

# function for slugifying slug imported in utils


# Happens before save
def article_pre_save(sender, instance, *args, **kwargs):
    # print('pre_save')
    if instance.slug is None:
        slugify_instance_title(instance)

pre_save.connect(article_pre_save, sender=Article)

# Happens after save. need to save
def article_post_save(sender, instance, created, *args, **kwargs):
    # print('post_save')
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)