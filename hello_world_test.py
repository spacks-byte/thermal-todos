#!/usr/bin/env python3

from escpos.printer import Usb

def main():
    # Initialize the USB printer
    # 0x456 and 0x0808 are the vendor ID and product ID from lsusb
    # 0x81 and 0x03 are the bEndpointAddress for input and output
    p = Usb(0x456, 0x0808, in_ep=0x81, out_ep=0x03, profile="POS-5890")
    
    # Print "Hello World"
    p.text("Hello World\n")
    
    # Add some spacing and cut the paper
    p.text("\n\n\n")

    

if __name__ == '__main__':
    main()
