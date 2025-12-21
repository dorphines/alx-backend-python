from django.test import TestCase
from .models import User, Conversation, Message

class ModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)

    def test_user_creation(self):
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user1.role, 'guest')

    def test_conversation_creation(self):
        self.assertEqual(self.conversation.participants.count(), 2)

    def test_message_creation(self):
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            message_body='Hello world'
        )
        self.assertEqual(message.message_body, 'Hello world')
        self.assertEqual(message.sender, self.user1)