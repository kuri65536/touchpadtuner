#! env python3
'''License: Modified BSD, see touchpadtuner.py'''
import sys
import unittest
import subprocess

if sys.version_info[0] == 2:
    import touchpadtuner2 as tgt
else:
    import touchpadtuner2 as tgt


class Test(unittest.TestCase):
    def setUp(self):  # {{{1
        tgt.opts = tgt.options()

    def test_options(self):  # {{{1
        tgt.options()

    def test_props(self):  # {{{1
        tgt.XInputDB.createpropsdb()

    def test_read(self):  # {{{1
        tgt.XInputDB.read(u"70-synaptics.conf")

    def test_save_0_not_override(self):  # {{{1
        fname = u"70-synaptics.conf"
        fnameOut = u"70-synaptics.conf.through0"
        db = tgt.XInputDB.read(fname)
        db[-1] = fname
        tgt.XInputDB.save(fnameOut, db)
        res = subprocess.check_output(["/usr/bin/diff", fname, fnameOut])
        _res = res.decode("utf-8")
        _res = _res.strip()
        assert _res == "", "must be same: {}".format(res)

    def test_save_11_override_fingerlow(self):  # {{{1
        fname = u"70-synaptics.conf"
        fnameOut = u"70-synaptics.conf.through11"
        db = tgt.XInputDB.read(fname)
        db[-1] = fname
        db[tgt.NProp.finger].vals = [10, 100, 20]
        tgt.XInputDB.save(fnameOut, db)
        try:
            res = subprocess.check_output(["/usr/bin/diff", fname, fnameOut])
            Test.fail()  # 0 == no change was detected
        except subprocess.CalledProcessError as ex:
            res = ex.output
        assert res != ""  # TODO(Shimoda): check more actual.

    def test_save_12_override_fingerhigh(self):  # {{{1
        fname = u"70-synaptics.conf"
        fnameOut = u"70-synaptics.conf.through12"
        db = tgt.XInputDB.read(fname)
        db[-1] = fname
        db[tgt.NProp.finger].vals = [50, 200, 20]
        tgt.XInputDB.save(fnameOut, db)
        try:
            res = subprocess.check_output(["/usr/bin/diff", fname, fnameOut])
            Test.fail()  # 0 == no change was detected
        except subprocess.CalledProcessError as ex:
            res = ex.output
        assert res != ""  # TODO(Shimoda): check more actual.

    def test_save_21_override_clickfinger1(self):  # {{{1
        fname = u"70-synaptics.conf"
        fnameOut = u"70-synaptics.conf.through21"
        db = tgt.XInputDB.read(fname)
        db[-1] = fname
        db[tgt.NProp.tap_action].vals = [0, 0, 0, 0, 1, 3, 2]
        tgt.XInputDB.save(fnameOut, db)
        try:
            res = subprocess.check_output(["/usr/bin/diff", fname, fnameOut])
            self.fail()  # 0 == no change was detected
        except subprocess.CalledProcessError as ex:
            res = ex.output
        assert res != ""  # TODO(Shimoda): check more actual.


if __name__ == "__main__":
    unittest.main()

# vi: ft=python:
