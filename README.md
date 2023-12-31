
### uRAD Hail Disdrometer

#### Prototype Python software for operating the uRAD radar as a hail disdrometer

https://urad.es/

Designed to be run on a Raspberry pi 4 with the urad connected via USB. The Raspberry pi 4 can also be confiured to act as a wireless hotspot, allowing remote access. A RTC should ideally be used and the UTC+0 timezone configured.

### Options

The main script is the `urad_capture.py`.
The following options are implemented:

**--iq** 

This will write the iq data to the ascii file __{data_path}/{prefix}_YYYYMMDDHHMMSS_iq.txt__. A new file is generate every five minutes.

**--results** 

This will write the results data to the ascii file __{data_path}/{prefix}_YYYYMMDDHHMMSS_results.txt__. A new file is generate every five minutes.

**--disp**  

This option will display any results data if an object is present

**--prefix**=STR 

Here the user defines a string which is used in the file naming

**--data_path**=STR

Here the user defined the data output folder as a string. This folder will be created if it does not exist

### How to run

An example of how to save results and print results follows:

`python3 urad_capture.py ---results --disp --prefix="urad" --data_path="/my/home/folder"`

The signal processing library provided by urad is contained in `uRAD_USB_SDK11_Ns400doppler.py`

### Data Structure

Results data contains the columns
seconds_since_start, velocity (m/s), SNG (dB)

IQ data rows consist of
seconds_since_start, sequence of I, sequence of Q

### Authors

uRAD team (Victor Torres, Diego Gaston), Joshua Soderholm, Julian Brimelow 

### Evironment

Raspberry Pi OS (64 Bit).
Miniforge (ARM64) -> use to create an env for this software.
Dependency: pyserial (installed via conda)
Enable RTC: first enable I2C from raspi-config, https://forums.raspberrypi.com/viewtopic.php?t=334986, write system time to hwclock using hwclock -w
