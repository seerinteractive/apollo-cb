#standard
from collections import namedtuple

#local
from apollo.utils import FilePattern



FilePatternCase = namedtuple('FilePatternCase', 'pattern,expected')

class MockObj:
    
    @property
    def greeting(self):
        return "Hi"

def file_func(obj, exclamation):
    return f'{obj.greeting} there{exclamation}'

FILE_PATTERN_SCENARIOS = [
    FilePatternCase(
        pattern =  FilePattern(
            lookup_obj = MockObj(),
            file_func = file_func,
            exclamation = '!'
        ),
        expected = 'Hi there!'
    ),
    FilePatternCase(
        pattern =  FilePattern(),
        expected = ''
    ),

]