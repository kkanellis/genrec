import os
import logging

LEVEL_DICT = {
    'WARN': logging.WARN,
    'DEBUG': logging.DEBUG,
    'ERROR': logging.ERROR,
    'INFO': logging.INFO
}


#The background is set with 40 plus the number of the color,
# and the foreground with 30
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = \
    ((COLOR_SEQ % (seq+30)) for seq in range(8))

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': CYAN,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

logging.captureWarnings(True)

def get_logger(name, terminal_log_level='DEBUG', file_log_level=None,
                    log_dir=None, include_time=False, include_date=False):
    """Create a custom logger with date and time

    If 'terminal_log_level' is None, no log messages will be printed to shell
    If 'file_log_level' is None, no file will be used to store log messages

    If 'log_dir' is None, file will be created in logs folder.
    If 'log_dir' is invalid, an IOError will be raised

    If 'include_time' is True, time will be included in the log message
    If 'include_time' is True, date will be included in the log message
    """

    if terminal_log_level and terminal_log_level not in LEVEL_DICT:
        raise ValueError('Invalid terminal log level defined [{}]'
                            .format(terminal_log_level))

    if file_log_level and file_log_level not in LEVEL_DICT:
        raise ValueError('Invalid file log level defined [{}]'
                            .format(file_log_level))

    # Create logger object
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not any( (file_log_level, terminal_log_level) ):
        # both loggers are disabled
        logger.disabled = True
        return logger

    # Create the datetime format string
    datetime_format = ""
    if include_date:
        datetime_format = "%Y-%m-%d "
    if include_time:
        datetime_format += " %H:%M:%S"
    datetime_format = datetime_format.strip()

    if file_log_level: # Log in file
        if not log_dir:
            log_dir = os.path.abspath(os.path.dirname(__file__))
            log_dir = os.path.join(log_dir, 'logs')

        # Create directories
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # File handler
        fh = logging.FileHandler(os.path.join(log_dir, name + '.log'))
        fh.setLevel(LEVEL_DICT[file_log_level])

        log_format = "[%(levelname)-5s] %(message)s"
        if datetime_format:
            log_format = "[%(asctime)s]: " + log_format

        file_formatter = ColoredFormatter(log_format, datetime_format)
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)

    if terminal_log_level: # Log in terminal
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(LEVEL_DICT[terminal_log_level])

        log_format = "[%(levelname)-5s] [%(name)s] %(message)s"
        if datetime_format:
            log_format = "[%(asctime)s]: " + log_format

        console_formatter = ColoredFormatter(log_format, datetime_format)
        ch.setFormatter(console_formatter)
        logger.addHandler(ch)

    return logger

class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt, date_fmt, use_color=True):
        super(ColoredFormatter, self).__init__(fmt, date_fmt)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLORS[levelname] + levelname + RESET_SEQ
            record.levelname = levelname_color
        return super(ColoredFormatter, self).format(record)
