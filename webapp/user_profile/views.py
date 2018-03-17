from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from user_profile.forms import UserProfileModelForm

# Create your views here.


class UserProfileView(FormView, LoginRequiredMixin):
    template_name = "user_profile/profile.html"
    form_class = UserProfileModelForm


class UserStatusView(TemplateView, LoginRequiredMixin):
    template_name = "user_profile/status.html"
