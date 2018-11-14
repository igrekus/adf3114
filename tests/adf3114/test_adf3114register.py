from adf3114register import *
from pyexpect import expect


def test_creation():
    reg = Adf3114Register(123)

    expect(reg.hex).to_equal('00007B')
    expect(reg.bin).to_equal('000000000000000001111011')
    expect(str(reg)).to_equal('<Adf3114Register>(bin=000000000000000001111011, hex=00007B, dec=123)')


def test_bit_set():
    reg = Adf3114Register()
    reg.set_bits(list(range(24)))
    expect(reg.bin).to_equal('111111111111111111111111')


def test_bit_unset():
    reg = Adf3114Register(0b111111111111111111111111)

    reg.unset_bits(list(range(1, 24, 2)))
    expect(reg.bin).to_equal('010101010101010101010101')


def test_bit_toggle():
    reg = Adf3114Register(0b010101010101010101010101)

    reg.toggle_bits(list(range(0, 24, 2)))
    expect(reg.bin).to_equal('000000000000000000000000')


def test_bit_pattern():
    reg = Adf3114Register()

    reg.set_bit_pattern([[DB0, 1], [DB4, 1], [DB8, 1], [DB12, 1], [DB12, 0]])
    expect(reg.bin).to_equal('000000000000000100010001')


