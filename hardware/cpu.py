import clr

open_hardware_monitor_hwtypes = ['Mainboard', 'SuperIO', 'CPU', 'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster',
                                 'HDD']

open_hardware_monitor_sensor_types = ['Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level',
                                      'Factor', 'Power', 'Data', 'SmallData']


def initialize_open_hardware_monitor():
    clr.AddReference("resources/OpenHardwareMonitorLib")

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle


def fetch_stats(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor(sensor)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor)


def parse_sensor(sensor):
    if sensor.Value is not None:
        if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
            sensor_types = open_hardware_monitor_sensor_types
            hardware_types = open_hardware_monitor_hwtypes
        else:
            return

        if sensor.SensorType == sensor_types.index('Temperature'):
            print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (
                hardware_types[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name,
                sensor.Value))


if __name__ == "__main__":
    print("OpenHardwareMonitor:")
    HardwareHandle = initialize_open_hardware_monitor()
    fetch_stats(HardwareHandle)
