TAPDISK_COMMANDS=Plugin.Query Datapath.activate Datapath.attach Datapath.deactivate Datapath.detach Datapath.open Datapath.close
LOOP_COMMANDS=Plugin.Query Datapath.activate  Datapath.attach  Datapath.deactivate  Datapath.detach
LIB_FILES=__init__.py device.py iscsi.py losetup.py tapdisk.py dmsetup.py nbdclient.py nbdtool.py image.py

.PHONY: clean
clean:

DESTDIR?=/
SCRIPTDIR?=/usr/libexec/xapi-storage-script
PYTHONDIR?=/usr/lib/python2.7/site-packages/xapi/storage/datapath

.PHONY: install
install:
	mkdir -p $(DESTDIR)$(SCRIPTDIR)/datapath/loop+blkback
	(cd src/loop+blkback; install -m 0755 $(LOOP_COMMANDS) $(DESTDIR)$(SCRIPTDIR)/datapath/loop+blkback)
	mkdir -p $(DESTDIR)$(SCRIPTDIR)/datapath/tapdisk
	(cd src/tapdisk; install -m 0755 $(TAPDISK_COMMANDS) $(DESTDIR)$(SCRIPTDIR)/datapath/tapdisk)
	(cd $(DESTDIR)$(SCRIPTDIR)/datapath ; ln -snf tapdisk raw+file ; ln -snf tapdisk vhd+file)
	mkdir -p $(DESTDIR)$(PYTHONDIR)
	(cd datapath; install -m 0755 $(LIB_FILES) $(DESTDIR)$(PYTHONDIR)/)
