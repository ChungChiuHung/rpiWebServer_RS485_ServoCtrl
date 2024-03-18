from CmdMsgGenerator import MessageGenerator
from CmdMsgGenerator import CmdCode
from cal_cmd_response_time import CommAnalyzer
from responseParser import ResponseParser
from commCode import SetBitStatus

# Initialize the message generator with destination address and control code
generator = MessageGenerator(destination_address=0x01, control_code=0x00)

# Generating a NOP command hex (expects no parameters)
nop_command_hex = generator.get_command(CmdCode.NOP, return_as_str=True)
print("NOP Command Hex:", nop_command_hex)

# Generating a SET_PARAM_2 command hex (expects param_group and write_value)
set_param_2_command_hex = generator.get_command(
    CmdCode.SET_PARAM_2,
    return_as_str=True,
    param_group=[0x01, 0x02],
    write_value=[0x03, 0x04]
)
print("SET_PARAM_2 Command Hex:", set_param_2_command_hex)

# Generating a SET_PARAM_4 command hex (expects param_group and write_value)
set_param_4_command_hex = generator.get_command(
    CmdCode.SET_PARAM_4,
    return_as_str=True,
    param_group=[0x01, 0x02],
    write_value=[0x00, 0x01, 0x02, 0x03]
)
print("SET_PARAM_4 Command Hex:", set_param_4_command_hex)

# Generating a SET_STATE_VALUE_WITHMASK_4 command hex
# (expects status_number, status_value, and mask)
set_state_value_withmask_4_command_hex = generator.get_command(
    CmdCode.SET_STATE_VALUE_WITHMASK_4,
    return_as_str=False,
    status_number=[0x00, 0x01],
    status_value=[0x00, 0x00, 0x00, 0x02],
    mask=[0xFF, 0xFF, 0xFF, 0xFF]
)
print("SET_STATE_VALUE_WITHMASK_4 Command Hex:", set_state_value_withmask_4_command_hex)

# Command Data Validate CRC
response = ResponseParser()
print(response.validate_crc(set_state_value_withmask_4_command_hex))

# Calculate the response time
analyzer = CommAnalyzer()
print("Response Time: " + str(analyzer.calculate_transmission_time_ms(set_state_value_withmask_4_command_hex,57600)) + " ms")

# Set Bit Status
# Example Usage:
home_status, home_mask = SetBitStatus("HOME", 1)
print("HOME Status:", home_status.hex(), "Mask:", home_mask.hex())

sel_no_status, sel_no_mask = SetBitStatus("SEL_NO", 1)  # 13 within 4 bits is within the valid range.
print("SEL_NO Status:", sel_no_status.hex(), "Mask:", sel_no_mask.hex())