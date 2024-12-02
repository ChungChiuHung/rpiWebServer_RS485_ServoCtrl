import serial
import time
import logging
from serial.serialutil import SerialException
import serial.tools.list_ports  # For dynamically listing available ports

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class SerialPortManager:
    def __init__(self, port=None, baud_rate=115200, timeout=1, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.serial_instance = None
        self.available_ports = self.list_available_ports()
        self.keep_running = True  # Flag to control reconnection attempts

    def list_available_ports(self):
        """List all available serial ports."""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports if ports else ["/dev/ttyS0", "/dev/ttyAMA0", "/dev/serial0", "/dev/ttyUSB0"]

    def connect(self):
        """Attempts to open a serial connection on a list of possible ports."""
        if not self.keep_running:
            return False

        if self.port:
            try:
                self.serial_instance = serial.Serial(self.port, self.baud_rate, timeout=self.timeout,
                                                     bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits)
                logging.info(
                    f"Connected to {self.port} at {self.baud_rate} baud.")
                return True
            except (SerialException, OSError) as e:
                logging.error(f"Failed to open serial port {self.port}: {e}")

        logging.info("Trying available ports...")
        for port in self.list_available_ports():
            if not self.keep_running:
                return False
            try:
                self.serial_instance = serial.Serial(port, self.baud_rate, timeout=self.timeout,
                                                     bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits)
                self.port = port
                logging.info(f"Connected to {port} at {self.baud_rate} baud.")
                return True
            except (SerialException, OSError) as e:
                logging.error(f"Failed to connect on {port}: {e}")

        logging.error("Failed to open any serial port.")
        return False

    def get_serial_instance(self):
        """Get the current serial instance, attempting to reconnect if necessary."""
        if self.serial_instance and self.serial_instance.is_open:
            return self.serial_instance
        else:
            if not self.keep_running:
                logging.info("Reconnection attempts stopped.")
                return None
            logging.info("Serial port is not open. Attempting to reconnect...")
            if self.connect():
                return self.serial_instance
            time.sleep(0.1)  # Add a delay to prevent rapid repeated attempts
            return None

    def disconnect(self):
        """Disconnect the serial connection and stop reconnection attempts."""
        self.keep_running = False
        if self.serial_instance and self.serial_instance.is_open:
            self.serial_instance.close()
            logging.info(f"Disconnected from {self.port}.")

    def send_and_receive(self, message, read_timeout=0.1):
        """Send a message and receive a response from the serial connection."""
        serial_conn = self.get_serial_instance()
        if serial_conn:
            # Ensure message is in bytes
            serial_conn.write(message.encode('utf-8'))
            logging.info(f"Send: {message}")
            time.sleep(read_timeout)  # Wait to receive the full message
            response = serial_conn.read_all()
            logging.info(f"Received: {response.decode('utf-8')}")
            return response
        else:
            logging.error("No active serial connection.")
            return None

    def get_baud_rate(self):
        """Get the current baud rate."""
        return self.baud_rate

    def get_connected_port(self):
        """Get the currently connected port."""
        return self.port if self.serial_instance and self.serial_instance.is_open else "Not connected"
