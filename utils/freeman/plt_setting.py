import platform
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

WIN_FONT_PATH = 'c:/Windows/Fonts/malgun.ttf'
WIN_FONT_NAME = 'MalgunGothic'
# 우분투에 새로운 폰트를 설치한 경우 해당 ttf을 지정하면 됨
UBUNTU_FONT_PATH = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
UBUNTU_FONT_NAME = 'NanumGothic'

def plt_settings(korean=True, etc=None):
    if korean:
        _set_korean()
    dpi = 100 if etc is None else etc
    _set_etc(dpi)

def _set_korean():
    # 기본적인 경우는 아래 4컬럼만 해도 됨
    os_name = platform.system()
    font_path = WIN_FONT_PATH if os_name == 'Windows' else UBUNTU_FONT_PATH
    font_family = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = font_family
    
    # 위와 같이 해도 안되는 경우,
    # Matplotlib에서 자체적으로 관리하는 폰트 캐시에 해당 문자를 추가함
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = [font_family]
    
    font_entry = fm.FontEntry(
        fname = WIN_FONT_PATH if os_name == 'Windows' else UBUNTU_FONT_PATH,
        name = WIN_FONT_NAME if os_name == 'Windows' else UBUNTU_FONT_NAME
    )
    fm.fontManager.ttflist.insert(0, font_entry)
    
def _set_etc(dpi=100):
    
    # Matplotlib x,y축 레이블이 마이너스 일 때, '-'로 표시하도록 설정
    plt.rcParams['axes.unicode_minus'] = False

    # 해상도 지정
    #  - 일반적으로는 100이면 충분하며, 인쇄용 고해상도가 필요할 때 200 이상 지정
    plt.rcParams['figure.dpi'] = dpi
