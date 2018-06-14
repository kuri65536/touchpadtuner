#! env python3
'''License: Modified BSD, see touchpadtuner.py'''
import sys
import os
import unittest
import subprocess

sys.path.append(os.path.realpath(os.path.join(
                os.path.dirname(__file__), "..")))

if sys.version_info[0] == 2:
    import touchpadtuner2 as tgt
else:
    import touchpadtuner2 as tgt


class cfg:
    fDryrun = False


class Test(unittest.TestCase):
    def setUp(self):  # {{{1
        # type: () -> None
        tgt.opts = tgt.options()

    def test_options(self):  # {{{1
        # type: () -> None
        tgt.options()

    def test_props(self):  # {{{1
        # type: () -> None
        tgt.XInputDB.createpropsdb()
        # print(tgt.XInputDB.propsdb)

    def test_click(self):  # {{{1
        # type: () -> None
        xi = tgt.XInputDB()
        seq = [xi.clks(0), xi.clks(1), xi.clks(2)]
        if cfg.fDryrun:
            return
        xi.fDryrun = False
        tmp = [5, seq[1], seq[2]]
        xi.clks(0, tmp)
        res = [xi.clks(0), xi.clks(1), xi.clks(2)]
        xi.clks(0, seq)  # restore.
        xi.fDryrun = True
        assert seq[0] != res[0]

    def test_read(self):  # {{{1
        # type: () -> None
        tgt.XInputDB.read(u"tests/70-synaptics.conf")

    def test_save_0_not_override(self):  # {{{1
        # type: () -> None
        fname = u"tests/70-synaptics.conf"
        fnameOut = u"build/70-synaptics.conf.through0"
        db = tgt.XInputDB.read(fname)
        tgt.XInputDB.save(fnameOut, fname, db)
        res = subprocess.check_output(["/usr/bin/diff", fname, fnameOut])
        _res = res.decode("utf-8")
        _res = _res.strip()
        assert _res == "", "must be same: {}".format(res)

    def test_save_11_override_fingerlow(self):  # {{{1
        # type: () -> None
        fname = u"tests/70-synaptics.conf"
        fnameOut = u"build/70-synaptics.conf.through11"
        db = tgt.XInputDB.read(fname)
        db[tgt.NProp.finger].vals = [10, 100, 20]
        tgt.XInputDB.save(fnameOut, fname, db)
        try:
            res = subprocess.check_output(["/usr/bin/diff", fname, fnameOut])
            self.fail()  # 0 == no change was detected
        except subprocess.CalledProcessError as ex:
            res = ex.output
        assert res != ""  # TODO(Shimoda): check more actual.

    def test_save_12_override_fingerhigh(self):  # {{{1
        # type: () -> None
        fname = u"tests/70-synaptics.conf"
        fnameOut = u"build/70-synaptics.conf.through12"
        db = tgt.XInputDB.read(fname)
        db[tgt.NProp.finger].vals = [50, 200, 20]
        tgt.XInputDB.save(fnameOut, fname, db)
        try:
            res = subprocess.check_output(["/usr/bin/diff", fname, fnameOut])
            self.fail()  # 0 == no change was detected
        except subprocess.CalledProcessError as ex:
            res = ex.output
        assert res != ""  # TODO(Shimoda): check more actual.

    def test_save_21_override_clickfinger1(self):  # {{{1
        # type: () -> None
        fname = u"tests/70-synaptics.conf"
        fnameOut = u"build/70-synaptics.conf.through21"
        db = tgt.XInputDB.read(fname)
        db[tgt.NProp.tap_action].vals = [0, 0, 0, 0, 1, 3, 2]
        tgt.XInputDB.save(fnameOut, fname, db)
        try:
            res = subprocess.check_output(["/usr/bin/diff", fname, fnameOut])
            self.fail()  # 0 == no change was detected
        except subprocess.CalledProcessError as ex:
            res = ex.output
        assert res != ""  # TODO(Shimoda): check more actual.


if __name__ == "__main__":
    import os
    try:
        os.mkdir("build")
    except:
        pass
    unittest.main()

# vi: ft=python:
