from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse # url resolver
from django.utils.text import slugify
from PIL import Image
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISHED)
       # return Post.Status.PUBLISHED

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length = 250)
    # unique for the date stored in the publish field 
    slug = models.SlugField(max_length = 250, unique_for_date= 'publish', ) 
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    image =models.ImageField(null=True,blank=True,upload_to='images/')
   
    status = models.CharField(max_length=2,choices=Status.choices,default = Status.DRAFT)
    #tags = TaggableManager()# allows to add,retrieve and remove tags
    
    # overiding save method

    def save(self, *args, **kwargs):
        if  not self.slug:
            self.slug = slugify(self.title)
            super(Post, self).save(*args, **kwargs)
   
    def resizer(self):  
        if self.image:
            img = Image.open(self.image)
            # img.save(self.image.path)
            size = (800, 600)
            thumb_size = (100,100)
            img.resize(size)
            thumb = img.thumbnail(thumb_size)
            #thumbnail_path = self.image.path.replace('images/','thumbnails/')
            img.save(self.image.path)
            thumb.save(self.image.path)
            #self.thumbnail.name = thumbnail_path.split('media/')[-1]
            #self.save(update_fields = ['thumbnail'])


    published = PublishedManager()
    objects = models.Manager()
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),]
    
    
    def __str__(self):
        return self.title
    
    
    # reverse func builds the URL dynamically using the URL name defined in the URL patterns
    def get_absolute_url(self):
        return reverse('blog:post_detail', args = [self.publish.year,
                                                   self.publish.month,
                                                   self.publish.day,
                                                   self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE,
                              related_name= 'comments') # associating a comment with a single post
    name = models.CharField(max_length = 80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add =True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default = True) # allows us to manually deactivate inappropriate comments using the admin site

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields = ['created']),]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


