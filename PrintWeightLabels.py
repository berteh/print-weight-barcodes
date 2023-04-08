#!/usr/bin/python3

"""
author : berteh, for co-labor
licence : CC-BY-SA
homepage, contributions : https://github.com/berteh/print-weight-barcodes
"""

import serial, re, random, cups, time
from string import Template
from tempfile import NamedTemporaryFile

# default settings
COM_SCALE='/dev/ttyS0'    # COM device name of RS-232 scale
PRINTER_NAME='zebra-raw'  # CUPS name of zebra printer
DEBUG = True
EMPTIES = 5    # number of white space bytes between blocks
FACTOR = 1000  # scale factor from unit of scale to unit of label barcode
""" label model in ZPL format. $kgs, $grams and $cheers will be replaced.
online editor/viewer at http://labelary.com/viewer.html"""
TEMPLATE_ZPL = """^XA
^FX section with header and readable weight
^CF0,70
^FO75,60^FDco-labor en vrac^FS
^CF0,35
^FO78,125^FD$cheers^FS
^FO570,125,1^FDTare: $kgs kg^FS

^FX section with bar code.
^BY5,3,140
^FO85,170^BE,,Y^FD0700000$grams^FS
^XZ"""       
CHEERS = ["Bravo !", "Merci.", "Parfait !", "Génial !", "Extra !", "Merci.", "Merci."]  # list of short cheers. One may be added at random on the label
#test DE chars : CHEERS = ["Génial, Glück & ß"]


def read_block(p = COM_SCALE, empties = EMPTIES):
	""" Buffers whole block from scale, separated by #empties empty characters
		Raises Error if cannot read from scale
	"""
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


def get_weight_from_scale(p = COM_SCALE) :
	""" Raises Error if cannot read from scale
	"""
	if DEBUG : print("getting weight from scale")  
	data = read_block(p)
	if DEBUG : print(f"data: {data}") 

	weight = re.search(f"\s{{{EMPTIES}}}(\S+)\skg\s", data)
	return(weight.group(1))


def get_zpl(kgs = "1,341") :
	if DEBUG : print("generating ZPL")
	grams = kgs.replace(",","").zfill(5);
	t = Template(TEMPLATE_ZPL)
	zpl = t.safe_substitute(kgs=kgs, grams=grams, cheers=random.choice(CHEERS))
	return(zpl)


def send_to_printer(zpl = TEMPLATE_ZPL, p = PRINTER_NAME) :
	""" Raises cups.IPPError if printer not found. 
		Pools the provided ZPL string if printer queue exists, even if printer is not connected
	"""
	if DEBUG : print("printing")
	f = NamedTemporaryFile(mode='w+b')

	try:
		conn = cups.Connection()		
		b = zpl.encode(encoding = 'utf-16')
		f.write(b)
		f.seek(0)   # rewind needed to allow cups to read file
		conn.printFile(p, f.name, 'Weigh label', {} )
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


def printer_pending_jobs(p = PRINTER_NAME) :
	try:
		conn = cups.Connection()
		open_jobs = conn.getJobs(which_jobs='not-completed', my_jobs=False)
	except cups.IPPError as err:
   		print(f"Cannot connect with the printer: {err}")
	finally :
		conn = None	
	return(len(open_jobs))


def test() :
	
	if DEBUG : print("testing all connections and label generation :")

	kgs = "0,999"
	zpl = get_zpl(kgs)
	if "00999" in zpl :
		print(f"OK ZPL : label content is  {zpl}")
	else :
		print(f"not OK ZPL : label content seems not to contain grams:  {zpl}")

	if DEBUG : print("\ntesting scale reading :")
	try :
		kgs = get_weight_from_scale()
	except Exception as err :
		print(f"not OK scale : could not connect to $COM_SCALE or could not get weight from scale")
	else :
		print(f"OK scale on #COM_SCALE: {kgs}")
	
	if DEBUG : print("\ntesting printing :")
	print_job = 0
	try :
		print_job = send_to_printer(TEMPLATE_ZPL)
	except Exception as err :
		print(f"not OK printing : could not find printer queue $PRINTER_NAME")
	else :
		print(f"OK adding print job to {PRINTER_NAME}")
	for attemps in range(5):		
		time.sleep(2)
		c = printer_pending_jobs()
		if (c == 0) : 
			print(f"OK printing: check out label.... job queue is now empty")
			return
		else :
			print(f". {c} job(s) pending")
	print("not OK printing : queue is still not empty... check if printer is ON.")
	


def weight_and_print() :
	try :
		kgs = get_weight_from_scale()		
	except Exception as err:
		raise RuntimeError('Scale connection problem') from err
	zpl = get_zpl(kgs)
	try :
		send_to_printer(zpl)
	except Exception as err:
		raise RuntimeError('Printer connection problem') from err
	


if __name__ == "__main__":
	#if DEBUG : test()
	
	weight_and_print()	