# -*- coding: utf-8 -*-

from collections import Counter
import re
from subprocess import getoutput

import psutil

__all__ = (
    'get_boot_time',
    'get_memory_data',
    'get_cpu_data',
    'get_disk_data',
    'get_processes_data',
    'get_temperature',
    'get_voltage',
    'get_system_info',
)


def get_boot_time():
    return psutil.get_boot_time()


def get_memory_data(memory):
    return {
        'percent': memory.percent,
        'total': memory.total,
        'used': memory.used,
    }


def get_cpu_data():
    cpu_data = []
    for perc in psutil.cpu_percent(interval=0, percpu=True):
        cpu_data.append(perc)
    return cpu_data


def get_disk_data():
    disk_data = []
    for p in psutil.disk_partitions():
        disk_usage = psutil.disk_usage(p.mountpoint)
        disk_data.append({
            'mountpoint': p.mountpoint,
            'percent': disk_usage.percent,
            'total': disk_usage.total,
            'used': disk_usage.used,
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
                )) else v ) for k, v in p_dict.items()
            })

    # return processes sorted by CPU percent usage
    try:
        processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
    except TypeError:
        pass

    return processes, dict(processes_status)


def get_vcgencmd(*commands):
    """
    Get information about onboard hardware sensors.
    """
    return getoutput('/opt/vc/bin/vcgencmd %s' % ' '.join(commands))


def get_temperature():
    """
    Temperatures sensors for the board itself are including as part of the
    `raspberrypi-firmware-tools` package.
    """
    output = get_vcgencmd('measure_temp')
    match = re.match(r'^temp\=([0-9.]+\'C)$', output)
    return match.group(1) if match else None


def get_voltage():
    """
    Voltage sensors for the board itself are including as part of the
    `raspberrypi-firmware-tools` package.
    """
    def voltage(sensor_id):
        output = get_vcgencmd('measure_volts', sensor_id)
        match = re.match(r'^volt\=([0-9.]+V)$', output)
        return match.group(1) if match else None

    return {
        'core': voltage('sdram_c'),
        'io': voltage('sdram_i'),
        'phy': voltage('sdram_p'),
    }


def get_system_info():
    return {
        'boot_time': get_boot_time(),
        'virtual_memory': get_memory_data(psutil.virtual_memory()),
        'swap_memory': get_memory_data(psutil.swap_memory()),
        'cpu': get_cpu_data(),
        'disks': get_disk_data(),
        'processes': get_processes_data(),
        'temperature': get_temperature(),
        'voltage': get_voltage(),
    }
