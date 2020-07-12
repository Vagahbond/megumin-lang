from enum import Enum

class PtrType(Enum):
    FUNC = "function"
    VAR = "variable"

class Pointer:

    def __init__(self, ptr_type : PtrType, address : str):
        self.type = ptr_type
        self.address = address
    