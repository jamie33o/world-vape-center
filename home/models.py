from django.db import models

class HeroSection(models.Model):
    
    title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='hero_section', blank=True , null=True)
    link = models.URLField(default='#')
    link_text = models.CharField(max_length=50, default='Shop Now')
    
    def __str__(self):
        return self.title if self.title else 'Hero Section'
