# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2024 Linh Pham
# wwdtm is released under the terms of the Apache License 2.0
"""Testing for object: :py:class:`wwdtm.validation`."""

import pytest

from wwdtm.validation import valid_int_id


@pytest.mark.parametrize("test_id", [54, 32767])
def test_validation_valid_int_id(test_id: int):
    """Testing for :py:meth:`wwdtm.validation.valid_int_id`.

    :param test_id: ID to test ID validation
    """
    assert valid_int_id(test_id), f"Provided ID {test_id} was not valid"


@pytest.mark.parametrize("test_id", [-54, 2**32, "hello", False])
def test_validation_invalid_int_id(test_id: int):
    """Negative testing for :py:meth:`wwdtm.validation.valid_int_id`.

    :param test_id: ID to test failing ID validation
    """
    assert not valid_int_id(test_id), f"Provided ID {test_id} was valid"


def test_validation_no_id():
    """Negative testing for :py:meth:`wwdtm.validation.valid_int_id`."""
    assert not valid_int_id(None), "Provided ID 'None' was valid"
