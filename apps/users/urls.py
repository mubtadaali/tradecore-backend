from django.urls.conf import path

from apps.users.views import SignInView, SignOutView, UpdatePassword, SignUpView


urlpatterns = [
    path('signin', SignInView.as_view(), name='sign-in'),
    path('signout', SignOutView.as_view(), name='sign-out'),
    path('signup', SignUpView.as_view(), name='sign-up'),
    path('users/<int:pk>/update-password', UpdatePassword.as_view(), name='update-password'),
]
