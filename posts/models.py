from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import Account
# Create your models here.

class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    uped = models.ManyToManyField(Account, blank=True, related_name='ups')
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    def num_ups(self):
        return self.uped.all().count()


    def num_answers(self):
        return self.answer_set.all().count()

    class Meta:
        ordering = ('-created',)
    
class Answer(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.pk)
    
UP_CHOICES = (
    ('Up', 'Up'),
    ('Unup', 'Unup'),
)

class Up(models.Model):
    user =models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=UP_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"










