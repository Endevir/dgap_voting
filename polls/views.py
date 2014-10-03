from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from polls.models import Choice, Poll, UserHash, UserProfile, LegacyUser, LegacyDorm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
import re
from random import randint
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from polls.forms import UserForm, UserProfileForm

maxInt = 2147483647

def check_user(request): 
    candidat = LegacyUser.objects.filter(name__icontains='{} {}'.format(request.POST['last_name'], request.POST['first_name'])).filter(cardnumber__regex=r'^.{14}' + request.POST['cardnumber']) 
    if not candidat.exists():
        return False
    dorm = LegacyDorm.objects.filter(last_name=request.POST['last_name']).filter(first_name=request.POST['first_name']).filter(room=request.POST['room'])
    if not dorm.exists():
        return False
    return True

def check_dorm(id):
    return UserProfile.objects.filter(dorm=id).exists()

def profile_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            if check_user(request):
#TODO тут уже надо нормально разобраться с кучей карточек и людьми с одинаковыми именами и фамилиями одновременно
# долгое и мучительное обдумывание привело к выводу: candidat, у которых одинаковые firts_name, last_name, cardnumber, считаются одинаковыми по определению
# по сути, проверяем, есть ли вообще подходящие карточки. Если нет, то уже выпилили. Если есть, то неважно, сколько их. Вероятность того, что в базе будет два человека с одинаковыми ФИ и днём рождения, считается малой

                dorm = LegacyDorm.objects.filter(last_name=request.POST['last_name']).filter(first_name=request.POST['first_name']).filter(room=request.POST['room'])

# что делать, если в базе несколько человек с одинаовыми ФИ?
# считаем, что их не поселят в одну комнату, иначе ручная обработка 

                if len(dorm) > 1:
                    messages.error(request, "К сожалению, мы не ФСБ, поэтому не можем однозначно определить вашу личность")
                elif check_dorm(dorm[0].id):
                    messages.error(request, "Пользователь с такими данными уже зарегистрирован")
                else:
                    dorm = dorm[0]
                    user_form.save()
                    profile_form.save()
                    request.user.userprofile.dorm = dorm.id
                    request.user.userprofile.middlename = dorm.middle_name
                    #request.user.userprofile.room = dorm.room
                    request.user.userprofile.group = dorm.group
                    request.user.userprofile.approval = True 
                    request.user.userprofile.save()
                    messages.success(request, "Регистрация пройдена. Теперь вы можете участвовать в голосовании")
                    return redirect('polls:done')
            else:
                messages.error(request, "Пользователя с данными именем, фамилией и номером карты в базе не обнаружено")
    else:
        user_form = UserForm(instance = request.user)
        profile_form = UserProfileForm(instance = request.user.userprofile)

    return render(request, 'polls/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

class Index(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.filter(begin_date__lte=timezone.now()).order_by('-begin_date')[:25]

class Detail(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        return Poll.objects.filter(begin_date__lte=timezone.now(), end_date__gte=timezone.now())

class Results(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Poll.objects.filter(end_date__lte=timezone.now())

def done(request):
    storage = messages.get_messages(request)
    if storage:
        return render(request, 'polls/done.html')
    else:
        return redirect('polls:index')

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    user = request.user
    if not user.is_authenticated():
        messages.error(request, 'Вы не вошли как зарегистрированный пользователь')
        return redirect('polls:detail', pk=poll_id)
    if not user.userprofile.approval:
        messages.error(request, 'Вы не являетесь подтверждённым пользователем')
        return redirect('polls:detail', pk=poll_id)
    if user.get_username() != 'admin' and p.voted_users.filter(pk=user.pk).exists():
        messages.error(request, 'Вы уже приняли участие в этом голосовании')
        return redirect('polls:detail', pk=poll_id)
    if not ((re.compile(p.target_room, re.IGNORECASE)).match(user.userprofile.room) and
            (re.compile(p.target_group, re.IGNORECASE)).match(user.userprofile.group)):
        messages.error(request, 'Вы не являетесь целевой аудиторией голосования')
        return redirect('polls:detail', pk=poll_id)
    choices = request.POST.getlist('choice', False)
    if not choices:
        messages.error(request, 'Вы не выбрали вариант ответа')
        return redirect('polls:detail', pk=poll_id)
    p.voted_users.add(user)
    userHashes = [1] * len(choices)
    message = 'Ваш голос учтён. Идентификационные ключи, соответствующие вашему выбору:\n'
    if p.answer_type == 'OWN':
        c = p.choice_set.create(choice_text=choices[0], votes = 0)
        choices[0] = c.pk
    for i in range(len(choices)):
        selected_choice = p.choice_set.get(pk=choices[i])
        selected_choice.votes += 1
        selected_choice.save()
        userHashes[i] = UserHash()
        userHashes[i].value = randint(0, maxInt)
        userHashes[i].choice = selected_choice
        message += str(userHashes[i].value) + '\n'
        if p.public:
            userHashes[i].user = user
        userHashes[i].save()
    messages.success(request, message)
    return redirect('polls:done')
   
