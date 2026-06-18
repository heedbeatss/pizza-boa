#!/bin/bash
BASE="/mnt/c/Users/deeh_/pizza-delivery/mobile/android/app/src/main/res"
for d in mdpi hdpi xhdpi xxhdpi xxxhdpi; do
  rm -f "$BASE/mipmap-$d/ic_launcher_foreground.png"
done
rm -f "$BASE/drawable-v24/ic_launcher_foreground.xml"
echo "Limpo!"
