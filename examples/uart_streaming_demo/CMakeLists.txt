cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(uart_streaming_demo)

set(APP_HW_TARGET XK-EVK-XU316)
set(APP_COMPILER_FLAGS -g -O2 -save-temps)
set(APP_DEPENDENT_MODULES "lib_uart")
set(APP_XSCOPE_SRCS src/uart.xscope)

set(XMOS_SANDBOX_DIR ${CMAKE_CURRENT_LIST_DIR}/../../..)

XMOS_REGISTER_APP()
