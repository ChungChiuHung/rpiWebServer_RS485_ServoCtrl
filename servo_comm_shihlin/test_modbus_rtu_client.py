import struct
from modbus_rtu_client import ModbusRTUClient
from modbus_command_code import CmdCode
from servo_control_registers import ServoControlRegistry

class MockSerialPortManager:
    def __init__(self):
        pass
    def get_serial_instance(self):
        return True
    def write(self, message):
        print(f"Mock write: {message.hex()}")
    def read_all(self):
        return bytes.fromhex('01020304')
    def inWaiting(self):
        return 4

def test_build_read_message():
    mock_serial_manager = MockSerialPortManager()
    modbus_client = ModbusRTUClient(device_number=1, serial_port_manager=mock_serial_manager)
    read_message = modbus_client.build_read_message(ServoControlRegistry.MOTOR_FEEDBACK_PULSE, word_length=2)
    print("Read Message:", read_message.hex())

def test_build_write_message():
    mock_serial_manager = MockSerialPortManager()
    modbus_client = ModbusRTUClient(device_number=1, serial_port_manager=mock_serial_manager)
    sample_data = struct.pack('>H', 1000)
    write_message = modbus_client.build_write_message(ServoControlRegistry.MOTOR_SPEED, sample_data)
    print("Write Message: ", write_message.hex())

def test_build_write_message_2():
    mock_serial_maanger = MockSerialPortManager()
    modbus_client = ModbusRTUClient(device_name=1, serial_port_manager=mock_serial_maanger)
    test_cases = [
        (ServoControlRegistry.SEL_DI_CONTROL_SOURCE, struct.pack('>H', 0xFFFF)),  # All bits set
        (ServoControlRegistry.DI_PIN_CONTROL, struct.pack('>H', 0x0001)),  # First bit set
        (ServoControlRegistry.JOG_SPEED, struct.pack('>H', 1500)),  # Mid-range speed
        (ServoControlRegistry.POS_PULSES_CMD_1, struct.pack('>H', 0x1234)),  # Example pulse count
    ]

    for registry, data in test_cases:
        message = modbus_client.build_write_message(registry, data)
        print(f"Test with {registry.name}: Message = {message.hex()}")

if __name__ == "__main__":
    test_build_read_message()
    test_build_write_message()
    test_build_write_message_2()
