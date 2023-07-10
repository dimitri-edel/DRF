from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Likes(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["owner", "post"]

    def __str__(self) -> str:
        return f"{self.owner} {self.post}"