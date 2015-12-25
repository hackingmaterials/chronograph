from datetime import datetime, timedelta

import sys

__author__ = 'Anubhav Jain <ajain@lbl.gov>'


# TODO: add docs

class Chronograph():

    def __init__(self, name=None, verbosity=0, m_logger=None, log_lvl=None, start_timing=False):
        self.name = name
        self.header = "Chronograph {}".format(name) if name else "Chronograph"
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
            label = label if label else str(len(self.timing_data)+1)
            self.timing_data.append({"start": datetime.now(), "label": label})
            if self.verbosity >= 2:
                self.print_fnc("{}: started at: {}\n".format(self.header, self.timing_data[-1]["start"]))
            return True
        else:
            self.print_fnc("{}: Warning: Cannot start Chronograph while in current state! Stop or reset chronograph before starting.\n".format(self.header))
            return False

    def stop(self):
        if self.timing_data and "stop" not in self.timing_data[-1]:
            self.timing_data[-1]["stop"] = datetime.now()
            if self.verbosity >= 2:
                self.print_fnc("{}: stopped at: {}\n".format(self.header, self.timing_data[-1]["start"]))
            if self.verbosity >= 1:
                last_split = self.last_split
                last_split_text = "Last split ({}) time: {} s.".format(last_split['label'], self.get_split_time(last_split))

                self.print_fnc("{}: Total elapsed time: {} s. {}\n".format(self.header, self.total_elapsed_time, last_split_text))
            return True
        else:
            self.print_fnc("{}: Warning: Cannot stop Chronograph while in current state! Start chronograph first.\n".format(self.header))
            return False

    def reset(self):
        self.timing_data = []
        if self.verbosity >= 2:
            self.print_fnc("{}: Reset at: {}\n".format(self.header, self.timing_data[-1]["start"]))
            return True
        return False

    def split(self, label=None):
        success = self.stop()
        if success:
            success = self.start(label=label)
        return success

    @property
    def total_elapsed_time(self):
        elapsed_time = 0.0
        for t in self.timing_data:
            start_time = t['start']
            stop_time = t['stop'] if 'stop' in t else datetime.now()
            elapsed_time += (stop_time - start_time).total_seconds()

        return elapsed_time

    @property
    def last_split(self):
        for t in reversed(self.timing_data):
            if 'stop' in t:
                return t
        return False

    @staticmethod
    def get_split_time(split_data):
        return (split_data['stop'] - split_data['start']).total_seconds()

    @property
    def last_split_time(self):
        return self.get_split_time(self.last_split) if self.last_split else 0

    def to_json(self):
        return self.timing_data  # TODO: does datetime need to be converted to/from JSON?

    # TODO: add pretty print report


if __name__ == "__main__":

    x = Chronograph(name="my stopwatch", verbosity=1)
    x.start()
    x.stop()
    x.start()
    x.split()
    x.split()

    print(x.to_json())



# TODO: allow with Chronograph() mode

# TODO: allow getting a Chronograph by name

# TODO: allow decorating a function with a Chronograph
