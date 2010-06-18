#! /bin/sh
echo Reading europython2010.txt, preparing _europython2010.tmp
./minicog.py europython2010.txt _europython2010.tmp
echo Reading _europython.tmp, preparing _europython.html
rst2html _europython2010.tmp > _europython2010.html
