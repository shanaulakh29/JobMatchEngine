from sentence_transformers import SentenceTransformer
import pdfplumber
from io import BytesIO
from docx import Document


#! TESTING FILE FOR VECTOR EMBEDDINGS

def bytes_to_text(file_bytes: bytes, filename: str) -> str:
    """
    Convert file bytes to plain text.
    Supports PDF, DOCX, TXT.
    """

    filename = filename.lower()

    # -------- PDF --------
    if filename.endswith(".pdf"):
        text_pages = []
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)
        return "\n".join(text_pages)

    # -------- DOCX --------
    elif filename.endswith(".docx"):
        doc = Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    # -------- TXT --------
    elif filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    else:
        raise ValueError("Unsupported file type")

# clean text
def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

# TODO: for better accuracy, can update this based on experiences, skills, education and etc
def chunk_text(text, chunk_size=250, overlap=50):
    words = text.split()
    chunks=[]
    
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size -overlap
    
    return chunks
    
    
    
# grab the txt/pdf file
file = open("test.txt")
file_pdf = open("test.pdf", "rb").read()

text = bytes_to_text(file_pdf, "test.pdf")
# clean the text
text = clean_text(text)


# chunk the file text
chunks = chunk_text(text)



sentences = ("This is an example sentence")



# chunk the data

# model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(chunks)
print(len(embeddings))
print(embeddings.shape)
