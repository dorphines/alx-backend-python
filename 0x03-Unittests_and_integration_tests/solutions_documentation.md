# Unittests and Integration Tests - Solutions Documentation

This document provides a summary of the solutions implemented for the "Unittests and Integration Tests" project, covering tasks from 0 to 8.

## Task 0: Parameterize a unit test (`test_utils.py`)

**Objective:** Familiarize with `utils.access_nested_map` and write a parameterized unit test for it.

**Solution:**
The `TestAccessNestedMap` class was created, inheriting from `unittest.TestCase`. The `test_access_nested_map` method was implemented and decorated with `@parameterized.expand`. This decorator allowed testing `access_nested_map` with multiple sets of inputs (nested map, path) and their expected outputs in a concise manner. `self.assertEqual` was used to verify the returned values.

**Code Snippet (from `test_utils.py`):**
```python
class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
```

## Task 1: Parameterize a unit test (exception) (`test_utils.py`)

**Objective:** Test that `KeyError` is raised for invalid paths in `utils.access_nested_map` and verify the exception message.

**Solution:**
The `test_access_nested_map_exception` method was added to `TestAccessNestedMap`. It uses `@parameterized.expand` to provide different invalid inputs. The `with self.assertRaises(KeyError) as context:` context manager was used to catch the `KeyError`, and `self.assertEqual(str(context.exception), f"'{path[-1]}'")` verified that the exception message matched the expected last key in the path.

**Code Snippet (from `test_utils.py`):**
```python
class TestAccessNestedMap(unittest.TestCase):
    # ... (previous test)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{path[-1]}'")
```

## Task 2: Mock HTTP calls (`test_utils.py`)

**Objective:** Test `utils.get_json` without making actual external HTTP calls, using mocking.

**Solution:**
The `TestGetJson` class was defined. The `test_get_json` method was decorated with `@parameterized.expand` for different URLs and payloads, and `@patch('utils.requests.get')` to mock the `requests.get` function. A `Mock` object was configured to return a specific `json.return_value` (the `test_payload`). `self.assertEqual` verified the output of `get_json`, and `mock_get.assert_called_once_with(test_url)` ensured that `requests.get` was called exactly once with the correct URL.

**Code Snippet (from `test_utils.py`):**
```python
class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)
```

## Task 3: Parameterize and patch (`test_utils.py`)

**Objective:** Test the `utils.memoize` decorator, ensuring the decorated method is called only once.

**Solution:**
The `TestMemoize` class was implemented. Inside its `test_memoize` method, a nested `TestClass` was defined with a method `a_method` and a memoized property `a_property` that calls `a_method`. `patch.object(TestClass, 'a_method', return_value=42)` was used to mock `a_method`. The test then called `a_property` twice and used `mock_method.assert_called_once()` to confirm that `a_method` was indeed called only once, demonstrating memoization.

**Code Snippet (from `test_utils.py`):**
```python
class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_instance = TestClass()
            self.assertEqual(test_instance.a_property, 42)
            self.assertEqual(test_instance.a_property, 42)
            mock_method.assert_called_once()
```

## Task 4: Parameterize and patch as decorators (`test_client.py`)

**Objective:** Test `client.GithubOrgClient.org` using `@patch` and `@parameterized.expand` decorators.

**Solution:**
A new file `test_client.py` was created. The `TestGithubOrgClient` class was defined. The `test_org` method was decorated with `@parameterized.expand` to test different organization names and `@patch('client.get_json')` to mock `get_json`. The mock was configured to return a simple payload, and the test asserted that `client.org` returned this payload and that `get_json` was called once with the correct GitHub API URL.

**Code Snippet (from `test_client.py`):**
```python
class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"payload": True}

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"payload": True})
        mock_get_json.assert_called_once_with(expected_url)
```

## Task 5: Mocking a property (`test_client.py`)

**Objective:** Unit-test `GithubOrgClient._public_repos_url` by mocking the `org` property.

**Solution:**
The `test_public_repos_url` method was added to `TestGithubOrgClient`. It used `patch('client.GithubOrgClient.org', new_callable=PropertyMock)` as a context manager to mock the `org` property. The mocked property was set to return a dictionary containing a `repos_url`. The test then asserted that `client._public_repos_url` correctly returned this mocked URL.

**Code Snippet (from `test_client.py`):**
```python
class TestGithubOrgClient(unittest.TestCase):
    # ... (previous tests)

    def test_public_repos_url(self):
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://example.com/repos"}
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, "http://example.com/repos")
```

## Task 6: More patching (`test_client.py`)

**Objective:** Unit-test `GithubOrgClient.public_repos` by mocking `get_json` and `_public_repos_url`.

**Solution:**
The `test_public_repos` method was added to `TestGithubOrgClient`. It used `@patch('client.get_json')` to mock the `get_json` function and `patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)` as a context manager to mock the `_public_repos_url` property. The mocks were configured to return specific payloads and URLs. The test asserted that `public_repos` returned the expected list of repository names, including filtering by license, and verified that both mocked components were called exactly once.

**Code Snippet (from `test_client.py`):**
```python
class TestGithubOrgClient(unittest.TestCase):
    # ... (previous tests)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3"},
        ]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "http://example.com/repos"
            client = GithubOrgClient("test_org")
            self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
            self.assertEqual(client.public_repos("apache-2.0"), ["repo1"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()
```

## Task 7: Parameterize (`test_client.py`)

**Objective:** Unit-test `GithubOrgClient.has_license` using parameterization.

**Solution:**
The `test_has_license` method was added to `TestGithubOrgClient`. It was decorated with `@parameterized.expand` to test `GithubOrgClient.has_license` with various combinations of repository dictionaries and license keys, along with their expected boolean outcomes. `self.assertEqual` was used to verify the returned boolean value.

**Code Snippet (from `test_client.py`):**
```python
class TestGithubOrgClient(unittest.TestCase):
    # ... (previous tests)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
```

## Task 8: Integration test: fixtures (`test_client.py`)

**Objective:** Write an integration test for `GithubOrgClient.public_repos` using fixtures and global patching.

**Solution:**
The `TestIntegrationGithubOrgClient` class was created and decorated with `@parameterized_class` to use the `TEST_PAYLOAD` from `fixtures.py`. The `setUpClass` class method was implemented to globally patch `requests.get` using `patch` and `side_effect` to return specific fixture data based on the URL requested. The `tearDownClass` method was implemented to stop the patcher. The `test_public_repos` method then called `client.public_repos` and asserted the results against the expected repository lists provided by the fixtures.

**Code Snippet (from `test_client.py`):**
```python
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]}
        cls.get_patcher = patch('requests.get', **config)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
```
