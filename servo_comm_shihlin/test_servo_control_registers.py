import struct
from servo_control_registers import ServoControlRegistry

# Access a register's details
print(ServoControlRegistry.MOTOR_FEEDBACK_PULSE)

# Calculate a dynamic address
try:
    pa_address = ServoControlRegistry.calculate_dynamic_address("PA", 1)
    print(f"Address for PA01: {hex(pa_address)}")
    pb_address = ServoControlRegistry.calculate_dynamic_address("PB", 40)
    print(f"Address for PB40: {hex(pb_address)}")
    pc_address = ServoControlRegistry.calculate_dynamic_address("PC", 38)
    print(f"Address for PC38: {hex(pc_address)}")
    pd_address = ServoControlRegistry.calculate_dynamic_address("PD", 31)
    print(f"Address for PD41: {hex(pd_address)}")
    pe_address = ServoControlRegistry.calculate_dynamic_address("PE", 30)
    print(f"Address for PE30: {hex(pe_address)}")
    pf_address = ServoControlRegistry.calculate_dynamic_address("PF", 82)
    print(f"Address for PF82: {hex(pf_address)}")

    address = ServoControlRegistry.ACCUMULATIVE_PULSES_ERROR.value

    data = struct.pack('>H', address)

    data_len = ServoControlRegistry.ACCUMULATIVE_PULSES_ERROR.data_length
    data_description = ServoControlRegistry.ACCUMULATIVE_PULSES_ERROR.description

    print(f"Address for {ServoControlRegistry.ACCUMULATIVE_PULSES_ERROR.name}: {data}, {data_len}, {data_description}")

    data_2 = struct.pack('>HH', 0x1111, 0x2222)

    print(f"Addres for 4 bytes: {data_2.hex()}")

except ValueError as error:
    print(error)