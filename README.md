
#### Prototype Python software for operating the uRAD radar as a hail disdrometer

https://urad.es/

Designed to be run on a Raspberry pi 4 with the urad connected via USB. The Raspberry pi 4 can also be confiured to act as a wireless hotspot, allowing remote access. A RTC should ideally be used and the UTC+0 timezone configured.

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

An example of how to save results and print results follows:

`python3 urad_capture.py ---results --disp --prefix="urad" --data_path="/my/home/folder"`

The signal processing library provided by urad is contained in `uRAD_USB_SDK11_Ns400doppler.py`

