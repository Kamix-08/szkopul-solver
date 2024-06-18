from groq import Groq
from bs4 import BeautifulSoup
import requests
import json

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
soup = BeautifulSoup(requests.get(url).text, "html.parser")

print("[.] Getting the contents of the task...")
unformatted = soup.find('section', {'class': 'main-content'}).div

image_count = 1
for span in unformatted.findAll('span', {'class': 'texmath'}):
    if image_count == 1:
        print()

    value = input(f"[?] Input the text seen on the image #{image_count}: ")
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
        formatted_text.append(element.get_text())

text = ' '.join(formatted_text)

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