from enum import Enum

class CmdCode(Enum):
    NOP = 0x00
    GET_PARAM_2 = 0x04
    GET_PARAM_4 = 0x05
    SET_PARAM_2 = 0x07
    SET_PARAM_4 = 0x08
    UNLOCK_PARAM_ALL = 0x0A
    SAVE_PARAM_ALL = 0x0B
    GET_STATE_VALUE_2 = 0x10
    GET_STATE_VALUE_4 = 0x11
    READ_EA05_DATA = 0x1E
    CLEAR_EA05_DATA = 0x1F
    READ_EA05_DATA_EX = 0x62
    SET_STATE_VALUE_WITHMASK_4 = 0x66
