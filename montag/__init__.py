import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # logging.FileHandler("log/debug.log"),
        logging.StreamHandler(sys.stdout)
    ],
)
