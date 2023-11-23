import os
import serial
import argparse
from time import time
from datetime import datetime

import uRAD_USB_SDK11_Ns400doppler as uRAD_USB_SDK11		# import uRAD libray

def main():
    
    #create directory
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        if not os.path.exists(data_path):
            raise Exception(f'Failed to create data directory {data_path}')

    # Serial Port configuration
    ser = serial.Serial()
    ser.port = '/dev/ttyACM0'
    ser.baudrate = 1e6

    # Sleep Time (seconds) between iterations
    timeSleep = 5e-3

    # Other serial parameters
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE

    # Method to correctly turn OFF and close uRAD
    def closeProgram():
        # switch OFF uRAD
        return_code = uRAD_USB_SDK11.turnOFF(ser)
        if (return_code != 0):
            exit()

    # Open serial port
    try:
        ser.open()
    except:
        closeProgram()

    # switch ON uRAD
    return_code = uRAD_USB_SDK11.turnON(ser)
    if (return_code != 0):
        closeProgram()

    # loadConfiguration uRAD
    return_code = uRAD_USB_SDK11.loadConfiguration(ser, mode, f0, BW, Ns, Ntar, Vmax, MTI, Mth, Alpha, distance_true, velocity_true, SNR_true, I_true, Q_true, movement_true)
    if (return_code != 0):
        closeProgram()

    #init output files
    start_str = datetime.strftime(datetime.now(),'%Y%m%d%H%M%S')
    t_0 = time()
    if save_iq:
        file_iq = open(f'{data_path}/{start_str}_{file_prefix}_iq.txt', 'w')
        iterations = 0
    if save_results:
        file_results = open(f'{data_path}/{start_str}_{file_prefix}_processed.txt', 'w')
    # infinite detection loop
    while True:

        # target detection request
        return_code, results, raw_results = uRAD_USB_SDK11.detection(ser)
        if (return_code != 0):
            closeProgram()

        #take timestamp
        t_i = time()

        # Extract results from outputs
        NtarDetected = results[0]
        velocity = results[2]
        SNR = results[3]
        I = raw_results[0]
        Q = raw_results[1]
        ts = t_i-t_0

        #create string
        results_str = ''
        # Iterate through desired targets
        for i in range(NtarDetected):
            # If SNR is big enough
            if (SNR[i] > 0):
                results_str += '%1.3f %1.2f %1.1f ' % (ts, velocity[i], SNR[i])
                    # Prints target information
                if print_results:
                    print("Target: %d, Velocity: %1.1f m/s, SNR: %1.1f dB" % (i+1, velocity[i], SNR[i]))

        if save_iq:        
            #create IQ string
            IQ_string = ''
            for index in range(len(I)):
                IQ_string += '%d ' % I[index]
            for index in range(len(Q)):
                IQ_string += '%d ' % Q[index]
            #write out
            file_iq.write(IQ_string + '%1.3f\n' % ts)
            #iterate
            iterations += 1
            #write out sampling rate
            if (iterations > 100):
                print('Fs %1.2f Hz' % (iterations/(t_i-t_0)))

        if save_results:
            # If number of detected targets is greater than 0 prints an empty line for a smarter output
            if (NtarDetected > 0):
                file_results.write('%s%1.3f\n' % (results_str, t_i))
                print(" ")

        if t_i-t_0 > file_max_duration:
            #new files
            start_str = datetime.strftime(datetime.now(),'%Y%m%d%H%M%S')
            t_0 = time()
            if save_iq:
                file_iq.close()
                file_iq = open(f'{data_path}/{start_str}_{file_prefix}_iq.txt', 'w')
                iterations = 0
            if save_results:
                file_results.close()
                file_results = open(f'{data_path}/{start_str}_{file_prefix}_processed.txt', 'w')
            


if __name__ == '__main__':
    """
    Global vars
    """

    # Parse arguments
    parser_description = "urad capture"
    parser = argparse.ArgumentParser(description = parser_description)
    parser.add_argument(
        '--iq',
        help='flag to save IQ data', action=argparse.BooleanOptionalAction)
    parser.add_argument(
        '--results',
        help='flag to save results', action=argparse.BooleanOptionalAction)
    parser.add_argument(
        '--disp',
        help='flag to display live results data', action=argparse.BooleanOptionalAction)
    parser.add_argument(
        '--prefix',
        default='urad',
        type=str,
        help='file prefix')
    parser.add_argument(
        '--data_path',
        default='/home/hailpi/urad_data',
        type=str,
        help='data folder')
    
    args = parser.parse_args()
    save_iq       = args.iq
    save_results  = args.results
    print_results = args.disp
    file_prefix   = args.prefix
    data_path   = args.data_path

    # input parameters
    mode = 1					# doppler mode
    f0 = 125					# output continuous frequency 24.125 GHz
    BW = 240					# don't apply in doppler mode (mode = 1)
    Ns = 400					# 200 samples
    Ntar = 3					# 3 target of interest
    Vmax = 75					# searching along the full velocity range
    MTI = 0						# MTI mode disable because we want information of static and moving targets
    Mth = 0						# parameter not used because "movement" is not requested
    Alpha = 10					# signal has to be 10 dB higher than its surrounding
    distance_true = False 		# mode 1 does not provide distance information
    velocity_true = False		# request velocity information
    SNR_true = False 			# Signal-to-Noise-Ratio information requested
    I_true = False 				# In-Phase Component (RAW data) not requested
    Q_true = False 				# Quadrature Component (RAW data) not requested
    movement_true = False 		# not interested in boolean movement detection
    file_max_duration = 300     # maximum duration of a file in seconds

    if save_iq:
        I_true = True 				# In-Phase Component (RAW data) requested
        Q_true = True 				# Quadrature Component (RAW data) requested        

    if save_results or print_results:
        velocity_true = True		# request velocity information
        SNR_true = True 			# Signal-to-Noise-Ratio information requested

    main()