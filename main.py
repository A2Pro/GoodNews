from flask import Flask, render_template
import requests
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key="YOUR_API_KEY")

def ask_gpt(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Here " + prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content

@app.route('/')
def main():
    return render_template("index.html")

@app.route("/sportsnews")
def current_scores():
    response = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey=YOUR_API_KEY')
    data = response.json()

    titles = []
    urls = []
    counter = 0
    for article in data['articles']:
        title = article['title']
        response = str(ask_gpt("Here is a title. From the title, is this article going to make people feel good? Yes or no. There must be a yes if it does, and there should be no yes if it does not." + title))
        print(title)
        print(response)
        if "yes" in response or "Yes" in response:
            counter += 1
            titles.append(article['title'])
            urls.append(article['url'])
        if counter == 15:
            break

    return render_template("sportsnews.html", titles=titles, urls=urls)

@app.route("/nytimes")
def nytimes():
    response = requests.get("https://api.nytimes.com/svc/mostpopular/v2/emailed/7.json?api-key=YOUR_API_KEY")
    response.raise_for_status()
    data = response.json()

    titles = []
    urls = []
    counter = 0
    for article in data['results']:
        title = article['title']
        response = str(ask_gpt("Here is a title. From the title, is this article going to make people feel good? Yes or no. There must be a yes if it does, and there should be no yes if it does not." + title))
        print(response)
        print(title)
        if "yes" in response or "Yes" in response:
            counter += 1
            titles.append(article['title'])
            urls.append(article['url'])
        if counter == 15:
            break

    return render_template("sportsnews.html", titles=titles, urls=urls)

if __name__ == "__main__":
    app.run(port=3945, host="0.0.0.0")
