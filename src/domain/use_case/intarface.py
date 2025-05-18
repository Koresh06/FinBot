from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Iterable


Entity = TypeVar("Entity") 


class GenericUseCase(ABC, Generic[Entity]):
    @abstractmethod
    def execute(self) -> Entity:
        """Execute a use case & return a generic type"""


class UseCaseOneEntity(GenericUseCase[Entity], ABC):
    @abstractmethod
    def execute(self) -> Entity:
        """Execute a use case & return a single entity object"""


class UseCaseMultipleEntities(GenericUseCase[Iterable[Entity]], ABC):
    @abstractmethod
    def execute(self) -> Iterable[Entity]:
        """Execute a use case & return multiple entity objects"""
