from .ocr_service import OCRService
from .pdf_service import PDFService


class ExtractTextService:
    def __init__(self):
        self.ocr_service = OCRService()
        self.pdf_service = PDFService()

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean extracted text by removing escape sequences and normalizing whitespace.

        Args:
            text (str): Raw extracted text.
        Returns:
            str: Cleaned text.
        """
        # Replace literal escape sequences (e.g. "\n", "\t", "\r") with a space
        text = text.replace("\\n", " ")
        text = text.replace("\\t", " ")
        text = text.replace("\\r", " ")

        # Replace actual newline / carriage-return characters with a space
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        text = text.replace("\t", " ")

        # Collapse multiple spaces into one
        while "  " in text:
            text = text.replace("  ", " ")

        return text.strip()

    def extract_text(self, file_path):
        """
        Service method to extract text from a given file path.

        Args:
            file_path (str): The path to the file from which to extract text.
        Returns:
            str: The extracted and cleaned text from the file.
        """
        if file_path.endswith(".pdf"):
            image_paths = self.pdf_service.pdf_to_images(file_path)
            text = ""
            for path in image_paths:
                extracted_text: str = self.ocr_service.extract(path)
                text += extracted_text + " "
            return self.clean_text(text)
        else:
            raw_text = self.ocr_service.extract(file_path)
            return self.clean_text(raw_text)
