from django.contrib import admin
from .models import Question, Profile, Answer, Tag

admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Answer)
# Register your models here.
