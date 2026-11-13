#!/usr/bin/env python3
"""Make the no-LED bootloader from the unit's own ATmegaBOOT image.

The unit's bootloader (0x7800-0x7F9D) is byte for byte Arduino's ATmegaBOOT_168_atmega328.hex.
Its only port-B accesses are three single-bit instructions of the LED code:

  0x7A98  sbi DDRB,5   (25 9A)   main(): LED_DDR |= _BV(PB5)     -> D13 becomes an output
  0x7A30  sbi PORTB,5  (2D 9A)   flash_led(): LED_PORT |= _BV(PB5)  -> D13 high (5 V)
  0x7A42  cbi PORTB,5  (2D 98)   flash_led(): LED_PORT &= ~_BV(PB5) -> D13 low

Each is replaced by a nop (00 00).  Nothing else changes: same size, same addresses, same protocol,
same 2 x 100 ms delay loop (so the application starts at the same time, 3 cycles = 0.19 us sooner).

Usage: mkpatch.py STOCK.hex OUT.hex
Refuses unless STOCK.hex is exactly the known stock image (SHA-256 below).
"""
import hashlib
import sys

STOCK_SHA256 = "2e5927f0"  # prefix checked against the full digest printed below
START, END = 0x7800, 0x7F9E   # END exclusive: 1950 bytes
PATCHES = [  # (address, expected bytes, replacement, what)
    (0x7A98, b"\x25\x9a", b"\x00\x00", "sbi DDRB,5  -> nop"),
    (0x7A30, b"\x2d\x9a", b"\x00\x00", "sbi PORTB,5 -> nop"),
    (0x7A42, b"\x2d\x98", b"\x00\x00", "cbi PORTB,5 -> nop"),
]


def read_ihex(path):
    mem, base = {}, 0
    for line in open(path):
        line = line.strip()
        if not line.startswith(":"):
            continue
        raw = bytes.fromhex(line[1:])
        if sum(raw) & 0xFF:
            sys.exit(f"{path}: bad checksum: {line}")
        n, addr, typ, data = raw[0], (raw[1] << 8) | raw[2], raw[3], raw[4:4 + raw[0]]
        if typ == 0:
            for i, b in enumerate(data):
                mem[base + addr + i] = b
        elif typ == 2:
            base = ((data[0] << 8) | data[1]) << 4
        elif typ == 4:
            base = ((data[0] << 8) | data[1]) << 16
        elif typ == 1:
            break
    return mem


def write_ihex(path, start, blob):
    out = []
    for off in range(0, len(blob), 16):
        chunk = blob[off:off + 16]
        a = start + off
        rec = bytes([len(chunk), (a >> 8) & 0xFF, a & 0xFF, 0]) + chunk
        out.append(":" + rec.hex().upper() + "%02X" % ((-sum(rec)) & 0xFF))
    out.append(":00000001FF")
    open(path, "w").write("\n".join(out) + "\n")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    mem = read_ihex(sys.argv[1])
    if any(a < START or a >= END for a in mem) or len(mem) != END - START:
        sys.exit("input is not exactly 0x7800-0x7F9D")
    blob = bytearray(mem[a] for a in range(START, END))
    digest = hashlib.sha256(blob).hexdigest()
    if not digest.startswith(STOCK_SHA256):
        sys.exit(f"input SHA-256 {digest} is not the stock ATmegaBOOT_168_atmega328 image: refusing")
    for addr, old, new, what in PATCHES:
        o = addr - START
        if bytes(blob[o:o + 2]) != old:
            sys.exit(f"0x{addr:04X}: expected {old.hex()}, found {blob[o:o+2].hex()}: refusing")
        blob[o:o + 2] = new
        print(f"0x{addr:04X}  {old.hex()} -> {new.hex()}  {what}")
    write_ihex(sys.argv[2], START, bytes(blob))
    print(f"stock  SHA-256 {digest}")
    print(f"no-LED SHA-256 {hashlib.sha256(blob).hexdigest()}  ({len(blob)} B, 0x{START:04X}-0x{END-1:04X})")


if __name__ == "__main__":
    main()
