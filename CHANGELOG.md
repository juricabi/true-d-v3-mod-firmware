# Changelog

All versions are mods of the Furious FPV True-D V3 firmware 3.9D.  The version shows on the boot
screen under `TRUE-D REV 3.9`.

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
