from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with it.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed to authenticated users.
        if not request.user or not request.user.is_authenticated:
            return False
        
        # The user must be a participant of the conversation.
        return obj.participants.filter(id=request.user.id).exists()
