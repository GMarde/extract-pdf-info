import os
from dotenv import load_dotenv
import PyPDF2
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
pdf_path = os.getenv("PDF_PATH")
output_path = "output.txt"
client = OpenAI(api_key=api_key)

def extract_text_from_pdf(path):
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def extract_info_with_chatgpt(pdf_text):
    prompt = f"""
Extract the following information from the text below:
- Full name
- CPF (Brazilian taxpayer ID)
- Postal code (CEP)

Text:
\"\"\"
{pdf_text}
\"\"\"

Respond only with the extracted data in this format:
Full name: ...
CPF: ...
Postal code: ...
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    return response.choices[0].message.content

# In case some information is missing (API key or the PDF)
def main():
    if not api_key or not pdf_path:
        print("Missing OPENAI_API_KEY or PDF_PATH.")
        return

    pdf_text = extract_text_from_pdf(pdf_path)
    extracted_info = extract_info_with_chatgpt(pdf_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(extracted_info)

    print(f"Data extracted and saved to: {output_path}")

if __name__ == "__main__":
    main()
