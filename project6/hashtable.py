
class Node:
    def __init__(self, keyVal, nextNode=None):
        self.keyVal = keyVal
        self.next = nextNode

    def setNext(self, nextNode):
        self.next = nextNode

    def getKey(self):
        return self.keyVal[0]

    def getValue(self):
        return self.keyVal[1]

    def updateTuple(self, key, value):
        self.keyVal = (key,value)

    def getNext(self):
        return self.next

class LinkedList:
    def __init__(self, headN):
        self.headNode = headN

    def insertNode(self, newNode):
        newNode.setNext(self.headNode)
        self.headNode = newNode

    def deleteNode(self, key):
        current = self.headNode
        previous = None

        while current != None:
            if current.getKey() == key:
                break
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.headNode.setNext(current.getNext())
        else:
            previous.setNext(current.getNext())

    def getItem(self, key):
        current = self.headNode
        while current:
            if current.getKey() == key:
                return current.getValue()
            else:
                current = current.getNext()
        return None

    def getKeys(self):
        keys = []
        current = self.headNode
        while current:
            keys.append(current.getKey())
            current = current.getNext()
        return keys

##    def __len__(self):
##        current = self.headNode
##        length = 0
##        while current:
##            length += 1
##            current = current.getNext()
##        return length

class Hashtable:
    def __init__(self, dict):
        self.hashTable = [None] * 8 
        self.count = len(dict)
        for item in dict:
            self.__setitem__(item, dict[item])

       

    def __getitem__(self, key):
        if self.hashTable[self.compress(hash(key))] is None:
            return None
        else:
            return self.hashTable[self.compress(hash(key))].getItem(key)
       

    def __setitem__(self, key, value):
        hashValue = hash(key)
        index = self.compress(hashValue)
        
        if key not in self.keys():
            if self.hashTable[index] == None:
                self.hashTable[index] = LinkedList(Node((key,value)))
            else:
                self.hashTable[index].insertNode(Node((key,value)))

            self.count += 1 #after inserting tuple update count

            if self.count > .9 * len(self.hashTable):
                self.rehash(self.hashTable)

        else:
             bucket = self.hashTable[index]
             current = bucket.headNode
             while current:
                if current.getKey() == key:
                    current.updateTuple(key, value)
                    break
                current = current.nextNode

        

    def rehash(self, hashT):
        newTable = [None] * (2 * len(hashT))
        oldTable = self.hashTable
        self.hashTable = newTable

        for item in oldTable:
            if item:
                current = item.headNode
                while current:
                    self.__setitem__(current.getKey(),current.getValue())
                    current = current.getNext()

    def __delitem__(self, key):
        index = self.compress(hash(key))
        self.hashTable[index].deleteNode(key)

    def compress(self, hashValue):
        if hashValue > 0:
            return ((3 * hashValue + 6) % 11) % len(self.hashTable)
        else:
            return -1 * ((3 * hashValue + 6) % 11) % len(self.hashTable)

    def keys(self):
        keys = []
        for index in self.hashTable:
            if index:
                keys += index.getKeys()
        return keys


if __name__ == "__main__":

    pass
