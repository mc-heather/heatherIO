from dataclasses import dataclass

from constants.datatypes import dataType

types = { # TODO: fix this fucking system, lord jesus christ.
    dataType.VAR_INT: lambda reader: reader.read_var_int()
}

def handle_packet(packet_data: bytes, structs: tuple) -> list:
    """
    Function to handle packet data sent by the client, alongside the respective type(s) to read them as.

    Note: This function and the Reader class are massively subject to change, this is just a basis.
    """
    
    reader = Reader(packet_data)
    return_data = []
    
    for _struct in structs:
        unpack_function = types.get(_struct, None)
        
        if not unpack_function: return_data += b""
        else: return_data.append(unpack_function(reader))

    if len(return_data) != 1: return return_data
    return return_data[0]

@dataclass
class Reader:
    packet_data: bytes
    offset: int = 0

    def read(self, offset_increment: int) -> bytes:
        return_data = self.packet_data[self.offset:self.offset + offset_increment] # TODO: switch away from offset?
        self.offset += offset_increment

        return return_data

    def read_int(self, size: int, signed: bool) -> int:
        return int.from_bytes(
            self.read(size),
            "little",
            signed=signed
        )

    def read_signed_int8(self) -> int: return self.read_int(1, True)

    def read_var_int(self) -> int:
        value = offset = 0

        while True:
            body = self.read_signed_int8()

            value |= (body & 0b01111111) << offset
            if (body & 0b10000000) == 0: break

            offset += 7

        return value

    