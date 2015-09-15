#!/usr/bin/env python

import sys
import os

import xapi
import xapi.storage.api.datapath
from xapi.storage import log

import argparse, json, urlparse

class Implementation(xapi.storage.api.datapath.Datapath_skeleton):
    def attach(self, dbg, uri, domain):
        u = urlparse.urlparse(uri)
        return {
            'domain_uuid': '0',
            'implementation': [ 'Blkback', u.path ],
        }
    def dctivate(self, dbg, uri, domain):
        return
    def detach(self, dbg, uri, domain):
        return
    def deactivate(self, dbg, uri, domain):
        return

if __name__ == "__main__":
    log.log_call_argv()
    cmd = xapi.storage.api.datapath.Datapath_commandline(Implementation())
    base = os.path.basename(sys.argv[0])
    if base == "Datapath.activate":
        cmd.activate()
    elif base == "Datapath.attach":
        cmd.attach()
    elif base == "Datapath.detach":
        cmd.detach()
    elif base == "Datapath.deactivate":
        cmd.deactivate()
    else:
        raise xapi.storage.api.datapath.Unimplemented(base)
