cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(app_multi_uart_demo)

set(APP_HW_TARGET XK-EVK-XU316)
set(APP_COMPILER_FLAGS -g -O3 -DMUART_RX_CHAN_COUNT=8 -DMUART_TX_CHAN_COUNT=8)
set(APP_DEPENDENT_MODULES "lib_uart")

set(XMOS_SANDBOX_DIR ${CMAKE_CURRENT_LIST_DIR}/../../..)

XMOS_REGISTER_APP()
