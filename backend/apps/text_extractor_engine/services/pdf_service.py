from pdf2image import convert_from_path


def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    paths = []

    for i, img in enumerate(images):
        path = f"{pdf_path}_page_{i}.jpg"
        img.save(path, "JPEG")
        paths.append(path)

    return paths
