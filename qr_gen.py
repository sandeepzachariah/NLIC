import qrcode
from PIL import Image, ImageDraw, ImageFont

LABEL = "New Life Indian Church"
URL = "https://www.newlifeindianchurch.com"
FONT_SIZE = 28
PADDING = 20  # space between QR and label, and below label

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4,
)
qr.add_data(URL)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
qr_w, qr_h = qr_img.size

# Try to load a clean font; fall back to default if not available
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", FONT_SIZE)
except (IOError, OSError):
    font = ImageFont.load_default()

# Measure text size
dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
bbox = dummy.textbbox((0, 0), LABEL, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

canvas_w = max(qr_w, text_w + PADDING * 2)
canvas_h = qr_h + PADDING + text_h + PADDING

canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
canvas.paste(qr_img, ((canvas_w - qr_w) // 2, 0))

draw = ImageDraw.Draw(canvas)
text_x = (canvas_w - text_w) // 2
text_y = qr_h + PADDING
draw.text((text_x, text_y), LABEL, fill="black", font=font)

canvas.save("NLIC_QR.png")
print(f"Saved NLIC_QR.png ({canvas_w}x{canvas_h}px)")
