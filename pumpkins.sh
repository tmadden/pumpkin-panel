#!/bin/bash
function check_online
{
    netcat -z -w 5 8.8.8.8 53 && echo 1 || echo 0
}

# Initial check to see if we are online
IS_ONLINE=check_online

# Loop while we're not online.
while [ $IS_ONLINE -eq 0 ]; do
    # We're offline. Sleep for a bit, then check again
    sleep 10;
    IS_ONLINE=check_online
done

# Now start the pumpkins.
cd /home/pi/pumpkin-panel
source ".venv/bin/activate"
python3 driver.py
