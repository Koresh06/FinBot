from aiogram_dialog import DialogManager

from src.presentation.bot.lexicon.dictionaries import TYPES_TRANSACTION


async def getter_response_ai(dialog_manager: DialogManager, **kwargs) -> dict:
    result = dialog_manager.dialog_data["result_ai"]
    
    return {
        "type_tr": TYPES_TRANSACTION[result["type"]],
        "cat": result["category"],
        "total_sum": result["total_sum"],
        "comment": "-" if result["comment"] is None else result["comment"],
    }