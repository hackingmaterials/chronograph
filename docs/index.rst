===========
Chronograph
===========

Introduction
============

Chronograph is a feature-packed timer/stopwatch/chronometer that makes it simple to time Python code and functions. Features include:

    * support for named Chronographs and labeled splits
    * reporting
    * multiple verbosity levels
    * built-in logging
    * JSON-compatible output data, including timestamps of start/stop
    * custom exceptions if desired
    * pain-free global management of multiple Chronographs
    * function decorators
    * support of with() syntax
    * cast to float gives total time
    * unit tested

Ten Examples of How to Use Chronograph
======================================

Example 1: Simple usage
-----------------------

Here is a straightforward usage example (note that Example #3 is even simpler)::

    import time
    from chronograph.chronograph import Chronograph

    cg = Chronograph(name="Testing Chronograph")

    cg.start("first section")
    time.sleep(0.5)
    cg.stop()

    cg.start("second section")
    time.sleep(0.25)
    cg.stop()


You can then print the output like this:

>>> print(cg.total_elapsed_time)
0.757287

>>> print(float(cg))
0.757287

>>> print(cg.last_split_time)
0.253046

>>> print(cg.report())
Report for Testing Chronograph
Split first section: 0.504241
Split second section: 0.253046
Total elapsed time: 0.757287

>>> print(cg.timing_data)
[{'start': datetime.datetime(2016, 2, 8, 20, 12, 38, 170123), 'stop': datetime.datetime(2016, 2, 8, 20, 12, 38, 674364), 'label': 'first section'}, {'start': datetime.datetime(2016, 2, 8, 20, 12, 38, 674395), 'stop': datetime.datetime(2016, 2, 8, 20, 12, 38, 927441), 'label': 'second section'}]

Example 2: Using splits
-----------------------

The stop/start functionality of the code above can be condensed by using split()::

    import time
    from chronograph.chronograph import Chronograph

    cg = Chronograph(name="Testing Chronograph")

    cg.start("first section")
    time.sleep(0.5)

    cg.split("second section")
    time.sleep(0.25)
    cg.stop()

*(see Example 1 for printing the output)*

Example 3: Starting timing quickly
----------------------------------

It is easy start timing quickly, for example::

    import time
    from chronograph.chronograph import Chronograph

    cg = Chronograph(start_timing=True)
    time.sleep(0.5)
    cg.stop()

*(see Example 1 for printing the output)*

Example 4: Controlling verbosity
--------------------------------

You can make the Chronograph verbose, e.g.::

    import time
    from chronograph.chronograph import Chronograph

    cg = Chronograph(verbosity=2, start_timing=True)
    time.sleep(0.5)
    cg.stop()

*(see Example 1 for printing the output)*

During timing, this option will print out something like::

    Chronograph: Split (1) started at: 2016-02-08 20:22:39.246814
    Chronograph: stopped at: 2016-02-08 20:22:39.246814
    Chronograph: Total elapsed time: 0.50099 s. Last split (1) time: 0.50099 s.

Example 5: Integrating with a logger
------------------------------------

It is easy to integrate the Chronograph with a logger::

    import logging
    import time
    from chronograph.chronograph import Chronograph

    # set up logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # anything debug and above passes through to the handler level
    fh = logging.FileHandler("chronograph.log", "a")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # start chronograph
    cg = Chronograph(verbosity=2, logger=logger, log_lvl="INFO", start_timing=True)
    time.sleep(0.5)
    cg.stop()

    cg.report(printout=True)

Example 6: Multiple chronographs with global scope
--------------------------------------------------

Need to manage multiple Chronographs across multiple files and functions? You can use the ``get_chronograph()`` function to get a global Chronograph that can be accessed anywhere::

    import time
    from chronograph.chronograph import get_chronograph


    def func1():
        cg = get_chronograph("my first chronograph")
        cg.start()
        time.sleep(0.5)
        cg.stop()


    def func2():
        cg = get_chronograph("my second chronograph")
        cg.start()
        time.sleep(0.25)
        cg.stop()

    if __name__ == "__main__":
        cg1 = get_chronograph("my first chronograph", start_timing=True)
        time.sleep(0.75)
        cg1.stop()
        func1()
        func2()
        cg1.report(printout=True)

        cg2 = get_chronograph("my second chronograph")
        cg2.report(printout=True)

The first time you call ``get_chronograph()``, it will be created and stored for future use. Note that you can set the initialization parameters for a Chronograph only on the first time that you call ``get_chronograph()``.

Example 7: Using the with() clause
----------------------------------

You can make the syntax of a Chronograph slightly more compact by using the ``with()`` clause::

    from chronograph.chronograph import get_chronograph

    with get_chronograph("hello") as f:
            import time
            time.sleep(1)

    print get_chronograph("hello").total_elapsed_time

Example 8: Throwing exceptions
------------------------------

Need to enforce correct usage? You can optionally throw exceptions::

    from chronograph.chronograph import Chronograph

    cg = Chronograph(name="TestCase", throw_exceptions=True)

    cg.start()
    cg.start()  # can't start a Chronograph that's already started!

Since the ``throw_exceptions`` parameter was set to True, this will throw the exception: ``chronograph.chronograph.ChronographError: TestCase: Warning: Cannot start Chronograph while in current state! Stop or reset chronograph before starting.``

Example 9: Function decorators
------------------------------

If you decorate a function with the ``add_chronograph`` decorator, it will automatically time a split every time that function is called. By default, the name of the Chronograph will be the function name, but you can set any Chronograph initialization parameters (such as name) that you desire::

    import time
    from chronograph.chronograph import add_chronograph, get_chronograph


    @add_chronograph()
    def func1():
        time.sleep(0.5)

    @add_chronograph(name="my func2 timer")
    def func2():
        time.sleep(0.25)


    if __name__ == "__main__":

        func1()
        func1()
        func1()
        func2()


        cg1 = get_chronograph("func1")
        cg1.report(printout=True)

        print("")

        cg2 = get_chronograph("my func2 timer")
        cg2.report(printout=True)

Example 10: JSON output and accessing split data
------------------------------------------------

The following code demonstrates how to access the split data as well as how to serialize and deserialize to JSON::

    import json
    import time
    from bson import json_util
    from chronograph.chronograph import Chronograph, get_split_time

    if __name__ == "__main__":

        cg = Chronograph(start_timing=True)
        time.sleep(0.25)
        cg.split()
        time.sleep(0.75)
        cg.stop()

        # JSON compatible data
        print json.dumps(cg.timing_data, default=json_util.default)

        # Iterate through timing data and get all splits
        for t in cg.timing_data:
            print get_split_time(t)

