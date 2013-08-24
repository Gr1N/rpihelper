# -*- coding: utf-8 -*-

from collections import Counter
from datetime import datetime

import psutil

__all__ = (
    'get_boot_time',
    'get_memory_data',
    'get_cpu_data',
    'get_disk_data',
    'get_processes_data',
    'get_system_info',
)


def get_boot_time():
    timestamp = psutil.get_boot_time()
    days = (datetime.utcnow() - datetime.utcfromtimestamp(timestamp)).days

    return {
        'timestamp': timestamp,
        'days': days,
    }


def get_memory_data(memory):
    to_mb = lambda b: b / 1024 / 1024

    return {
        'percent': memory.percent,
        'total': to_mb(memory.total),
        'used': to_mb(memory.used),
    }


def get_cpu_data():
    cpu_data = []
    for perc in psutil.cpu_percent(interval=0, percpu=True):
        cpu_data.append(perc)
    return cpu_data


def get_disk_data():
    to_gb = lambda b: b / 1024 / 1024 / 1024

    disk_data = []
    for p in psutil.disk_partitions():
        disk_usage = psutil.disk_usage(p.mountpoint)
        disk_data.append({
            'mountpoint': p.mountpoint,
            'percent': disk_usage.percent,
            'total': to_gb(disk_usage.total),
            'used': to_gb(disk_usage.used),
        })
    return disk_data


def get_processes_data():
    processes = []
    processes_status = Counter()
    for p in psutil.process_iter():
        try:
            p_dict = p.as_dict([
                'username', 'get_nice', 'get_memory_info', 'get_memory_percent',
                'get_cpu_percent', 'get_cpu_times', 'name', 'status', 'pid',
            ])

            processes_status[str(p_dict['status'])] += 1
        except psutil.NoSuchProcess:
            pass
        else:
            processes.append({
                k: (dict(v.__dict__) if isinstance(v, (
                    psutil._common.nt_meminfo,
                    psutil._common.nt_cputimes,
                )) else (str(v) if isinstance(v, (
                    psutil._common.constant,
                )) else v )) for k, v in p_dict.items()
            })

    # return processes sorted by CPU percent usage
    try:
        processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
    except TypeError:
        pass

    return processes, dict(processes_status)


def get_system_info():
    return {
        'boot_time': get_boot_time(),
        'virtual_memory': get_memory_data(psutil.virtual_memory()),
        'swap_memory': get_memory_data(psutil.swap_memory()),
        'cpu': get_cpu_data(),
        'disks': get_disk_data(),
        'processes': get_processes_data(),
    }
