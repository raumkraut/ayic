#!/usr/bin/env python2
"""
	Script which wraps a single X11 window and intercepts input events
	
	## TODO: Work out why focus/keyboard input only works when
	the embedded process is not run from the same script/shell
	as the containing process..!
"""
import argparse

from PyQt4 import QtCore
from PyQt4 import QtGui


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

class WrapperDialog(QtGui.QDialog):
	""" Dialog which wraps another window """
	def __init__(self, embed_wid, *args, **kwargs):
		super(WrapperDialog, self).__init__(*args, **kwargs)
		
		## TODO: Replicate original window params
		self.setWindowTitle('Wewt')
		self.resize(600, 400)
		
		self.embed = EmbedWidget(parent=self, wid=embed_wid)
		self.embed.clientClosed.connect(self.close)
		layout = QtGui.QVBoxLayout()
		layout.setMargin(0)
		layout.addWidget(self.embed)
		self.setLayout(layout)
		
		## TODO: None of this focus stuff works :(
		
	def focusInEvent(self, event):
		print 'DIAFOCI', event
		
	def keyPressEvent(self, event):
		print 'DIAKP', event
		
	
class EmbedWidget(QtGui.QX11EmbedContainer):
	""" Widget which embeds another window """
	def __init__(self, wid, *args, **kwargs):
		super(EmbedWidget, self).__init__(*args, **kwargs)
		
		self.window_id = wid
		self.embedClient(wid)
		
	def focusInEvent(self, event):
		print 'WIDFOCI', event
		
	def keyPressEvent(self, event):
		print 'WIDKP', event
		
	

if __name__ == '__main__':
	args = arg_parser.parse_args()
	
	# Create our own window with just a socket
	app = QtGui.QApplication([])
	window = WrapperDialog(embed_wid=args.window_id)
	window.show()
	
	## TODO: Intercept key events
	
	# Run the simulation
	app.exec_()
	
