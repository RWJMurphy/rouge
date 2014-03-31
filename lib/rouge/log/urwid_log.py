from rouge.log import Log

class UrwidLog(Log):
    def write_log_line(self, level, message):
        self.ui.main_view.messages.add_message(message, "LOG_" + level)
