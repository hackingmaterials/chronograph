import json
import unittest
import time

from chronograph.chronograph import Chronograph, get_split_time, get_chronograph, ChronographError, add_chronograph

__author__ = 'Anubhav Jain <ajain@lbl.gov>'


class ChronographTests(unittest.TestCase):

    def test_example1(self):
        cg = Chronograph(name="Testing Chronograph")

        cg.start("first section")
        time.sleep(0.5)
        cg.stop()

        cg.start("second section")
        time.sleep(0.25)
        cg.stop()

        self.assertAlmostEqual(cg.total_elapsed_time, 0.75, 1)
        self.assertAlmostEqual(float(cg), 0.75, 1)
        self.assertAlmostEqual(cg.last_split_time, 0.25, 1)
        for idx, t in enumerate(cg.timing_data):
            self.assertEqual(set(t.keys()), set(["start", "stop", "label"]))
            if idx == 0:
                self.assertEqual(t["label"], "first section")
                self.assertAlmostEqual(get_split_time(t), 0.5, 1)
            else:
                self.assertEqual(t["label"], "second section")
                self.assertAlmostEqual(get_split_time(t), 0.25, 1)

    def test_example2(self):
        cg = Chronograph(name="Testing Chronograph")

        cg.start("first section")
        time.sleep(0.5)

        cg.split("second section")
        time.sleep(0.25)
        cg.stop()

        self.assertAlmostEqual(cg.total_elapsed_time, 0.75, 1)

    def test_example3(self):
        cg = Chronograph(start_timing=True)
        time.sleep(0.5)
        cg.stop()
        self.assertAlmostEqual(cg.total_elapsed_time, 0.5, 1)

    def test_example4(self):
        pass

    def test_example5(self):
        pass

    def test_example6(self):
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

        cg1 = get_chronograph("my first chronograph", start_timing=True)
        time.sleep(0.75)
        cg1.stop()
        func1()
        func2()

        self.assertAlmostEqual(cg1.total_elapsed_time, 1.25, 1)

        cg2 = get_chronograph("my second chronograph")
        self.assertAlmostEqual(cg2.total_elapsed_time, 0.25, 1)

    def test_example7(self):
        with get_chronograph("hello") as f:
                import time
                time.sleep(1)

        self.assertAlmostEqual(get_chronograph("hello").total_elapsed_time, 1.0, 1)

    def test_example8(self):
        cg = Chronograph(name="TestCase", throw_exceptions=True)

        cg.start()
        self.assertRaises(ChronographError, cg.start)  # can't start a Chronograph that's already started!

    def test_example8b(self):
        cg = Chronograph(name="TestCase", throw_exceptions=False)

        cg.start()
        cg.start()  # shouldn't throw exception

        t1 = cg.total_elapsed_time
        c1 = get_split_time(cg.timing_data[0], allow_still_running=True)
        time.sleep(0.1)
        t2 = cg.total_elapsed_time
        c2 = get_split_time(cg.timing_data[0], allow_still_running=True)
        self.assertGreater(t2, t1)
        self.assertGreater(c2, c1)

        cg.stop()

    def test_example9(self):
        @add_chronograph()
        def func1():
            time.sleep(0.5)

        @add_chronograph(name="my func2 timer")
        def func2():
            time.sleep(0.25)


        func1()
        func1()
        func1()
        func2()

        cg1 = get_chronograph("func1")
        self.assertAlmostEqual(cg1.total_elapsed_time, 1.5, 1)
        self.assertEqual(len(cg1.timing_data), 3)

        cg2 = get_chronograph("my func2 timer")
        self.assertAlmostEqual(cg2.total_elapsed_time, 0.25, 1)

    def test_example10(self):
        try:
            from bson import json_util
        except:
            raise unittest.SkipTest("bson package not installed")
        cg = Chronograph(start_timing=True)
        time.sleep(0.25)
        cg.split("s2")
        time.sleep(0.75)
        cg.stop()

        # JSON compatible data
        json_format = json.dumps(cg.timing_data, default=json_util.default)
        timing_data = json.loads(json_format, object_hook=json_util.object_hook)
        # Iterate through timing data and get all splits

        self.assertAlmostEqual(get_split_time(timing_data[0]), 0.25, 1)
        self.assertAlmostEqual(get_split_time(timing_data[1]), 0.75, 1)
        self.assertEqual(timing_data[0]["label"], "1")
        self.assertEqual(timing_data[1]["label"], "s2")