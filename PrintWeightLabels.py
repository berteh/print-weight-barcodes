#!/usr/bin/python3

import serial, re, random, cups
from string import Template
from tempfile import NamedTemporaryFile

# settings
COM_SCALE='/dev/ttyS0'    # COM device name of RS-232 scale
PRINTER_NAME='zebra-raw'  # CUPS name of zebra printer
DEBUG = False
EMPTIES = 5    # number of white space bytes between blocks
FACTOR = 1000  # scale factor from unit of scale to unit of label barcode
APPEND_CHECKSUM = True
""" label model in ZPL format. $kgs, $grams, $checksum and $cheers will be replaced.
online editor/viewer at http://labelary.com/viewer.html"""
TEMPLATE_ZPL = """^XA
^FX section with header and readable weight
^CF0,70
^FO75,50^FDco-labor en vrac^FS
^CF0,35
^FO78,115^FD$cheers^FS
^FO570,115,1^FDTare: $kgs kg^FS

^FX section with bar code.
^BY4,3,130
^FO55,170^BC,,N,,,D^FD0700000$grams$checksum^FS
^XZ"""       
CHEERS = ["Bravo !", "Merci.", "Parfait !", "Merci.", "Merci.", "Génial !", "Extra !"]  # list of short cheers. One may be added at random on the label

# buffer whole block from scale
def read_block(p = COM_SCALE, empties = EMPTIES):
	if DEBUG : print(f"connecting to scale on {p}")  
	s = serial.Serial(port=p, baudrate=9600, bytesize=serial.EIGHTBITS, timeout=None, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)

	res = ""
	blank = empties	* 2 + 2
	while(blank > 0) :
		b = s.read()
		if b == b' ':
			blank -= 1
		#if DEBUG : print(f"  {b}")
		res += b.decode('ascii', 'backslashreplace')  # or use 	b.decode('cp437') to avoir overhead of replacing unknown characters
	return res


def get_weight_from_scale() :
	if DEBUG : print("getting weight from scale")  
	data = read_block()
	if DEBUG : print(f"data: {data}") 

	weight = re.search(f"\s{{{EMPTIES}}}(\S+)\skg\s", data)
	return(weight.group(1))


def calc_check_digit(number):
    """Calculate the EAN check digit for 12-digit numbers.
    from https://github.com/arthurdejong/python-stdnum/blob/master/stdnum/ean.py"""
    return str((10 - sum((3, 1)[i % 2] * int(n)
                         for i, n in enumerate(reversed(number)))) % 10)


def get_zpl(kgs = "1,341") :
	if DEBUG : print("generating ZPL")
	grams = kgs.replace(",","").zfill(5);
	if APPEND_CHECKSUM :
		checksum = calc_check_digit(f"0700000{grams}")
	else : checksum = ""
	t = Template(TEMPLATE_ZPL)
	zpl = t.safe_substitute(kgs=kgs, grams=grams, checksum=checksum, cheers=random.choice(CHEERS))
	return(zpl)


def send_to_printer(zpl = TEMPLATE_ZPL, p = PRINTER_NAME) :
	if DEBUG : print("printing")
	f = NamedTemporaryFile(mode='w+b')

	try:
		conn = cups.Connection()		
		b = zpl.encode(encoding = 'utf-8')
		f.write(b)
		f.seek(0)   # rewind needed to allow cups to read file
		conn.printFile(p, f.name, 'Weigh label', {} )

	except cups.IPPError as err:
   		print(f"There is an error connecting with the printer: {err}")
	finally :
		f.close()
		conn = None


def purge_printer_queue(p = PRINTER_NAME) :
	if DEBUG : print("cleaning printing jobs in queue")
	
	try:
		conn = cups.Connection()
		conn.cancelAllJobs(p, my_jobs=False, purge_jobs=True)

	except cups.IPPError as err:
   		print(f"Cannot connect with the printer: {err}")
	finally :
		conn = None	


def test() :
	print("testing label content generation :")
	kgs = "0,346"
	zpl = get_zpl(kgs)
	print(zpl)

	print("\ntesting scale reading :")
	kgs = get_weight_from_scale()
	print(kgs)

	print("\ntesting printing :")
	send_to_printer(TEMPLATE_ZPL)


def weight_and_print() :
	kgs = get_weight_from_scale()
	#kgs = ("0,678")
	zpl = get_zpl(kgs)
	send_to_printer(zpl)


if __name__ == "__main__":
	#if DEBUG : test()
	
	weight_and_print()
	
	#purge_printer_queue()