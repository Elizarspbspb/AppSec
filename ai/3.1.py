# cipher[i] = plain[i] XOR key[i mod K]
KM = list(map(int, input().split()))
plain = str(input())
plain_2 = str(input())

plain_bytes = [ord(c) for c in plain]
plain_bytes_2 = [ord(c) for c in plain_2]
 
cipher = []
cipher_2 = []
key = "word"
key_bytes = [ord(c) for c in key]

#key_bytes = [c.encode('utf-8').hex(' ') for c in key]

#for i in range(len(plain_bytes)):
#    cipher_byte = plain_bytes[i] ^ key[i % KM[0]]

cipher_hex = []

for i in range(len(plain)):
    cipher.append(int(plain_bytes[i]) ^ int(key_bytes[i % KM[0]]))
print(cipher)
cipher_hex.append(''.join(f'{b:02x}' for b in cipher))
print(cipher_hex[0])

for i in range(len(plain_2)):
    cipher_2.append(int(plain_bytes_2[i]) ^ int(key_bytes[i % KM[0]]))
print(cipher_2)
cipher_hex.append(''.join(f'{b:02x}' for b in cipher_2))
print(cipher_hex[1])


shifr = []
for i in range(KM[1]):
    #cipher_hex = str(input())
    cipher_bytes = bytes.fromhex(cipher_hex[i])
    #print(cipher_bytes)
    shifr.append(cipher_bytes)

H_start = str(input())
message = []

for i in shifr:
    for j, ci in enumerate(i):
        print(ci)
        if j > KM[0]:
            message.append(int(ci) ^ int(key_bytes[j % KM[0]]))
            #cipher.append(int(plain_bytes[i]) ^ int(key_bytes[i % KM[0]]))
    #message = "hi"
    message_good = "".join([chr(b) for b in message])
    print(H_start + ":", message_good)
    message.clear()