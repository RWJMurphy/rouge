class Log:
    log_levels = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR']

    def __init__(self, ui, log_level='INFO'):
        self.ui = ui
        self.log_level = log_level

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

    def set_level(self, level):
        if self.valid_log_level(level):
            self.log_level = self.log_levels.index(level)
        else:
            raise ValueError("Log level {} not in {}".format(
                level,
                self.log_levels
            ))

    def will_log(self, level):
        return self.log_levels.index(level) >= self.log_level

    def valid_log_level(self, level):
        return level in self.log_levels

    def log(self, level, message):
        if not self.valid_log_level(level):
            self.error("Log level {} not in {}".format(
                level,
                self.log_levels
            ))
            self.trace(traceback.format_tb())

        if self.will_log(level):
            self.write_log_line(level, message)

    def write_log_line(self, level, message):
        raise NotImplemented()
