# logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

log_dir = "/var/log/sysintel"
os.makedirs(log_dir, exist_ok=True)

log_path = os.path.join(log_dir, "sysintel.log")

logger = logging.getLogger("sysintel")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_path, maxBytes=500000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
