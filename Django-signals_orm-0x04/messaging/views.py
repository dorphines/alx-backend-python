from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import json
from .models import Message

@csrf_exempt
@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Logged in successfully', 'user_id': user.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@login_required
@require_POST
def delete_user(request):
    user = request.user
    user.delete()
    return JsonResponse({'status': 'success', 'message': 'User deleted successfully.'})

def serialize_thread(message):
    """
    Recursively serialize a message and its replies.
    """
    return {
        'id': message.id,
        'sender': message.sender.username,
        'content': message.content,
        'timestamp': message.timestamp,
        'edited': message.edited,
        'replies': [serialize_thread(reply) for reply in message.replies.all()]
    }

@login_required
@require_GET
def message_thread(request, message_id):
    """
    Retrieve a message and its full reply thread, optimized with prefetch_related.
    """
    try:
        # We prefetch all replies recursively.
        # This is not a true recursive DB query, but it's often efficient enough.
        # For very deep threads, other strategies might be needed.
        message = Message.objects.select_related('sender').prefetch_related('replies').get(id=message_id)

        thread_data = serialize_thread(message)
        return JsonResponse(thread_data)

    except Message.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found.'}, status=404)

from django.views.decorators.cache import cache_page
from django.db.models import Q
from .models import Message, MessageHistory

@login_required
@require_GET
@cache_page(60)
def message_list(request, user_id):
    """
    Retrieve the conversation between the logged-in user and another user.
    This view is cached for 60 seconds.
    """
    user = request.user
    other_user = get_object_or_404(User, id=user_id)

    messages = Message.objects.filter(
        (Q(sender=user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=user))
    ).order_by('timestamp')

    data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp,
        'edited': msg.edited
    } for msg in messages]

    return JsonResponse(data, safe=False)

@login_required
@require_GET
def unread_messages(request):
    """
    Retrieve all unread messages for the logged-in user.
    """
    user = request.user
    messages = Message.unread.unread_for_user(user)
    
    data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp,
        'edited': msg.edited
    } for msg in messages]

    return JsonResponse(data, safe=False)

@login_required
@require_GET
def message_history(request, message_id):
    """
    Retrieve the edit history of a message.
    """
    message = get_object_or_404(Message, id=message_id)
    history = message.messagehistory_set.all().order_by('-timestamp')
    
    data = [{
        'old_content': h.old_content,
        'timestamp': h.timestamp
    } for h in history]
    
    return JsonResponse(data, safe=False)
