import pytest

from app.util.decorator import elapsed_time


@elapsed_time
@pytest.fixture
def calc():
    return 1000


def test_elapsed_time(calc):
    """시간 측정 데코레이터 테스트"""
    assert calc == 1000
