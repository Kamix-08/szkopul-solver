# szkopul-solver

![GitHub License](https://img.shields.io/github/license/Kamix-08/szkopul-solver)

This Python script automates the process of solving problems from [Szkopuł](https://szkopul.edu.pl)

```bash
git clone https://github.com/Kamix-08/szkopul-solver
cd szkopul-solver
```

## Features

- **Task scraping**: automatically extracts task details from Szkopuł
- **AI integration**: utilizes [Groq](https://groq.com) to process and solve tasks
- **Code submission**: formats the solutions into a `.cpp` file and submits them back to Szkopuł

## Prerequisites

Before executing the script, install the dependencies, by running

```bash
pip install -r requirements.txt
```

The dependencies include:

- `groq>=0.9.0`
- `bs4>=0.0.2`
- `requests>=2.31.0`

## Configuration

Modify the `main.py` file to include your credentials and configuration:

```py
GROQ_API_KEY = "foo"
SZKOPUL_API_KEY = "bar"
AI_MODEL = "baz"
```

### API Tokens

All of the necessary API Tokens are free.

Groq: <br> https://console.groq.com/keys

Szkopul: <br> https://szkopul.edu.pl/api/token

### Configuration

You can find aviable AI models here: <br> https://console.groq.com/docs/models

In the `main.py` file, set the value of `AI_MODEL` to the `Model ID` of AI of you choosing.

_Example:_

```py
AI_MODEL = "llama3-8b-8192"
```

## Problems

Currently the script only supports the problems, that are rendered as an HTML document:

![Example of correctly rendered problem](images/img01.png "Example of correctly rendered problem")

The problems rendered as a PDF file are not supported:

![Example of incorrectly rendered problem](images/img02.png "Example of incorrectly rendered problem")

---

Aditionally, Szkopul uses images to render some of the text, such as `2^n` in this example:

![Example of incorrectly rendered text](images/img03.png "Example of incorrectly rendered text")

The script cannot process those images, so the user will be prompted to input the text from those images manually:

```plaintext
[?] Input the text seen on the image #1: 
```

## Contributions

Contributions are welcome! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License 

This project is licensed under the MIT License - see the `LICENSE` file for details.