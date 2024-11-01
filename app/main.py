from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> object:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: object) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.public_name} must be int")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"{self.public_name} must be between "
                f"{self.min_amount} and {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            (
                self.limitation_class
                (
                    age=visitor.age,
                    weight=visitor.weight,
                    height=visitor.height
                )
            )
            return True
        except ValueError:
            return False
