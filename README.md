# AES-256-python
Implementation of AES-256 fully in Python. Zero usage of additional libraries, staying as much as close to plain python as possible. No optimizations as of yet, as this is as close as we can be to a 1 to 1 recreation of the original NIST specification for AES-256. The NIST paper for AES available in the sources and <a href="https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf" target="_blank">here</a>

## Current work
 - Implemented Key Expansion. Tested with NIST example for AES-256.
 - Implemented Encrypt. Tested with NIST example for AES-256.
 - Implemenrted Decrypt. Tested with NIST example for AES-256 and cyclic Encrypt -> Decrypt with arbitrary data.
 - Implemented Galois Counter Mode of operation. Tested with a cyclic Encrypt -> Decrypt. Can be expanded further if need be.

## Future work
This implementation will be used as a starting point and testbed for an FPGA implementation on the Xilinx PYNQ Z2 board. Leveraging the power of having Python on the board itself, this code will be used to validate the Overlay on the Z2 implementing AES-256 in FPGA fabric.
