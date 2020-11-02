# return block pt
def plaintext_to_block(byte_pt, block_length):
    pt = [str(x).rjust(3, "0") for x in byte_pt]
    pt = ''.join(pt)
    # pt = [int(str(int(pt[i:i+block_length])).ljust(block_length, "0")) for i in range(0, len(pt), block_length)]
    pt = [str(pt[i:i+block_length]) for i in range(0, len(pt), block_length)]
    pt[-1] = pt[-1].ljust(block_length, "0")
    temp = [int(i) for i in pt]
    # print(pt)
    print("hasil konkat :", temp)
    return temp

# return plaintext bytes
def block_to_plaintext(arr_block, block_length):
    arr = [str(i).rjust(block_length, "0") for i in arr_block]
    arr = "".join(arr)
    arr = [(int(arr[i:i+3]) % 256) for i in range(0, len(arr), 3)]
    print("array int : ",arr)
    return bytes(arr).rstrip(b'\x00')

if __name__ == "__main__":
    f = open("test.txt", "rb")
    pt = f.read()
    f.close()
    plaintext_to_block(pt, 10)
