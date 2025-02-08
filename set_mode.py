import asyncio
from bleak import BleakClient
from typing import Dict

from characteristic_parser import parse_characteristic

DEVICE_ADDRESS = ""
NOTIFY_UUID = "F000EFE3-0451-4000-0000-00000000B000"
WRITE_UUID = "F000EFE1-0451-4000-0000-00000000B000"

MODE_COMMANDS: Dict[str, list] = {
    "sport": [
        "fc0f600100000000000000000000000000000000",
        "fc0f620100000000000000000000000000000000",
        "fc0f610100000000000000000000000000000000",
    ],
    "ecg": [
        "fc0f600101000000000000000000000000000000",
        "fc0f620100000000000000000000000000000000",
        "fc0f610101000000000000000000000000000000",
    ],
    "hrv": [
        "fc0f600100000000000000000000000000000000",
        "fc0f620101000000000000000000000000000000",
        "fc0f610101000000000000000000000000000000",
    ],
}


class ModeConfigurator:
    def __init__(self):
        self._ready = asyncio.Event()
        self.current_params = {"ecg": None, "sr": None, "xo": None}

    def _notification_handler(self, sender: str, data: bytes):
        """处理特征值通知"""
        result = parse_characteristic(data)

        if result["type"] == "SportModel":
            self.current_params["ecg"] = result["data"].get("ecg")
        elif result["type"] == "SR":
            self.current_params["sr"] = result["data"].get("sr")
        elif result["type"] == "XO":
            self.current_params["xo"] = result["data"].get("xo")

        if all(v is not None for v in self.current_params.values()):
            self._ready.set()

    def _get_current_mode(self) -> str:
        """根据参数判断当前模式"""
        ecg, sr, xo = self.current_params.values()

        if ecg == 0 and sr == 0 and xo == 0:
            return "sport"
        if ecg == 1 and sr == 0 and xo == 1:
            return "ecg"
        if ecg == 0 and sr == 1 and xo == 1:
            return "hrv"
        return "unknown"

    async def _read_current_mode(self, client: BleakClient):
        """读取当前配置参数"""
        # 发送读取命令
        await client.write_gatt_char(
            WRITE_UUID, bytes.fromhex("fc0f600000000000000000000000000000000000")
        )
        await client.write_gatt_char(
            WRITE_UUID, bytes.fromhex("fc0f620000000000000000000000000000000000")
        )
        await client.write_gatt_char(
            WRITE_UUID, bytes.fromhex("fc0f610000000000000000000000000000000000")
        )

        try:
            await asyncio.wait_for(self._ready.wait(), timeout=10.0)
        except asyncio.TimeoutError:
            print("读取设备参数超时")

    async def _set_target_mode(self, client: BleakClient, mode: str):
        """设置目标模式"""
        commands = MODE_COMMANDS.get(mode, [])
        if not commands:
            print("无效模式")
            return False

        print(f"正在设置 {mode} 模式...")
        for cmd in commands:
            await client.write_gatt_char(WRITE_UUID, bytes.fromhex(cmd))
            await asyncio.sleep(0.2)  # 命令间隔

        return True

    async def run(self):
        async with BleakClient(DEVICE_ADDRESS) as client:
            # 设置通知回调
            await client.start_notify(NOTIFY_UUID, self._notification_handler)

            # 读取当前模式
            print("正在读取当前模式...")
            await self._read_current_mode(client)
            current_mode = self._get_current_mode()
            print(f"当前设备模式: {current_mode}")

            # 获取用户输入
            target_mode = input("请输入目标模式 (sport/ecg/hrv): ").strip().lower()

            # 设置新模式
            if await self._set_target_mode(client, target_mode):
                print("模式设置成功！")
            else:
                print("模式设置失败")


if __name__ == "__main__":
    configurator = ModeConfigurator()
    asyncio.run(configurator.run())
