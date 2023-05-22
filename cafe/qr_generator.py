import qrcode

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=2
    )

    qr.add_data(url)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    return qr_image


for i in range(0, 100):
    qr_image = generate_qr_code(f"https://menu-rosy-three.vercel.app/{i}")
    qr_image.save(f"qr_codes/table_{i // 4 + 1}_{i % 4 if i % 4 != 0 else 4}.png")

url = "https://google.com"
generate_qr_code(url)