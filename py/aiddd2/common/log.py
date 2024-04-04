import uuid
from datetime import datetime

import aiddd2.common.config as cfg
import aiddd2.common.message as msg


class Log:
    def __init__(self, type='none'):
        self._uniqueId = str(uuid.uuid4()).split('-')[-1]
        self._startTime = None
        self._baseMessage = msg.LOG[type]
        self._start()
        
    def _start(self):
        if cfg.IS_DEBUG_MODE:
            self._startTime = datetime.now()
            self._print(f'{self._baseMessage} {msg.LOG["start"]}')
            
    def mid(self, message):
        if cfg.IS_DEBUG_MODE:
            self._print(message)
            
    def stop(self):
        if cfg.IS_DEBUG_MODE:
            self._print(
                f'{self._baseMessage} {msg.LOG["end"]}',
                datetime.now()-self._startTime
            )
            
    def _print(self, message, pTime=None):
        print(f'[{self._uniqueId}][{datetime.now()}] {message}', end='')
        if pTime is not None:
            print(f', {msg.LOG["total"]}: {pTime}')
        else:
            print()