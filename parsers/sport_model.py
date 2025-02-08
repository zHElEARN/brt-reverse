from typing import Dict


class SportModelParser:
    @staticmethod
    def parse_sport_model(payload: bytes) -> Dict[str, int]:
        return {"en": payload[0], "ecg": payload[1]} if len(payload) >= 2 else {}

    @staticmethod
    def parse_xo(payload: bytes) -> Dict[str, int]:
        return {"en": payload[0], "xo": payload[1]} if len(payload) >= 2 else {}

    @staticmethod
    def parse_sr(payload: bytes) -> Dict[str, int]:
        return {"en": payload[0], "sr": payload[1]} if len(payload) >= 2 else {}
