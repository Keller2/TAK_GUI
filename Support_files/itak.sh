#!/bin/bash

#Program Setup
#Change username to your username
username=$1
arg1=$2
arg2=$3

echo "Username:" $username " this should be your PC username or it will cause errors." 
echo "Creating user " $arg1
echo "On Team " $arg2

# Switch to the target directory
cd /opt/tak/certs/

# Execute the commands with sudo
sudo su tak -c "
    # Print the current process ID for debugging
    echo Current Process ID: $$
    
    # Execute the makeCert script
    ./makeCert.sh client $arg1

    # Exit from the 'tak' user
    exit
"

# Run the command using the generated certificate
sudo java -jar /opt/tak/utils/UserManager.jar certmod /opt/tak/certs/files/$arg1.pem

sudo java -jar /opt/tak/utils/UserManager.jar usermod -ig _Users_ -g $arg2 -ig _Global_Eye_ $arg1

#sudo systemctl restart takserver

sudo su tak -c "
    # Print the current process ID for debugging
    echo Current Process ID: $$
    
    # Execute the makeCert script

    cd /opt/tak/certs/files/
    chmod 777 $arg1.*

    # Exit from the 'tak' user
    exit
"

cp -r ~/Desktop/TAK_GUI/Support_files/DO_NOT_EDIT_ITAK ~/Downloads/$arg1

cp /opt/tak/certs/files/$arg1.p12 ~/Downloads/$arg1/iphone.p12

cd /home/$username/Downloads/

sudo zip -v -r $arg1.zip $arg1

wait

sudo chown $username $arg1.zip

wait

rm -r $arg1

















