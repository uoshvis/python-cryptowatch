"""Test fixtures."""
import pytest


@pytest.fixture
def assets_keys(scope='module'):
    """Mock keys fixture."""
    return ['result', 'allowance']
