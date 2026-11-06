# ELRS VRx backpack

With an ExpressLRS VRx backpack wired to the True-D:

- **Channel:** when you change the VTX channel from the radio (ELRS Lua → VTX Administrator, or the
  VTX channel switch on the TX), the True-D switches to the same channel.  All 6 bands work.
- **Telemetry:** the top line of the main screen shows link and battery data instead of the pilot
  name, 2 s per page:

| page | example | contents |
|---|---|---|
| link | `LQ99 -67` | uplink link quality (%) and RSSI (dBm) |
| battery | `16.4V 45%` | voltage, and the remaining % from the flight controller when it is below 100 |
| capacity | `1234mAh` | capacity used, only with a current sensor |

It disappears 3 s after the last frame.  There are no alarms.  The OLED is not visible with the
goggles on, so this is for before and after the flight, or for a spotter.

## Setup

1. Flash a VRx backpack board (ESP8285 / ESP-01F based) with the ExpressLRS Configurator, in
   **Backpack** mode, target **TBS Fusion**, with your binding phrase.  It is a stock target; no
   custom backpack firmware is needed.
2. The ELRS TX module needs its own backpack (built in or external) with the same binding phrase.
   For telemetry, enable backpack telemetry in the ELRS Lua (Backpack folder).
3. Wire it to the True-D:

| backpack | True-D |
|---|---|
| TX | ATmega328P **PD0 / RXD** (TQFP-32 pin 30, Arduino D0) |
| GND | GND |
| 5 V or 3.3 V, depending on the board | the True-D's 5 V rail, or a 3.3 V regulator |
| RX | not connected (receive only) |

4. Settings → `ELRS:ON` (default OFF).

**D0 is also the USB serial line used for flashing.**  Check whether your board has a series
resistor between the USB chip and pin 30, and connect the backpack on the ATmega side of it.
Disconnect or unpower the backpack while flashing over USB, otherwise the two drivers fight.  The
ESP's 3.3 V output is enough for the ATmega's input at 5 V.

## Notes

- **UART:** 500 kbaud, 8N1 (the TBS Fusion target's rate).  Frames with a bad CRC, a wrong length or a
  UART error are dropped; a noisy line cannot flood the CPU.
- **During a scan, search or calibration** a channel command waits until the sweep is done.
- **RX TUNE** measures a channel change from the backpack 0.8 s later, once the VTX has arrived (ELRS
  sends it only while disarmed).
- **Power-up:** the backpack sends the current channel once, 1–1.5 s after power-up.  If the module did
  not follow, send the VTX settings again from the radio.
- **Status:** implemented and reviewed, not yet tested with a real backpack.
