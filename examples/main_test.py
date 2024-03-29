import unittest
from message_generator import MessageGenerator
from base_msg_generator import BaseMsgGenerator
from examples.servo_command_code import CmdCode
from servo_params import ServoParams
from io_status_fetcher import IOStatusFetcher, IOStatusFetcher_Test
from cal_cmd_response_time import CmdDelayTime
from status_bit_mapping import BitMap, BitMapOutput
from set_servo_io_status import SetServoIOStatus
from response_parsing import ResponseMsgParser
import math

class TestServoCommunication(unittest.TestCase):
    
    @staticmethod
    def print_byte_array_as_spaced_hex(byte_array, data_name):
        hex_string = ' '.join(f"{byte:02X}" for byte in byte_array)
        print(f"{data_name}: {hex_string}")

    @staticmethod
    def decimal_to_2_bytes(number):
        if not (0 <= number <= 65535):
            raise ValueError("Number out of range. Must be between 0 and 65535.")
        return number.to_bytes(2, byteorder='big')
    
    def test_decimal_to_2bytes(self):
        print("======  decimal to 2-bytes ======")
        params_no = 32
        bytes = self.decimal_to_2_bytes(params_no)
        self.print_byte_array_as_spaced_hex(bytes, "Parameter Group ")

    def test_byte_operation(self):
        print("=== Test Byte Operation ===")
        print(CmdCode.SET_STATE_VALUE_WITHMASK_4)
        print(CmdCode.SET_STATE_VALUE_WITHMASK_4.name)
        print(CmdCode.SET_STATE_VALUE_WITHMASK_4.value)

        bit_array = [CmdCode.SET_STATE_VALUE_WITHMASK_4.value, CmdCode.GET_PARAM_2.value]

        self.print_byte_array_as_spaced_hex(bit_array, "bit array")

        int_value = 123455
        byte_length = math.ceil(int_value.bit_length()/8)
        dynamic_byte_array = int_value.to_bytes(byte_length, byteorder='big')

        print("The hex value: ",dynamic_byte_array)
        self.print_byte_array_as_spaced_hex(dynamic_byte_array, "dynamic byte array")

    def test_message_generator(self):
        print("=== Test BaseMsgGenerator ===")
        base_msg_generator = BaseMsgGenerator()
        # Generate a message.
        # Replace the following example values with your actual values.
        protocol_id = 1 # 1 : Single Master Protocol.
        destination_address = 1
        dir_bit = 0 # 0:Command Message, 1:Response Message  
        #toggle_bit = 0x00 # Set 0 and 1 alternatively every time the host controller sends a command message.
                      # The amplifer sends back the same value in the response message
        error_code = 0 # fixed value (Command Message)
        cmd_code = CmdCode.SET_STATE_VALUE_WITHMASK_4.value # Page 12- List of Commands
        parameter_data = [0x04, 0x05]  # Example parameter data.Page 12- List of Commands

        message = base_msg_generator.generate_message(protocol_id, destination_address, dir_bit, error_code, cmd_code, parameter_data)

        # Now 'message' contains your structured message including the CRC.
        # print("Generated Message:", message.hex())
        self.print_byte_array_as_spaced_hex(message, "message")   

    def test_servo_io_status(self):
        setter = SetServoIOStatus()
        result_bytes = setter.set_bit_status(BitMap.SEL_NO, 3)
        print("Resulting bytes for SEL_NO set to 3:", result_bytes)
        self.print_byte_array_as_spaced_hex(result_bytes, "Resulting bytes for SEL_NO set to 3:")
    
        binary_result = ' '.join(format(byte, '08b') for byte in result_bytes)
        print("Resulting bytes for SEL_NO set to 3 in binary:", binary_result)
    
        result_bytes = setter.set_bit_status(BitMap.HOME, 1)
        print("Resulting bytes for HOME set to 1:", result_bytes)
        self.print_byte_array_as_spaced_hex(result_bytes, "Resulting bytes for HOME set to 1:")
    
        binary_result = ' '.join(format(byte, '08b') for byte in result_bytes)
        print("Resulting bytes for HOME set to 1 in binary:", binary_result)

    def test_get_trasmmision_time(self):
        base_msg_generator = BaseMsgGenerator()
        protocol_id = 1 
        destination_address = 1
        dir_bit = 0 # 0:Command Message, 1:Response Message  
        error_code = 0 # fixed value (Command Message)
        cmd_code = CmdCode.SET_STATE_VALUE_WITHMASK_4.value # Page 12- List of Commands

        # SEL_NO 0~15
        setter = SetServoIOStatus()
        parameter_code = setter.set_bit_status(BitMap.SEL_NO, 1)
        parameter_data = parameter_code # Example parameter data.Page 12- List of Commands

        message = base_msg_generator.generate_message(protocol_id, destination_address, dir_bit, error_code, cmd_code, parameter_data)
        self.print_byte_array_as_spaced_hex(message, "Communication Code: ")
        # Calculate the response time
        analyzer = CmdDelayTime(57600)
        print("Response Time: " + str(analyzer.calculate_transmission_time_ms(message)) + " ms")

        # SVON 0/1
        parameter_code = setter.set_bit_status(BitMap.SVON, 1)
        parameter_data = parameter_code
        message = base_msg_generator.generate_message(protocol_id, destination_address, dir_bit, error_code, cmd_code, parameter_data)
        self.print_byte_array_as_spaced_hex(message, "Communication Code: ")

        # GET_STATE_VALUE_4
        print("GET_STATE_VALUE_4")
        protocol_id = 1
        destination_address = 1
        dir_bit = 0
        error_code = 0
        cmd_code = CmdCode.GET_STATE_VALUE_4.value

        # Status No.0:Alarm 
        # Status No.288:Logic I/O Input
        # Status No.296:Logic I/O Output
        status_no = 288
        parameter_code = self.decimal_to_2_bytes(status_no) 
        parameter_data = parameter_code
        message = base_msg_generator.generate_message(protocol_id, destination_address, dir_bit, error_code, cmd_code, parameter_data)
        self.print_byte_array_as_spaced_hex(message, "Communication Code: ")

    def test_response_parser(self):

        response_parser = ResponseMsgParser()
        protocol_id = 1 
        destination_address = 1
        comm_code = CmdCode.GET_STATE_VALUE_4.value

        # SEL_NO 0~15
        setter = SetServoIOStatus()
        parameter_code = setter.set_respone_bit(BitMap.PAUSE, 1)
        parameter_data = parameter_code # Example parameter data.Page 12- List of Commands

        message = response_parser.generate_response_message(protocol_id, destination_address, comm_code,parameter_data)
        response_message = message

        response_parser = ResponseMsgParser()

        try:
            parsed_data = response_parser.parse_message(response_message)
            print("Parsed response data:", parsed_data)

        except ValueError as e:
            print("Error parsing response message:", e)

    def test_get_response_to_json(self):
        # Example usage:
        # Assuming you have an input_response that mimics the expected response structure:
        input_response = bytes([0x26, 0x01, 0x80, 0x11, 0xAA, 0xBB, 0xCC, 0xDD, 0x75, 0xE0])

        fetcher = IOStatusFetcher_Test()
        print(fetcher.get_output_io_status(input_response))

if __name__ == "__main__":
    unittest.main()
    