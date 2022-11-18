from django.db import models

# Create your models here.
class Blogpost(models.Model):
    post_id        = models.AutoField(primary_key=True)
    title          = models.CharField(max_length=255, null=True)
    published_date = models.DateField()
    heading        = models.CharField(max_length=255, null = True)
    cheading       = models.TextField(null=True)
    heading1       = models.CharField(max_length=255, null = True)
    cheading1      = models.TextField(null=True)
    heading2       = models.CharField(max_length=255, null = True)
    cheading2      = models.TextField(null=True)
    blog_img       = models.ImageField(upload_to="blog/images", default="")

    def __str__(self):
        return self.title
    
