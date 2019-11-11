# Comms Class 2.0
**NOTE**: In its current state, reading information from the Arduino does is not fully implemented and may cause a crash


The past assignments were key challenges that helped develop the foundation for communications. In demo 1, we developed the necessary lower-level protocols needed for basic command and control. It was also a great time for establishing the accruacy of our control algorithms. 

Demo 2 brings about a new challenge which requires further abstracton of our protocols and procedures. Comms 2.0 features a heavily updated and cleaner API. This new interface handles low-level operations and simiplifies the process of sending commands.


## Packets
This class was designed to send only floats. The packet structure is as follows

## Parameters
```py
CHANGE_POS = 0x03
WRITE_ANGLE = 0x09
READ_ANGLE = 0x0A
```
## How to use

### Initializing
```py
import numpy as np
from Comms import Comms
com = Comms("SUPERBOT") # init a comms object. init string writes to string
```

### Sending Data
Contruct a list such that the first element is the instruction. Every element following the instruction should be of type **float**. For most cases, you will only need to send an instruction and a single value.

```py
payload = [com.WRITE_ANGLE, np.pi/2] # Construct a packet
com.sendData(payload) # send data
```

**NOTE**: If you try to send data in the form of a string, or if float values are not of type float, the function call will simply return without sending any data to the arduino. 




## Packet Structure
How does the Comms class format the actual bytes payload that gets sent to the Arduino? 
This is important to know when handling incoming packets on the Arduino. 
We know from the [Sending Data](###sending-data) section that for a simple angle change, we call the ```Comms.sendData``` method with a specified packet structure. 
This method converts the instruction and floating-point values into raw bytes before sending.
The method also embeds some extra information regarding the size of the packet as well.
Such packet has the following format

Byte:
1. Instruction
2. Number of floating point values following the instruction
3. Floating-point value 1: Byte 0
4. Floating-point value 1: Byte 1
5. Floating-point value 1: Byte 2
6. Floating-point value 1: Byte 3

7. etc ...