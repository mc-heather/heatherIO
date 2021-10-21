from dataclasses import dataclass

from constants.datatypes import dataType

import struct

types = { # TODO: fix this fucking system, lord jesus christ.
    dataType.VAR_INT: lambda reader: reader.read_var_int(),
    dataType.VAR_LONG: lambda reader: reader.read_var_long(),
    dataType.BOOLEAN: lambda reader: reader.read_bool()
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

    def _read_int(self, size: int, signed: bool) -> int:
        return int.from_bytes(
            self.read(size),
            "little",
            signed=signed
        )

    def read_bool(self) -> bool: return self.read(1) == b"0x01" # thanks for the simple implementation
    def read_byte(self) -> int: return self._read_int(1, True)
    def read_unsigned_byte(self) -> int: return self._read_int(1, False)
    def read_short(self) -> int: return self._read_int(2, True)
    def read_unsigned_short(self) -> int: return self._read_int(2, False)
    def read_int(self) -> int: return self._read_int(4, True)
    def read_long(self) -> int: return self._read_int(8, True)
    def read_float(self) -> float: return struct.unpack('f', self.read(4))
    def read_double(self) -> float: return struct.unpack('d', self.read(8))

    def read_string(self) -> str:
        if self.read_var_int() != 0x0b: return ""

        return self.read(self.read_var_int()).decode()

    def read_chat(self) -> dict:
        raw_format = self.read_string()

        # TODO: experiment and make this work (chat is fucking json?)

        return NotImplemented

    def read_identifier(self) -> str:
        raw_format = self.read_string()

        # TODO: make this work (add handlers for all identifiers!)

        return NotImplemented

    def read_var_int(self) -> int:
        value = offset = 0

        while True:
            assert offset < 35, "VarInt is too big!"

            body = self.read_byte()

            value |= (body & 0b01111111) << offset
            if (body & 0b10000000) == 0: break

            offset += 7

        return value

    def read_var_long(self) -> int: # god i love how practically useless this is
        value = offset = 0

        while True:
            assert offset < 70, "VarLong is too big!"

            body = self.read_byte()

            value |= (body & 0b01111111) << offset
            if (body & 0b10000000) == 0: break

            offset += 7

        return value

    def read_entity_metadata(self): # type?
        index = self.read_unsigned_byte()
        if index == 0xff: return # end of metadata

        type = self.read_var_int() # TODO: type -> function
        # value = get_value_of_type(type) TODO

        return NotImplemented

    def read_slot(self): # type?
        if not self.read_bool(): return

        item_id = self.read_var_int()
        item_count = self.read_byte()
        nbt = self.read_nbt()
        if nbt == 0: return # ?

        return NotImplemented # handle it here????? idfk man#

    def read_nbt(self): # type?
        ...