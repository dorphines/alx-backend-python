# Integration Test Task Solution

This document explains the solution for implementing the integration tests for the `GithubOrgClient.public_repos` method.

## Task

The task was to implement two test methods:

1.  `test_public_repos`: To test the `GithubOrgClient.public_repos` method without any arguments and ensure it returns the expected results based on the fixtures.
2.  `test_public_repos_with_license`: To test the `public_repos` method with the argument `license="apache-2.0"` and make sure the result matches the expected value from the fixtures.

## Implementation

The changes were made in the `test_client.py` file, specifically in the `TestIntegrationGithubOrgClient` class.

The original `test_public_repos` method was split into two separate methods to handle the two test cases as requested.

### `test_public_repos`

This method tests the `public_repos` method without any arguments. It asserts that the list of public repositories returned by the `GithubOrgClient` matches the `expected_repos` from the `TEST_PAYLOAD` fixture.

```python
def test_public_repos(self):
    """
    Test public_repos method in an integration test.
    """
    client = GithubOrgClient("google")
    self.assertEqual(client.public_repos(), self.expected_repos)
```

### `test_public_repos_with_license`

This method tests the `public_repos` method with the `license` argument set to `"apache-2.0"`. It asserts that the list of public repositories with the "apache-2.0" license returned by the `GithubOrgClient` matches the `apache2_repos` from the `TEST_PAYLOAD` fixture.

```python
def test_public_repos_with_license(self):
    """
    Test public_repos method with license in an integration test.
    """
    client = GithubOrgClient("google")
    self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
```

## Verification

The tests were run after the implementation, and all tests passed successfully, confirming that the implementation is correct.
