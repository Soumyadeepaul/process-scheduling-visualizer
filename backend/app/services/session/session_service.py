# Handles session lifecycle.
import random
import string

class Session:
    __activeSession= set()
    
    def __generateId(self):
        length = 10
        return ''.join(random.choices(string.ascii_letters + string.punctuation + string.digits, k=length))
        
    def createSession(self):
        id=self.__generateId()
        while id in self.__activeSession:
            id=self.__generateId()
        self.__activeSession.add(id)
        return id
    
    def endSession(self, sessionId):
        self.__activeSession.discard(sessionId)
        