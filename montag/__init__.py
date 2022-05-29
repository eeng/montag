import logging
import sys

CALLBACK_PARAMS_QUEUE = 'CALLBACK_PARAMS_QUEUE'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # logging.FileHandler("log/debug.log"),
        logging.StreamHandler(sys.stdout)
    ],
)
