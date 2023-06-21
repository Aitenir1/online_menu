import qrcode



for i in range(1,6):
    data = f"http://192.168.0.47:3000/{i}"
    img = qrcode.make(data)
    img.save(f'qrcodes/table_{i}_qr_code.png')

