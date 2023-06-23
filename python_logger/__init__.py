import logging
from colorama import Fore, Back, Style, init

def add_success(cls):
    SUCCESS = 60
    logging.addLevelName(SUCCESS, "SUCCESS")
    def success(msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        print(cls)
        if cls.isEnabledFor(SUCCESS):
            cls._log(SUCCESS, msg, args, **kwargs)

    cls.success = success
    return cls




class StreamColoredHandler(logging.StreamHandler):
    
    def __init__(self, level=logging.INFO):
        init()
        logging.StreamHandler.__init__(self)
        self.setLevel(level)
        self.setFormatter(logging.Formatter(fmt='[%(asctime)s] (%(levelname)s) | %(filename)s | %(lineno)s | %(funcName)s | %(message)s'))
    
    def emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            try:
                if record.levelno == logging.DEBUG:
                    msg = Fore.LIGHTBLACK_EX + self.format(record)
                if record.levelno == logging.INFO:
                    msg = Fore.CYAN + self.format(record)
                elif record.levelno == logging.WARNING:
                    msg = Fore.LIGHTYELLOW_EX + self.format(record)
                elif record.levelno == logging.ERROR:
                    msg = Fore.RED + self.format(record)
                elif record.levelno == logging.CRITICAL:
                    msg = Back.RED +  Fore.WHITE + self.format(record)
            except Exception as err:
                print("[Logging Error] ==> {err}".format(err=err))
                msg = self.format(record)
            msg = msg + Style.RESET_ALL
            stream = self.stream
            # issue 35046: merged two stream.writes into one.
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)