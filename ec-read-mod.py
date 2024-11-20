import os.path
import sys
import serial
import time
import struct
import argparse
import crcmod
import binascii

# Strip charactes out of the byte stream
def strip_chars(string, index, N):
    substr = string[index:index+N]
    return substr

def strip_data(string):
    substr = strip_chars(string, 10, 4) + strip_chars(string, 6, 4)
    return substr

def strip_crc(string):
    substr = strip_chars(string, 24, 2) + strip_chars(string, 22, 2)
    return substr

def strip_msg(string):
    substr = strip_chars(string, 0, 22)
    return substr

def hex2float (input):
    val = round(struct.unpack("!f", bytes.fromhex(input))[0],2)
    return val

def compute_crc(byte_string):
    # Split the hex stream into pairs of characters
    hex_pairs = [byte_string[i:i+2] for i in range(0, len(byte_string), 2)]

    #Map to bytearray
    b = bytearray()
    for pair in hex_pairs:
        b +=  binascii.unhexlify(pair)

    crc_fun = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    crc = hex(crc_fun(b))[2:].zfill(4)

    return crc

def check_crc(comp_crc, extr_crc):
    if comp_crc == extr_crc:
        result = True
    else:
        result = False
    return result

# Parse arguments with argparse

parser = argparse.ArgumentParser()
parser.add_argument("channelNum", help="the channel number to read", type=int)
args = parser.parse_args()
chan = args.channelNum

# Check availability of adapters and sanity checks

#TODO: check for possible adapter numbering swapping (edge case, unlikely)

if os.path.exists("/dev/ttyUSB0"):
    print("First Modbus adapter detected.")
else:
    print("The first Modbus adapter does not exist. Aborting")
    sys.exit(1)

if os.path.exists("/dev/ttyUSB1"):
    print("Second Modbus adapter detected. Channel 3-4 enabled")
    chan34 = True
else:
    print("The second Modbus adapter does not exist")
    chan34 = False

if chan > 2 and chan34 == False:
    print("Nonexistent channel chosen. Aborting")
    sys.exit(1)
else:
    print("Channel " + str(chan) + " selected")

# Adapter conditionals

if chan in (1, 2):
   usedPort = '/dev/ttyUSB0'
elif chan in (3, 4):
   usedPort = '/dev/ttyUSB1'

# Create a serial connection based on selected channel
ser = serial.Serial(
    port=usedPort,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1
    )

# Check if it's "odd" or "even" channel (because not really!)
# Probe addresses are identical in both buses, only different port

if chan in (1, 3):
    ec_read = [0x03, 0x03, 0x00, 0x00, 0x00, 0x04, 0x45, 0xEB]
    sl_read = [0x03, 0x03, 0x00, 0x08, 0x00, 0x04, 0xC4, 0x29]
    tm_read = [0x03, 0x03, 0x00, 0x04, 0x00, 0x04, 0x04, 0x2A]
elif chan in (2, 4):
    ec_read = [0x06, 0x03, 0x00, 0x00, 0x00, 0x04, 0x45, 0xBE]
    sl_read = [0x06, 0x03, 0x00, 0x08, 0x00, 0x04, 0xC4, 0x7C]
    tm_read = [0x06, 0x03, 0x00, 0x04, 0x00, 0x04, 0x04, 0x7F]

ser.write(serial.to_bytes(ec_read)) #EC command
ec_raw = ser.read(13).hex()         #EC raw stream
ex_crc = strip_crc(ec_raw)
ec_msg = strip_msg(ec_raw)
ec_crc = compute_crc(ec_msg)
ec_vld = check_crc(ec_crc, ex_crc)
ser.flushInput()

ser.write(serial.to_bytes(tm_read)) #Temp command
tm_raw = ser.read(13).hex()         #Temp raw stream
tx_crc = strip_crc(tm_raw)
tm_msg = strip_msg(tm_raw)
tm_crc = compute_crc(tm_msg)
tm_vld = check_crc(tm_crc, tx_crc)
ser.flushInput()

ser.write(serial.to_bytes(sl_read)) #Salinity command
sl_raw = ser.read(13).hex()         #Salinity raw stream
sx_crc = strip_crc(sl_raw)
sl_msg = strip_msg(sl_raw)
sl_crc = compute_crc(sl_msg)
sl_vld = check_crc(sl_crc, sx_crc)
ser.flushInput()

# Strip the data part of the stream
ec_data = strip_data(ec_raw)
tm_data = strip_data(tm_raw)
sl_data = strip_data(sl_raw)

# Conversions
if ec_vld == False:
    print("EC reading corrupted")
    sys.exit(42)
else:
    ec_val = hex2float(ec_data)

if tm_vld == False:
   print("Temp reading corrupted")
   sys.exit(42)
else:
   tm_val = hex2float(tm_data)

if sl_vld == False:
   print("Salinity reading corrupted")
   sys.exit(42)
else:
   sl_val = hex2float(sl_data)

# Output the values
print('ec_val: ', ec_val)
print('tm_val: ', tm_val)
print('sl_val: ', sl_val)

# Debug print
#print('Raw output :', ec_raw)
#print('EC FP data :', ec_data)
#print('EC message :', ec_msg)
#print('Extr\'d CRC :',ex_crc)
#print('Calc\'d CRC :',ec_crc)
#print('CRC match? :', ec_vld)

# Close the serial connection
ser.close()
