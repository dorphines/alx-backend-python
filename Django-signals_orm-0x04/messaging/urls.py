from django.urls import path
from . import views

urlpatterns = [
    path('user/delete/', views.delete_user, name='delete_user'),
    path('messages/<int:message_id>/', views.message_thread, name='message_thread'),
    path('messages/unread/', views.unread_messages, name='unread_messages'),
    path('messages/with/<int:user_id>/', views.message_list, name='message_list'),
]
