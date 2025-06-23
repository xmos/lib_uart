// Copyright 2015-2025 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <xs1.h>
#include <platform.h>
#include <uart.h>
#include <print.h>

on tile[0]: in  buffered port:32 p_uart_rx = XS1_PORT_8B;
on tile[1]: out buffered port:8 p_uart_tx  = XS1_PORT_8A;
on tile[0]: in  port p_uart_clk_tl0 = XS1_PORT_1A;
on tile[1]: in  port p_uart_clk_tl1 = XS1_PORT_1D;

on tile[0]: clock clk_uart_tl0 = XS1_CLKBLK_4;
on tile[1]: clock clk_uart_tl1 = XS1_CLKBLK_5;

// Found solution: IN 24.000MHz, OUT 1.843200MHz, VCO 2764.80MHz, RD  5, FD  576, FRAC 0.000 (m =   0, n =   0), OD  5, FOD   75, ERR -0.0ppm
#define APP_PLL_CTL_REG 0x0A023F04
#define APP_PLL_DIV_REG 0x8000004A
#define APP_PLL_FRAC_REG 0x00000000

// Set secondary (App) PLL control register safely.
void set_app_pll_init (tileref tile, int app_pll_ctl)
{
    // Disable the PLL 
    write_node_config_reg(tile, XS1_SSWITCH_SS_APP_PLL_CTL_NUM, (app_pll_ctl & 0xF7FFFFFF));
    // Enable the PLL to invoke a reset on the appPLL.
    write_node_config_reg(tile, XS1_SSWITCH_SS_APP_PLL_CTL_NUM, app_pll_ctl);
    // Must write the CTL register twice so that the F and R divider values are captured using a running clock.
    write_node_config_reg(tile, XS1_SSWITCH_SS_APP_PLL_CTL_NUM, app_pll_ctl);
    // Now disable and re-enable the PLL so we get the full 5us reset time with the correct F and R values.
    write_node_config_reg(tile, XS1_SSWITCH_SS_APP_PLL_CTL_NUM, (app_pll_ctl & 0xF7FFFFFF));
    write_node_config_reg(tile, XS1_SSWITCH_SS_APP_PLL_CTL_NUM, app_pll_ctl);
    // Wait for PLL to lock.
    delay_microseconds(500);
}

void gen_app_pll_clk (void) {
	// Initialise the AppPLL and get it running.
    set_app_pll_init (tile[0], APP_PLL_CTL_REG);
    // Write the fractional-n register
    write_node_config_reg(tile[0], XS1_SSWITCH_SS_APP_PLL_FRAC_N_DIVIDER_NUM, APP_PLL_FRAC_REG);
    // And then write the clock divider register to enable the output
    write_node_config_reg(tile[0], XS1_SSWITCH_SS_APP_CLK_DIVIDER_NUM, APP_PLL_DIV_REG);
    delay_milliseconds(1);
}

void rx_uart(streaming chanend c_rx) {
  // Generate the clock for the UART
  gen_app_pll_clk();
  // Configure the clock for the port and start uart rx
  configure_in_port(p_uart_rx, clk_uart_tl0);
  configure_clock_src(clk_uart_tl0, p_uart_clk_tl0);
  start_clock(clk_uart_tl0);
  multi_uart_rx_pins(c_rx, p_uart_rx, 8);
}

void tx_uart(chanend c_tx) {
  // Configure the clock for the port and start uart tx
  configure_out_port(p_uart_tx, clk_uart_tl1, 0);
  configure_clock_src(clk_uart_tl1, p_uart_clk_tl1);
  start_clock(clk_uart_tl1);
  multi_uart_tx_pins(c_tx, p_uart_tx, 1843200);
}

void rx_client(streaming chanend c_rx, client multi_uart_rx_if i_rx, chanend c_intertile) {
  i_rx.init(c_rx);

  size_t slot = 0;

  while(1) {
    c_intertile <: 1; // Signal that the rx client is ready
    select{
      case multi_uart_data_ready(c_rx, slot):
        uint8_t data;
        if (i_rx.read(slot, data) == UART_RX_VALID_DATA) {
          printhex(data);
        } else {
          printstrln("Rx data invalid");
        }
        break;
    }
  }
}

void tx_client(chanend c_tx, client multi_uart_tx_if i_tx, chanend c_intertile) {
  i_tx.init(c_tx);

  size_t slot = 0;
  uint8_t data = 0x55; // Example data to send
  unsigned int val;

  while (1) {
    c_intertile :> val; // Wait for signal from rx client
    if (i_tx.is_slot_free(slot)) {
      i_tx.write(slot, data);
      printstr("  ");
      data++; // Increment data for next transmission
    } else {
      printstrln("Tx buffer overflow");
    }
  }
}
    

int main(void)
{
  interface multi_uart_rx_if i_rx;
  streaming chan c_rx;
  chan c_intertile;
  chan c_tx;
  interface multi_uart_tx_if i_tx;

  par {
    on tile[0]: rx_uart(c_rx);
    on tile[0]: multi_uart_rx_buffer(i_rx, 1843200, 115200, UART_PARITY_NONE, 8, 1);
    on tile[0]: rx_client(c_rx, i_rx, c_intertile);

    on tile[1]: tx_uart(c_tx);
    on tile[1]: multi_uart_tx_buffer(i_tx, 1843200, 115200, UART_PARITY_NONE, 8, 1);
    on tile[1]: tx_client(c_tx, i_tx, c_intertile);
  }
  return 0;
}
