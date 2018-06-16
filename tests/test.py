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
    import xprops
    import xconf
else:
    import touchpadtuner2 as tgt
    import xprops
    import xconf


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

        # change it.
        xi.fDryrun = False
        rnd = (seq[0] + 1) % 3 + 1  # make 1 -> 3
        tmp = [rnd, seq[1], seq[2]]
        xi.clks(0, tmp)
        res = xi.clks(0)
        assert res == rnd, "{} != {} ?can't set?".format(res, rnd)

        xi.fDryrun = True
        rnd = (rnd + 1) % 3 + 1  # make 1 -> 3
        tmp = [rnd, seq[1], seq[2]]
        xi.clks(0, tmp)
        res = xi.clks(0)
        assert res != rnd, "{} == {} ?dry run enabled??".format(res, rnd)

        xi.fDryrun = False
        xi.clks(0, seq)  # restore.
        res = xi.clks(0)
        assert res != rnd, "{} == {} ?can't set?".format(res, rnd)

    def test_read(self):  # {{{1
        # type: () -> None
        xconf.XConfFile().read(u"tests/70-synaptics.conf")

    def test_save_0_not_override(self):  # {{{1
        # type: () -> None
        fname = u"tests/70-synaptics.conf"
        fnameOut = u"build/70-synaptics.conf.through0"
        xf = xconf.XConfFile()
        db = xf.read(fname)
        xf.save(fnameOut, fname, db)
        res = subprocess.check_output(["/usr/bin/diff", fname, fnameOut])
        _res = res.decode("utf-8")
        _res = _res.strip()
        assert _res == "", "must be same: {}".format(res)

    def test_save_11_override_fingerlow(self):  # {{{1
        # type: () -> None
        fname = u"tests/70-synaptics.conf"
        fnameOut = u"build/70-synaptics.conf.through11"
        xf = xconf.XConfFile()
        db = xf.read(fname)
        db[tgt.NProp.finger].vals = [10, 100, 20]
        xf.save(fnameOut, fname, db)
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
        xf = xconf.XConfFile()
        db = xf.read(fname)
        db[tgt.NProp.finger].vals = [50, 200, 20]
        xf.save(fnameOut, fname, db)
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
        xf = xconf.XConfFile()
        db = xf.read(fname)
        db[tgt.NProp.tap_action].vals = [0, 0, 0, 0, 1, 3, 2]
        xf.save(fnameOut, fname, db)
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
