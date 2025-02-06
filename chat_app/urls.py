from django.urls import path
from . import views
# from .views import HomeView ,UserCreateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, CustomUserListView, ChatView, LogoutView, send_message, EmailChangeView, UsernameChangeView, passchange, passchange2, ImgChangeView

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path('friends/', CustomUserListView.as_view(), name="friends"),
    path('talkroom/<int:recipient_id>/', ChatView.as_view(), name="talkroom"),
    path('send_message/', send_message, name="send_message"),
    path('conversation/refresh/<int:recipient_id>/', views.refresh_conversation, name='refresh_conversation'),
    path("setting/", views.setting, name="setting"),
    path("", LogoutView.as_view(), name="logout"),
    path('email/', EmailChangeView.as_view(), name="email"),
    path('username/', UsernameChangeView.as_view(), name="username"),
    path('logout/', LogoutView.as_view(), name = "logout"),
    path('password/', passchange.as_view(), name="password"),
    path('password2/', passchange2.as_view(), name="password2"),
    path('img/', ImgChangeView.as_view(), name='img'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)