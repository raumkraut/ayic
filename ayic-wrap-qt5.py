#!/usr/bin/env python2
"""
	Script which wraps a single X11 window and intercepts input events
"""
import argparse

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtX11Extras


def window_id_typer(val):
	"""
		Returns the numeric window_id for the givel `val` string
	"""
	if val.startswith('0x'):
		return long(val, 16)
	return long(val)
	

arg_parser = argparse.ArgumentParser(
	description='Wrap an X11 window and process input events',
)
arg_parser.add_argument(
	'window_id',
	type=window_id_typer,
	help='the window ID to grab and wrap',
)


class WrapperWindow(QtGui.QWindow):
	def __init__(self, *args, **kwargs):
		super(WrapperWindow, self).__init__(*args, **kwargs)
		
	def keyPressEvent(self, event):
		print 'KP', event
	
if __name__ == '__main__':
	args = arg_parser.parse_args()
	
	app = QtWidgets.QApplication([])
	window = WrapperWindow.fromWinId(args.window_id)
	window.setTitle('Wewt')
	window.show()
	## NB. QWidget::createWindowContainer to embed it elsewhere?
	## (reportedly, embedding has the same focus problems as before)
	
	## TODO: Intercept key events
	
	# Run the simulation
	app.exec_()
	
