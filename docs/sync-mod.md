# Sync mod (LM1881)

Without the mod, a diversity switch lands at a random point of the picture.  The two receivers'
video differs slightly in level, so a switch can show as a short bright streak that fades over a
few lines.  With a sync separator, the firmware times the switches:

- a **quality switch** (the other receiver is better on average, the picture is still fine) waits for
  the next vertical sync (at most 16.7 ms NTSC / 20 ms PAL) and lands in the vertical blanking, where
  the goggle has time to settle;
- a **deep-fade switch** waits only for the next line sync (at most 64 µs).

Without the signals (no mod, or the picture already broken) it switches at once, as before.  No
firmware change is needed: the same image works with and without the mod.  On the main screen `S`
shows the line sync and `V` the vertical sync when they arrive.

## Parts (about €2–3)

| part | value | connection |
|---|---|---|
| LM1881 (LM1881N DIP-8 / LM1881M SOIC-8), or EL4581 | — | pin 8 +5 V, pin 4 GND |
| capacitor | 0.1 µF | **switched** video output (the video to the goggle) → pin 2 |
| resistor | 680 kΩ | pin 6 → GND |
| capacitor | 0.1 µF | pin 6 → GND |
| capacitor | 0.1 µF | pin 8 → GND, at the chip |
| wire | — | pin 1 (composite sync out) → ATmega328P **PD2 / INT0** (TQFP pin 32, Arduino D2) |
| wire | — | pin 3 (vertical sync out) → ATmega328P **PD3 / INT1** (TQFP pin 1, Arduino D3) |

D2 and D3 are unused by the stock firmware; the mod firmware gives them pull-ups, so they are safe
when nothing is connected.

**Status:** implemented and reviewed, not yet tested with a real LM1881.
