

class FilePath:

    def __init__(self,
                 file_func=lambda x: x,
                 pattern_params={}
                 ):
        self._file_func = file_func
        self._pattern_params = pattern_params
         
    @property
    def file_func(self,):
        return self._file_func

    @property
    def pattern_params(self,):
        return self._pattern_params