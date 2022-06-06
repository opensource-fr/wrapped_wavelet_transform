PWDD := $(shell pwd)
BLOCKS := $(shell basename $(PWDD))

# ---- Include Partitioned Makefiles ----

CONFIG = caravel_user_project

export COCOTB_REDUCED_LOG_FMT=1
export PYTHONPATH := $(DESIGNS)/verilog/rtl/wavelet_transform/test
export LIBPYTHON_LOC=$(shell cocotb-config --libpython)


include $(MCW_ROOT)/verilog/dv/make/env.makefile
include $(MCW_ROOT)/verilog/dv/make/var.makefile
include $(MCW_ROOT)/verilog/dv/make/cpu.makefile
include $(MCW_ROOT)/verilog/dv/make/sim.makefile

coco_test: wavelet_transform.hex
	rm -rf sim_build/
	mkdir sim_build/

	iverilog -Ttyp -DFUNCTIONAL -DSIM -DCOCOTB_SIM -DUSE_POWER_PINS -DUNIT_DELAY=#1 \
	-f$(VERILOG_PATH)/includes/includes.rtl.caravel \
	-f$(USER_PROJECT_VERILOG)/includes/includes.rtl.$(CONFIG) -o sim_build/sim.vvp wavelet_transform_tb.v

	TESTCASE=test_start,test_modulated_sine MODULE=test_wavelet_transform vvp -M $$(cocotb-config --prefix)/cocotb/libs -m libcocotbvpi_icarus sim_build/sim.vvp
	# TESTCASE=test_start,test_audio MODULE=test_wavelet_transform vvp -M $$(cocotb-config --prefix)/cocotb/libs -m libcocotbvpi_icarus sim_build/sim.vvp
	! grep failure results.xml

coco_test_gl: wavelet_transform.hex
	rm -rf sim_build/
	mkdir sim_build/

	iverilog -Ttyp -DFUNCTIONAL -DSIM -DUSE_POWER_PINS -DUNIT_DELAY=#1 \
	-f$(VERILOG_PATH)/includes/includes.rtl.caravel \
	-f$(USER_PROJECT_VERILOG)/includes/includes.gl.$(CONFIG) -o sim_build/sim.vvp wavelet_transform_tb.v

	TESTCASE=test_start,test_wavelet_gl MODULE=test_wavelet_transform vvp -M $$(cocotb-config --prefix)/cocotb/libs -m libcocotbvpi_icarus sim_build/sim.vvp
	! grep failure results.xml
