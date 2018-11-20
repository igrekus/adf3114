from adf4113ncountlatch import Adf4113NcountLatch
from pyexpect import expect


def test_creation():
    reg = Adf4113NcountLatch()

    expect(reg.hex).to_equal('000001')
    expect(reg.bin).to_equal('000000000000000000000001')
    expect(str(reg)).to_equal('<Adf3114NcountLatch>(bin=000000000000000000000001, hex=000001, dec=1)')


def test_a_counter():
    reg = Adf4113NcountLatch()
    expect(reg.bin).to_equal('000000000000000000000001')

    reg.a_counter = 10
    expect(reg.bin).to_equal('000000000000000000101001')
    reg.a_counter = 30
    expect(reg.bin).to_equal('000000000000000001111001')
    reg.a_counter = 60
    expect(reg.bin).to_equal('000000000000000011110001')
    reg.a_counter = 63
    expect(reg.bin).to_equal('000000000000000011111101')
    expect(reg.a_counter).to_equal(63)


def test_b_counter():
    reg = Adf4113NcountLatch()
    expect(reg.bin).to_equal('000000000000000000000001')

    reg.b_counter = 10
    expect(reg.bin).to_equal('000000000000101000000001')
    reg.b_counter = 100
    expect(reg.bin).to_equal('000000000110010000000001')
    reg.b_counter = 1000
    expect(reg.bin).to_equal('000000111110100000000001')
    reg.b_counter = 8191
    expect(reg.bin).to_equal('000111111111111100000001')
    expect(reg.b_counter).to_equal(8191)


def test_lock_detect_precision():
    reg = Adf4113NcountLatch()
    expect(reg.bin).to_equal('000000000000000000000001')

    reg.cp_gain = 3
    expect(reg.bin).to_equal('001000000000000000000001')
    reg.cp_gain = 2
    expect(reg.bin).to_equal('000000000000000000000001')
    reg.cp_gain = 1
    expect(reg.bin).to_equal('001000000000000000000001')
    reg.cp_gain = 0
    expect(reg.bin).to_equal('000000000000000000000001')


