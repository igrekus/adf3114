from adf3114refcountlatch import Adf3114RefcountLatch
from pyexpect import expect


def test_creation():
    reg = Adf3114RefcountLatch()

    expect(reg.hex).to_equal('000000')
    expect(reg.bin).to_equal('000000000000000000000000')
    expect(str(reg)).to_equal('<Adf3114RefcountLatch>(bin=000000000000000000000000, hex=000000, dec=0)')


def test_antibacklashe_pulse_width():
    reg = Adf3114RefcountLatch()
    expect(reg.bin).to_equal('000000000000000000000000')

    reg.antibacklash_pulse_width = 3
    expect(reg.bin).to_equal('000000110000000000000000')
    reg.antibacklash_pulse_width = 2
    expect(reg.bin).to_equal('000000100000000000000000')
    reg.antibacklash_pulse_width = 1
    expect(reg.bin).to_equal('000000010000000000000000')
    reg.antibacklash_pulse_width = 0
    expect(reg.bin).to_equal('000000000000000000000000')


def test_reference_counter():
    reg = Adf3114RefcountLatch()
    expect(reg.bin).to_equal('000000000000000000000000')

    reg.reference_counter = 100
    expect(reg.bin).to_equal('000000000000000110010000')
    reg.reference_counter = 1000
    expect(reg.bin).to_equal('000000000000111110100000')
    reg.reference_counter = 10000
    expect(reg.bin).to_equal('000000001001110001000000')
    reg.reference_counter = 16383
    expect(reg.bin).to_equal('000000001111111111111100')
    expect(reg.reference_counter).to_equal(16383)


def test_lock_detect_precision():
    reg = Adf3114RefcountLatch()
    expect(reg.bin).to_equal('000000000000000000000000')

    reg.lock_detect_precision = 1
    expect(reg.bin).to_equal('000100000000000000000000')
    reg.lock_detect_precision = 0
    expect(reg.bin).to_equal('000000000000000000000000')


def test_sync_mode():
    reg = Adf3114RefcountLatch()
    expect(reg.bin).to_equal('000000000000000000000000')

    reg.sync_mode = 3
    expect(reg.bin).to_equal('011000000000000000000000')
    reg.sync_mode = 2
    expect(reg.bin).to_equal('010000000000000000000000')
    reg.sync_mode = 1
    expect(reg.bin).to_equal('001000000000000000000000')
    reg.sync_mode = 0
    expect(reg.bin).to_equal('000000000000000000000000')


