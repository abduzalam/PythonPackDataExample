import struct

# Example data
index = 42 # the position of the data in the file
value = 3.14 # the value to be stored

# Pack data as 4 byte integer followed by 4 byte float
packed_data = struct.pack('if', index, value)
print(packed_data)
# struct.pack() is the function used to take your Python values and convert them into a bytes object.
'''
The first argument `'if'` is a format string that specifies the format of the data to be packed. 
        - `i` stands for an integer, which is typically 4 bytes in C (hence, a 4-byte integer).
        - `f` stands for a float, which is typically 4 bytes in C (hence, a 4-byte float).
   - The subsequent arguments are the values to be packed according to the format string. In this case, `index` is packed as an integer and `value` as a float.

The result, `packed_data`, is a bytes object that contains the binary representation of `index` and `value` in the order specified by the format string.

You can also unpack the data, converting it back to Python values:
'''

# Unpack data as 4 byte integer followed by 4 byte float

unpacked_data = struct.unpack('if', packed_data)
print(unpacked_data )

'''
In this example, `struct.unpack()` is the inverse operation of `struct.pack()`. It takes a bytes object and converts it back into Python values based on the format string provided. The returned value is a tuple containing the unpacked data.

It's important to note that the `struct` module adheres to C standards, and so the size and format of the data can depend on the system architecture (32-bit vs 64-bit, endianness, etc.). To ensure consistency across platforms, `struct` provides character prefixes to the format string that allow you to specify endianness and standard sizes:

- `<` indicates little-endian
- `>` indicates big-endian
- `=` uses the native endianness and size
- `!` is network (= big-endian)

For example, `struct.pack('<if', index, value)` ensures little-endian packing regardless of the system's native endianness.
'''