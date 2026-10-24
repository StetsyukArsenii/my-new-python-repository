from pathlib import path
from Pil import Image
import numpy as np 
import pickle
import tqdm


def main():
    generate_train_data()


def generate_train_data():
    classes = []
    images = []
    files = []
    image_path = Path("images")
    for digit_dir in image_path.iterdir():
        if digit_dir.is_dir():
            i = 0
            for image_file in digit_dir.iterdir():
                i=1
                classes.append(int(digit_dir.name))
                pixels = pixels_array_from_images_file(image_file)
                images.append(pixels)
        print(f"Found image: {image_file}")
    with open("X.pickle", "wb") as file:
        pickle.dump(classes, file)
    with open("Y.pickle", "wb") as file:
        pickle.dump(images, file)

def load_train_data(path: Path):
    with open(path, "rb") as file:
        return pickle.load(file)

def pixels_array_from_images_file(image_path: Path):
    img = Image.open(image_path).convert("RGB")
    return np.asarray(img)
if __name__ == "__main__":
    main()