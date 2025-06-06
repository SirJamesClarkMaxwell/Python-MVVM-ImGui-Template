from dataclasses import dataclass,field
from typing import List, Optional, Any, Callable, Dict,Self,Union
from src.core.logger import AppLogger

@dataclass(order=True)
class ShortcutBinding:
    id: str = field(default="",compare=True)
    function: Callable[..., Any] = field(default=None)
    pre_process: Optional[Callable[[Any], Any]] = field(default=None)
    post_process: Optional[Callable[[Any, Any], None]] = field(default=None)

@dataclass(order=True)
class Shortcut:
    """
    Shortcut class represents a keyboard shortcut in the application.
    It contains information about the shortcut's keys, category, context, and description.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    id: str = field(compare=True)
    keys: List[str]
    category: str
    context: List[str]
    description: str
    enable_threading: bool
    bingings: ShortcutBinding = field(default_factory=ShortcutBinding,repr=False)

    def __call__(self, app: Any) -> None:
        AppLogger.get().info(f"Executing shortcut '{self.id}'")

        if not self.bingings.function:
            raise ValueError("Missing target function")

        args, kwargs = (), {}

        if self.bingings.pre_process:
            args = [self.bingings.pre_process(app)]

        result = self.bingings.function(app,*args, **kwargs)

        if self.bingings.post_process:
            self.bingings.post_process(app, result)


    def __eq__(self, other: Union[Self, ShortcutBinding, list[Self]]) -> bool:
        if isinstance(other, Shortcut):
            return self.id == other.id
        elif isinstance(other, ShortcutBinding):
            return self.id == other.id
        elif isinstance(other, list):
            return any(self.id == item.id for item in other if isinstance(item, Shortcut))
        return NotImplemented


    def __ne__(self, other: Union[Self, ShortcutBinding, list[Self]]) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def to_dict(self):
        return {
            "id": self.id,
            "keys": self.keys,
            "category": self.category,
            "context": self.context,
            "description": self.description,
            "enable_threading": self.enable_threading,
        }
