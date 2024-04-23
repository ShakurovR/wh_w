import logging

log = logging.getLogger("WORKER")
LOG_FORMAT = "[%(levelname)7s %(filename)15s:%(lineno)3s - %(funcName)15s() ] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
log.setLevel(logging.DEBUG)
