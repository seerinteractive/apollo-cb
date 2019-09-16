#standard
from pprint import pprint as p

#third party
import pytest

#local
from apollo.request.api_request import APIRequest

from apollo.builder.converters import DictConverter
from apollo.builder.converters import ListConverter

from tests.data.request_builder_data import DICT_CONVERTER_ERROR_SCENARIOS
from tests.data.request_builder_data import DICT_CONVERTER_SAFE_SCENARIOS

from tests.data.request_builder_data import LIST_CONVERTER_SAFE_SCENARIOS
from tests.data.request_builder_data import LIST_CONVERTER_ERROR_SCENARIOS

@pytest.mark.parametrize('case',DICT_CONVERTER_ERROR_SCENARIOS)
@pytest.mark.error_dict_converter
@pytest.mark.converters
def test_error_dict_converter(case):

    with pytest.raises(case.expected):

        conv = DictConverter(
            static = case.static, 
            dynamic = case.dynamic
        )
        conv.static
        conv.dynamic

@pytest.mark.parametrize('case',DICT_CONVERTER_SAFE_SCENARIOS)
@pytest.mark.safe_dict_converter
@pytest.mark.converters
def test_safe_dict_converter(case):

    conv = DictConverter(
        static = case.static, 
        dynamic = case.dynamic
    )

    expected = [a for a in conv]

    assert case.static  == conv.static
    assert case.dynamic  == conv.dynamic
    assert case.expected == expected
    assert isinstance(conv, DictConverter)


@pytest.mark.parametrize('case',LIST_CONVERTER_SAFE_SCENARIOS)
@pytest.mark.safe_list_converter
@pytest.mark.converters
def test_safe_list_converter(case):


    conv = ListConverter(
        static = case.static, 
        dynamic = case.dynamic,
        delimiter = case.delimiter
    )
    
    conv_static_case = case.static if isinstance(case.static, list) else [case.static]

    expected = [a for a in conv]

    assert conv_static_case == conv.static
    assert case.dynamic  == conv.dynamic
    assert case.expected == expected

    assert ListConverter.count_lists(case.dynamic) == 0
    assert isinstance(expected, list)


@pytest.mark.parametrize('case',LIST_CONVERTER_ERROR_SCENARIOS)
@pytest.mark.error_list_converter
@pytest.mark.converters
def test_error_list_converter(case):

    with pytest.raises(case.expected):

        conv = ListConverter(
            static = case.static, 
            dynamic = case.dynamic,
            delimiter = case.delimiter
        )
        conv.static
        conv.dynamic
        conv.delimiter