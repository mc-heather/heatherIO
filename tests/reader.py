from constants.datatypes import dataType
from reader import handle_packet

def test_var_int_read() -> None:
    print("Running VarInt reader on bytes '0x01' (Expected outcome: 1)")

    result = handle_packet(
        bytearray([0x01]), 
        (dataType.VAR_INT,)
    )

    print(f"Result from packet reader: {result}")

if __name__ == "__main__": test_var_int_read()