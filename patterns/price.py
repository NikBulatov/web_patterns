class Price(float):
    def __new__(cls, value):
        return float.__new__(cls, value)

    def __init__(self, value: float):
        self._value = value
        self.__currency = None

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.currency}{self.__str__()}" if self.currency else self.__str__()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, currency: str):
        self.__currency = currency
