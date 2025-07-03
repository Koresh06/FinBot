from typing import Any, Iterable, TypeVar, Generic, Optional
from abc import ABC, abstractmethod


Entity = TypeVar("Entity")

class GenericUseCase(ABC, Generic[Entity]):
    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Entity:
        """Execute a use case & return a generic type"""

class UseCaseNoReturn(ABC):
    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> None:
        """Execute a use case without returning anything"""

class UseCaseOneEntity(GenericUseCase[Optional[Entity]], ABC):
    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Optional[Entity]:
        """Execute a use case & return a single entity object"""

class UseCaseMultipleEntities(GenericUseCase[Iterable[Entity]], ABC):
    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Iterable[Entity]:
        """Execute a use case & return multiple entity objects"""