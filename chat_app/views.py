from typing import Any
from .forms import CustomUserCreationForm, EmailChangeForm, UsernameChangeForm, ImgChangeForm
from chat_app.models import CustomUser, Message
from django.db.models.query import QuerySet, Q 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse

def index(request):
    return render(request, 'chat_app/index.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'chat_app/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'chat_app/login.html'

class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'chat_app/friends.html'
    context_object_name = "users"
    
    def get_queryset(self):
        user_id = self.request.user.id
        
        sent_to = Message.objects.filter(sender=user_id).values_list('recipient', flat=True)
        received_from = Message.objects.filter(recipient=user_id).values_list('sender', flat=True)

        talked_users_ids = list(sent_to) + list(received_from)
        return CustomUser.objects.exclude(id=user_id).order_by('-pub_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        for user in context['users']:
            print(user.id)
            last_message = Message.objects.filter(
                Q(sender_id=user.id)|Q(recipient_id=user.id)
            ).order_by('-timestamp').first()

            print(last_message)
            user.last_message = last_message.content if last_message else "まだトークしていません"
            user.last_message_time = last_message.timestamp if last_message else None

            if not user.img:
                user.img_url = 'path/to/default/icon.png'
            else:
                user.img_url = user.img.url
        

        return context
    
class ChatView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chat_app/talkroom.html'
    context_object_name = 'messages'

    def get_queryset(self):
        recipient_id = self.kwargs['recipient_id']
        return Message.objects.filter(
            Q(sender=self.request.user, recipient_id=recipient_id) |
            Q(recipient=self.request.user, sender_id=recipient_id)
        ).order_by('timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipient_id = self.kwargs['recipient_id']
        
        try:
            context['recipient'] = CustomUser.objects.get(id=recipient_id)
        except CustomUser.DoesNotExist:
            context['recipient'] = None
        
        return context

def send_message(request):
    if request.method == 'POST':
        try:
            recipient = CustomUser.objects.get(id=request.POST['recipient_id'])
            content = request.POST['content']
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return redirect('talkroom', recipient_id=recipient.id)
        except CustomUser.DoesNotExist:
            return redirect('friends')
        
def refresh_conversation(request, recipient_id):
    recipient = get_object_or_404(CustomUser, id=recipient_id)

    messages = Message.objects.filter(
        Q(sender=request.user, recipient_id=recipient_id) |
        Q(recipient=request.user, sender_id=recipient_id)
    ).order_by('timestamp')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'messages': list(messages.values)
        })
    
    return render(request, 'chat_app/talkroom.html', {
        'recipient': recipient,
        'messages':messages
    })

def setting(request):
    return render(request, 'chat_app/setting.html')

class Logout(LogoutView):
    template_name = 'chat_app/setting.html'
    next_page = 'chat_app/index.html'

class EmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'chat_app/email.html'
    form_class = EmailChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs
    
    def form_valid(self, form):
        form.update(user=self.request.user)
        return render(self.request ,'chat_app/email2.html', {'form':form, 'message': 'メールアドレス変更完了'})
    
class UsernameChangeView(LoginRequiredMixin, FormView):
    template_name = 'chat_app/username.html'
    form_class = UsernameChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs
    
    def form_valid(self, form):
        form.update(user=self.request.user)
        return render(self.request ,'chat_app/username2.html', {'form':form, 'message': 'ユーザー名変更完了'})
    
class passchange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'chat_app/password.html'
    next_page = 'chat_app/password2.html'

class passchange2(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'chat_app/password2.html'
    next_page = 'chat_app/setting.html'

class ImgChangeView(LoginRequiredMixin, FormView):
    template_name = 'chat_app/img.html'
    form_class = ImgChangeForm
    
    def form_valid(self, form):
        user = self.request.user
        user.img = form.cleaned_data['img']
        user.save()
        return self.render_to_response(self.get_context_data(
            form=form, message = 'アイコンが変更されました'
        ))
    