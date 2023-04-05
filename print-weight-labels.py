#!/usr/bin/python3

import serial, re

# settings #################################################
COM='/dev/ttyS0'
DEBUG = False
EMPTIES=5    # number of white space bytes between blocks
FACTOR=1000  # factor between unit of scale and ticket
LABEL_ZPL="""^XA

^FX Top section with logo, name and address.
^CF0,40
^FO60,40^FDco-labor en vrac^FS

^FX section with bar code.
^BY3,3,90
^FO40,100^BC^FD0110.5g^FS

^XZ"""       # label model in ZPL format. online editor/viewer at http://labelary.com/viewer.html

# settings #################################################


# buffer whole block
def read_block(empties = EMPTIES):
	res = ""
	blank = empties	* 2 + 2
	while(blank > 0) :
		b = s.read()
		if b == b' ':
			blank -= 1
		if DEBUG : print(b)
		res += b.decode('ascii', 'backslashreplace')  # or use 	b.decode('cp437') to avoir overhead of replacing unknown characters
	return res


s = serial.Serial(port=COM, baudrate=9600, bytesize=serial.EIGHTBITS, timeout=None, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)

data = read_block()
print(data)

weight = re.search(f"\s{{{EMPTIES}}}(\S+)\skg\s", data)

print(weight.group(1))
