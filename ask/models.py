from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import datetime


class TagManager(models.Manager):
  def get_tag(self, tag_name):
    try:
      result = Tag.objects.get(name=tag_name)
      result.popularity += 1
    except Exception:
      result = Tag(name=tag_name, popularity=1)
    return result


class QuestionManager(models.Manager):
  def recent_questions(self):
    try:
      result = self.order_by('added_at').reverse()
    except Exception:
      pass
    return result

  def best_questions(self):
    try:
      result = self.order_by('votes').reverse()
    except Exception:
      pass
    return result

  def create_question(self, profile, _title, _text, tags):
    quest = Question(title = _title, text=_text, author=profile, votes=0)
    quest.save()
    for tag in tags:
      tbag = Tag.objects.get_tag(tag)
      tbag.save()
      quest.tag.add(tbag)


class AnswerManager(models.Manager):
  def get_answers_to_question(self, question_id):
    try:
      result = self.filter(question = question_id).order_by('added_at').reverse()
    except Exception:
      result = None #fixsed
    return result

  def create_answer(self, profile, _text, quest):
    ans = Answer(text=_text, author=profile, question=quest)
    ans.votes = 0
    ans.save()

class ProfileManager(models.Manager):
  def get_profile(self, usr):
    try:
      result = self.get(user = usr)
    except Exception:
      result = None
    return result

  def create_profile(self, usrname, f_name, _email, psword, image):
    usr = User.objects.create_user(username = usrname, first_name = f_name, email = _email, password=psword)
    usr.save()
    prof = Profile()
    prof.avatar = image
    prof.user = usr
    prof.save()

  def change_profile(self, usr, image):
    prof = Profile.objects.get(user = usr)
    prof.avatar = image
    usr.save()
    prof.save()


class Profile(models.Model):
  user = models.OneToOneField(User)
  avatar = models.ImageField()
  objects = ProfileManager()


class Tag(models.Model):
    name = models.CharField(max_length=60)
    popularity = models.IntegerField(default = 0)
    objects = TagManager()



class Question(models.Model):
  title = models.CharField(max_length = 200)
  text = models.TextField()
  added_at = models.DateTimeField(default = datetime.datetime.now)
  author = models.ForeignKey(Profile)
  votes = models.IntegerField()
  tag = models.ManyToManyField(Tag)
  liked = models.ManyToManyField(Profile, related_name='liked')
  objects = QuestionManager()



class Answer(models.Model):
  text = models.TextField()
  author = models.ForeignKey(Profile)
  added_at = models.DateTimeField(default = datetime.datetime.now)
  question = models.ForeignKey(Question)
  votes = models.IntegerField()
  voted = models.ManyToManyField(Profile, related_name='voted')
  objects = AnswerManager()
