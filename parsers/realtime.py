from typing import Dict, List, Union
from utils import bytes_to_signed_short


class RealtimeParser:
    @staticmethod
    def parse_hr(payload: bytes) -> Dict[str, Union[int, float]]:
        return (
            {
                "num": payload[0],
                "sport_time": payload[1],
                "heart_rate": bytes_to_signed_short(payload[2], payload[3]) / 100.0,
                "cadence": bytes_to_signed_short(payload[4], payload[5]),
                "steps": bytes_to_signed_short(payload[6], payload[7]),
            }
            if len(payload) >= 8
            else {}
        )

    @staticmethod
    def parse_rri(payload: bytes) -> Dict[str, Union[int, List[int]]]:
        if len(payload) < 2:
            return {"num": 0, "CN": 0, "rri": []}

        rri_values = []
        max_pairs = payload[1]
        byte_index = 2

        for _ in range(max_pairs):
            if byte_index + 1 >= len(payload):
                break
            rri_values.append(
                bytes_to_signed_short(payload[byte_index], payload[byte_index + 1])
            )
            byte_index += 2

        return {"num": payload[0], "CN": payload[1], "rri": rri_values}
