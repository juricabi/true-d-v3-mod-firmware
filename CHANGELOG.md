# Changelog

All versions are mods of the Furious FPV True-D V3 firmware 3.9D.  The version shows on the boot
screen under `TRUE-D REV 3.9`.

## MOD 1.15

- **Antenna check (new):** the main menu shows each receiver's share of the time since the last
  channel change (`A62 B38`), once the diversity has had to choose a few times.  A dead antenna or
  receiver reads ~0 %, which the diversity hides otherwise.
- **Quad finder:** beeps from ~6 % (stock: silent below 70 %), faster the stronger; a line marks the
  highest level since it was opened.
- **Smart search:** each VTX's own channel first, strongest first, and weak VTXs are found too; then
  the other channels the same VTXs were found on, as in stock.  Every channel is read twice, so a Wi-Fi
  burst (5 GHz Wi-Fi shares the L band) is not listed as a VTX.
- **Band scanner:** BEST no longer names a channel on the other side of a wide gap in the channel table
  (F8/R7 showed as E5, R1 as E3, R8 as E7, B1 as R3); L1 and E8 show the right MHz; a pick from a
  single noisy sweep is dropped.
- **Diversity:** ~25 % less CPU.  FILTER now also sets how deep a fade must be for an instant switch
  (NORMAL is the same as 1.13).  With the sync mod a deep fade no longer waits behind a pending
  quality switch, and a better receiver is taken right after the vertical sync, but only while the
  active picture is not good.
- **RX TUNE:** the picture comes ~2 s sooner at power-up (tuned before the boot screen); the final
  frequency is set 0.14–0.21 s after a change; on the ALL, SAVED and SEARCH lists a channel is measured
  only after 0.4 s on it, so stepping through a list shows the picture; when the retry fails too, the
  stored offset is used again (1.13 left the receivers untuned until the next change).
- **ELRS backpack:** the telemetry was wiped on about half of the frames; RSSI shows its minus sign;
  capacity shows as `MAH` (the font has no lowercase); the telemetry clears 3 s after the link is gone;
  5880 MHz goes to F8 on the F band, else R7; a channel command waits while a popup or the saved-list
  editor is open.
- **Goggle-bay link:** no 80 ms stall per goggle reply; malformed commands are ignored; a goggle
  "start search" is ignored during a calibration or a running search; a channel change from the goggle
  is measured by RX TUNE after 0.4 s, as on a list.
- **Receivers:** the tuning bus is driven at the stock speed with extra timing margin.
- **Keys and screens:** a short tap right after a channel change is no longer lost (stock too); a key
  still held across a screen change no longer acts on the next screen; a key press restarts the auto
  lock; the popup closes itself after 8 s; DELETE of the last saved channel and SAVE of a listed channel fixed; short pilot names no longer
  run into the B label.
- **Boot:** a damaged stored calibration is detected and the unit asks for a calibration; leftovers of
  another firmware no longer switch ELRS on or RX TUNE off.
- The display updates ~3 ms faster per frame.

## MOD 1.13 (first public release)

- Beeps play in the background (stock: 75 ms in which nothing else ran, on every key press).
- Goggle-bay link: no packet in the 30 ms after a retune (it spoiled the scanner, search and
  calibration readings) and none during a beep; the 3-bit channel code must read the same twice
  (a one-pass glitch could step the channel in flight).
- Band scanner: of two channels that tune the receiver identically (A4/R5, A1/B8, F8/R7) the one
  shown stays; the measured MHz is shown.
- RX TUNE: the measurement averages one video field on each side, and waits the stock firmware's
  30 ms after every retune; repeat measurements agree to a quarter MHz.

## MOD 1.11

- Final multi-agent review, every finding verified; all confirmed issues fixed.
- Every reading 30 ms after a retune (scanner, search, calibration) is settled with every FILTER
  setting (on HIGH they read up to ~70 counts low).
- Band scanner BEST rebuilt: per-channel level kept over sweeps, `--` with no VTX, the VTX's own
  channel instead of a neighbour.  The smart search's first result uses the same pick.
- Diversity thresholds in fixed RSSI counts: the same switching, independent of the calibration,
  and ~25 % less CPU.
- RX TUNE: scans run at the nominal frequencies; a neighbour channel's VTX is not stored as its
  offset; ELRS channel changes are measured once the VTX has arrived.
- Lock, goggle link, ELRS telemetry and calibration-prompt fixes.

## MOD 1.6 – 1.10

- RX TUNE: automatic receiver tuning at every channel change, with the offset on the main screen.

## MOD 1.2 – 1.5

- Measurements on a real unit; diversity parameters tuned on recordings of a walk with the quad.
- Earlier RX TUNE versions (manual, then a blocking scan), removed again in 1.5.

## MOD 1.0 – 1.1

- Fast interrupt-driven diversity, floor-referenced normalisation (any antenna mix).
- ELRS VRx backpack support (TBS Fusion protocol), default off.
- Optional sync-timed switching with an LM1881.
- Standard LowRace L band.
- Stock bug fixes: smart search, scanner restore, calibration, EEPROM validation, goggle link,
  FILTER labels, display driver.
