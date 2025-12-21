# Messaging App

A Django-based messaging application with CI/CD integration.

## Project Structure

- `messaging_app/`: Main Django application source code.
- `chats/`: Chat functionality app.
- `tests.py`: Unit tests.

## CI/CD Pipelines

### Jenkins

This project includes a `Jenkinsfile` for a Declarative Pipeline that:
1.  **Checkouts** the code from GitHub.
2.  **Installs Dependencies** in a virtual environment.
3.  **Runs Tests** using `pytest` and generates JUnit reports.
4.  **Builds** a Docker image (using legacy builder for compatibility).
5.  **Pushes** the image to Docker Hub.

**Setup:**
- Ensure Jenkins has the Docker Pipeline and Git plugins installed.
- Configure `github-credentials` (Username/Password or Token) in Jenkins.
- Configure `dockerhub-credentials` (Username/Password) in Jenkins.

### GitHub Actions

Workflows are located in `.github/workflows/` (Note: for GitHub to detect these, the `.github` folder must be at the repository root).

1.  **`ci.yml`**:
    - Runs on Push/PR to `main`.
    - Sets up MySQL service.
    - Installs dependencies.
    - Runs `flake8` linting.
    - Runs tests with `pytest` and coverage reporting.

2.  **`dep.yml`**:
    - Runs on Push to `main`.
    - Builds and Pushes Docker image to Docker Hub.
    - Requires `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets in GitHub repository settings.

## Running Tests Locally

```bash
cd messaging_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-django
pytest
```
