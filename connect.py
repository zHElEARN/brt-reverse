import asyncio
import numpy as np
from datetime import datetime
from bleak import BleakClient
from pathlib import Path

# 从之前重构的模块中导入
from characteristic_parser import parse_characteristic
from utils import create_date_payload

# 蓝牙配置
DEVICE_ADDRESS = ""
NOTIFY_UUID = "F000EFE3-0451-4000-0000-00000000B000"
WRITE_UUID = "F000EFE1-0451-4000-0000-00000000B000"

# 数据存储配置
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


class DeviceManager:
    def __init__(self):
        self.ecg_data = []
        self.acc_data = {"x": [], "y": [], "z": []}
        self.device_mode = None
        self._sport_model = None
        self._sr = None
        self._xo = None
        self.mode_determined = False

    def _notification_handler(self, sender: str, data: bytes):
        """处理特征值通知"""
        result = parse_characteristic(data)
        print("Received:", result)

        # 处理设备模式判断
        if result["type"] == "SportModel":
            self._sport_model = result["data"].get("ecg")
        elif result["type"] == "SR":
            self._sr = result["data"].get("sr")
        elif result["type"] == "XO":
            self._xo = result["data"].get("xo")

        if (
            all([v is not None for v in [self._sport_model, self._sr, self._xo]])
            and not self.mode_determined
        ):
            self._determine_mode()

        # 数据存储处理
        if result["type"] == "ECG" and result["data"]:
            self.ecg_data.extend(result["data"]["ecg"])
        elif result["type"] == "GSensor" and result["data"]:
            self.acc_data["x"].append(result["data"]["x1"])
            self.acc_data["y"].append(result["data"]["y1"])
            self.acc_data["z"].append(result["data"]["z1"])

    def _determine_mode(self):
        """判断设备工作模式"""
        if self._sport_model == 0 and self._sr == 0 and self._xo == 0:
            self.device_mode = "sport"
        elif self._sport_model == 1 and self._sr == 0 and self._xo == 1:
            self.device_mode = "ecg"
        elif self._sport_model == 0 and self._sr == 1 and self._xo == 1:
            self.device_mode = "hrv"
        else:
            self.device_mode = "unknown"
        self.mode_determined = True
        print(f"Device mode detected: {self.device_mode}")

    async def _write_command(self, client: BleakClient, hex_str: str):
        """发送蓝牙命令"""
        await client.write_gatt_char(WRITE_UUID, bytes.fromhex(hex_str), response=True)

    async def connect_and_manage(self):
        async with BleakClient(DEVICE_ADDRESS) as client:
            # 启用通知
            await client.start_notify(NOTIFY_UUID, self._notification_handler)

            # 启动加速度计
            await self._write_command(
                client, "fc14040001000000000000000000000000000000"
            )

            # 启动心电数据
            time_payload = create_date_payload(datetime.now())
            await client.write_gatt_char(WRITE_UUID, time_payload)

            # 读取配置参数
            await asyncio.gather(
                self._write_command(client, "fc0f600000000000000000000000000000000000"),
                self._write_command(client, "fc0f620000000000000000000000000000000000"),
                self._write_command(client, "fc0f610000000000000000000000000000000000"),
                self._write_command(client, "fc42060000000000000000000000000000000000"),
                self._write_command(client, "fc420b0000000000000000000000000000000000"),
                self._write_command(client, "fc42010000000000000000000000000000000000"),
            )

            # 保持连接直到用户中断
            while True:
                await asyncio.sleep(1)

    def save_data(self):
        """保存数据到文件"""
        if self.ecg_data:
            np.save(DATA_DIR / "ecg_data", np.array(self.ecg_data))
        if any(self.acc_data.values()):
            np.savez(
                DATA_DIR / "acc_data",
                x=self.acc_data["x"],
                y=self.acc_data["y"],
                z=self.acc_data["z"],
            )


async def main():
    manager = DeviceManager()
    try:
        await manager.connect_and_manage()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        manager.save_data()


if __name__ == "__main__":
    asyncio.run(main())
