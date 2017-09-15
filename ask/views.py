from django.template.context_processors import csrf
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import loader
from ask.models import Question, Tag, Profile, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from ask.forms import LoginForm, SignupForm, SettingsForm, QuestionForm, AnswerForm
#from django.core.urlresolvers import resolve


def test (request):
    return render_to_response ('test.html', [])

def index(request):
    profile = Profile.objects.get_profile(request.user)
    recent = Question.objects.recent_questions()
    tbags = Tag.objects.all()
    page, paginator = paginate(recent, request)
    context = {
        'recent': page,
        'paginator': paginator,
        'tags': tbags,
        'profile': profile,
        'user': request.user,
    }
    return render_to_response ('index.html', context)

def ask(request):
    profile = Profile.objects.get_profile(request.user)
    tbags = Tag.objects.all()
    error_message = ''
    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            Question.objects.create_question(profile, form.cleaned_data['titleField'],
            form.cleaned_data['questionTextField'],
            form.cleaned_data['tagsField'].split())
            return redirect('/ask/')
        else:
            error_message = form.errors

    context = {
        'profile': profile,
        'tags': tbags,
        'error_message': error_message,
        'form': form,
        'user': request.user,
    }
    context.update(csrf(request))
    return render_to_response ('ask.html', context)

def login_me(request):
    tbags = Tag.objects.all()
    error_message = ''
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['usernameField']
            password = request.POST['passwordField']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ask')
            else:
                error_message = 'User is not found'
        else:
            error_message = 'Form\'s not valid'

    context = {
        'tags': tbags,
        'error_message': error_message,
        'form': form,
        'user': request.user,
    }
    context.update(csrf(request))
    return render_to_response('login.html', context)

def logout_me(request):
  logout(request)
  return redirect('/ask/')

def signup(request):
  profile = Profile.objects.get_profile(request.user)
  tbags = Tag.objects.all()
  error_message = ''
  form = SignupForm()
  if request.method == 'POST':
    form = SignupForm(request.POST, request.FILES)
    if form.is_valid():
      if (request.POST['repeat'] == request.POST['passwordField']):
        Profile.objects.create_profile(form.cleaned_data['usernameField'], form.cleaned_data['firstNameField'],
        form.cleaned_data['emailField'], form.cleaned_data['passwordField'], form.cleaned_data['imageField'])
        return redirect('/ask/')
      else:
        error_message = 'Password is not correct'
    else:
      error_message = form.errors  # 'Form\'s not valid'

  context = {
    'tags': tbags,
    'error_message': error_message,
    'form': form,
    'profile': profile,
    'user': request.user,
  }
  context.update(csrf(request))
  return render_to_response('signup.html', context)

def question(request, questionId):#page with answers
  profile = Profile.objects.get_profile(request.user)
  question = get_object_or_404(Question, pk=questionId)
  tbags = Tag.objects.all()
  answers = Answer.objects.get_answers_to_question(questionId)
  page, paginator = paginate(answers, request)
  form = AnswerForm()
  error_message = ''

  if request.method == 'POST':
    form = AnswerForm(request.POST)
    if form.is_valid():
      Answer.objects.create_answer(profile, form.cleaned_data['answerTextField'], question)
      return redirect('/ask/question/' + str(questionId))
    else:
      error_message = form.errors  # 'Form\'s not valid'

  context = {
    'question': question,
    'answers': page,
    'paginator': paginator,
    'tags': tbags,
    'form': form,
    'error_message': error_message,
    'profile': profile,
    'user': request.user,
  }
  context.update(csrf(request))
  return render_to_response('question.html', context)

def hot(request):
  profile = Profile.objects.get_profile(request.user)
  hot = Question.objects.best_questions()
  page, paginator = paginate(hot, request)
  tbags = Tag.objects.all()

  context = {
    'recent': page,
    'paginator': paginator,
    'tags': tbags,
    'profile': profile,
    'user': request.user,
  }
  return render_to_response('index.html',context)

def tag(request, tagValue):
  profile = Profile.objects.get_profile(request.user)
  tbg = Tag.objects.filter(name=tagValue)
  recent = Question.objects.filter(tag=tbg)
  tbags = Tag.objects.all()
  page, paginator = paginate(recent, request)
  context = {
    'recent': page,
    'paginator': paginator,
    'tags': tbags,
    'profile': profile,
    'user': request.user,
  }
  return render_to_response('index.html', context)



def paginate(objects_list, request):
  paginator = Paginator(objects_list, 10)
  try:
    page = request.GET.get('page')
    objPage = paginator.page(page)
  except PageNotAnInteger:
    objPage = paginator.page(1)
  except EmptyPage:
    objPage = paginator.page(paginator.num_pages)
  return objPage, paginator

