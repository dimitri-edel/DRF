from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    # List of available image filters
    image_filter_choices = [
        ('_1977', '1977'), ('brannan', 'Brannan'),
        ('earlybird', 'Earlybird'), ('hudson', 'Hudson'),
        ('inkwell', 'Inkwell'), ('lofi', 'Lo-Fi'),
        ('kelvin', 'Kelvin'), ('normal', 'Normal'),
        ('nashville', 'Nashville'), ('rise', 'Rise'),
        ('toaster', 'Toaster'), ('valencia', 'Valencia'),
        ('walden', 'Walden'), ('xpro2', 'X-pro II')
    ]
  
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='iamges/',
        default='../cld-sample-5'
    )
    # Selection field for an image filter
    image_filter = models.CharField(max_length=32, choices=image_filter_choices, default='normal')

    class Meta:
        ordering = ['-created_at']

        def __str__(self) -> str:
            return f"{self.id} {self.title}"
