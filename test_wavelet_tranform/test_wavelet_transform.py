import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, with_timeout
import math
import random
import wave
import struct
from rich.progress import Progress


@cocotb.test()
async def test_start(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.fork(clock.start())

    dut.RSTB.value = 0
    dut.power1.value = 0
    dut.power2.value = 0
    dut.power3.value = 0
    dut.power4.value = 0

    await ClockCycles(dut.clk, 8)
    dut.power1.value = 1
    await ClockCycles(dut.clk, 8)
    dut.power2.value = 1
    await ClockCycles(dut.clk, 8)
    dut.power3.value = 1
    await ClockCycles(dut.clk, 8)
    dut.power4.value = 1

    await ClockCycles(dut.clk, 80)
    dut.RSTB.value = 1

    # Before starting first module test wait for sequence of falling then
    # running edge of 'o_active' signal.
    await with_timeout(FallingEdge(dut.o_active), 700, "us")
    await with_timeout(RisingEdge(dut.o_active), 700, "us")


@cocotb.test()
async def test_audio(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.fork(clock.start())

    # These should be held low by default
    dut.i_data_clk.value = 0
    dut.i_value.value = 0
    dut.i_select_output_channel.value = 0

    await RisingEdge(dut.clk)

    # output should be zero if prior values are zero
    assert dut.o_multiplexed_wavelet_out == 0

    # audio input setup
    audio_in = wave.open("./wavs/hello.wav")
    nframes = audio_in.getnframes()
    print("sending %d frames" % nframes)

    # values for switching the output channel
    channel_select = 0
    channel_select_counter = 200

    with Progress() as progress:
        test_progress = progress.add_task("[green]Processing...", total=nframes // 10)
        # process audio through dut
        for i in range(nframes // 10):
            await RisingEdge(dut.clk)

            frame = audio_in.readframes(1)
            (val,) = struct.unpack("h", frame)

            if channel_select_counter == 0:
                channel_select += 1
                dut.i_select_output_channel.value = channel_select % 7
                channel_select_counter = 200
            else:
                channel_select_counter -= 1

            if val > 0:
                dut.i_value.value = min(int((val / 32768.0 * 127)), 127)
            elif val < 0:
                dut.i_value.value = max(int((val / 32768.0 * 127)), -128)
            else:
                dut.i_value.value = 0

            # clk in data
            dut.i_data_clk.value = 1

            await RisingEdge(dut.clk)

            dut.i_data_clk.value = 0

            await RisingEdge(dut.clk)
            await RisingEdge(dut.clk)
            await RisingEdge(dut.clk)
            await RisingEdge(dut.clk)

            progress.update(test_progress, advance=1)


@cocotb.test()
async def test_modulated_sine(dut):
    with Progress() as progress:

        clock = Clock(dut.clk, 25, units="ns")
        cocotb.fork(clock.start())

        # These should be held low by default
        dut.i_data_clk.value = 0
        dut.i_value.value = 0
        dut.i_select_output_channel.value = 0

        await RisingEdge(dut.clk)

        # output should be zero if prior values are zero
        assert(dut.o_multiplexed_wavelet_out.value == 0)

        counter = 0
        channel_select = 0
        channel_select_counter = 200

        # process audio through dut
        test_progress = progress.add_task("[green]Processing...", total=5000)
        for i in range(5000):
            await RisingEdge(dut.clk)

            if channel_select_counter == 0:
                channel_select += 1
                dut.i_select_output_channel.value = channel_select % 7
                channel_select_counter = 200
            else:
                channel_select_counter -= 1

            dut.i_value.value = max(
                min(int(math.sin(0.1 * counter * (1 + 0.01 * counter)) * 128), 127),
                -128,
            )
            counter = 1 + counter

            # clk in data
            dut.i_data_clk.value = 1

            # wait two clock cycles before reading output
            # then test that the channel select is works correctly
            await RisingEdge(dut.clk)
            await RisingEdge(dut.clk)

            dut.i_data_clk.value = 0

            if (dut.i_select_output_channel.value == 0):
                assert(dut.o_multiplexed_wavelet_out == dut.uut.mprj.wrapped_wavelet_transform.wavelet_transform.fir_0.o_wavelet.value)
            if (dut.i_select_output_channel.value == 1):
                assert(dut.o_multiplexed_wavelet_out == dut.uut.mprj.wrapped_wavelet_transform.wavelet_transform.fir_1.o_wavelet.value)
            if (dut.i_select_output_channel.value == 2):
                assert(dut.o_multiplexed_wavelet_out == dut.uut.mprj.wrapped_wavelet_transform.wavelet_transform.fir_2.o_wavelet.value)
            if (dut.i_select_output_channel.value == 3):
                assert(dut.o_multiplexed_wavelet_out == dut.uut.mprj.wrapped_wavelet_transform.wavelet_transform.fir_3.o_wavelet.value)
            if (dut.i_select_output_channel.value == 4):
                assert(dut.o_multiplexed_wavelet_out == dut.uut.mprj.wrapped_wavelet_transform.wavelet_transform.fir_4.o_wavelet.value)
            # if (dut.i_select_output_channel.value == 5):
            #     assert(dut.o_multiplexed_wavelet_out == dut.uut.mprj.wrapped_wavelet_transform.wavelet_transform.fir_5.o_wavelet.value)
            # if (dut.i_select_output_channel.value == 6):
            #     assert(dut.o_multiplexed_wavelet_out == dut.uut.mprj.wrapped_wavelet_transform.wavelet_transform.fir_6.o_wavelet.value)


            await RisingEdge(dut.clk)
            await RisingEdge(dut.clk)
            await RisingEdge(dut.clk)
            await RisingEdge(dut.clk)
            progress.update(test_progress, advance=1)
