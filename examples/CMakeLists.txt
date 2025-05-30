cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(lib_uart_examples)

add_subdirectory(multi_uart_demo)
add_subdirectory(uart_demo)
add_subdirectory(uart_streaming_demo)
