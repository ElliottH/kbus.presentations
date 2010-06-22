#! /bin/sh
# Use bruce the presentation tool to present the slideshow
cd ~/sw/kbus/talks/bruce-3.2.1
#
# -p Show page numbers - is this a good idea if I have a lot?
# -t Show a timer - how long the slideshow has been running for.
# -w The EuroPython2010 wiki appears to show all projectors supporting
#    1024x768, and any larger size being squashed
./bruce.sh -p -t  -w 1024x768 ../europython2010.slides.rst
