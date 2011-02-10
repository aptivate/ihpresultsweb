#!/bin/sh

CONF=apache/dev.conf

LISTEN=`grep Listen $CONF | sed -e 's/Listen //'`
echo "Starting Apache dev server on http://$LISTEN/"

apache2 -f $CONF -D FOREGROUND
