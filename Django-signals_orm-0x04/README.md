# Django Signals, ORM & Advanced ORM Techniques

This project implements a messaging application to demonstrate the use of Django Signals, advanced ORM techniques, and caching.

## Features

### Task 0: Implement Signals for User Notifications
- A `Message` model to store messages between users.
- A `Notification` model to store notifications for new messages.
- A `post_save` signal on the `Message` model that automatically creates a `Notification` for the receiver of a new message.

### Task 1: Create a Signal for Logging Message Edits
- The `Message` model is updated with an `edited` boolean field.
- A `MessageHistory` model to log the original content of a message before it is edited.
- A `pre_save` signal on the `Message` model that logs the old content to `MessageHistory` and sets the `edited` flag to `True` when a message is modified.

### Task 2: Use Signals for Deleting User-Related Data
- A `delete_user` view that allows a user to delete their own account.
- The `on_delete=models.CASCADE` option is used in the `Message`, `Notification`, and `MessageHistory` models. This ensures that when a user is deleted, all their related data is automatically removed by the database, respecting foreign key constraints.

### Task 3: Leverage Advanced ORM Techniques for Threaded Conversations
- The `Message` model includes a self-referential `parent_message` foreign key to allow for threaded conversations.
- A `message_thread` view that retrieves a message and all its replies.
- The view uses `prefetch_related('replies')` to efficiently fetch all replies in a conversation with a minimal number of database queries. A recursive serialization function in Python is then used to build the nested thread structure.

### Task 4: Custom ORM Manager for Unread Messages
- The `Message` model has a `read` boolean field to track whether a message has been read.
- A custom model manager, `UnreadMessagesManager`, is implemented on the `Message` model.
- This manager provides an `unread_for_user(user)` method that returns all unread messages for a specific user.
- The query is optimized using `.only()` to fetch only the necessary fields, improving performance.
- An `unread_messages` view is provided to display a user's unread messages.

### Task 5: Implement Basic View Cache
- The project is configured for basic caching using Django's `locmem` cache backend.
- A `message_list` view is created to display the conversation between two users.
- The `@cache_page(60)` decorator is applied to this view, caching the response for 60 seconds to reduce database load for frequently accessed conversations.

## Project Structure
The project is contained within the `messaging` app. The key files are:
- `models.py`: Contains all the model definitions (`Message`, `Notification`, `MessageHistory`).
- `signals.py`: Contains the signal handlers for creating notifications and logging message edits.
- `apps.py`: Configures the `messaging` app and connects the signals.
- `views.py`: Contains the API views for deleting users, and retrieving message threads, unread messages, and conversations.
- `urls.py`: Defines the URL patterns for the views.
- `tests.py`: Contains unit tests for all the implemented features.
- `settings.py`: Contains the cache configuration.

## To Run the Project
1.  Install Django and other dependencies.
2.  Configure your database in the main project's `settings.py`.
3.  Include the `messaging` app in your `INSTALLED_APPS`.
4.  Include the `messaging.urls` in your main project's `urls.py`.
5.  Run migrations: `python manage.py migrate`.
6.  Run the development server: `python manage.py runserver`.
7.  You can then interact with the API endpoints defined in `messaging/urls.py`.

## To Run Tests
`python manage.py test messaging`
