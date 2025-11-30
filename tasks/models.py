from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    estimated_hours = models.IntegerField()
    importance = models.IntegerField(help_text="Scale of 1-10")
    # Storing dependencies as JSON text for SQLite simplicity
    dependencies = models.JSONField(default=list, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title