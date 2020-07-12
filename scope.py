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

    
    def addPtr(self, name : str,  ptr : Pointer):
        if name in self.pointers:
            raise ValueError('The name '+ name + ' already exists in this scope.')
        
        self.pointers[name] = Pointer(ptr.type, ptr.address)

    

    def affectValue(self, name, value):

        if name in self.pointers:
            Scope.datapool[self.pointers[name].address] = value
            self.pointers[name].type = PtrType.VAR

        elif self.parent != None:
            self.parent.affectValue(name, value)

        else :
            raise ValueError('Name : ' + name + ' does not exist in this scope.')
    

    def affectPtr(self, name: str, pointer: Pointer):

        if name in self.pointers:
            self.pointers[name].address = Pointer(pointer.type, pointer.address)

        elif self.parent != None:
            self.parent.affectValue(name, pointer)

        else :
            raise ValueError('Name : ' + name + ' does not exist in this scope.')



    def getValue(self, name : str, type:PtrType):
        if name in self.pointers:
            ptr = self.pointers[name]

            if ptr.type != type:
                raise ValueError(name + "is a " + type + "!")

            return Scope.datapool[ptr.address]

        if (self.parent == None): 
            raise ValueError("Name : " + name + " is undefined")

        return self.parent.getValue(name, type)

            

    def getPtr(self, name:str):

        if name in self.pointers:
            return self.pointers[name]

        if (self.parent != None):
            return (self.parent.getValue(name))

        else:
            raise ValueError("Name : " + name + " is undefined")





    def getVarType(self, name: str):
        
        if name in self.pointers:
            return self.pointers[name].type
 
        if (self.parent != None):
            return (self.parent.getValue(name))
            
        else:
            raise ValueError("Name : " + name + " is undefined")

    