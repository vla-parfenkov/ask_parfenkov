from django.core.management.base import BaseCommand
from ask.models import Question, Tag, Profile, Answer, User
from django.contrib.auth import authenticate, login, logout

class Command(BaseCommand):
  args = '<test base ...>'
  help = 'our help string comes here'

  def fill_db(self):
    for i in range(0, 30):
      usr = User(username='user' + str(i), password='password' + str(i), first_name='User')
      usr.save()
      prof = Profile(avatar='avatar.jpeg', user = usr)
      prof.save()
      try:
        tbag = Tag.objects.get(name='Bucket' + str(i % 20))
        tbag.popularity += 1
      except Exception:
        tbag = Tag(name = 'Bucket' + str(i % 20), popularity = 1)
      tbag.save()

      quest = Question(title = str(i) + 'bucket', text = 'see my bucket, I have a' + str(10000 - i) + ' bucket remains', author = prof, votes = i)
      quest.save()
      quest.liked.add(prof)
      quest.tag.add(tbag)

      for j in range(0, 20):
        ans = Answer(text='Test answer' + str(i), author=prof, question=quest)
        ans.votes = int(((i + j) * 6) % 40)
        ans.save()
        ans.voted.add(prof)


  def handle(self, *args, **options):
    self.fill_db()