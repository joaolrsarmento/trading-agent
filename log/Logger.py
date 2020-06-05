import json
import datetime
import os

class Logger(object):
    """
    This class represents a log file.

    """

    def __init__(self, tool_name=None, path_for_log_file="tmp", parameters=None):
        """
        Class constructor.

        @param tool_name: name of the tool that generated this log
        @@type tool_name: string
        @param path_for_log_file: path to save the log
        @@type path_for_log_file: string
        @param parameters: parameters the tool wanna save
        @@type parameters: None
        """
        self.path = os.path.join(path_for_log_file, "")
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
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
        print('Saving log...')
        with open(os.path.join(self.path, f"log_{'__'.join(str(self.date).split(' '))}.json"), 'w') as f:
            json.dump(self._data, f)
