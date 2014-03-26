from rouge.log import Log

class UrwidLog(Log):
    def log(self, level, message):
        if level not in self.__class__.log_levels:
            self.error("Log level {} not in {}".format(
                level,
                self.__class__.log_levels
            ))
            self.trace(traceback.format_tb())
            return False

        self.ui.main_view.messages.add_message(message, "LOG_" + level)
