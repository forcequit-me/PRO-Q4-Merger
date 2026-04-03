from PIL import Image
img = Image.open(r'C:\Users\plagi\Desktop\PRO-Q4\Pro Q 4 UI Screenshot.png')
# Resize to make pixel access fast
small = img.resize((256, 144), Image.NEAREST).convert('RGB')
sw, sh = small.size
print(f"Resized to {sw}x{sh}")

# Map original coords (2559x1439) to small (256x144)
def sample(name, ox, oy):
    x = int(ox * 256 / 2559)
    y = int(oy * 144 / 1439)
    r, g, b = small.getpixel((x, y))
    print(f"{name}: #{r:02x}{g:02x}{b:02x} rgb({r},{g},{b})")

sample("bg_top_center", 1280, 60)
sample("bg_center_dark", 1280, 720)
sample("bg_lower_dark", 1280, 1200)
sample("bg_bottom_left", 200, 1300)
sample("header_bar", 1280, 17)
sample("blue_eq_fill", 900, 500)
sample("green_eq_fill", 1800, 480)
sample("teal_line_area", 1400, 480)
sample("red_band_dot", 545, 468)
sample("blue_band_dot", 985, 338)
sample("green_band_dot", 1117, 525)
sample("magenta_band_dot", 1703, 350)
sample("orange_curve_mid", 1000, 430)
sample("orange_curve_low", 400, 480)
sample("gain_label_orange", 2100, 375)
sample("freq_label_gray", 1415, 1120)
sample("bottom_status_bar", 1280, 1420)
sample("grid_zero_line", 1280, 478)
sample("pink_curve_area", 1800, 420)
