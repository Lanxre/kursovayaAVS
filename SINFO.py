import psutil
import platform
import cpuinfo
import wmi

import os



class SINFO:

    def __init__(self):
        # names
        self.__uname = platform.uname()

        # processor info
        self.__physicalCores = psutil.cpu_count(logical=False)
        self.__totalCores = psutil.cpu_count(logical=True)
        self.__cure = psutil.cpu_freq()
        self.__cpuPercent = psutil.cpu_percent()

        # disk info
        self.__partitions = psutil.disk_partitions()
        self.__disk_io = psutil.disk_io_counters()

        # memory info

        self.__svmem = psutil.virtual_memory()

        # gpu info

        self.__gpus = wmi.WMI().Win32_VideoController()[0]

        # board info

        self.__board = wmi.WMI().Win32_BaseBoard()[0]

        # usb info

        self.__usb = wmi.WMI().Win32_USBHub()


    @property
    def get_info(self):
        return [self.get_processor_info,
                self.get_disk_info,
                self.get_memory_info,
                self.get_gpu_info,
                self.get_board_info,
                self.get_usb_info
                ]

    @property
    def get_processor_info(self):
        processor = ['Процессор', cpuinfo.get_cpu_info()['brand_raw'], {
            'Физическия ядра:': self.__physicalCores,
            'Общее кол-во ядер:': self.__totalCores,
            'Макс. частота (МГц):': self.__cure.max,
            'Мин. частота (МГц):': self.__cure.min,
            'Текущая частота (МГц):': self.__cure.current,
            'Нагруженость процессора (%):': self.__cpuPercent}
                     ]
        return processor

    @property
    def get_disk_info(self):
        disk = ['Диск']
        for partition in self.__partitions:
            disk.append(partition.device)
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk.append({
                'Всего памяти:': SINFO.bytesToGb(partition_usage.total),
                'Использовано:': SINFO.bytesToGb(partition_usage.used),
                'Свободно:': SINFO.bytesToGb(partition_usage.free),
                'Испрользовано в %:': partition_usage.percent,
                'Считано:': SINFO.bytesToGb(self.__disk_io.read_bytes),
                'Записано:': SINFO.bytesToGb(self.__disk_io.write_bytes),
            })
        return disk

    @property
    def get_memory_info(self):
        memory = ['Память', os.popen('wmic memorychip get Manufacturer').read(), {
            'Всего (ГБ):': SINFO.bytesToGb(self.__svmem.total),
            'Доступно (ГБ):': SINFO.bytesToGb(self.__svmem.available),
            'Используется (ГБ):': SINFO.bytesToGb(self.__svmem.used),
            'Используется в (%):': SINFO.bytesToGb(self.__svmem.percent),
            'Частота в (МГц):': os.popen('wmic memorychip get Speed').read(),
            'Слоты: ': os.popen('wmic memorychip get DeviceLocator').read(),
            'Форм. фактор:': os.popen('wmic memorychip get formfactor').read(),
        }]
        return memory

    @property
    def get_gpu_info(self):
        gpu = ['Видеокарта', self.__gpus.Name, {
            'Видео процессор: ': self.__gpus.VideoProcessor,
            'Объем видео ОЗУ (ГБ): ': self.__gpus.VideoMemoryType,
            'Макс частота обновления(МГц): ': self.__gpus.MaxRefreshRate,
            'Мин частота обновления(МГц): ': self.__gpus.MinRefreshRate,
            ' ': self.__gpus.VideoModeDescription,

        }]
        return gpu

    @property
    def get_board_info(self):
        board = ['Системная плата', self.__board.Manufacturer, {
            'Чипсет:': self.__board.Product,
            'Назначение:': self.__board.Caption,
            'Серийный номер:': self.__board.SerialNumber
        }]
        return board


    @property
    def get_usb_info(self):
        usb = ['USB устройство']
        for usb_device in self.__usb:
            usb.append({
                'Name: ': usb_device.Name,
                'DeviceID: ': usb_device.DeviceID,
                'PNPDeviceID: ': usb_device.PNPDeviceID,
                'Description: ': usb_device.Description,

            })
        return usb

    @staticmethod
    def bytesToGb(value):
        return value // (1024. ** 3)
