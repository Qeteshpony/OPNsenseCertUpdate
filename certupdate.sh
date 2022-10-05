#!/usr/bin/env bash
# copy certfiles from external server - make sure user has access to the file on the target server
scp user@host:path/fullchain.pem /root/
scp user@host:path/privkey.pem /root/

# update the config
/usr/bin/env python3 /root/OPNsenseCertUpdate.py

# restart Web UI
/usr/local/etc/rc.restart_webgui
