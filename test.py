from datetime import datetime
from characteristic_parser import parse_characteristic
from utils import create_date_payload


if __name__ == "__main__":
    raw_data_list = [
        "0f60000100000000000000000000000000000000",
        "0f62000000000000000000000000000000000000",
        "0f61000100000000000000000000000000000000",
        "420b007d00000000000000000000000000000000",
        "4160271127132710270726fd26f926fb2702270c",
        "14069d0e1cdd0000000000000000000000000000",
        "1407b3020350035c000000000000000000000000",
        "0f12061400eb0106ff8b00ee0108ff8ef8260127",
    ]

    sample_data_list = [bytes.fromhex(data) for data in raw_data_list]
    for sample_data in sample_data_list:
        print(parse_characteristic(sample_data))
    
    test_date = datetime(2025, 2, 4, 23, 47, 21)
    print(create_date_payload(test_date).hex())
