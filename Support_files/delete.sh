#!/bin/bash
#Version 1.1
#Username is passed by GUI from config.json
username=$1
arg1=$2
dir=/opt/tak
certs=$dir/certs/files
revokeCert=$dir/certs/revokeCert.sh

echo "Username:" $username " this should be your PC username or it will cause errors." 
echo "Deleting user " $arg1

# Switch to the target directory

#This section of code is from @myTeckNet.com

# Determine the Issuing CA (.pem)
echo $username " " $arg1

YELLOW='\033[0;33m'
NC='\033[0m'
if [[ -f $certs/$arg1.pem ]]; then
    issuer=(`openssl x509 -text -in /opt/tak/certs/files/$arg1.pem | grep -Eo "CN=.+"`)
    issuer="${issuer[0]:3}"
    # Check CoreConfig for CA Element
    crl=(`cat /opt/tak/CoreConfig.xml | grep -Eo "<crl.+/>"`)
    if [[ -z "${crl[0]}" ]]; then
        echo -e "${YELLOW}CRL Element not found in Configuration.${NC}"
        echo -e "${YELLOW}Add the following line within the tls element within the CoreConfig to apply the revokation.${NC}"
        echo -e "${YELLOW}<crl _name="TAKServer CA" crlFile="certs/files/ca.crl"/>${NC}"
        echo -e "${YELLOW}Replace ca.crl with the appropriate crl file.${NC}"
        echo ""
    fi
# Find Issuing CA (.pem)
    if [[ -f $certs/${issuer[0]}.pem ]]; then
        ca="${issuer[0]}"
        key="${issuer[0]}"
    else
# Default Issuing CA
        echo "Issuing CA not found, reverting to default."
        ca="ca"
        key="ca-do-not-share"
    fi
else
    display_err
    exit 0
fi

#End copied code.

# Execute the commands with sudo
sudo su root -c "
    # Print the current process ID for debugging
    echo Current Process ID: $$
    cd $dir/certs || exit
    # Execute the revokeCert script
    $revokeCert $certs/$arg1 $certs/$key $certs/$ca

    #Testing not deleting the revoked certs
    rm -v $certs/$arg1.{pem,key,csr,jks}

    # Exit from the 'tak' user
    exit
"

echo "Deleted user" $arg1
