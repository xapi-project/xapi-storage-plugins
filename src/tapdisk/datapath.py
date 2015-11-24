#!/usr/bin/env python

import urlparse
import os
import sys
import xapi
import xapi.storage.api.datapath
import xapi.storage.api.volume
from xapi.storage.datapath import tapdisk, image
from xapi.storage import log
import pickle

TD_PROC_METADATA_DIR = "/var/run/nonpersistent/dp-tapdisk"
TD_PROC_METADATA_FILE = "meta.pickle"


class Implementation(xapi.storage.api.datapath.Datapath_skeleton):

    def activate(self, dbg, uri, domain):
        u = urlparse.urlparse(uri)
        # XXX need some datapath-specific errors below
        if not(os.path.exists(u.path)):
            raise xapi.storage.api.volume.Volume_does_not_exist(u.path)
        if u.scheme[:3] == "vhd":
            img = image.Vhd(u.path)
        elif u.scheme[:3] == "raw":
            img = image.Raw(u.path)
        else:
            raise
        tap = self.load_tapdisk(dbg, uri)
        tap.open(dbg, img)
        self.save_tapdisk(dbg, uri, tap)

    def attach(self, dbg, uri, domain):
        tap = tapdisk.create(dbg)
        self.save_tapdisk(dbg, uri, tap)
        return {
            'domain_uuid': '0',
            'implementation': ['Tapdisk3', tap.block_device()],
        }

    def close(self, dbg, uri):
        u = urlparse.urlparse(uri)
        # XXX need some datapath-specific errors below
        if not(os.path.exists(u.path)):
            raise xapi.storage.api.volume.Volume_does_not_exist(u.path)
        return None

    def detach(self, dbg, uri, domain):
        tap = self.load_tapdisk(dbg, uri)
        tap.destroy(dbg)
        self.forget_tapdisk(dbg, uri)

    def deactivate(self, dbg, uri, domain):
        tap = self.load_tapdisk(dbg, uri)
        tap.close(dbg)

    def open(self, dbg, uri, persistent):
        u = urlparse.urlparse(uri)
        # XXX need some datapath-specific errors below
        if not(os.path.exists(u.path)):
            raise xapi.storage.api.volume.Volume_does_not_exist(u.path)
        return None

    def _metadata_dir(self, uri):
        return TD_PROC_METADATA_DIR + "/" + uri

    def save_tapdisk(self, dbg, uri, tap):
        """ Record the tapdisk metadata for this URI in host-local storage """
        dirname = self._metadata_dir(uri)
        try:
            os.makedirs(dirname, mode=0755)
        except OSError as e:
            if e.errno != 17:  # 17 == EEXIST, which is harmless
                raise e
        with open(dirname + "/" + TD_PROC_METADATA_FILE, "w") as fd:
            pickle.dump(tap.__dict__, fd)

    def load_tapdisk(self, dbg, uri):
        """Recover the tapdisk metadata for this URI from host-local
           storage."""
        dirname = self._metadata_dir(uri)
        if not(os.path.exists(dirname)):
            # XXX throw a better exception
            raise xapi.storage.api.volume.Volume_does_not_exist(dirname)
        with open(dirname + "/" + TD_PROC_METADATA_FILE, "r") as fd:
            meta = pickle.load(fd)
            tap = tapdisk.Tapdisk(meta['minor'], meta['pid'], meta['f'])
            tap.secondary = meta['secondary']
            return tap

    def forget_tapdisk(self, dbg, uri):
        """Delete the tapdisk metadata for this URI from host-local storage."""
        dirname = self._metadata_dir(uri)
        try:
            os.unlink(dirname + "/" + TD_PROC_METADATA_FILE)
        except:
            pass

if __name__ == "__main__":
    log.log_call_argv()
    cmd = xapi.storage.api.datapath.Datapath_commandline(Implementation())
    base = os.path.basename(sys.argv[0])
    if base == "Datapath.activate":
        cmd.activate()
    elif base == "Datapath.attach":
        cmd.attach()
    elif base == "Datapath.close":
        cmd.close()
    elif base == "Datapath.deactivate":
        cmd.deactivate()
    elif base == "Datapath.detach":
        cmd.detach()
    elif base == "Datapath.open":
        cmd.open()
    else:
        raise xapi.storage.api.datapath.Unimplemented(base)
