# 0x03-Unittests_and_integration_tests

This project focuses on writing unit tests and integration tests for Python applications, specifically for a GithubOrgClient. It covers various testing patterns such as mocking, parameterization, and fixtures using the `unittest` module and `parameterized` library.

## Table of Contents

- [Learning Objectives](#learning-objectives)
- [Requirements](#requirements)
- [Tasks](#tasks)
  - [0. Parameterize a unit test](#0-parameterize-a-unit-test)
  - [1. Parameterize a unit test (exception)](#1-parameterize-a-unit-test-exception)
  - [2. Mock HTTP calls](#2-mock-http-calls)
  - [3. Parameterize and patch](#3-parameterize-and-patch)
  - [4. Parameterize and patch as decorators](#4-parameterize-and-patch-as-decorators)
  - [5. Mocking a property](#5-mocking-a-property)
  - [6. More patching](#6-more-patching)
  - [7. Parameterize](#7-parameterize)
  - [8. Integration test: fixtures](#8-integration-test-fixtures)
- [Usage](#usage)
- [Author](#author)

## Learning Objectives

At the end of this project, you are expected to be able to explain to anyone, without the help of Google:

- The difference between unit and integration tests.
- Common testing patterns such as mocking, parameterizations and fixtures.

## Requirements

- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7).
- All your files should end with a new line.
- The first line of all your files should be exactly `#!/usr/bin/env python3`.
- A `README.md` file, at the root of the folder of the project, is mandatory.
- Your code should use the `pycodestyle` style (version 2.5).
- All your files must be executable.
- All your modules should have a documentation (`python3 -c 'print(__import__("my_module").__doc__)'`).
- All your classes should have a documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`).
- All your functions (inside and outside a class) should have a documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`).
- A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified).
- All your functions and coroutines must be type-annotated.

## Tasks

### 0. Parameterize a unit test

This task involves familiarizing with `utils.access_nested_map` and writing a unit test for it. The `TestAccessNestedMap.test_access_nested_map` method uses `@parameterized.expand` to test various valid inputs and asserts the expected results.

### 1. Parameterize a unit test (exception)

This task extends the `TestAccessNestedMap` class to include `test_access_nested_map_exception`. It uses `assertRaises` and `@parameterized.expand` to verify that `KeyError` is raised for invalid paths and that the exception message is as expected.

### 2. Mock HTTP calls

This task focuses on testing `utils.get_json`. The `TestGetJson` class implements `test_get_json` which uses `unittest.mock.patch` to mock `requests.get`. This ensures that no actual external HTTP calls are made during testing. The method is parameterized to test different URLs and payloads, verifying that `get_json` returns the expected data and that `requests.get` was called correctly.

### 3. Parameterize and patch

This task involves testing the `utils.memoize` decorator. The `TestMemoize` class's `test_memoize` method defines a `TestClass` with a memoized property. It uses `patch.object` to mock an internal method and asserts that the memoized property returns the correct value while ensuring the underlying method is called only once.

### 4. Parameterize and patch as decorators

This task introduces testing the `client.GithubOrgClient` class. The `TestGithubOrgClient` class in `test_client.py` implements `test_org`. This method uses `@patch` as a decorator to mock `client.get_json` and `@parameterized.expand` to test with different organization names, ensuring `GithubOrgClient.org` returns the correct value without making external HTTP calls.

### 5. Mocking a property

This task implements `test_public_repos_url` within `TestGithubOrgClient`. It uses `patch` as a context manager to mock the `GithubOrgClient.org` property, making it return a known payload. The test then verifies that `_public_repos_url` correctly extracts the repository URL from the mocked payload.

### 6. More patching

This task implements `TestGithubOrgClient.test_public_repos`. It uses `@patch` to mock `get_json` and `patch` as a context manager to mock `GithubOrgClient._public_repos_url`. The test verifies that `public_repos` returns the expected list of repositories based on the mocked data and that the mocked methods were called once.

### 7. Parameterize

This task implements `TestGithubOrgClient.test_has_license`. It uses `@parameterized.expand` to test `GithubOrgClient.has_license` with various repository payloads and license keys, asserting the correct boolean return value.

### 8. Integration test: fixtures

This task involves writing an integration test for `GithubOrgClient.public_repos`. The `TestIntegrationGithubOrgClient` class uses `setUpClass` and `tearDownClass` to manage patching `requests.get` globally. It uses `@parameterized_class` with fixtures from `fixtures.py` to test the `public_repos` method with real-like data, ensuring that external requests are mocked and the method behaves as expected.

## Usage

To run the tests:

1.  Navigate to the project directory:
    ```bash
    cd /home/dorfin/alx/repos/alx-backend-python/0x03-Unittests_and_integration_tests
    ```
2.  (If not already done) Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install required packages:
    ```bash
    pip install parameterized requests
    ```
4.  Run the unit tests:
    ```bash
    python -m unittest test_utils.py
    python -m unittest test_client.py
    ```

## Author

[Your Name/Alias] - Replace with your actual name or alias.
