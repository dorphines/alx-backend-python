# Project: Understanding Middlewares

This project demonstrates the implementation of several Django middlewares for a messaging application.

## Task 0: Project Setup

The project was set up by copying the `messaging_app` directory to a new directory named `Django-Middleware-0x03`.

## Task 1: Logging User Requests (Basic Middleware)

A middleware for logging user requests was implemented.

- **File:** `chats/middleware.py`
- **Class:** `RequestLoggingMiddleware`
- **Functionality:** Logs the timestamp, user (or 'Anonymous'), and request path for every incoming request to the `requests.log` file.
- **Configuration:** The middleware was added to the `MIDDLEWARE` list in `messaging_app/settings.py`.

## Task 2: Restrict Chat Access by Time

A middleware was created to restrict access to the application based on the time of day.

- **File:** `chats/middleware.py`
- **Class:** `RestrictAccessByTimeMiddleware`
- **Functionality:** Restricts access to the application to business hours (9am to 6pm). If a user tries to access the application outside of these hours, a `403 Forbidden` response is returned.
- **Configuration:** The middleware was added to the `MIDDLEWARE` list in `messaging_app/settings.py`.

## Task 3: Detect and Block Offensive Language (Rate Limiting)

A middleware was implemented to limit the number of messages a user can send in a given time frame. Although the task was named "Detect and Block Offensive Language", the implementation follows the instructions for rate limiting.

- **File:** `chats/middleware.py`
- **Class:** `OffensiveLanguageMiddleware`
- **Functionality:** Limits users to 5 POST requests per minute based on their IP address. If the limit is exceeded, a `403 Forbidden` response is returned.
- **Configuration:** The middleware was added to the `MIDDLEWARE` list in `messaging_app/settings.py`.

## Task 4: Enforce Chat User Role Permissions

A middleware was created to enforce role-based access control.

- **File:** `chats/middleware.py`
- **Class:** `RolepermissionMiddleware`
- **Functionality:** Restricts access to users who are not staff members (`is_staff=False`). Non-staff users will receive a `403 Forbidden` response.
- **Configuration:** The middleware was added to the `MIDDLEWARE` list in `messaging_app/settings.py`.
