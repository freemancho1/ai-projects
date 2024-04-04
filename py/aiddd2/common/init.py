import warnings


class AppInit:
    def __init__(self):
        self._setWarning()
        
    def _setWarning(self):
        warnings.filterwarnings(
            'ignore',
            category=UserWarning,
            module='openpyxl.styles.stylesheet'
        )