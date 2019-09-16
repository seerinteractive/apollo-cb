groups = [
    'equest_builder_error',
    'auth',
    'asyncio',
    'client_builder',
    'error_dict_converter',
    'safe_dict_converter',
    'converters',
    'safe_list_converter',
    'error_list_converter',
    'request_builder_safe',
    'request_builder',
    'request_builder_error',
    'file_pattern',
    'one_client_builder',
    'api_request',
    'bamboohr',
    'pipedrive',
    'harvest,'
    'api',
    'rate_limit',
]

def pytest_configure(config):
    for mark in groups:
        config.addinivalue_line(
            "markers", mark,
        )