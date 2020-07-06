from enum import Enum

class PtrType(Enum):
    FUNC = 1
    VAR = 2
    PTR = 3

class Pointer:

    def __init__(self, ptr_type : PtrType, address : str):
        self.type = ptr_type
        self.address = address
    