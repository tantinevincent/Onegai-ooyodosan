class Message:
    def __init__(self):
        self._check_flag = False
        
    def is_need_check(self):
        return self._check_flag
        
    def set_need_check(self, flag):
        self._check_flag = flag