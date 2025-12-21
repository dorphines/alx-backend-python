from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('user/delete/', views.delete_user, name='delete_user'),
    path('messages/<int:message_id>/', views.message_thread, name='message_thread'),
    path('messages/<int:message_id>/history/', views.message_history, name='message_history'),
    path('messages/unread/', views.unread_messages, name='unread_messages'),
    path('messages/with/<int:user_id>/', views.message_list, name='message_list'),
]
