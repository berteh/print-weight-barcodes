#!/usr/bin/python3

"""
author : berteh, for co-labor
licence : CC-BY-SA
homepage, contributions : https://github.com/berteh/print-weight-barcodes
"""

import serial, re, random, cups, time, yaml, os
from string import Template
from tempfile import NamedTemporaryFile

config = yaml.safe_load(open(os.path.realpath(os.path.dirname(__file__))+"/config.yaml"))
DEFAULT_STATION = config['default CLI station']
DEBUG = config['debug']


def get_config_GUI_details() :
	global config
	return config['gui stations']



class PrintWeightLabels:
		
	""" 
	constructor overloading based on number of arguments: either
	PrintWeightLabels(scale, printer, label_template_name, clean_print_queue_on_run)  or
	PrintWeightLabels(station name)
	"""
	def __init__(self, *args):
		global DEBUG, DEFAULT_STATION, config
				
		DEBUG = DEBUG | config['debug']

		if len(args) > 1 :
			if DEBUG : print(f"configuring new PrintWeightLabel station : {args[0]} > {args[1]}")
			self.scale = args[0]
			self.printer = args[1]					
			self.zpl_template = config['templates'][args[2]]['zpl']
			self.cleanQueue = args[3]


		elif len(args) == 1 :
			if DEBUG : print(f"configuring new PrintWeightLabel {args[0]}")
			self.printer = config[args[0]]['printer name']
			self.scale = config[args[0]]['scale port']
			self.zpl_template = config['templates'][config[args[0]]['label template']]['zpl']
			self.cleanQueue = config[args[0]]['empty print queue on launch']
		
		else : raise RuntimeError(f"Number of arguments must be 1 (station) or 3 (printer, scale, label), it is {len(args)}")

		if self.cleanQueue :
			self.purge_printer_queue()


	def get_weight_from_scale(self) :
		""" Raises Error if cannot read from scale
		"""
		global DEBUG, config

		if DEBUG : print("getting weight from scale")  
		s = serial.Serial(port=self.scale, baudrate=9600, bytesize=serial.EIGHTBITS, timeout=2, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
		b = s.read(config['scale bytes'])
		data = b.decode('ascii', 'backslashreplace')  # or use 	b.decode('cp437') to avoir overhead of replacing unknown characters
		if DEBUG : print(f"data: {data}") 
		if (data == "") : raise RuntimeError(f"Timeout getting weight from scale {self.scale}")

		weight = re.search(f"\s{{{config['scale empties']}}}(\S+)\skg\s", data)
		return(weight.group(1))


	def get_zpl(self, kgs = "0,251") :
		global DEBUG, config

		if DEBUG : print("preparing label content")
		grams = kgs.replace(",","").zfill(5);
		t = Template(self.zpl_template)
		lzpl = t.safe_substitute(kgs=kgs, grams=grams, cheers=random.choice(config['cheers']))
		return(lzpl)


	def send_to_printer(self, lzpl) :
		""" Raises cups.IPPError if printer not found. 
			Pools the provided ZPL string if printer queue exists, even if printer is not connected
		"""
		global DEBUG
		if DEBUG : print("printing")

		f = NamedTemporaryFile(mode='w+b')
		try:
			conn = cups.Connection()		
			b = lzpl.encode(encoding = 'utf-16')
			f.write(b)
			f.seek(0)   # rewind needed to allow cups to read file
			conn.printFile(self.printer, f.name, 'Weigh label', {} )
		finally :
			f.close()
			conn = None


	def purge_printer_queue(self) :
		global DEBUG		
		if DEBUG : print("cleaning printing jobs in queue")
		
		try:
			conn = cups.Connection()
			conn.cancelAllJobs(self.printer, my_jobs=False, purge_jobs=True)

		except cups.IPPError as err:
	   		print(f"Cannot connect with the printer {self.printer}: {err}")
		finally :
			conn = None	


	def printer_pending_jobs(self) :
		try:
			conn = cups.Connection()
			open_jobs = conn.getJobs(which_jobs='not-completed', my_jobs=False) #TODO filter only self.printer
		except cups.IPPError as err:
	   		print(f"Cannot connect with the printer: {err}")
		finally :
			conn = None	
		return(len(open_jobs))


	def test(self) :
		global DEBUG		
		if DEBUG : print("testing all connections and label generation :")

		kgs = "0,999"
		zpl = self.get_zpl(kgs)
		if "00999" in zpl :
			print(f"OK ZPL : label content is  {zpl}")
		else :
			print(f"not OK ZPL : label content seems not to contain grams:  {zpl}")

		if DEBUG : print("\ntesting scale reading :")
		try :
			kgs = self.get_weight_from_scale()
		except Exception as err :
			print(f"not OK scale : could not connect to {self.scale} or could not get weight from scale")
		else :
			print(f"OK scale on {self.scale}: {kgs}")
		
		if DEBUG : print("\ntesting printing :")
		print_job = 0
		try :
			print_job = self.send_to_printer(self.zpl_template)
		except Exception as err :
			print(f"not OK printing : could not find printer queue {self.printer}")
		else :
			print(f"OK adding print job to {self.printer}")
		for attemps in range(5):		
			time.sleep(1.5)
			c = self.printer_pending_jobs()
			if (c == 0) : 
				print(f"OK printing: check out label.... job queue is now empty")
				return
			else :
				print(f". {c} job(s) pending")
		print("not OK printing : queue is still not empty... check if printer is ON.")
		


	def weight_and_print(self) :
		try :
			kgs = self.get_weight_from_scale()		
		except Exception as err:
			raise RuntimeError('Scale connection problem') from err
		zpl = self.get_zpl(kgs)
		try :
			self.send_to_printer(zpl)
		except Exception as err:
			raise RuntimeError('Printer connection problem') from err
		


if __name__ == "__main__":
	if DEBUG : print(f"configuring {DEFAULT_STATION}")

	station = PrintWeightLabels(DEFAULT_STATION)

	if TEST :
		station.test()
	else :
		station.weight_and_print()