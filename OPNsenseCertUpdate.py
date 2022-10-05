#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ETree
import time
import shutil
import base64

certfile = "/root/fullchain.pem"  # path to the certificate file
keyfile = "/root/privkey.pem"  # path to the private key file
configpath = "/conf/"  # OPNsense config dir - should not change
backuppath = "/conf/backup/"  # backup dir - default OPNsense config backup dir
configfile = "config.xml"  # filename of the config.xml
certname = "LetsEncrypt"  # The name of the certificate to be replaced as seen under System -> Trust -> Certificates


def replace_in_xml(description: str, newcert: str, newprivkey: str):
    """
    Load the config and replace the certificate with <descr>:param description:</descr>

    :param description: Description string of the certificate
    :param newcert: new certificate, base64 encoded
    :param newprivkey: new private key, base64 encoded
    """
    # create backup of current config file
    shutil.copyfile(configpath + configfile,
                    backuppath + configfile + time.strftime(".%Y-%m-%d-%H.%M.%S.bak"))
    # load tree from disk
    tree = ETree.parse(configpath + configfile)
    root = tree.getroot()
    # find all children with name <cert>
    for cert in root.findall("cert"):
        # find <cert> with matching <descr>
        for child in cert.findall("descr"):
            if child.text == description:
                # find <crt> and <prv> elements and replace their content
                crt = cert.find("crt")
                prv = cert.find("prv")
                crt.text = newcert
                prv.text = newprivkey
    # write tree to disk
    tree.write(configpath + configfile)


def main():
    # read the certificate files and encode them with base64
    with open(certfile, "r") as f:
        newcert = f.read().encode()
    crt = base64.b64encode(newcert).decode()

    with open(keyfile, "r") as f:
        newprivkey = f.read().encode()
    prv = base64.b64encode(newprivkey).decode()

    # write the encoded certificate to the config
    replace_in_xml(certname, crt, prv)

    # write log entry
    os.system('logger -t certupdate "UI-Certficiate updated"')


if __name__ == "__main__":
    main()
