import warnings

'''
경고 발생방법 변경:
  1. 엑셀파일을 읽을 때, openpyxl라이브러리에서 스타일관련 경고를 출력하는 경우가
     종종 발생하는데 이 경고는 무시해도 무방하기 때문에 출력되지 않도록 변경
'''
def _warning_setting():
    warnings.filterwarnings(
        'ignore',
        category=UserWarning,
        module='openpyxl.styles.stylesheet'
    )


def app_init():
    _warning_setting()