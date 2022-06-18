CRC_POLY_32 = 0xEDB88320


class ChecksumHandler:

    def __init__(self):
        self.crc32_tab_calculated: bool = False
        self.crc32_tab = []

    def calculate_crc32(self, input_data: bytes) -> int:
        crc: int = 0xFFFFFFFF

        if not self.crc32_tab_calculated:
            self.init_crc32_tab()

        for byte in input_data:
            long_c = 0x000000FF & byte
            tmp = crc ^ long_c
            crc = (crc >> 8) ^ self.crc32_tab[tmp & 0xff]

        crc ^= 0xffffffff
        return crc & 0xffffffff

    def init_crc32_tab(self):
        for i in range(256):
            crc = i
            for j in range(8):
                if crc & 0x00000001:
                    crc = (crc >> 1) ^ CRC_POLY_32
                else:
                    crc = crc >> 1

            self.crc32_tab.append(crc)

        self.crc32_tab_calculated = True
