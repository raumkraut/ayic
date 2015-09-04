#!/usr/bin/env python2
"""
	Script which wraps a single X11 window and intercepts input events
"""
import argparse


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

if __name__ == '__main__':
	# Create a GTK window and embed the identified window in it
	args = arg_parser.parse_args()
	
	from gi.repository import Gtk
	from gi.repository import Gdk
	
	# Create our own window with just a socket
	window = Gtk.Window()
	window.set_title('Wewt')
	socket = Gtk.Socket()
	socket.set_can_focus(True)
	window.add(socket)
	
	# Link up useful events
	window.connect('delete_event', Gtk.main_quit)
	socket.connect('destroy', Gtk.main_quit)
	
	# TODO: Replicate original window params
	
	# Intercept keystrokes
	window.set_events(
		  Gdk.EventMask.KEY_PRESS_MASK
		| Gdk.EventMask.KEY_RELEASE_MASK
	)
	# TODO: Are these defined somewhere?
	# Keyboard scan-codes for the actual physical keys
	keycode_q = 24
	keycode_esc = 9
	def swap_q_esc(widget, event):
		""" Map Esc keypresses to Q, and vice-versa """
		print event, event.keyval, event.hardware_keycode
		if event.hardware_keycode == keycode_q:
			event.hardware_keycode = keycode_esc
			event.keyval = Gdk.KEY_Escape
		elif event.hardware_keycode == keycode_esc:
			event.hardware_keycode = keycode_q
			event.keyval = Gdk.KEY_q
		
		return False
		
	def focus_socket(widget, event):
		print 'FOCUS'
		# The focus, it does nothing!
		socket.grab_focus()
		socket.child_focus(Gtk.DirectionType.TAB_FORWARD)
		
	def defocus_socket(widget, event):
		print 'DEFOCUS'
		
	window.connect('key_press_event', swap_q_esc)
	window.connect('key_release_event', swap_q_esc)
	window.connect('focus_in_event', focus_socket)
	window.connect('focus_out_event', defocus_socket)
	
	# Embed dat window
	socket.add_id(args.window_id)
	# Run the simulation
	window.show_all()
	Gtk.main()
	
