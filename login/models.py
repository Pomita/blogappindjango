from django.db import models

class blogpage(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

class comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=30)
    body = models.TextField()
    blog = models.ForeignKey(blogpage)

    def __unicode__(self):
        return self.title
