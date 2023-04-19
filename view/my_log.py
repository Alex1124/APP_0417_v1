import logging
from pathlib import Path
import sys
# https://orcahmlee.github.io/python/python-logging/


#loggin 紀錄
def my_logging():
    "紀錄設定，回傳dev_logger物件記錄程式重要處"  

   


    dev_logger: logging.Logger = logging.getLogger(name='dev')
    dev_logger.handlers = []
    
    dev_logger.setLevel(logging.DEBUG)
    handler: logging.StreamHandler = logging.StreamHandler(stream=sys.stdout.flush())
    filepath : logging.FileHandler = logging.FileHandler(Path('log') / 'logging.txt', mode='a', encoding='utf-8')

  
    formatter: logging.Formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filepath.setLevel(logging.DEBUG)
    filepath.setFormatter(formatter)

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    dev_logger.addHandler(handler)
    dev_logger.addHandler(filepath)
    
    

    
    return dev_logger
    
    
    
