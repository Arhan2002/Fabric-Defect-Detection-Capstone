import bluetooth
 
devices = bluetooth.discover_devices(lookup_names=True)
print(type(devices))
 
print("Devices found: %s" % len(devices))
 
for item in devices:
    print(item)

# def send_data(device_address, data):
#     try:
#         # Create a Bluetooth socket for sending data
#         socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#         socket.connect((device_address, 3))  # You may need to change the channel number

#         # Send data
#         socket.send(data)

#         # Close the socket 
#         socket.close()

#         print("Data sent successfully.")
#     except Exception as e:
#         print("Error: ", e)
        
# def send_msg(msg):
#     import serial
#     ser=serial.Serial("COM4", 9600)
#     ser.write(bytes(msg, "utf-8"))
if __name__ == "__main__":
    device_address = '24:0A:C4:59:8D:F2'  # Replace with the Bluetooth device address you want to connect to
    data_to_send = "1"

    # send_data(device_address, data_to_send)
    # send_msg("1")