from PIL import Image, ImageTk

def load_image(path, size=(300, 300)):
    img = Image.open(path)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)
