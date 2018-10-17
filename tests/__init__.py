import logging

logger = logging.getLogger()
file_handler = logging.FileHandler('../logs/test_log.txt', 'w')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
