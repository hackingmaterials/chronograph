from datetime import datetime

import sys

__author__ = 'Anubhav Jain <ajain@lbl.gov>'


# TODO: add docs

class Chronograph():

    def __init__(self, name="Default", start_timing=False, verbosity=0, m_logger=None, log_lvl=None):
        self.name = name
        self.timing_data = []
        self.verbosity = verbosity
        if m_logger:
            self.print_fnc = getattr(m_logger, log_lvl.lower())
        else:
            self.print_fnc = sys.stdout.write

        if start_timing:
            self.start()

    def start(self, label=None):
        if not self.timing_data or "stop" in self.timing_data[-1]:
            self.timing_data.append({"start": datetime.now(), "label": label})
            return True
        else:
            self.print_fnc("Warning: Cannot start Chronograph in current state\n")
            return False

    def stop(self):
        if self.timing_data and "stop" not in self.timing_data[-1]:
            self.timing_data[-1]["stop"] = datetime.now()
            return True
        else:
            self.print_fnc("Warning: Cannot stop Chronograph in current state\n")
            return False

    def reset(self):
        self.timing_data = []
        return True

    def split(self, label=None):
        success = self.stop()
        if success:
            success = self.start(label=label)
        return success

    def to_json(self):
        return self.timing_data


if __name__ == "__main__":

    x = Chronograph()
    x.start("my label")
    x.stop()
    x.split("code part 2")
    x.split()
    print(x.to_json())



        # TODO: allow with Chronograph() mode

        # TODO: allow getting a Chronograph by name

        # TODO: allow decorating a function with a Chronograph

        # TODO: allow dumping Chronograph data to JSON
