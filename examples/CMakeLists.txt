cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(lib_uart_examples)

add_subdirectory(app_multi_uart_demo)
add_subdirectory(app_uart_demo)
add_subdirectory(app_uart_streaming_demo)
