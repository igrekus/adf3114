from adf4113funclatch import Adf4113FuncLatch
from pyexpect import expect


def test_creation():
    reg = Adf4113FuncLatch()

    expect(reg.hex).to_equal('000002')
    expect(reg.bin).to_equal('000000000000000000000010')
    expect(str(reg)).to_equal('<Adf3114FuncLatch>(bin=000000000000000000000010, hex=000002, dec=2)')


def test_counter_reset_toggle():
    reg = Adf4113FuncLatch()

    expect(reg.counter_reset).to_equal(0)
    reg.counter_reset = 1
    expect(reg.counter_reset).to_equal(1)
    expect(reg.bin).to_equal('000000000000000000000110')
    reg.counter_reset = 0
    expect(reg.counter_reset).to_equal(0)
    expect(reg.bin).to_equal('000000000000000000000010')


def test_set_power_down_mode():
    reg = Adf4113FuncLatch()
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.power_down_mode = 0
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.power_down_mode = 1
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.power_down_mode = 2
    expect(reg.bin).to_equal('000000000000000000001010')

    reg.power_down_mode = 3
    expect(reg.bin).to_equal('001000000000000000001010')

    expect(reg.power_down_mode).to_equal(3)


def test_set_muxout_control():
    reg = Adf4113FuncLatch()
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.muxout_control = 0
    expect(reg.bin).to_equal('000000000000000000000010')
    reg.muxout_control = 1
    expect(reg.bin).to_equal('000000000000000000010010')
    reg.muxout_control = 2
    expect(reg.bin).to_equal('000000000000000000100010')
    reg.muxout_control = 3
    expect(reg.bin).to_equal('000000000000000000110010')
    reg.muxout_control = 4
    expect(reg.bin).to_equal('000000000000000001000010')
    reg.muxout_control = 5
    expect(reg.bin).to_equal('000000000000000001010010')
    reg.muxout_control = 6
    expect(reg.bin).to_equal('000000000000000001100010')
    reg.muxout_control = 7
    expect(reg.bin).to_equal('000000000000000001110010')

    expect(reg.muxout_control).to_equal(7)


def test_pd_polarity():
    reg = Adf4113FuncLatch()
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.phase_detector_polarity = 1
    expect(reg.bin).to_equal('000000000000000010000010')

    reg.phase_detector_polarity = 0
    expect(reg.bin).to_equal('000000000000000000000010')


def test_charge_pump():
    reg = Adf4113FuncLatch()
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.charge_pump_mode = 1
    expect(reg.bin).to_equal('000000000000000100000010')

    reg.charge_pump_mode = 0
    expect(reg.bin).to_equal('000000000000000000000010')


def test_fastlock_mode():
    reg = Adf4113FuncLatch()
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.fastlock_mode = 2
    expect(reg.bin).to_equal('000000000000011000000010')

    reg.fastlock_mode = 1
    expect(reg.bin).to_equal('000000000000001000000010')

    reg.fastlock_mode = 0
    expect(reg.bin).to_equal('000000000000000000000010')


def test_timer_counter_mode():
    reg = Adf4113FuncLatch()
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.timer_counter_mode = 15
    expect(reg.bin).to_equal('000000000111100000000010')
    reg.timer_counter_mode = 13
    expect(reg.bin).to_equal('000000000110100000000010')
    reg.timer_counter_mode = 10
    expect(reg.bin).to_equal('000000000101000000000010')
    reg.timer_counter_mode = 7
    expect(reg.bin).to_equal('000000000011100000000010')
    reg.timer_counter_mode = 5
    expect(reg.bin).to_equal('000000000010100000000010')
    reg.timer_counter_mode = 1
    expect(reg.bin).to_equal('000000000000100000000010')
    reg.timer_counter_mode = 0
    expect(reg.bin).to_equal('000000000000000000000010')


def test_current_setting_1():
    reg = Adf4113FuncLatch()
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.current_setting_1 = 7
    expect(reg.bin).to_equal('000000111000000000000010')
    reg.current_setting_1 = 4
    expect(reg.bin).to_equal('000000100000000000000010')
    reg.current_setting_1 = 1
    expect(reg.bin).to_equal('000000001000000000000010')
    reg.current_setting_1 = 0
    expect(reg.bin).to_equal('000000000000000000000010')


def test_current_setting_2():
    reg = Adf4113FuncLatch()
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.current_setting_2 = 7
    expect(reg.bin).to_equal('000111000000000000000010')
    reg.current_setting_2 = 4
    expect(reg.bin).to_equal('000100000000000000000010')
    reg.current_setting_2 = 1
    expect(reg.bin).to_equal('000001000000000000000010')
    reg.current_setting_2 = 0
    expect(reg.bin).to_equal('000000000000000000000010')


def test_prescaler_value():
    reg = Adf4113FuncLatch()
    expect(reg.bin).to_equal('000000000000000000000010')

    reg.prescale_value = 3
    expect(reg.bin).to_equal('110000000000000000000010')
    reg.prescale_value = 2
    expect(reg.bin).to_equal('100000000000000000000010')
    reg.prescale_value = 1
    expect(reg.bin).to_equal('010000000000000000000010')
    reg.prescale_value = 0
    expect(reg.bin).to_equal('000000000000000000000010')

