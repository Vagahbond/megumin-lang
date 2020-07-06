from pointer import Pointer
from pointer import PtrType
import uuid

class Scope:
    datapool = {}
    def __init__(self , parent):
        self.pointers = {} #pointers
        self.parent = parent
        self.ret_value = None

    def exists(self, name):
        if (name in self.pointers):
            return True
        if (self.parent != None):
            return self.parent.exists(name)
        return False

    def addValue(self, ptr_type : PtrType, name : str, value):
        if name in self.pointers:
            raise ValueError('The name '+ name+ ' already exists in this scope.')
        hash = uuid.uuid4()
        self.pointers[name] = Pointer(ptr_type,hash)
        Scope.datapool[hash] = value

    def affectValue(self, name, value):
        if name in self.pointers:
            Scope.datapool[self.pointers[name].address] = value
        elif self.parent != None:
            self.parent.affectValue(name, value)
        else :
            raise ValueError('Name : '+ name+ ' does not exist in this scope.')

    def getValue(self, name : str):
        if name in self.pointers:
            return Scope.datapool[self.pointers[name].address]
        if (self.parent != None):
            return (self.parent.getValue(name))
        else:
            raise ValueError("Name : "+ name+ " is undefined")
