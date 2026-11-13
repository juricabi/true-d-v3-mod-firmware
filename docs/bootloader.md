# Optional: the no-LED bootloader

**You do not need this to use the firmware.**  It removes the last thing on the True-D that pushes 5 V into a bay
pin, as extra safety for goggles whose processor pins are wired straight to the bay (the HDZero 3-wire mod).  It
needs a second Arduino as a programmer and one thin wire soldered inside the module.  Done once on one unit
(2026-11-13); read it all before you start.

## Why

The **bootloader** is the small program that lets you flash firmware over USB.  The stock one (Arduino's
ATmegaBOOT) blinks the "LED" pin D13 at every power-up: **bay pin 3 at 5 V for 0.1 s, then low for ~1.3 s**, before
the firmware starts, whatever firmware is installed.  Fat Shark-style bays have always lived with that.  In a goggle
whose 3.3 V processor pins are wired to the bay it is the one remaining 5 V drive; 4.7 kΩ resistors in the mod's
wires already make it harmless ([goggle-bay.md](goggle-bay.md)).  The no-LED bootloader removes it at the source.

**What changes:** exactly three instructions of the stock bootloader (the LED on, off, and D13 as an output) become
"do nothing".  Same address, same 57600 baud, same protocol, same timing: XLoader and avrdude flash firmware exactly
as before, and the fuses stay as they are.

**It cannot be done over USB.**  The stock bootloader's lock bits (0x0F) forbid any software from rewriting the
bootloader, and the USB adapter can only pulse RESET, not hold it.  A programmer on the ISP pins is the only way.

## What you need

- A **5 V Arduino** as the programmer: Uno, Nano or Mega 2560.  Not a 3.3 V board (ESP32, RP2040, …) without a level
  shifter.
- The Arduino IDE (to put the `ArduinoISP` sketch on it) and **avrdude 8.x**
  (https://github.com/avrdudes/avrdude/releases; XLoader's avrdude is too old for this).
- A thin wire (enamelled or 30 AWG), a fine soldering tip, a multimeter, jumper wires.
- A spare **100 nF ceramic capacitor** (0402 or 0603) in case C10 breaks (below).
- From this folder: [`bootloader/TrueD-MOD-1.17-noled-bootloader.hex`](../bootloader/TrueD-MOD-1.17-noled-bootloader.hex)
  (the no-LED bootloader + MOD 1.17 in one image).

## 1. Open the module and find RESET (C10)

1. Remove the **small screw on the front**; the module opens in two halves.
2. On the board with the ATmega328P, find the small capacitor **C10 near the ATmega chip**.  It is the USB
   adapter's auto-reset capacitor: one pad goes to the USB chip, the other to the ATmega's RESET.
3. Check it, with the module on USB (meter on DC volts, black probe on the USB socket's metal shell): **one pad of
   C10 reads about 5 V (4.5-5 V) — that is RESET**; the other reads about 3.3 V (the USB chip's side).  No other
   capacitor there has that 5 V / 3.3 V pair.
4. Unplug USB.  Solder one thin wire to the **5 V pad of C10**.  Keep the solder joint small and do not pull on the
   wire: C10 is tiny.  (The ATmega itself is in a very small leadless package; do not try to solder to it.)

## 2. The programmer

1. Arduino IDE: File → Examples → 11.ArduinoISP → **ArduinoISP**, upload it to the programmer Arduino.
2. Wire it to the True-D.  The True-D stays **out of the goggle**, powered by **its own USB cable** on the same PC;
   the programmer's 5V pin stays **unconnected** (one supply only, common ground).

| signal | Uno / Nano | Mega 2560 | True-D |
|---|---|---|---|
| RESET | D10 | D10 | the wire on C10 |
| MOSI | D11 | D51 | bay pin 1 |
| MISO | D12 | D50 | bay pin 2 |
| SCK | D13 | D52 | bay pin 3 |
| GND | GND | GND | bay pin 7 |

Bay pins: pin 7 is GND (it beeps to an antenna connector's metal body), pin 9 next to it is +5 V, **pin 1 is at
the other end**.  If an Uno / Nano programmer does not answer avrdude, put a 10 µF capacitor between its own RESET
and GND (Arduino's ArduinoISP instructions).

## 3. The commands, in this order

`COM3` is an example: use the programmer's port.  With avrdude 7.x write `-c arduino` instead of
`-c arduino_as_isp`.  **Never `-c stk500v1` or `-c avrisp`** with ArduinoISP: the EEPROM (your calibration) would be
read and written at the wrong addresses.

```
set P=-c arduino_as_isp -b 19200 -P COM3 -p m328p
```

(That is the Windows command prompt; every command below is `avrdude` followed by these options.)

1. **Connection.**  `avrdude %P% -U signature:r:-:h` must print `0x1e,0x95,0xf`.  Anything else: stop, check the
   wiring (MOSI and SCK swapped does no harm; swap them and try again).
2. **Fuses and lock, read only.**
   `avrdude %P% -U lfuse:r:-:h -U hfuse:r:-:h -U efuse:r:-:h -U lock:r:-:h`
   Expected: `0xff`, **`0xda`**, `0xfd`, `0xcf` (= 0x0F).  **If hfuse is not 0xda, stop.**  Never write a fuse.
3. **Backup.**  `avrdude %P% -U flash:r:flash-backup.hex:i -U eeprom:r:eeprom-backup.hex:i`, then read the EEPROM a
   second time into another file and compare: they must be identical.  The EEPROM holds your calibration and
   settings, and the next step erases it.
4. **Erase and write** the no-LED bootloader with MOD 1.17:
   `avrdude %P% -e -U flash:w:TrueD-MOD-1.17-noled-bootloader.hex:i`  (verified by avrdude)
5. **Settings back:** `avrdude %P% -U eeprom:w:eeprom-backup.hex:i`  (verified)
6. **Protect the bootloader:** `avrdude %P% -U lock:w:0xef:m`.  It reads back as `0xef`.  This keeps a USB upload
   from ever overwriting the bootloader.
7. **Test over USB:** disconnect the programmer, flash `TrueD-MOD-1.17.hex` over USB as usual (XLoader or avrdude
   at 57600).  It must upload and verify: the new bootloader works.

If step 4 or 5 fails, nothing is lost as long as the programmer is connected: run it again.  To go back to the
stock bootloader, write Arduino's `ATmegaBOOT_168_atmega328.hex` (Arduino AVR core, `bootloaders/atmega/`) the same
way, with MOD 1.17 or the stock firmware.

## 4. Closing up, and C10

On the first unit **C10 broke when the wire was taken off**.  The module still ran normally, but flashing over USB
stopped working (`not in sync`: the PC could no longer reset the chip).  A new 100 nF capacitor in C10's place fixed
it.  So either leave the wire on, cut short and insulated, or remove it very gently with the iron, not by pulling.

Then close the module.  Keep the 4.7 kΩ resistors in an HDZero 3-wire mod anyway: they also protect against a
module on USB in the bay, other firmware, and a programmer connected by mistake.

## Files

| file | what | SHA-256 |
|---|---|---|
| `bootloader/TrueD-MOD-1.17-noled-bootloader.hex` | the no-LED bootloader + MOD 1.17, one image for step 4 | `882b01bc…a1a3` (file) |
| `bootloader/ATmegaBOOT_328_noled.hex` | the no-LED bootloader alone (0x7800-0x7F9D, 1950 bytes) | `68d65339…d54a` (file) |
| `bootloader/mkpatch.py` | makes the no-LED bootloader from Arduino's own `ATmegaBOOT_168_atmega328.hex` (checks it first) | |
| `bootloader/ATmegaBOOT_168-noled.diff` | the same change in the bootloader's source code | |

Full hashes: `bootloader/SHA256SUMS`.  The bootloader is GPL v2 (see [NOTICE.md](../NOTICE.md)).
