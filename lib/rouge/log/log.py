class Log:
    log_levels = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'TRACE']

    def __init__(self, ui):
        self.ui = ui

    def debug(self, message):
        self.log('DEBUG', message)

    def info(self, message):
        self.log('INFO', message)

    def warn(self, message):
        self.log('WARN', message)

    def error(self, message):
        self.log('ERROR', message)

    def trace(self, message):
        self.log('TRACE', message)

    def log(self, level, message):
        raise NotImplemented()
