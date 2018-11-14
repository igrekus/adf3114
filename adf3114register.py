# 0000_0000_0000_00xx
# управляют режимом работы регистра
DB0, \
DB1, \
DB2, \
DB3, \
DB4, \
DB5, \
DB6, \
DB7, \
DB8, \
DB9, \
DB10, \
DB11, \
DB12, \
DB13, \
DB14, \
DB15, \
DB16, \
DB17, \
DB18, \
DB19, \
DB20, \
DB21, \
DB22, \
DB23 = range(24)
C1 = DB0
C2 = DB1


class Adf3114Register:

    def __init__(self, bits=0):
        self._bits = bits

    def __str__(self):
        return f'<{self.__class__.__name__}>(bin={self._bits:024b}, hex={self._bits:06X}, dec={self._bits})'

    def nth_bit(self, n):
        return int(bool(self._bits & (1 << n)))

    def set_nth_bit(self, n):
        self._bits |= (1 << n)

    def set_bits(self, numbers: list):
        for n in numbers:
            self.set_nth_bit(n)

    def set_nth_bit_to(self, state: list):
        """
        :param state: [n, val]
        :return:
        """
        n, val = state
        if val:
            self.set_nth_bit(n)
        else:
            self.unset_nth_bit(n)

    def set_bit_pattern(self, pattern: list):
        """
        :param pattern: [ [n, state] ... ]
        :return:
        """
        for state in pattern:
            self.set_nth_bit_to(state)

    def unset_nth_bit(self, n):
        if not self.nth_bit(n):
            return
        self._bits ^= (1 << n)

    def unset_bits(self, numbers: list):
        for n in numbers:
            self.unset_nth_bit(n)

    def toggle_nth_bit(self, n):
        self.unset_nth_bit(n) if self.nth_bit(n) else self.set_nth_bit(n)

    def toggle_bits(self, numbers: list):
        for n in numbers:
            self.toggle_nth_bit(n)

    @property
    def hex(self):
        return f'{self._bits:06X}'

    @property
    def bin(self):
        return f'{self._bits:024b}'
