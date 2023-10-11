from aiddd.app.init import app_init
from aiddd.load_data import get_provide_data
from aiddd.proprocess_data import preprocess
from aiddd.utils.logs import Log

def main():
    app_init()
    logs = Log()
    
    try:
        logs.start('학습시작')
        preprocess(get_provide_data())
    except Exception as e:
        print(f'Error: {e}')
    logs.stop('학습종료')
        
if __name__ == '__main__':
    main()