set(LIB_NAME lib_uart)
set(LIB_VERSION 3.2.0)
set(LIB_INCLUDES api src)
set(LIB_COMPILER_FLAGS -O3 -Wall -Werror)
set(LIB_DEPENDENT_MODULES "lib_xassert(4.3.1)" "lib_gpio(2.2.0)" "lib_logging(3.3.1)")
set(LIB_OPTIONAL_HEADERS uart_rx_conf.h)

XMOS_REGISTER_MODULE()
