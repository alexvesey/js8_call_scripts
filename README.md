# js8_call_scripts

## Venv Setup Instructions

You will only need to do this once when setting up the project initially

`python3 -m venv .venv`
`source .venv/bin/activate`
`pip3 install -r requirements.txt`

See also the [pyjs8call install instructions](https://github.com/simplyequipped/pyjs8call?tab=readme-ov-file#installation) TL;DR `sudo apt install xvfb`

## Running the scripts
- `./ghostnet.sh` will start the raio and set the freq to the [ghostnet frequency on the 40m band](https://github.com/s2underground/GhostNet). This script takes no args.
- `./js8call.sh` is the same as `./ghostnet.sh` bit sets the frequency to the standard js8 frequency on the 40m band (7.078Mhz).
- `python3 js8.py --gn` or `python3 js8.py --gn` You can run the python script directly but will need to have activated the venv to do so.

By default all of the scripts log both to stdout (the terminal) and a file called 'js8call.log' that gets created in the root directory of this repo. Note: This log file is appended to so it will persist messages through a stop and restart of the script.

## Assumptions
These scripts assume:
- that your radio is set up correctly (minus the frequency setting)
- that JS8call is installed and configured correctly for your radio.
- that you are running on Ubuntu
- probably a lot of other things
