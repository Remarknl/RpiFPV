raspivid -n -w 1280 -h 720 -b 1200000 -fps 30 -t 0 -o - | \
gst-launch-1.0 -v fdsrc \
! rtph264pay config-interval=1 pt=96 \
! udpsink host=videoserver.ulab.nl port=5004