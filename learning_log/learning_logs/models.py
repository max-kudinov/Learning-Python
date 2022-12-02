from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """A topic the user is learning about"""

    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    topic_visibility_options = [(False, "Private"), (True, "Public")]
    public = models.BooleanField(
        max_length=10, choices=topic_visibility_options, default=False
    )

    def __str__(self):
        """Return a string representation of the model"""
        return self.text


class Entry(models.Model):
    """Some text in the topic"""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        """Return a string representation of the model"""
        if len(self.text) > 50:
            str = f"{self.text[:50]}..."
        else:
            str = self.text
        return str
