# -*- coding: utf-8 -*-

import psutil

__all__ = (
    'get_system_info',
)


def get_system_info():

    def get_memory_data(memory):
        to_mb = lambda b: b / 1024 / 1024

        return {
            'percent': memory.percent,
            'total': to_mb(memory.total),
            'used': to_mb(memory.used),
        }

    def get_cpu_data():
        cpu_data = []
        for cpu_num, perc in enumerate(psutil.cpu_percent(interval=0, percpu=True)):
            cpu_data.append((cpu_num, perc))
        return cpu_data

    return {
        'virtual_memory': get_memory_data(psutil.virtual_memory()),
        'swap_memory': get_memory_data(psutil.swap_memory()),
        'cpu': get_cpu_data(),
    }
