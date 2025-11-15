from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    QUESTION_TYPES = (
        ('NUM', 'Numeric'),
        ('BOOL', 'Boolean'),
        ('TEXT', 'Text'),
    )
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)

    def __str__(self):
        return self.text

class CheckupSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkup #{self.id} - {self.user.username}"

class Response(models.Model):
    submission = models.ForeignKey(CheckupSubmission, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return f"{self.submission} - {self.question.text}"
