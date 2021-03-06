# The TARGET variable determines what target system the application is
# compiled for. It either refers to an XN file in the source directories
# or a valid argument for the --target option when compiling.

TARGET = SLICEKIT-L16

# The APP_NAME variable determines the name of the final .xe file. It should
# not include the .xe postfix. If left blank the name will default to
# the project name

APP_NAME =

# The flags passed to xcc when building the application
# You can also set the following to override flags for a particular language:
#
#    XCC_XC_FLAGS, XCC_C_FLAGS, XCC_ASM_FLAGS, XCC_CPP_FLAGS
#
# If the variable XCC_MAP_FLAGS is set it overrides the flags passed to
# xcc for the final link (mapping) stage.

COMMON_FLAGS = -save-temps -O2 -report $(EXTRA_FLAGS)

baud ?= 115200
parity ?= UART_PARITY_NONE

XCC_FLAGS_smoke = $(COMMON_FLAGS) -DSMOKE_TEST=1 -DBAUD=$(baud) -DSTOPBITS=$(stop_bits)
XCC_FLAGS_full  = $(COMMON_FLAGS) -DFULL_TEST=1 -DBAUD=$(baud) -DSTOPBITS=$(stop_bits)

# The USED_MODULES variable lists other module used by the application.

USED_MODULES = lib_uart lib_xassert lib_logging

test: bin/app_uart_test.xe
	$(info Baud: $(baud))
	xsim bin/app_uart_test.xe --xscope "-offline uart_test.xmt" 

#=============================================================================
# The following part of the Makefile includes the common build infrastructure
# for compiling XMOS applications. You should not need to edit below here.

XMOS_MAKE_PATH ?= ../..
include $(XMOS_MAKE_PATH)/xcommon/module_xcommon/build/Makefile.common
