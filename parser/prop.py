from htmlparser.errors.parser_error import UnknownPropError, UnknownPropValueError

KNOWN_PROPS = ["background", "color"]
KNOWN_PROP_VALUES = {
        "background": ["white", "black", "green", "blue", "red",],
        "color": ["white", "black", "green", "blue", "red",],
        }

class Prop(object):
    key: str
    value: str

    def __init__(self, key: str, value: str = "") -> None:
        if key not in KNOWN_PROPS:
            raise UnknownPropError("Couldn't find prop with key '{key}'".format(key=key))
        self.key = key
        self.value = value

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Prop):
            return self.key == __value.key and self.value == __value.value
        return False

    def setValue(self, value):
        if value not in KNOWN_PROP_VALUES[self.key]:
            raise UnknownPropValueError("Value '{value}' not found for key '{key}'.".format(value=value, key=self.key))
        self.value = value

    def __repr__(self) -> str:
        if self.value is str:
            return "Prop{key=" + self.key + ", value=" + self.value + "}"
        else:
            return "Prop{key=" + self.key + ", value=" + self.value.__repr__() + "}"
