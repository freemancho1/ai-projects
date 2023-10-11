import uuid
from datetime import datetime
import aiddd.app.config as CFG

class Log:
    def __init__(self):
        self._unique_id = str(uuid.uuid4()).split('-')[-1]
        self._start_time = None
        self._end_time = None
        
    def start(self, message):
        if CFG.IS_DEBUG_MODE:
            self._start_time = datetime.now()
            print(f'[{self._unique_id}][{self._start_time}] {message}')
            
    def mid(self, message):
        if CFG.IS_DEBUG_MODE:
            print(f'[{self._unique_id}][{datetime.now()}] {message}')
    
    def stop(self, message):
        if CFG.IS_DEBUG_MODE:
            self._end_time = datetime.now()
            print(
                f'[{self._unique_id}][{self._end_time}] {message}, '
                f'처리시간: {self._end_time - self._start_time}'
            )
        