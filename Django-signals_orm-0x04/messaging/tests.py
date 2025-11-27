from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingSignalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello, this is a test message."
        )

    def test_notification_created_on_new_message(self):
        # A new message is created in setUp, so a notification should exist.
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, self.message)
        self.assertFalse(notification.is_read)

    def test_message_edit_logs_history(self):
        # Check that no message history exists initially
        self.assertEqual(MessageHistory.objects.count(), 0)

        # Update the message content
        old_content = self.message.content
        self.message.content = "This is the updated content."
        self.message.save()

        # Check that a message history record was created
        self.assertEqual(MessageHistory.objects.count(), 1)
        history = MessageHistory.objects.first()
        self.assertEqual(history.message, self.message)
        self.assertEqual(history.old_content, old_content)

        # Check that the message is marked as edited
        self.assertTrue(self.message.edited)

        # Test that saving without changing content doesn't create new history
        self.message.save()
        self.assertEqual(MessageHistory.objects.count(), 1)

    def test_delete_user_cleans_up_data(self):
        # Create a message from user2 to user1 as well
        Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Hello back!"
        )
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(Notification.objects.count(), 2)

        # Edit the first message to create history
        self.message.content = "Updated content again"
        self.message.save()
        self.assertEqual(MessageHistory.objects.count(), 1)

        # Delete user1
        user1_id = self.user1.id
        self.user1.delete()

        # Check that user1 is deleted
        self.assertFalse(User.objects.filter(id=user1_id).exists())

        # Check that messages involving user1 are deleted
        self.assertEqual(Message.objects.count(), 0)

        # Check that notifications for user1 and for messages sent to user1 are deleted
        self.assertEqual(Notification.objects.count(), 0)

        # Check that message histories for messages involving user1 are deleted
        self.assertEqual(MessageHistory.objects.count(), 0)

    def test_message_thread_view(self):
        # Create a reply to the original message
        reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="This is a reply.",
            parent_message=self.message
        )

        # Create a reply to the reply
        reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="This is a nested reply.",
            parent_message=reply1
        )
        
        self.client.force_login(self.user1)
        response = self.client.get(f'/messages/{self.message.id}/')
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        self.assertEqual(data['id'], self.message.id)
        self.assertEqual(len(data['replies']), 1)
        
        reply_data = data['replies'][0]
        self.assertEqual(reply_data['id'], reply1.id)
        self.assertEqual(len(reply_data['replies']), 1)
        
        nested_reply_data = reply_data['replies'][0]
        self.assertEqual(nested_reply_data['id'], reply2.id)
        self.assertEqual(len(nested_reply_data['replies']), 0)
from django.test import TestCase, override_settings

    def test_unread_messages_view(self):
        # user2 has one unread message from setUp
        self.assertEqual(Message.unread.unread_for_user(self.user2).count(), 1)

        # Create another message for user2 and mark it as read
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="This is a read message.",
            read=True
        )

        # Create a message for user1 to ensure it's not included
        Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="A message for user1."
        )

        self.client.force_login(self.user2)
        response = self.client.get('/messages/unread/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.message.id)

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_message_list_view_caching(self):
        self.client.force_login(self.user1)
        response = self.client.get(f'/messages/with/{self.user2.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Check that the cache-control header is set
        self.assertTrue(response.has_header('Cache-Control'))
        self.assertIn('max-age=60', response['Cache-Control'])
