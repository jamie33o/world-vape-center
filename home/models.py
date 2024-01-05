from django.db import models

class HomePage(models.Model):
    title = models.CharField(max_length=100)
    jumbotron_text = models.TextField()
    jumbotron_image = models.ImageField(upload_to='jumbotron_images/')

    def __str__(self):
        return self.title
