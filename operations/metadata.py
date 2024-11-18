from pathlib import Path
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

def get_meta_data(path):
    with open(path, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        return doc.info[0]

keys = ['Keywords', 'ModDate', 'Subject', 'CreationDate', 'Author', 'Producer', 'Title', 'Creator']

def meta_check(path) -> bool:
    metadata = get_meta_data(path)
    for key in keys:
        value = metadata.get(f"{key}", "")
        if value != "":
            try:
                _ = value.decode()
            except:
                return False
    return True

producers = ["OpenPDF 1.3.30.jaspersoft.2", "Samsung Electronics", "iText 2.1.7 by 1T3XT"]

def producer_check(path) -> bool:
    metadata = get_meta_data(path)

    value = metadata.get("Producer", "")
    if value != "":
        try:
            _ = value.decode()
            if value.decode() in producers:
                return True
            else:
                return False
        except:
            return False
    else:
        return False

def z_check(path) -> bool:
    metadata = get_meta_data(path)

    value = metadata.get(f"CreationDate", "")
    if value != "":
        try:
            _ = value.decode()
            if "Z" in value.decode():
                return False
            else:
                return True
        except:
            return False
    else:
        return False