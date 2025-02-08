from typing import Dict
from utils import bytes_to_signed_short


class GSensorParser:
    @staticmethod
    def parse_gsensor(data: bytes) -> Dict[str, int]:
        if len(data) < 12:
            return {}

        return {
            "x1": bytes_to_signed_short(data[0], data[1]),
            "y1": bytes_to_signed_short(data[2], data[3]),
            "z1": bytes_to_signed_short(data[4], data[5]),
            "x2": bytes_to_signed_short(data[6], data[7]),
            "y2": bytes_to_signed_short(data[8], data[9]),
            "z2": bytes_to_signed_short(data[10], data[11]),
        }
