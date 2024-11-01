from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("The value should be an integer.")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"The value should not be "
                             f"less than {self.min_amount} "
                             f"and greater than {self.max_amount}.")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator:
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self, name: str,
            limitation_class: type(SlideLimitationValidator)
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                height=visitor.height,
                weight=visitor.weight
            )
            return True
        except (TypeError, ValueError):
            return False
