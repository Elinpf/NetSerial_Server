import logging
import paramiko
from config import conf


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh_formatter = logging.Formatter(
    '%(asctime)-6s: - %(levelname)s - %(message)s')
sh_formatter = logging.Formatter('[%(levelname)s] %(message)s')

# to file
fh = logging.FileHandler('log/console.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(fh_formatter)

# to screen
sh = logging.StreamHandler()
# sh.setLevel(logging.INFO)
sh.setLevel(logging.DEBUG)
sh.setFormatter(sh_formatter)

# add Handler
logger.addHandler(fh)
logger.addHandler(sh)

logger.info("============= Start New Process =============")

paramiko.util.log_to_file(conf.SSH_PARAMIKO_LOG_PATH)