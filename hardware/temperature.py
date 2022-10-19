import clr


class Temperature(object):
    _gpu = None
    _temperature_sensor = None

    def __init__(self):
        clr.AddReference("hardware/resources/OpenHardwareMonitorLib")

        from OpenHardwareMonitor import Hardware

        computer = Hardware.Computer()
        computer.GPUEnabled = True
        computer.Open()
        gpu_list = computer.Hardware
        if len(gpu_list) == 0:
            raise Exception("No GPU Hardware found")
        self._gpu = gpu_list[0]
        print(f"GPU Hardware found: {self._gpu.Name}")
        for sensor in self._gpu.Sensors:
            if sensor.SensorType == 2:  # temperature
                self._temperature_sensor = sensor
        if self._temperature_sensor is None:
            raise Exception("No GPU temperature sensor found")

    def fetch_temperature(self):
        self._gpu.Update()
        return int(self._temperature_sensor.Value)
