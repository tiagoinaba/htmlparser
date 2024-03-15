class Prop(object):
    key: str
    value: bool | str

    def __init__(self, key: str, value: str = "") -> None:
        self.key = key
        self.value = value

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Prop):
            return self.key == __value.key and self.value == __value.value
        return False

    def __repr__(self) -> str:
        if self.value is str:
            return "Prop{key=" + self.key + ", value=" + self.value + "}"
        else:
            return "Prop{key=" + self.key + ", value=" + self.value.__repr__() + "}"
