import pytest
from apollo.utils import FilePattern
from apollo.utils import FilePath
from apollo.utils import RateLimit
from tests.data.utils_data import FILE_PATTERN_SCENARIOS

@pytest.mark.parametrize('case',FILE_PATTERN_SCENARIOS)
@pytest.mark.file_pattern
def test_file_pattern(case):

    assert isinstance(case.pattern.path, FilePath)
    assert str(case.pattern.path) == case.expected

@pytest.mark.rate_limit
def test_rate_limit():
    r = RateLimit()

    assert r.rate == 5
    assert r.limit == 5

    with pytest.raises(ValueError):
        f = RateLimit(
            rate = 0, 
            limit = 0
        )
