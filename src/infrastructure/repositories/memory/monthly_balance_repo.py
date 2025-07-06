from dataclasses import dataclass, field

from src.domain.entities.monthly_balance import MonthlyBalance
from src.domain.repositories.monthly_balance_interface import IMonthlyBalanceRepository


@dataclass
class MonthlyBalanceMemoryRepositoryImpl(IMonthlyBalanceRepository):
    items: list[MonthlyBalance] = field(default_factory=list)
    counter: int = 1

    def snapshot(self):
        import copy
        return copy.deepcopy(self.items)

    def restore(self, state):
        self.items = state

    async def get_current_by_item_id(self, tg_id: int, year: int, month: int) -> MonthlyBalance | None:
        for item in self.items:
            if item.tg_id == tg_id and item.year == year and item.month == month:
                return item
            
        return None
    
    async def create(self, new_item: MonthlyBalance) -> MonthlyBalance:
        new_item.id = self.counter
        self.counter += 1
        self.items.append(new_item)

        return new_item
        

    async def update(self, update_data: MonthlyBalance) -> None:
        for index, item in enumerate(self.items):
            if item.id == update_data.id:
                self.items[index] = update_data
                return
        raise ValueError(f"item with item_id={update_data.id} not found")