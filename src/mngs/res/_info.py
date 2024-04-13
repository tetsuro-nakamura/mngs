#!./env/bin/python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-04-13 18:05:08"
# Author: Yusuke Watanabe (ywata1989@gmail.com)

"""
This script provides detailed system information including system basics, boot time, CPU, memory, disk, network, and custom user environment variables.
"""

import platform as _platform
import sys
from datetime import datetime as _datetime
from pprint import pprint

import matplotlib.pyplot as plt
import psutil as _psutil
import yaml as _yaml


def info(
    system=True,
    boot_time=True,
    cpu=True,
    gpu=True,
    disk=True,
    network=True,
    verbose=False,
    yaml=False,
):
    import mngs

    # To prevent import errors, _SUPPLE_INFO is collected here.
    global _SUPPLE_INFO
    _SUPPLE_INFO = mngs.res._utils.get_env_info()._asdict()

    collected_info = {}  # OrderedDict()

    collected_info["Collected Time"] = _datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    if system:
        collected_info["System Information"] = _system_info()
    # if boot_time:
    #     collected_info["Boot Time"] = _boot_time_info()
    if cpu:
        collected_info["CPU Info"] = _cpu_info()
        collected_info["Memory Info"] = _memory_info()
    if gpu:
        collected_info["GPU Info"] = _supple_nvidia_info()
        # mngs.gen.placeholder()
    if disk:
        collected_info["Disk Info"] = _disk_info()
    if network:
        collected_info["Network Info"] = _network_info()

    if yaml:
        collected_info = _yaml.dump(collected_info, sort_keys=False)

    if verbose:
        pprint(collected_info)

    return collected_info


def _system_info():
    uname = _platform.uname()
    return {
        "OS": _supple_os_info()["os"],
        # "GCC version": _supple_os_info()["gcc_version"],
        # "System": uname.system,
        "Node Name": uname.node,
        "Release": uname.release,
        "Version": uname.version,
        # "Machine": uname.machine,
        # "Processor": uname.processor,
    }


# def _boot_time_info():
#     boot_time_timestamp = _psutil.boot_time()
#     bt = _datetime.fromtimestamp(boot_time_timestamp)
#     return {
#         "Boot Time": f"{bt.year}-{bt.month:02d}-{bt.day:02d} {bt.hour:02d}:{bt.minute:02d}:{bt.second:02d}"
#     }


def _cpu_info():
    cpufreq = _psutil.cpu_freq()
    cpu_usage_per_core = _psutil.cpu_percent(percpu=True, interval=1)
    return {
        "Physical cores": _psutil.cpu_count(logical=False),
        "Total cores": _psutil.cpu_count(logical=True),
        "Max Frequency": f"{cpufreq.max:.2f} MHz",
        "Min Frequency": f"{cpufreq.min:.2f} MHz",
        "Current Frequency": f"{cpufreq.current:.2f} MHz",
        "CPU Usage Per Core": {
            f"Core {i}": f"{percentage}%"
            for i, percentage in enumerate(cpu_usage_per_core)
        },
        "Total CPU Usage": f"{_psutil.cpu_percent()}%",
    }


def _memory_info():
    import mngs

    svmem = _psutil.virtual_memory()
    swap = _psutil.swap_memory()

    return {
        "Memory": {
            "Total": mngs.gen.readable_bytes(svmem.total),
            "Available": mngs.gen.readable_bytes(svmem.available),
            "Used": mngs.gen.readable_bytes(svmem.used),
            "Percentage": svmem.percent,
        },
        "SWAP": {
            "Total": mngs.gen.readable_bytes(swap.total),
            "Free": mngs.gen.readable_bytes(swap.free),
            "Used": mngs.gen.readable_bytes(swap.used),
            "Percentage": swap.percent,
        },
    }


def _disk_info():
    import mngs

    partitions_info = {}
    partitions = _psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = _psutil.disk_usage(partition.mountpoint)
            partitions_info[partition.device] = {
                "Mountpoint": partition.mountpoint,
                "File system type": partition.fstype,
                "Total Size": mngs.gen.readable_bytes(usage.total),
                "Used": mngs.gen.readable_bytes(usage.used),
                "Free": mngs.gen.readable_bytes(usage.free),
                "Percentage": usage.percent,
            }
        except PermissionError:
            continue

    disk_io = _psutil.disk_io_counters()
    return {
        "Partitions": partitions_info,
        "Total read": mngs.gen.readable_bytes(disk_io.read_bytes),
        "Total write": mngs.gen.readable_bytes(disk_io.write_bytes),
    }


def _network_info():
    import mngs

    if_addrs = _psutil.net_if_addrs()
    interfaces = {}
    for interface_name, interface_addresses in if_addrs.items():
        interface_info = []
        for address in interface_addresses:
            interface_info.append(
                {
                    # "Address Type": "IP" if address.family == _psutil.AF_INET else "MAC",
                    "Address": address.address,
                    "Netmask": address.netmask,
                    "Broadcast": address.broadcast,
                }
            )
        interfaces[interface_name] = interface_info

    net_io = _psutil.net_io_counters()
    return {
        "Interfaces": interfaces,
        "Total Sent": mngs.gen.readable_bytes(net_io.bytes_sent),
        "Total Received": mngs.gen.readable_bytes(net_io.bytes_recv),
    }


def _python_info():
    return _supple_python_info()


def _supple_os_info():
    _SUPPLE_OS_KEYS = [
        "os",
        "gcc_version",
    ]
    return {k: _SUPPLE_INFO[k] for k in _SUPPLE_OS_KEYS}


def _supple_python_info():
    _SUPPLE_PYTHON_KEYS = [
        "python_version",
        "torch_version",
        "is_cuda_available",
        "pip_version",
        "pip_packages",
        "conda_packages",
    ]

    return {k: _SUPPLE_INFO[k] for k in _SUPPLE_PYTHON_KEYS}


def _supple_nvidia_info():
    _SUPPLE_NVIDIA_KEYS = [
        "nvidia_gpu_models",
        "nvidia_driver_version",
        "cuda_runtime_version",
        "cudnn_version",
    ]

    def replace_key(key):
        return key

    def replace_key(key):
        key = key.replace("_", " ")
        key = key.replace("nvidia", "NVIDIA")
        key = key.replace("gpu", "GPU")
        key = key.replace("cuda", "CUDA")
        key = key.replace("cudnn", "cuDNN")
        key = key.replace("driver", "Driver")
        key = key.replace("runtime", "Runtime")
        return key

    return {replace_key(k): _SUPPLE_INFO[k] for k in _SUPPLE_NVIDIA_KEYS}


if __name__ == "__main__":
    import mngs

    # Start
    CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(sys, plt)

    information = mngs.res.info()
    mngs.io.save(information, "info.yaml")

    # Close
    mngs.gen.close(CONFIG)

# EOF

"""
/home/ywatanabe/proj/entrance/mngs/res/_info.py
"""
