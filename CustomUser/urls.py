# users/urls.py
from django.urls import path
from .views import SignUpView, UserEditView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accaunt/<int:pk>', UserEditView.as_view(), name='accauntEdit')
]