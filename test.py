CHANNEL_ID = bytes([0])
xx = "abc"
extra_data = CHANNEL_ID + xx.encode('utf-8')
print(extra_data)