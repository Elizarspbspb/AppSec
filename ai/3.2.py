KM = list(map(int, input().split()))
H_start = str(input())
message = []
shifr = []

for i in range(KM[1]):
    cipher_hex = str(input())
    cipher_bytes = bytes.fromhex(cipher_hex)
    shifr.append(cipher_bytes)

key_bytes = []

for i in shifr:
    for j, ci in enumerate(i):
        if j >= KM[0]:
            break
        key_bytes_2 = [ord(c) for c in H_start]
        key_bytes.append(int(key_bytes_2[j]) ^ int(ci))
    #key_bytes = [ord(c) for c in H_start]
    for jj, ci in enumerate(i):
        #key_bytes = [ord(c) for c in H_start]
        #message.append(int(ci) ^ int(key_bytes[j % KM[0]]))
        if jj > len(H_start):
            message.append(int(ci) ^ int(key_bytes[jj % KM[0]]))
    message_good = "".join([chr(b) for b in message])
    print(H_start + ":" + message_good)
    message.clear()