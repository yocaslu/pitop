import platform
import psutil
from loguru import logger

WIFI_ADAPTER_NAME = 'wlp5s0'

class System():
    def __init__(self) -> None:
        self.system = None
        self.net    = None
        self.cpu    = None
        self.mem    = None
        self.disk   = None
        self.temp   = None

        pass

    def update(self):
        self.system = self._get_system_info()
        self.net    = self._get_net_info()
        self.cpu    = self._get_cpu_info()
        self.mem    = self._get_mem_info()
        self.disk   = self._get_disk_info()
        self.temp   = self._get_temp_info()


    def _get_net_info(self) -> dict[str, str] | None:
        host_ip = None
        mask = None

        try:
            net = psutil.net_if_addrs()
            if WIFI_ADAPTER_NAME in net:
                adapter = net[WIFI_ADAPTER_NAME]
                if adapter:
                    conn = adapter[0]
                    host_ip = conn.address
                    mask = conn.netmask
                else:
                    logger.error(f'adapter array is empty!')
            else:
                logger.error(f'{WIFI_ADAPTER_NAME} not in psutil.net_if_addrs()')

            return {'host_ip': host_ip, 'mask': mask}
        except Exception as e:
            logger.error(f'failed to get network info: {e}')

    def _get_system_info(self) -> dict[str, str] | None:
        try:
            sys = platform.system()
            aarch, _ = platform.architecture()
            machine = platform.machine()
            return {'system': sys, 'arch': aarch, 'machine': machine}
        except Exception as e:
            logger.error(f'failed to get system info: {e}')

    def _get_cpu_info(self) -> dict[str, list[float] | float] | None:
        try:
            processor = platform.processor()
            percent = psutil.cpu_percent(interval=1, percpu=True)
            freq = psutil.cpu_freq().current
            return {'processor': processor, 'use percent': percent, 'frequency': freq}
        except Exception as e:
            logger.error(f'failed to get cpu info: {e}')

    def _get_mem_info(self) -> dict[str, float] | None:
        try:
            mem = psutil.virtual_memory()
            total = mem.total / (1024 ** 3) # converting to gigabytes
            available = mem.available / (1024 ** 3)
            percent = (total - available) / total * 100
            return {'total': total, 'available': available, 'percent': percent}
        except Exception as e:
            logger.error(f'failed to get memory info: {e}')


    def _get_disk_info(self) -> list[dict[str,  str | dict[str, int | float]]] | None:
        try:
            disks = []
            devices = psutil.disk_partitions(all=False)
            for device in devices:
                usage = psutil.disk_usage(device.mountpoint)
                disks.append(
                   {
                       'device': device.device,
                       'mountpoint': device.mountpoint,
                       'usage': {'total' : usage.total, 'used' : usage.used, 'free' : usage.free},
                   }
                )
            return disks
        except Exception as e:
            logger.error(f'failed to get disk info: {e}')

    def _get_temp_info(self) -> dict[str, dict[str, str | float]] | None:
        try:
            temp = psutil.sensors_temperatures()
            values = {}
            for sensor_name, cores in temp.items():
                t = []
                if len(cores):
                    for i in cores:
                        t.append({'label': i.label, 'current': i.current, 'high': i.high, 'critical': i.critical}) # converting to tuple
                values[sensor_name] = t

            return values
        except Exception as e:
            logger.error(f'failed to get temp info: {e}')

    def to_dict(self):
        return {
            'system': self.system,
            'net'   : self.net,
            'cpu'   : self.cpu,
            'mem'   : self.mem,
            'disk'  : self.disk,
            'temp'  : self.temp,
        }

RASPBERRY_PY = System()
RASPBERRY_PY.update()