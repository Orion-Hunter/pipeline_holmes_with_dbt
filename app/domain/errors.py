class ExtractError(Exception):
    def __init__(self, message = ''):
        super().__init__(message)
        
        
class TransformError(Exception):
    def __init__(self, message=''):
        super().__init__(message)
        

class LoadError(Exception):
    def __init__(self, message=''):
        super().__init__(message)