#!/usr/bin/python3

from os import path

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo


GObject.threads_init()
Gst.init(None)


class Player(object):
    def __init__(self):
        self.window = Gtk.Window()
        self.window.connect('destroy', self.quit)
        self.window.set_default_size(1280, 720)
        
        self.box = Gtk.Box(spacing=6)
        
        self.drawingarea = Gtk.DrawingArea()
        self.drawingarea.set_size_request(640, 480)
        self.box.add(self.drawingarea)

        
        self.label = Gtk.Label("test")
        self.box.add(self.label)
        self.window.add(self.box)
        
        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)
	#self.bus.connect('message', self.debug)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        self.caps = Gst.caps_from_string('application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264')

        # Create GStreamer elements
        self.udpsrc = Gst.ElementFactory.make('udpsrc', None)
        self.depay = Gst.ElementFactory.make("rtph264depay", None)
        self.decode = Gst.ElementFactory.make("avdec_h264", None)
        self.convert = Gst.ElementFactory.make("videoconvert", None)
        self.sink = Gst.ElementFactory.make("autovideosink", None)

        # Add playbin to the pipeline
        self.pipeline.add(self.udpsrc)
        self.pipeline.add(self.depay)
        self.pipeline.add(self.decode)
        self.pipeline.add(self.convert)
        self.pipeline.add(self.sink)

        self.udpsrc.link_filtered(self.depay, self.caps)
        self.depay.link(self.decode)
        self.decode.link(self.convert)
        self.convert.link(self.sink)

        # Set properties
        self.udpsrc.set_property('port', 5008)
        self.sink.set_property('sync', False)
	#self.pipeline.set_state(Gst.State.PLAYING)

    def run(self):
        self.window.show_all()
        # You need to get the XID after window.show_all().  You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there.
        self.xid = self.drawingarea.get_property('window').get_xid()
        #print(self.xid)
        self.pipeline.set_state(Gst.State.PLAYING)
	
        Gtk.main()

    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    #def debug(self, bus, msg):
	#print(msg.get_structure().get_name())	
	#print(msg.get_structure().get_field_type(msg.get_structure().get_name()))

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)

    def on_eos(self, bus, msg):
        print('on_eos(): seeking to start of video')
        self.pipeline.seek_simple(
            Gst.Format.TIME,        
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())


p = Player()
p.run()
