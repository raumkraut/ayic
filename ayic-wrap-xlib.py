#!/usr/bin/env python3
"""
	Script which wraps a single X11 window and intercepts input events
	
	As a demonstration; converts caps lock to "m", and mouse button 8
	(first thumb) to space.
	
	Use xwininfo to identify the Window ID you want to wrap, then use that
	as the sole argument to this script.
	
	Requirements (Debian):
		python3
		python3-xlib
"""
import Xlib.X


def winid_to_int(val):
	"""
		Returns the numeric window_id for the given `val`
	"""
	if isinstance(val, str) and val.startswith('0x'):
		return int(val, 16)
	return int(val)
	

KEYCODE_caps = 66
KEYCODE_m = 58
KEYCODE_space = 65
KEYCODE_lctrl = 37
BUTTON_thumb1 = 8

def grab_stuff(window):
	""" Grab just the individual items we're interested in """
	window.grab_key(
		KEYCODE_caps,
		Xlib.X.AnyModifier,
		True,
		Xlib.X.GrabModeAsync,
		Xlib.X.GrabModeAsync,
	)
	window.grab_button(
		button=BUTTON_thumb1,
		modifiers=Xlib.X.AnyModifier,
		owner_events=True,
		event_mask=Xlib.X.ButtonPressMask | Xlib.X.ButtonReleaseMask,
		pointer_mode=Xlib.X.GrabModeAsync,
		keyboard_mode=Xlib.X.GrabModeAsync,
		confine_to=0,
		cursor=0,
	)
	
def ungrab_stuff(window):
	""" Ungrab our grabs """
	window.ungrab_key(KEYCODE_caps, Xlib.X.AnyModifier)
	window.ungrab_button(BUTTON_thumb1, Xlib.X.AnyModifier)
	



if __name__ == '__main__':
	import sys
	
	import Xlib.display
	import Xlib.error
	import Xlib.protocol.event
	
	
	if len(sys.argv) < 2:
		print('Window ID argument required')
		exit(1)
	
	winid = winid_to_int(sys.argv[1])
	display = Xlib.display.Display()
	window = display.create_resource_object('window', winid)
	# Make sure the winid is valid
	try:
		window.get_wm_class()
	except Xlib.error.BadWindow:
		print('No window found for ID: {raw} / {int}'.format(raw=sys.argv[1], int=winid))
		exit(2)
		
	
	# We wants it, we needs it
	grab_stuff(window)
	
	
	def handle_event(event):
		""" Event handler and remapper """
		print('EVIN ', event)
		# Do remapping if necessary
		new_event = event
		new_type = type(event)
		new_detail = None
		if event.type in (Xlib.X.KeyPress, Xlib.X.KeyRelease):
			if event.detail == KEYCODE_caps:
				new_detail = KEYCODE_m
				
		elif event.type in (Xlib.X.ButtonPress, Xlib.X.ButtonRelease):
			if event.detail == BUTTON_thumb1:
				# Need to pick a new event type/class to go button->key
				new_type = {
					Xlib.X.ButtonPress: Xlib.protocol.event.KeyPress,
					Xlib.X.ButtonRelease: Xlib.protocol.event.KeyRelease,
				}[event.type]
				new_detail = KEYCODE_space
				
		
		if new_detail is not None:
			# Create a new event to send to the window
			new_event = new_type(
				time=event.time,
				root=event.root,
				window=window,
				same_screen=event.same_screen,
				child=event.child,
				root_x=event.root_x,
				root_y=event.root_y,
				event_x=event.event_x,
				event_y=event.event_y,
				state=event.state,
				detail=new_detail,
			)
		
		# NB. send_event works, but the events are marked as synthetic,
		# which means some programs will ignore them
		# Possible solution: http://www.semicomplete.com/blog/geekery/xsendevent-xdotool-and-ld_preload.html
		print('EVOUT', new_event)
		window.send_event(new_event, propagate=False)
		
		# And relax
		display.allow_events(Xlib.X.AsyncBoth, Xlib.X.CurrentTime)
		
	
	
	while True:
		event = display.next_event()
		handle_event(event)
		
	
