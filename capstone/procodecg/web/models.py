from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    verification = models.BooleanField(default=False)
    pass


class Event (models.Model): 
    event_name = models.CharField(max_length= 200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    time_start = models.CharField(max_length= 5, default = "00:00")
    time_end = models.CharField(max_length= 5, default = "00:00")
    weekly = models.BooleanField(default=False)
    students = models.ManyToManyField("User", related_name="schedule", blank=True)
    def serialize(self):
        return {
            "id": self.id,
            "event_name": self.event_name,
            "start_date_week_day": self.start_date.strftime('%-w'),
            "start_date_day": self.start_date.strftime('%-d'),
            "start_date_month": self.start_date.strftime('%-m'),
            "start_date_year": self.start_date.strftime('%Y'),
            "end_date_day": self.end_date.strftime('%-d'),
            "end_date_month": self.end_date.strftime('%-m'),
            "end_date_year": self.end_date.strftime('%Y'),
            "start_time": self.time_start,
            "end_time": self.time_end,
            "description": self.description,
            "weekly": self.weekly,
            "students": [user.username for user in self.students.all()] 
        }
    def __str__(self):
        return f'{self.event_name} ({self.start_date} - {self.end_date})'


class CreateComment(models.Manager):
    def create_card(self, task_name, description, attachment_1, attachment_2, students, status):
        creating = self.create(task_name=task_name, description=description, attachment_1=attachment_1, 
                               attachment_2=attachment_2, students=students, status=status)
        return creating


class ProgressCard (models.Model):
    status_list = [
        ('To Do', 'todo'),
        ('On Going', 'ongoing'),
        ('Completed', 'completed')
    ]
    task_name = models.CharField(max_length=200)
    description = models.TextField()
    attachment_1 = models.FileField(null = True, blank=True, upload_to='web/files/')
    attachment_2 = models.FileField(null = True, blank=True, upload_to='web/files/')
    students = models.ManyToManyField("User", related_name="card", blank=True)
    status = models.CharField(choices=status_list, blank=True, max_length=20)
    def serialize(self):
        return {
            "id": self.id,
            "task_name": self.task_name,
            "students": [user.username for user in self.students.all()],
            "description": self.description,
             "attachment_1": self.attachment_1.url if self.attachment_1 else None,
             "attachment_2": self.attachment_2.url if self.attachment_2 else None,
            "status": self.status,
        }