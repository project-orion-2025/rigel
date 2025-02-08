import pytest
from configs.tags_config import generate_auth_token

@pytest.fixture(scope="session", autouse=True)
def auth_token():
    """Generate authentication token once for all tests"""
    return generate_auth_token()

@pytest.fixture(autouse=True)
def setup_test():
    """Setup before each test"""
    # Add any test setup here
    yield
    # Add any test cleanup here

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "tags_api: marks tests as tags API tests"
    )
    config.addinivalue_line(
        "markers",
        "create: marks tests as create operations"
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"report_{report.when}", report)
