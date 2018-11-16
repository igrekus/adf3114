from adf3114registerbase import *
from pyexpect import expect


def test_creation():
    reg = Adf3114RegisterBase(123)

    expect(reg.hex).to_equal('00007B')
    expect(reg.bin).to_equal('000000000000000001111011')
    expect(str(reg)).to_equal('<Adf3114RegisterBase>(bin=000000000000000001111011, hex=00007B, dec=123)')


def test_bit_set():
    reg = Adf3114RegisterBase()
    reg.set_bits(tuple(range(24)))
    expect(reg.bin).to_equal('111111111111111111111111')


def test_bit_unset():
    reg = Adf3114RegisterBase(0b111111111111111111111111)

    reg.unset_bits(tuple(range(1, 24, 2)))
    expect(reg.bin).to_equal('010101010101010101010101')


def test_bit_toggle():
    reg = Adf3114RegisterBase(0b010101010101010101010101)

    reg.toggle_bits(list(range(0, 24, 2)))
    expect(reg.bin).to_equal('000000000000000000000000')


def test_bit_pattern():
    reg = Adf3114RegisterBase()
    bits = (DB21, DB3)
    mode = {
        0: [0, 0],
        1: [0, 0],
        2: [0, 1],
        3: [1, 1]
    }

    reg.set_bit_pattern(3, bits, mode)
    expect(reg.bin).to_equal('001000000000000000001000')


