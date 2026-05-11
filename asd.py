def XTime(a):
        #print("@(posedge clk);")
        #print("input_byte = 8\'d" + str(a)+";")
        retval=(((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)
        #print("assert (output_byte == 8\'d" + str(retval) + ");")
        return retval
for i in range(256):
    print(f"8'h"+"{:02x}".format(i)+": x_time=8'h"+"{:02x}".format(XTime(i))+";")