import abc
from .models import Authentication

class IConnection(abc.ABC):
    """
    """
    
    @abc.abstractmethod
    def connect(self, auth: Authentication) -> None:
        """
        """
    
    @abc.abstractmethod
    def get_all(self) -> list:
        """
        """
    
    @abc.abstractmethod
    def close(self) -> None:
        """
        """
