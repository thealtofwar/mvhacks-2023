from PIL import Image
import numpy as np
import sys

def is_flashing(img, variance_threshold=1_000, pixel_threshold=0.1, chunk_size = 10) -> bool:
    with Image.open(img) as im:
        im.seek(0)
        frames = []
        try:
            while 1:
                im.seek(im.tell() + 1)
                grayscale = im.convert("L")
                imarray = np.array(grayscale)
                clumps: "list[np.ndarray]" = []
                for i in range(0, imarray.shape[0], chunk_size):
                    for j in range(0, imarray.shape[1], chunk_size):
                        clumps.append(imarray[i:i+chunk_size,j:j+chunk_size])
                converted = []
                for clump in clumps:
                    converted.append(np.average(clump))
                frames.append(converted)
        except EOFError:
            pass
        print(im.tell())
        moved: list[list[float]] = []
        for frame in frames:
            for i in range(len(frame)):
                if len(moved) == i:
                    moved.append([])
                moved[i].append(frame[i])
        bad_pixels = len(list(filter(lambda k: k > variance_threshold, map(np.var, moved))))
        im.seek(0)
        return (im.size[0] * im.size[1]) / (chunk_size ** 2) * pixel_threshold <= bad_pixels

if __name__ == "__main__":
    print(is_flashing(sys.argv[1]))