# -*- coding: UTF-8 -*-
import serial

from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal
from arduino.arduinospi import ArduinoSpi
from arduino.arduinospimock import ArduinoSpiMock


mock_enabled = True


class Domain(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._progr = None

    def connectProgr(self):

        def available_ports():
            result = list()
            for port in [f'COM{i+1}' for i in range(256)]:
                try:
                    s = serial.Serial(port)
                    s.close()
                    result.append(port)
                except (OSError, serial.SerialException):
                    pass
            print(f'available ports: {result}')
            return result

        def find_arduino():
            for port in available_ports():
                print(f'trying {port}')
                s = serial.Serial(port=port, baudrate=9600, timeout=1)
                if s.is_open:
                    s.write(b'<n>\n')
                    sleep(0.5)
                    ans = s.read_all()
                    s.close()
                    if ans[:3] == b'SPI':
                        print(f'STM32 found on {port}')
                        return port
            else:
                return ''

        if not mock_enabled:
            port = find_arduino()
            if port:
                self._progr = ArduinoSpi(port=port, baudrate=9600, parity=serial.PARITY_NONE, bytesize=8,
                                         stopbits=serial.STOPBITS_ONE, timeout=1)

        else:
            self._progr = ArduinoSpiMock(port=(find_arduino()), baudrate=9600, parity=serial.PARITY_NONE, bytesize=8,
                                         stopbits=serial.STOPBITS_ONE, timeout=1)
        return bool(self._progr)

    def disconnectProgr(self):
        self._progr.disconnect()

    def send(self, command):
        try:
            res = self._progr.query(command)
        except Exception as ex:
            print(ex)

