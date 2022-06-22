from django.urls import path

from users.views import SighUpView, LogInView

urlpatterns = [
    path('/signup', SighUpView.as_view()),
    path('/login', LogInView.as_view())
]