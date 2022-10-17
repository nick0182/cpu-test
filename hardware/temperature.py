import clr


class Temperature(object):
    gpu = None
    temperature_sensor = None

    def __init__(self):
        clr.AddReference("hardware/resources/OpenHardwareMonitorLib")

        from OpenHardwareMonitor import Hardware

        computer = Hardware.Computer()
        computer.GPUEnabled = True
        computer.Open()
        gpu_list = computer.Hardware
        if len(gpu_list) == 0:
            raise Exception("No GPU Hardware found")
        self.gpu = gpu_list[0]
        print(f"GPU Hardware found: {self.gpu.Name}")
        for sensor in self.gpu.Sensors:
            if sensor.SensorType == 2:  # temperature
                self.temperature_sensor = sensor
        if self.temperature_sensor is None:
            raise Exception("No GPU temperature sensor found")

    def fetch_temperature(self):
        self.gpu.Update()
        return self.temperature_sensor.Value
