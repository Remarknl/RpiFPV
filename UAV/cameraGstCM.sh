raspivid -n -w 640 -h 480 -b 1200000 -fps 30 -t 0 -o - | \
gst-launch-1.0 -v fdsrc \
! h264parse \
! rtph264pay config-interval=1 pt=96 \
! udpsink host=192.168.1.3 port=5004
