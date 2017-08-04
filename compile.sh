#!/bin/bash

#Import tools for compiling extension binaries
export PATH=$PATH:/opt/libreoffice5.3/sdk/bin/

#Setup directories 
mkdir "${PWD}"/SMF/
mkdir "${PWD}"/SMF/META-INF/

#Compile the binaries
idlc -I /opt/libreoffice5.3/sdk/idl "${PWD}"/idl/Xsmf.idl
regmerge -v "${PWD}"/SMF/Xsmf.rdb UCR "${PWD}"/idl/Xsmf.urd
rm "${PWD}"/idl/Xsmf.urd

#Copy extension files and generate metadata
cp -f "${PWD}"/src/smf.py "${PWD}"/SMF/
cp -f "${PWD}"/src/morningstar.py "${PWD}"/SMF/
cp -f "${PWD}"/src/yahoo.py "${PWD}"/SMF/
cp -f "${PWD}"/src/advfn.py "${PWD}"/SMF/
cp -f "${PWD}"/src/description-en-US.txt "${PWD}"/SMF/
python "${PWD}"/src/generate_metainfo.py

#Package into oxt file
pushd "${PWD}"/SMF/
zip -r "${PWD}"/SMF.zip ./*
popd
mv "${PWD}"/SMF/SMF.zip "${PWD}"/SMF.oxt
