from serial_port_manager import SerialPortManager
from modbus_ascii_client import ModbusASCIIClient
from servo_control_registers import ServoControlRegistry
import struct

def test_modbus_ascii_client():
    print("Initializing SerialPortManager...")
    serial_manager = SerialPortManager()

    print("Creating ModbusASCIIClient instance...")
    modbus_client = ModbusASCIIClient(device_number=1, serial_port_manager=serial_manager)

    print("Testing connection ...")
    if not modbus_client.ensure_connection():
        print("Failed to connect to the device")
        return
    
    try:
        address =struct.pack('>H', ServoControlRegistry.DI_PIN_CONTROL.value)
        print(f"Address of {ServoControlRegistry.DI_PIN_CONTROL.name}: {address.hex()}")
        data = 0x0001
        message = modbus_client.build_write_message(ServoControlRegistry.DI_PIN_CONTROL, data)
        print(f"Build Write Message: {message}")

        message = modbus_client.build_read_message(ServoControlRegistry.DI_STATUS)
        print(f"Build Read Message: {message}")

        modbus_client.send_and_receive(message)

    except Exception as e:
        print(f"An error occurred during testing: {e}")

    finally:
        print("Cleaning up ...")
        serial_manager.disconnect()
        print("Test complteted and port disconnected.")


if __name__ == "__main__":
    test_modbus_ascii_client()
