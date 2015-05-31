import tempfile
import os
from rambutan3 import ROpSysUtil
from rambutan3.op_sys.RFileAccessEnum import RFileAccessEnum


def test_access():
    core_test_access(effective_ids=True)
    core_test_access(effective_ids=False)


def core_test_access(*, effective_ids: bool):
    temp_file = tempfile.NamedTemporaryFile()

    # Prove a regular file works with normal privs.
    os.chmod(temp_file.name, 0o644)
    assert ROpSysUtil.access(temp_file.name, RFileAccessEnum.READ,
                             effective_ids=effective_ids)
    assert ROpSysUtil.access(temp_file.name, RFileAccessEnum.WRITE,
                             effective_ids=effective_ids)
    assert not ROpSysUtil.access(temp_file.name, RFileAccessEnum.EXECUTE,
                                 effective_ids=effective_ids)
    assert ROpSysUtil.access(temp_file.name, (RFileAccessEnum.READ, RFileAccessEnum.WRITE),
                             effective_ids=effective_ids)
    assert not ROpSysUtil.access(temp_file.name, (RFileAccessEnum.READ, RFileAccessEnum.WRITE, RFileAccessEnum.EXECUTE),
                                 effective_ids=effective_ids)

    # Prove a regular file works with zero privs.
    os.chmod(temp_file.name, 0o000)
    assert not ROpSysUtil.access(temp_file.name, RFileAccessEnum.READ,
                                 effective_ids=effective_ids)
    assert not ROpSysUtil.access(temp_file.name, RFileAccessEnum.WRITE,
                                 effective_ids=effective_ids)
    assert not ROpSysUtil.access(temp_file.name, RFileAccessEnum.EXECUTE,
                                 effective_ids=effective_ids)
    assert not ROpSysUtil.access(temp_file.name, (RFileAccessEnum.READ, RFileAccessEnum.WRITE),
                                 effective_ids=effective_ids)
    assert not ROpSysUtil.access(temp_file.name, (RFileAccessEnum.READ, RFileAccessEnum.WRITE, RFileAccessEnum.EXECUTE),
                                 effective_ids=effective_ids)

    temp_file2 = tempfile.NamedTemporaryFile()
    temp_file2.close()
    link_path = temp_file2.name
    os.symlink(temp_file.name, link_path)
    try:
        # Prove a symlink to regular file works with normal privs.
        os.chmod(temp_file.name, 0o644)
        assert ROpSysUtil.access(link_path, RFileAccessEnum.READ,
                                 effective_ids=effective_ids)
        assert ROpSysUtil.access(link_path, RFileAccessEnum.WRITE,
                                 effective_ids=effective_ids)
        assert not ROpSysUtil.access(link_path, RFileAccessEnum.EXECUTE,
                                     effective_ids=effective_ids)
        assert ROpSysUtil.access(link_path, (RFileAccessEnum.READ, RFileAccessEnum.WRITE),
                                 effective_ids=effective_ids)
        assert not ROpSysUtil.access(link_path, (RFileAccessEnum.READ, RFileAccessEnum.WRITE, RFileAccessEnum.EXECUTE),
                                     effective_ids=effective_ids)

        # Prove a symlink to regular file works with zero privs.
        os.chmod(temp_file.name, 0o000)
        assert not ROpSysUtil.access(link_path, RFileAccessEnum.READ,
                                     effective_ids=effective_ids)
        assert not ROpSysUtil.access(link_path, RFileAccessEnum.WRITE,
                                     effective_ids=effective_ids)
        assert not ROpSysUtil.access(link_path, RFileAccessEnum.EXECUTE,
                                     effective_ids=effective_ids)
        assert not ROpSysUtil.access(link_path, (RFileAccessEnum.READ, RFileAccessEnum.WRITE),
                                     effective_ids=effective_ids)
        assert not ROpSysUtil.access(link_path, (RFileAccessEnum.READ, RFileAccessEnum.WRITE, RFileAccessEnum.EXECUTE),
                                     effective_ids=effective_ids)

    finally:
        os.remove(link_path)
