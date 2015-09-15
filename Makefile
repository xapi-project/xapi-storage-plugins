LIB_FILES=__init__.py device.py iscsi.py losetup.py tapdisk.py dmsetup.py nbdclient.py nbdtool.py image.py

.PHONY: clean
clean:

DESTDIR?=/
SCRIPTDIR?=/usr/libexec/xapi-storage-script
PYTHONDIR?=/usr/lib/python2.7/site-packages/xapi/storage/datapath


install:
	mkdir -p $(DESTDIR)$(SCRIPTDIR)/datapath/loop+blkback
	(cd src/loop+blkback; install -m 0755 plugin.py datapath.py $(DESTDIR)$(SCRIPTDIR)/datapath/loop+blkback)
	(cd $(DESTDIR)$(SCRIPTDIR)/datapath/loop+blkback; for link in Datapath.attach Datapath.activate Datapath.deactivate Datapath.detach; do ln -s datapath.py $$link; done)
	(cd $(DESTDIR)$(SCRIPTDIR)/datapath/loop+blkback; for link in Plugin.Query; do ln -s plugin.py $$link; done)
	mkdir -p $(DESTDIR)$(SCRIPTDIR)/datapath/tapdisk
	(cd src/tapdisk; install -m 0755 plugin.py datapath.py $(DESTDIR)$(SCRIPTDIR)/datapath/tapdisk)
	(cd $(DESTDIR)$(SCRIPTDIR)/datapath/tapdisk; for link in Datapath.open Datapath.attach Datapath.activate Datapath.deactivate Datapath.detach Datapath.close; do ln -s datapath.py $$link; done)
	(cd $(DESTDIR)$(SCRIPTDIR)/datapath/tapdisk; for link in Plugin.Query; do ln -s plugin.py $$link; done)
	mkdir -p $(DESTDIR)$(SCRIPTDIR)/datapath/raw+block
	(cd src/raw+block; install -m 0755 plugin.py datapath.py $(DESTDIR)$(SCRIPTDIR)/datapath/raw+block)
	(cd $(DESTDIR)$(SCRIPTDIR)/datapath/raw+block; for link in Datapath.attach Datapath.activate Datapath.deactivate Datapath.detach; do ln -s datapath.py $$link; done)
	(cd $(DESTDIR)$(SCRIPTDIR)/datapath/raw+block; for link in Plugin.Query; do ln -s plugin.py $$link; done)
	(cd $(DESTDIR)$(SCRIPTDIR)/datapath ; ln -snf tapdisk raw+file ; ln -snf tapdisk vhd+file)
	mkdir -p $(DESTDIR)$(PYTHONDIR)
	(cd datapath; install -m 0755 $(LIB_FILES) $(DESTDIR)$(PYTHONDIR)/)
