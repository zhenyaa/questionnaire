from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import  CustomUser
###################################
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/signup.html'

class UserEditView(UpdateView):
    model = CustomUser
    fields = ('avatar','username','first_name', 'last_name', 'email', 'dob', 'aMyself', )
    template_name = "registration/userPage.html"
    pk_url_kwarg = 'pk'
    context_object_name = 'post'
    success_url = reverse_lazy('home')

    def get_initial(self):
        print('ITS initial!!!!!')
        user = get_object_or_404(CustomUser , pk= self.kwargs.get('pk'))
        print(user.username)
        return {"username": user.username}