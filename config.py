import os
import logging

TOKEN = os.environ.get("API_TOKEN", "placeholder")
owner_id = int(os.environ.get("OWNER_ID", "0"))
Password = os.environ.get("ADMIN_PASSWORD", "placeholder")
AUTHENTICATION_ENABLED = os.environ.get("AUTHENTICATION_ENABLED", "false").strip().lower() == "true"
vlc_verbose = os.environ.get("VLC_VERBOSE", "0")
MIXER = os.environ.get("MIXER", "PCM")

#================= LOGGER =====================
LOG_DIR = os.environ.get("LOG_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
FILE_NAME = os.environ.get("FILE_NAME", "raffosberrybot.log")
LOG_FILE = os.environ.get("LOG_FILE", os.path.join(LOG_DIR, FILE_NAME))
FILE_LOG_LEVEL = os.environ.get("FILE_LOG_LEVEL", logging.DEBUG)
CONSOLE_LOG_LEVEL = os.environ.get("CONSOLE_LOG_LEVEL", logging.INFO)
MAX_LOG_SIZE_BYTES = os.environ.get("MAX_LOG_SIZE_BYTES", 2 * 1024 * 1024 ) # 2 MB
BACKUP_COUNT = os.environ.get("BACKUP_COUNT", 5)
LOG_FORMAT = os.environ.get("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(name)s - %(message)s")
ROOT_LOGGER_NAME = os.environ.get("ROOT_LOGGER_NAME", "RaffoSberryBot")