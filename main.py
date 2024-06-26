from groq import Groq
from bs4 import BeautifulSoup
import requests
import json
from PyPDF2 import PdfReader
import os

f = open("config.json", "r")
data = json.load(f)

GROQ_API_KEY = data["GROQ_API_KEY"]
SZKOPUL_API_KEY = data["SZKOPUL_API_KEY"]
AI_MODEL = data["AI_MODEL"]

contest_id = input("[?] Enter the ID of the contest: ")
problem_short_name = input("[?] Enter the short name of the problem: ")
print('')

print("[.] Getting the webpage...")
url = f"https://szkopul.edu.pl/c/{contest_id}/p/{problem_short_name}/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

def parse_html():
    global text

    image_count = 1
    for span in unformatted.findAll('span', {'class': 'texmath'}):
        if image_count == 1:
            print()

        value = input(f"[?] Input the text seen on the LaTeX image #{image_count}: ")
        span.string = value
        image_count += 1

    if image_count != 1:
        print()

    print("[.] Formatting the HTML...")
    formatted_text = []
    for element in unformatted.children:
        if element.name == 'h3':
            formatted_text.append(element.get_text() + '\n')

        elif element.name == 'h2':
            formatted_text.append('\n' + element.get_text())

        else:
            try:
                formatted_text.append(element.get_text())
            except:
                formatted_text.append("[nie udało się pobrać zawartości elementu]")
   
    text = ' '.join(formatted_text)

def parse_pdf():
    global text

    document_path = f"{problem_short_name}.pdf"
    with open(document_path, "wb") as f:
        f.write(response.content)

    reader = PdfReader(document_path)

    image_count = 1
    formatted_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        while text.find("\n ") != -1:
            if image_count == 1:
                print()

            value = input(f"[?] Input the text seen on the LaTeX image #{image_count} from page #{i+1}: ")
            text = text.replace("\n ", value, 1)
            image_count += 1

        formatted_text.append(text)

    if image_count != 1:
        print()

    print("[.] Formatting the PDF...")
    text = '\n\n'.join(formatted_text)

    if os.path.exists(document_path):
        os.remove(document_path)

print("[.] Getting the contents of the task...")
try:
    unformatted = soup.find('section', {'class': 'main-content'}).div
    parse_html()
except:
    parse_pdf()

question = f"""Odpowiedz, podając kod rozwiązania w C++:

{text}""";

print("[.] Connecting with Groq API...")
client = Groq(
    api_key=GROQ_API_KEY,
)

print("[.] Asking the question...")
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": question,
        }
    ],
    model=AI_MODEL,
)

print("[.] Formatting the answer...")
answer = chat_completion.choices[0].message.content

start_index = answer.find('#')
end_index = answer.find('`', start_index)

answer = answer[ start_index : end_index ]

print("[.] Creating a new file...")
file_path = f"{problem_short_name}.cpp"
f = open(file_path, "w")
f.write(answer)
f.close()

print("[.] Subbmiting the answer...")
headers = {
    'Authorization': 'Token ' + SZKOPUL_API_KEY
}
files = {
    'file': (file_path, open(file_path, 'rb'), 'text/cpp')
}
data = {
    'contest_name': contest_id,
    'problem_short_name': problem_short_name
}

url = f"https://szkopul.edu.pl/api/c/{contest_id}/submit/{problem_short_name}"
response = requests.post(url, headers=headers, files=files, data=data)

print("\n[!] Process complete.\n")

print("[i] You can view the result at:")
print(f"https://szkopul.edu.pl/c/{contest_id}/s/{response.text}/")