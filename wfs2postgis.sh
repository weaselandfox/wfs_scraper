BASEURL="https://geodata.nationaalgeoregister.nl/bodemkaart50000/wfs?service=wfs"

for LAYERNAME in `wget -qO- $BASEURL"&request=GetCapabilities" | xpath -q -e "//FeatureType/Name/text()"` ; do 
    PARTS=(${LAYERNAME//:/ })
    FILENAME=${PARTS[1]}
    wget $BASEURL"&request=GetFeature&typeName="$LAYERNAME"&srsName=EPSG:4326&outputFormat=csv" -O $FILENAME".csv"
    sudo -u postgres shp2pgsql -s 4326 -I -S -c -W LATIN1 $FILENAME".csv" $FILENAME | sudo -u postgres psql bodem
done
