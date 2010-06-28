#! /bin/sh
machine=`uname -n`
echo Machine $machine
if [ x"$machine" == x"spoon" ]
then
  echo "Installing KBUS"
  pushd ~/sw/kbus/kbus
  sudo insmod kbus.ko
  popd
fi

echo Reading europython2010.txt, preparing _europython2010.tmp
./minicog.py europython2010.txt _europython2010.tmp
echo Reading _europython.tmp, preparing _europython.html
rst2html _europython2010.tmp > _europython2010.html
echo Reading _europython2010.tmp, preparing _europython2010.pdf
rst2pdf _europython2010.tmp -o _europython2010.pdf \
                --fit-literal-mode=overflow

if [ x"$machine" == x"spoon" ]
then
  echo "Uninstalling KBUS"
  sudo rmmod kbus
fi
