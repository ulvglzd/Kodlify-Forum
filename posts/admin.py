from django.contrib import admin
from .models import Post, Answer, Up

# Register your models here.

admin.site.register(Post)
admin.site.register(Answer)
admin.site.register(Up)