import pyvisa
#import visa
import matplotlib.pyplot as plt

print('hello world')
# Make connection to instrument
visa_identifier = 'USB0::0x2A8D::0x0396::CN62097178::0::INSTR' 
                     # in the form: <connection type>::<address>::<interface>::INSTR
                     # can also be copied from a VISA software
                     # We have Keysight Connection Expert on our PC.
                     # Connect to the machine and copy the VISA address here 
rm = pyvisa.ResourceManager()
scope = rm.open_resources(visa_identifier)

# Measurement setup variables
vRange = 2  #oscilloscope's vertical range
tRange = 500e-9 # time range (horizontal axis)
trigLevel = 0 # trigger level
ch = 1 #channel of interest

#TODO: check the machine we are using and set varaibles as needed
# we need frequency as horizontal axis, dB and degrees as vertical axis


# preset and wait for operation to complete
scope.write('*rst') # this is for setting instrument back to default configuration
scope.write('*opc?') # this is for waiting until completion of previous commands before moving forward


# set up vertical and horizontal ranges
# scope.write(f'channel{ch}:range{vRange}')
# scope.write(f'timebase:range{tRange}')
# set up trigger mode and level
# scope.write('trigger:mode edge')
# scope.write(f'trigger:level{ch}, {trigLevel}')

#TODO: still, check SCPI command to set our own configurations, this is code example for an oscilloscope

# set waveform source
scope.write(f'waveform:source channel{ch}')

# specify waveform format
scope.write('waveform:format byte') # any waveform data sent is formatted as signed 8-bit integers

# Capture data
scope.write('digitize')

# Transfer binary waveform data from scope
data = scope.query_binary_values('waveform:data?', datatype = 'b') # keep datatype same as data sent from instrument
                                                                   # note for signed, unsigned and big endian, little endian
                                                                   # query_binary_values() has argument us_big_endian to specify
                                                        
# Query x and y values to scale the data appropriately for plotting
xIncrement = float(scope.query('waveform:xincrement?'))
xOrigin = float(scope.query('waveform:xorigin?'))
yIncrement = float(scope.query('waveform:yincrement?'))
yOrigin = float(scope.query('waveform:yorigin?'))
length = len(data)


# list storage of x-axis and y-axis
time = [(t * xIncrement) + xOrigin for t in range(length)] # x-axis
wfm = [(d * yIncrement) + yOrigin for d in data] # y-axis

# plot waveform data
plt.plot(time, wfm)
plt.title('Waveform')
plt.xlabel('Time (sec)')
plt.ylabel('Voltage (V)')
plt.show()