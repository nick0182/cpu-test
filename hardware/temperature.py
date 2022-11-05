import clr


class Temperature(object):

    def __init__(self):
        clr.AddReference("hardware/resources/OpenHardwareMonitorLib")

        from OpenHardwareMonitor import Hardware

        computer = Hardware.Computer()
        computer.CPUEnabled = True
        computer.Open()
        gpu_list = computer.Hardware
        if len(gpu_list) == 0:
            raise Exception("No CPU Hardware found")
        self._cpu = gpu_list[0]
        print(f"CPU Hardware found: {self._cpu.Name}")
        self._temperature_sensor = None

    def fetch_temperature(self):
        self._cpu.Update()
        if self._temperature_sensor is None:
            self._resolve_temperature_sensor()
        return int(self._temperature_sensor.Value)

    def _resolve_temperature_sensor(self):
        for sensor in self._cpu.Sensors:
            if sensor.SensorType == 2:  # temperature
                print(f"got cpu temperature sensor: {sensor.Name}")
                self._temperature_sensor = sensor
                return
