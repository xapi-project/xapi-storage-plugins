#!/usr/bin/env python

import urlparse
import os
import sys
import xapi
import xapi.storage.api.datapath
import xapi.storage.api.volume
from xapi.storage.datapath import tapdisk, image
from xapi.storage import log


class Implementation(xapi.storage.api.datapath.Datapath_skeleton):

    def activate(self, dbg, uri, domain):
        return

    def attach(self, dbg, uri, domain):
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
        tap = tapdisk.create(dbg)
        tap.open(dbg, img)
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

    def deactivate(self, dbg, uri, domain):
        return

    def detach(self, dbg, uri, domain):
        u = urlparse.urlparse(uri)
        # XXX need a datapath-specific error
        if not(os.path.exists(u.path)):
            raise xapi.storage.api.volume.Volume_does_not_exist(u.path)
        tap = tapdisk.find_by_file(dbg, image.Path(u.path))
        tap.close(dbg)
        tap.destroy(dbg)

    def open(self, dbg, uri, persistent):
        u = urlparse.urlparse(uri)
        # XXX need some datapath-specific errors below
        if not(os.path.exists(u.path)):
            raise xapi.storage.api.volume.Volume_does_not_exist(u.path)
        return None

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
