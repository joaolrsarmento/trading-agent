import json
import datetime


class Logger(object):
    """
    This class represents a log file.

    """

    def __init__(self, tool_name=None, path_for_log_file="tmp/", parameters=None):
        """
        @param tool_name: name of the tool that generated this log
        @@type tool_name: string
        @param path_for_log_file: path to save the log
        @@type path_for_log_file: string
        @param parameters: parameters the tool wanna save
        @@type parameters: None
        """
        self.path = path_for_log_file if path_for_log_file[-1] == '/' else path_for_log_file + '/'
        self._data = None
        self.date = datetime.datetime.now()

    def log(self, data):
        """
        Log the data.
        
        """
        self._data = data
        self._save()

    def get_data(self):
        """
        Get data stored.

        @return data: data stored
        @@@type data: dict
        """
        return self._data

    def _save(self):
        """
        Save the data stored.

        """
        with open(f"{self.path}log_{self.date}.json", 'w') as f:
            json.dump(self._data, f)
