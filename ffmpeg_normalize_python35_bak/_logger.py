import logging
from platform import system
from tqdm import tqdm
from multiprocessing import Lock
import sys

loggers = {}


# https://stackoverflow.com/questions/38543506/
class TqdmLoggingHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(sys.stderr)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.set_lock(Lock())
            tqdm.write(msg, file=sys.stderr)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


def setup_custom_logger(name):
    """
    Create a logger with a certain name and level
    """
    global loggers

    if loggers.get(name):
        return loggers.get(name)

    formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")

    # handler = logging.StreamHandler()
    handler = TqdmLoggingHandler()
    handler.setFormatter(formatter)

    # \033[1;30m - black
    # \033[1;31m - red
    # \033[1;32m - green
    # \033[1;33m - yellow
    # \033[1;34m - blue
    # \033[1;35m - magenta
    # \033[1;36m - cyan
    # \033[1;37m - white

    if system() not in ["Windows", "cli"]:
        logging.addLevelName(
            logging.ERROR, "[1;31m"+logging.getLevelName(logging.ERROR)+"[1;0m"
        )
        logging.addLevelName(
            logging.WARNING,
            "[1;33m"+logging.getLevelName(logging.WARNING)+"[1;0m",
        )
        logging.addLevelName(
            logging.INFO, "[1;34m"+logging.getLevelName(logging.INFO)+"[1;0m"
        )
        logging.addLevelName(
            logging.DEBUG, "[1;35m"+logging.getLevelName(logging.DEBUG)+"[1;0m"
        )

    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    # if (logger.hasHandlers()):
    #     logger.handlers.clear()
    if logger.handlers:
        logger.handlers = []
    logger.addHandler(handler)
    loggers.update(dict(name=logger))

    return logger
