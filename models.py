from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    book_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="General")
    status = models.CharField(max_length=20, default="Available")
    borrow_count = models.IntegerField(default=0)

    issued_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    student_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    student_id = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    issue_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
    
class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"