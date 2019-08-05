import argparse

parser = argparse.ArgumentParser(description="CRC Calculator")
parser.add_argument("width", type=int, help="CRC width")
parser.add_argument("poly", type=str, help="CRC polynomial")
parser.add_argument("seed", type=str, help="CRC seed")
parser.add_argument("data", type=str, help="data")
parser.add_argument("size", type=int, help="data size")
parser.add_argument("--base", type=int, default=16, help="input base")
parser.add_argument("-f", "--forward", action='store_true', help="use forward architecture")
parser.add_argument("-l", "--lsb_first", action='store_true', help="read data LSB first")
parser.add_argument("-p", "--print", action='store_true', help="print architecture info")
parser.add_argument("-d", "--debug", action='store_true', help="enable debug output")
args = parser.parse_args()

def calc_crc(width, poly, seed, data, size):

    lfsr = seed

    mask = (1 << width) - 1

    if(args.debug):
        print(("Poly: {:0" + str(width) + "b}").format(poly))
        print(("Seed: {:0" + str(width) + "b}").format(seed))

    for i in range(1, size+1):

        if args.lsb_first:
            bit_in = (data >> i ) & 1
        else:
            bit_in = (data >> size - i) & 1

        bit_out = (lfsr >> (width - 1)) & 1
        shifted = ((lfsr << 1) | bit_in) & mask;

        if(args.debug):
            print_crc(width, poly, lfsr)

        if bit_out:
            if args.forward:
                # Forward
                lfsr = shifted ^ poly ^ bit_in
            else:
                # Non-forward
                lfsr = shifted ^ poly
        else:
            lfsr = shifted


    return lfsr

def print_crc(width, poly, content=None):
    print("   _______" + (args.width - 1)*"________" + " ")

    line = ["  ", "  ", "--"]
    for i in range(0, width):
            line[0] += "|  ___  " if (poly >> i & 1) else "   ___  "
            line[1] += "| |   | " if (poly >> i & 1) else "  |   | "
            line[2] += "{}-| {} |-".format("0" if (poly >> i & 1) else "-", str(content >> i & 1) if content else " ")
    print(line[0] + "|")
    print(line[1] + "|")
    print(line[2])

    print("    |___| " + (args.width - 1)*"  |___| ")
    print("")

crc = calc_crc(args.width, int(args.poly, args.base), int(args.seed, args.base), int(args.data, args.base), args.size)
print(("0x{:0" + str(args.width) + "x}").format(crc))

if args.print:
    print_crc(args.width, int(args.poly, args.base))
