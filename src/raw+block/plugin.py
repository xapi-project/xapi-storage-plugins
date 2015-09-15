#!/usr/bin/env python

import os
import sys
import xapi
import xapi.storage.api.plugin
from xapi.storage import log


class Implementation(xapi.storage.api.plugin.Plugin_skeleton):

    def query(self, dbg):
        return {
            "plugin": "tapdisk",
            "name": "The raw blkback plugin",
            "description": ("This plugin is a no-op because blkback can"
                            "already talk to block devices directly."),
            "vendor": "Citrix",
            "copyright": "(C) 2015 Citrix Inc",
            "version": "3.0",
            "required_api_version": "3.0",
            "features": [
            ],
            "configuration": {},
            "required_cluster_stack": []}

if __name__ == "__main__":
    log.log_call_argv()
    cmd = xapi.storage.api.plugin.Plugin_commandline(Implementation())
    base = os.path.basename(sys.argv[0])
    if base == "Plugin.Query":
        cmd.query()
    else:
        raise xapi.storage.api.plugin.Unimplemented(base)
