from abc import ABC, abstractmethod

class Observador(ABC):

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def subscribe(self):
        pass
    
    @abstractmethod
    def unsubscribe(self):
        pass

    @abstractmethod
    def join(self):
        pass
    
    @abstractmethod
    def leave(self):
        pass
    
    @abstractmethod
    def criarMao(self):
        pass
    
    @abstractmethod
    def adicionarPonto(self):
        pass

    @abstractmethod
    def adicionarRodada(self):
        pass
    @abstractmethod
    def resetarRodada(self):
        pass
    @abstractmethod
    def limparCartasJogadas(self):
        pass
    @abstractmethod
    def resetarMao(self):
        pass
    