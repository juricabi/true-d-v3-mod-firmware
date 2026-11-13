# The goggle bay (MOD 1.17)

The three channel pins of the 9-pin bay (pins 1, 2, 3) are how a goggle tells a module which channel to use.  MOD
1.17 follows the usual ways goggles do that.  Choose the one your goggle uses in **Settings → `BAY`** (OK steps
through them; applied at once and stored).

| your goggle | goggle setting | True-D `BAY` | tested |
|---|---|---|---|
| **Orqa FPV.One** | Receiver module **rapidFIRE** | **`ORQA`** | yes: the goggle sets channel and band, its OSD shows the module's channel and follows the True-D's own buttons |
| **Orqa FPV.One** | Receiver module **other** | `1-8` or `STEP` | yes |
| Fat Shark goggles with channel buttons | | `STEP` (as stock) or `1-8` | stock STEP: yes |
| HDZero Goggle / Goggle 2 with the 3-wire bay mod (below) | module type **rapidFIRE** | `RAPIDFIRE` (default) | not yet on hardware |
| ExpressLRS VRx backpack, "Rapidfire" target, wired to the bay pins | | `RAPIDFIRE` | not yet on hardware |
| goggles that hold static channel pins (HDZero type Switch, …) | | `1-8` | not yet on hardware |

- **`RAPIDFIRE`** (default): ImmersionRC's rapidFIRE SPI commands (band, channel, checksummed, each sent 3 times).
  A band or channel counts when two copies agree.  It never drives a bay pin and has no pull-ups.
- **`ORQA`**: the Orqa FPV.One's rapidFIRE mode.  The Orqa clocks much faster (~6 µs per level) and asks the module
  for its channel every 100 ms; a module that does not answer is set back to the goggle's channel.  `ORQA` follows
  that clock and answers, so the goggle and the module stay in step both ways.  `RAPIDFIRE` cannot follow the Orqa.
- **`1-8`**: the 3-bit code on pins 1-3 (pin 1 = the lowest bit) is channel 1-8 of the True-D's current band.
- **`STEP`**: the code as up / down steps, as the stock firmware does for Fat Shark buttons.
- **`BAY CLK:D11`** (the next Settings line): the pin order of `RAPIDFIRE` and `ORQA`.  Leave it at `D11`, the order
  of the bay connector.  `D13` is only for a sender wired by hand the other way round.

**A wrong pair of settings cannot damage anything.**  A goggle on "other" with `RAPIDFIRE` / `ORQA`, or the Orqa's
rapidFIRE with `RAPIDFIRE`, does nothing.  The Orqa's rapidFIRE with `1-8` / `STEP` can move the channel (its
rapidFIRE start holds all three pins low for 1 s, which `1-8` reads as channel 1): set the two to match.

## What the module does on the bay pins

- `RAPIDFIRE`, `1-8` and `STEP` **never drive a bay pin**: the pins are inputs from the firmware's first
  instruction.  `1-8`, `STEP` and `ORQA` switch on the ATmega's internal pull-ups (~35 kΩ to 5 V).
- `ORQA` **pulls pin 2 (DATA) low, never high**, and only right after the goggle has asked a valid question.  Pins 1
  and 3 are never outputs.
- **The stock bootloader** (the part that lets you flash over USB) drives pin 3 at 5 V for 0.1 s and then low for
  ~1.3 s at every power-up, before the firmware starts, whatever firmware is on the module.  It has always done that
  in every goggle; Fat Shark-style bays are built for 5 V modules.  It can be replaced by a no-LED bootloader with
  a second Arduino as the programmer (optional): [bootloader.md](bootloader.md).
- **The stock firmware 3.9D and MOD 1.15** drive pin 3 at 5 V for ~6 s at every power-up (their goggle link).
  MOD 1.17 does not.

## HDZero with the 3-wire bay mod: read this first

A stock HDZero goggle does not connect the bay's channel pins at all: any module is safe in it, but the goggle cannot
change the module's channel.  The 3-wire mod (pkendall64's analog module control) solders three wires from the bay's
pins 1-3 to the goggle's processor.  Those processor pins run at 3.3 V (possibly 1.8 V) and are also the goggle's
WiFi bus.  The usual rapidFIRE / SteadyView modules only listen on them; the True-D is a 5 V module whose bootloader
drives pin 3 at 5 V at power-up.  So with a True-D:

- put a **4.7 kΩ resistor in each of the three wires** (3.3-6.8 kΩ works), at the goggle end, with the shortest
  possible wire between the goggle pin and the resistor;
- check that the goggle's bank is **3.3 V** (a 1.8 V bank cannot drive the True-D's 5 V inputs without a level
  shifter);
- use **MOD 1.17** with `BAY:RAPIDFIRE`; never the stock firmware, MOD 1.15 or 1.16 in a wired bay;
- **never plug the True-D's USB in, or flash it, while it sits in a wired bay**; insert and remove it with the
  goggle off.

The True-D itself has no resistors on these pins.  With 4.7 kΩ the bootloader's pulse puts about 0.3-0.6 mA into
the goggle pin, which is harmless; without them it is tens of mA.

## Orqa FPV.One

- `BAY:ORQA` with Receiver module rapidFIRE gives full control from the goggle (channel with a short press, band
  with a long press) and the module's channel on the goggle's OSD.  `BAY:1-8` / `STEP` work with the goggle's
  "other" module type.
- In `ORQA` the module pauses for about 1 ms ten times a second to answer the goggle: the diversity takes ~1 % fewer
  samples meanwhile, and an ELRS backpack's frames on D0 that fall into such a pause are lost (it repeats them).
- The Orqa's stock bay cover is made for the rapidFIRE module.  A printable cover made for the Furious / AKK module
  shape: [FPV ORQA Module Cover - FuriousFPV AKK](https://www.thingiverse.com/thing:4057038) by HotBrotato (CC BY;
  the author checked it with an AKK module; lay the front face flat on the build plate before slicing).
