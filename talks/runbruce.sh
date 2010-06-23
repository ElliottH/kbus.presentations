#! /bin/sh
# Use bruce the presentation tool to present the slideshow

cd ~/sw/kbus/talks/bruce-3.2.1

if [ x$1 == x--help -o x$1 == x-help -o x$1 == x-h ]; then
    echo "Present my EuroPython 2010 KBUS slides using Bruce the presentation tool"
    echo "Any arguments will be added to the end of the Bruce command line"
    echo
    ./bruce.sh --help
    exit
fi
#
# -p Show page numbers - is this a good idea if I have a lot?
# -t Show a timer - how long the slideshow has been running for.
# -w The EuroPython2010 wiki appears to show all projectors supporting
#    1024x768, and any larger size being squashed (800x600 should also work)
./bruce.sh -p -t  -w 1024x768 ../europython2010.slides.rst $*
