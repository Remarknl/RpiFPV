gst-launch-1.0 -v v4l2src device=/dev/video0 \
! 'video/x-raw,width=640,height=480' \
! videoconvert \
! x264enc tune=zerolatency \
! rtph264pay config-interval=1 pt=96 \
! udpsink host=videoserver.ulab.nl port=5004
