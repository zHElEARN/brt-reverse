from typing import Dict
from utils import to_signed_byte
from parsers.ecg import EcgParser
from parsers.gsensor import GSensorParser
from parsers.realtime import RealtimeParser
from parsers.sport_model import SportModelParser


def parse_characteristic(data: bytes) -> Dict:
    result = {"type": "Other", "data": list(data)}
    if len(data) != 20:
        return result

    command_byte = to_signed_byte(data[0])
    sub_command = data[1]
    payload = data[2:]

    # 0x0F (15) Command group
    if command_byte == 0x0F:
        if sub_command == 0x12:  # 18
            return {
                "type": "GSensor",
                "data": GSensorParser.parse_gsensor(data[4:16]),
            }
        if sub_command == 0x60:  # 96
            return {
                "type": "SportModel",
                "data": SportModelParser.parse_sport_model(payload),
            }
        if sub_command == 0x61:  # 97
            return {"type": "XO", "data": SportModelParser.parse_xo(payload)}
        if sub_command == 0x62:  # 98
            return {"type": "SR", "data": SportModelParser.parse_sr(payload)}

    # 0x14 (20) Command group
    elif command_byte == 0x14:
        if sub_command == 0x06:  # 6
            return {
                "type": "HR",
                "data": RealtimeParser.parse_hr(payload),
            }
        if sub_command == 0x07:  # 7
            return {
                "type": "RRI",
                "data": RealtimeParser.parse_rri(payload),
            }

    # 0x41 (65) ECG Data
    elif command_byte == 0x41:
        return {"type": "ECG", "data": EcgParser.parse_ecg(data[1:])}

    # 0x42 (66) ECG Info
    elif command_byte == 0x42:
        if sub_command == 0x01:
            return {"type": "ECGSignal", "data": EcgParser.parse_signal(payload)}
        if sub_command == 0x06:
            return {
                "type": "ECGSpeed",
                "data": EcgParser.parse_speed(payload),
            }
        if sub_command == 0x0B:
            return {
                "type": "ECRSR",
                "data": EcgParser.parse_sr(payload),
            }

    return result
