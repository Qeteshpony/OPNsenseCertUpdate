# Automatic OPNsense Certificate Update
I use an external server to generate Lets Encrypt wildcard certificates for my internally used domain
These scripts help replacing the certificate in OPNsense without using the WEB-UI by encoding the certificate files
and replacing the elements in the config.xml

## Installation
Edit certupdate.sh and OPNsenseCertUpdate.py to reflect your configuration

Place certupdate.sh and OPNsenseCertUpdate.py in /root

Place actions_certupdate in /usr/local/opnsense/service/conf/actions.d and run `service configd restart`

Go to System -> Settings -> Cron and add a cronjob to run "Automatically replace an ssl certificate" once a week
