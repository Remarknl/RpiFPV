gst-launch-1.0 -v udpsrc port=5004 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' \
! rtpjitterbuffer latency=5000 \
! rtph264depay \
! h264parse \
! omxh264dec \
! eglglessink
