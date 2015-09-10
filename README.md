# Plugins to manage xapi storage datapaths

These plugins dictate how a storage volumes (local files, local block
devices, iSCSI LUNs, Ceph RBD devices etc etc) should be mapped to
Virtual Machines running on Xen.

The [xapi storage interface](https://xapi-project.github.io/xapi-storage)
describes the concepts, features and APIs
in more detail.

Datapath plugins are named by URI schemes. The following schemes are defined:

- `raw+file`: the block data is in a local file (or block device) and
  is in raw format
- `vhd+file`: the block data is in a vhd-formatted local file (or block
  device)

Internally we have the following low-level implementations. These should not
be referenced directly by Volume plugins:

- `loop+blkback`: converts a file into a `/dev/loop` device using `losetup`
  and then connects the device to the VM with the `blkback` kernel driver.
- `tapdisk`: opens a file with `tapdisk` and then `tapdisk` serves the
  VM directly using the user-space grant-table and grant-mapping code.
