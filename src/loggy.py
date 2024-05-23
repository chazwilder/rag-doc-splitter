import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('rag_logger')
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler('rag_logger.log', maxBytes=10*1024*1024, backupCount=1, encoding='utf-8', errors='ignore')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)