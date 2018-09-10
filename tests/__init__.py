import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('./logs/test_log.txt', 'w')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)