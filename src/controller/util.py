

# return block pt
def plaintext_to_block(byte_pt, block_length):
    pt = [str(x).rjust(3, "0") for x in byte_pt]
    pt = ''.join(pt)
    pt = [int(pt[i:i+block_length]) for i in range(0, len(pt), block_length)]
    # print(pt)
    return pt

# return plaintext bytes
def block_to_plaintext(arr_block, block_length):
    arr = [str(i).rjust(block_length, "0") for i in arr_block]
    arr = "".join(arr)
    arr = [int(arr[i:i+3]) for i in range(0, len(arr), 3)]
    return bytes(arr)

if __name__ == "__main__":
    f = open("test.txt", "rb")
    pt = f.read()
    f.close()
    plaintext_to_block(pt, 10)
    