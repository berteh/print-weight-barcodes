#!/usr/bin/python3

"""
author : berteh, for co-labor
licence : CC-BY-SA
homepage, contributions : https://github.com/berteh/print-weight-barcodes
"""

import yaml, pytest
from  PrintWeightLabels import *


@pytest.fixture
def config_station() :
	return 'station1';

@pytest.fixture
def config_explicit() :
	return ('/dev/ttyS0', 'zebra-raw-D2', '5x2.5 TLP2824', True)

@pytest.fixture
def devices_KO() :
	return ('/dev/ttyS32KO', 'zebra-raw-not-existing-printer', '5x2.5 TLP2824', True)
	
@pytest.fixture
def label_KO() :
	return ('/dev/ttyS0', 'zebra-raw-D2', '5x2.5 ZebraNotExistingLabel', True)

@pytest.fixture
def test_label():
	return """^XA
	^FX text
	^CF0,30
	^FO30,50^FDtesting printer connection^FS
	^FX bar code.
	^BY2,2,60
	^FO40,90^BC^FD123456789^FS
	^XZ"""



# test LOADING
def test_config_loading_from_station_name(config_station) :
	pwl1 = PrintWeightLabels(config_station)
	zplt = pwl1.zpl_template
	assert "^XZ" in zplt and "^XA" in zplt, f"no valid ZPL template could be loaded for '{config_station}', check configuration"


def test_config_loading_from_explicit_config(config_explicit) :
	pwl1 = PrintWeightLabels(*config_explicit)
	zplt = pwl1.zpl_template
	assert "^XZ" in zplt and "^XA" in zplt, f"no valid ZPL template could be loaded for explicit {config_explicit}, check configuration"

def test_wrong_label_template(label_KO) :
	with pytest.raises(KeyError):
		pwl1 = PrintWeightLabels(*label_KO)


def test_config_infos_for_gui(config_station) :
	conf = get_config_GUI_details()
	print(f"GUI config values are: {conf[0].values()}")
	assert 'scale port' in conf[0].keys(), "GUI config does not contains scale adress, check configuration"
	pwl1 = PrintWeightLabels(*conf[0].values())

# test SCALE
def test_scale_wrong_connection(devices_KO) :
	with pytest.raises(RuntimeError):
		pwl1 = PrintWeightLabels(*devices_KO)
		kgs = pwl1.get_weight_from_scale()
		assert kgs != "", f"weight from scale is 0 or not available at {pwl1.scale}. check connection, settings and put something on the scale"

def test_scale_connection(config_station) :
	pwl1 = PrintWeightLabels(config_station)
	kgs = pwl1.get_weight_from_scale()
	assert kgs != "", f"weight from scale is 0 or not available at {pwl1.scale}. check connection, settings and put something on the scale"

	
# test LABEL
def test_label_content_generation(config_station) :
	pwl1 = PrintWeightLabels(config_station)
	zplt = pwl1.zpl_template
	assert "^XZ" in zplt and "^XA" in zplt, f"no valid ZPL template could be loaded, check configuration"
	kgs = "0,999"
	zpl = pwl1.get_zpl(kgs)
	assert "00999" in zpl, f"label content (ZPL) seems not to contain grams:  {zpl}"

# test PRINTER
def test_printer_connection(config_station) :
	pwl1 = PrintWeightLabels(config_station)
	c = pwl1.printer_pending_jobs()
	assert int(c+1), f"check printer configuration: could not get number of printing jobs from queue."

@pytest.mark.skip(reason="skiping: not properly detected yet. TODO check for particular printer and not whole CUPS pool")
def test_printer_wrong_connection(devices_KO) :
	with pytest.raises(RuntimeError):
		pwl1 = PrintWeightLabels(*devices_KO)
		c = pwl1.printer_pending_jobs()		


# test whole chain
@pytest.mark.skip(reason="skiping: should only print a label IF all other tests are fine")
def test_whole_chain(config_station) :
	pwl1 = PrintWeightLabels(config_station)
	pwl1.weight_and_print()