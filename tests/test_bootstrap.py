import pytest
from idk.core import bootstrap

def test_bootstrap():
    result: str = bootstrap.base_checks()
    assert result == 'MAIN_OK_ALL_BASE_CHECK_SUCCESS'
    
def test_os_check():
    result: str = bootstrap.os_check()

    assert result == 'OK_OS_SUPPORTED'