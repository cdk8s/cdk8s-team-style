#!/bin/bash
wd=`pwd`
sed -i 's/[ ]*//g' BatchClone.txt
for path in `cat BatchClone.txt`
do

cd "${wd}"
dir=${path#*//}

if [ ! -x "$dir" ]; then
echo "= Creating: project in ${wd} ="

echo "- Running: git clone ${path} -"
git clone "${path}"
echo "= Successfully cloned ${path} ="
fi
done
