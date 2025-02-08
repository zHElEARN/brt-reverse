from typing import Dict, List, Union
from utils import bytes_to_signed_short


class EcgParser:
    @staticmethod
    def parse_ecg(data: bytes) -> Dict[str, Union[int, List[float]]]:
        if len(data) < 3:
            return {"id": None, "uid": None, "ecg": []}

        header = data[0]
        return {
            "id": header >> 4,
            "uid": header & 0x0F,
            "ecg": [
                ((bytes_to_signed_short(data[i], data[i + 1]) - 10000) / 10.5) + 10000
                for i in range(1, len(data) - 1, 2)
            ],
        }

    @staticmethod
    def parse_speed(payload: bytes) -> Dict[str, int]:
        return (
            {"ecg_speed": bytes_to_signed_short(payload[0], payload[1])}
            if len(payload) >= 2
            else {}
        )

    @staticmethod
    def parse_signal(payload: bytes) -> Dict[str, int]:
        return (
            {"ecg_signal": bytes_to_signed_short(payload[0], payload[1])}
            if len(payload) >= 2
            else {}
        )

    @staticmethod
    def parse_sr(payload: bytes) -> Dict[str, int]:
        return (
            {"ecg_sr": bytes_to_signed_short(payload[0], payload[1])}
            if len(payload) >= 2
            else {}
        )
