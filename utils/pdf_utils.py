import fitz
import os

class PDFCompareError(Exception):
    pass

class PDFComparer:
    def __init__(self, file1, file2):
        if not os.path.exists(file1) or not os.path.exists(file2):
            raise PDFCompareError("One or both PDF files not found.")
        self.doc1 = fitz.open(file1)
        self.doc2 = fitz.open(file2)

    def close(self):
        self.doc1.close()
        self.doc2.close()

    def compare(self, check: str, **kwargs):
        try:
            match check:
                case "page_count":
                    return self.doc1.page_count == self.doc2.page_count

                case "total_text":
                    text1 = "".join(p.get_text() for p in self.doc1)
                    text2 = "".join(p.get_text() for p in self.doc2)
                    return len(text1) == len(text2)

                case "text_range":
                    start = kwargs.get("start", 0)
                    end = kwargs.get("end", min(self.doc1.page_count, self.doc2.page_count))
                    text1 = "".join(self.doc1[i].get_text() for i in range(start, end))
                    text2 = "".join(self.doc2[i].get_text() for i in range(start, end))
                    return text1 == text2

                case "marker_section":
                    page = kwargs["page"]
                    start_marker = kwargs["start_marker"]
                    end_marker = kwargs["end_marker"]

                    def extract_section(doc):
                        text = doc[page].get_text()
                        start = text.find(start_marker)
                        end = text.find(end_marker, start)
                        return text[start:end+len(end_marker)] if start != -1 and end != -1 else ""

                    return extract_section(self.doc1) == extract_section(self.doc2)

                case "position":
                    keyword = kwargs["keyword"]
                    page = kwargs["page"]
                    positions = []
                    words = self.doc1[page].get_text("words")
                    for w in words:
                        if w[4] == keyword:
                            positions.append((w[0], w[1]))  # x, y
                    return positions

                case _:
                    raise PDFCompareError(f"Unknown comparison type: {check}")
        except Exception as e:
            raise PDFCompareError(f"Error during '{check}' comparison: {e}")


#Usage Example
""" from pdf_compare_utils import PDFComparer

assert PDFComparer("doc1.pdf", "doc2.pdf").compare("page_count")
assert PDFComparer("doc1.pdf", "doc2.pdf").compare("total_text")
assert PDFComparer("doc1.pdf", "doc2.pdf").compare("text_range", start=0, end=2)
assert PDFComparer("doc1.pdf", "doc2.pdf").compare("marker_section", start_marker="Start", end_marker="End", page=0)
positions = PDFComparer("doc1.pdf", "doc2.pdf").compare("position", keyword="Invoice", page=0)
 """