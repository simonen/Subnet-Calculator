print(">>> Hex To Binary Converter <<< by don simone")
print("### MAC Example: E8-11-32-4E-07-DB. Type 'quit' to end the program ###")
mac = input("Enter MAC address: ")

while mac != "quit":
    mac = mac.split("-")
    try:
        res = [f"{int(x, 16):08b}" for x in mac]
        print("-".join(res))
    except:
        print("Invalid HEX number")
    mac = input("Enter MAC address: ")

# for i in range(len(hex)):
#     hex[i] = f"{int(hex[i], 16):08b}"

# print("-".join(hex))
