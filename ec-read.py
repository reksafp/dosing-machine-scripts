import serial
import time
import struct

# Output the data part of the stream
def strip_chars(string, index, N):
    substr = string[index:index+N]
    return substr

def hex2float (input):
    val = round(struct.unpack("!f", bytes.fromhex(input))[0],2)
    return val

# Create a serial connection
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1
    )

ec_read = [0x03, 0x03, 0x00, 0x00, 0x00, 0x04, 0x45, 0xEB]
sl_read = [0x03, 0x03, 0x00, 0x08, 0x00, 0x04, 0xC4, 0x29]
tm_read = [0x03, 0x03, 0x00, 0x04, 0x00, 0x04, 0x04, 0x2A]

ser.write(serial.to_bytes(ec_read)) #EC command
ec_raw = ser.read(17).hex()         #EC raw stream
ser.flushInput()

ser.write(serial.to_bytes(tm_read)) #Temp command
tm_raw = ser.read(17).hex()         #Temp raw stream
ser.flushInput()

ser.write(serial.to_bytes(sl_read)) #Salinity command
sl_raw = ser.read(17).hex()
ser.flushInput()

#TODO: implement CRC16 checking on incoming byte streams

# Strip the data part of the stream
#ec_data = strip_chars(ec_raw, 6, 8) # assuming CDAB byte order
ec_data = strip_chars(ec_raw, 10, 4) + strip_chars(ec_raw, 6, 4) #assuming ABCD byte order
tm_data = strip_chars(tm_raw, 10, 4) + strip_chars(tm_raw, 6, 4)
sl_data = strip_chars(sl_raw, 10, 4) + strip_chars(sl_raw, 6, 4)

# Conversions
ec_val = 0
tm_val = 0
sl_val = 0
try:
  ec_val = hex2float(ec_data)
  tm_val = hex2float(tm_data)
  sl_val = hex2float(sl_data)

except:
  print("no reply from the probe")

# Debug print the values
print('ec_val: ', ec_val)
print('tm_val: ', tm_val)
print('sl_val: ', sl_val)
#print(ec_raw)
#print(ec_data)


# Close the serial connection
ser.close()
