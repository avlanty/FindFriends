from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    # path('login/', views.new_activation_email, name="new_activation"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('activate/<uidb64>/<token>', views.activate_user, name="activate"),
    path('profile/<str:username>', views.profile_user, name="profile"),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name="registration/reset_password.html"), 
         name="password_reset"),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name="registration/reset_password_done.html"), 
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>', 
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/reset_password_confirm.html", form_class=SetPasswordForm), 
         name="password_reset_confirm"),  
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/reset_password_complete.html"), 
         name="password_reset_complete"), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)