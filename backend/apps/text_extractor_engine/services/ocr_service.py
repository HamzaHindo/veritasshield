import easyocr

reader = easyocr.Reader(["en"])


class OCRService:
    @staticmethod
    def extract(image_path: str):
        result = reader.readtext(image_path)

        text_parts = [line[1] for line in result]

        confidence = 0
        if result:
            confidence = sum(line[2] for line in result) / len(result)

        return "\n".join(text_parts)
