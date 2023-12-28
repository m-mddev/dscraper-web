from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests as r
from bs4 import BeautifulSoup
import uvicorn

URL = "https://dictionary.cambridge.org/dictionary/english/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

app = FastAPI()
app.mount('/static', StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.get("/word")
def get_data(request: Request):
    word = request.query_params.get("word")
    result = fetch_data(word)
    return {"result": result}

def fetch_data(word: str):
    try:
        response = r.get(URL +  word, headers=HEADERS)
    except:
        return
    #check if the operation successfuly completed.
    if response.status_code == 200:
        #create a html file
        soup = BeautifulSoup (response.content, 'html.parser')
        container = soup.find_all('div', class_= "di-body")
        parents = soup.find_all('span', class_= "dpron-i")
        try:
            soup6 = BeautifulSoup (str(parents[1]), 'html.parser')
        except:
            return
        pro = soup6.find_all('span', class_='dpron')
        soup7 = BeautifulSoup(str(pro[0]), 'html.parser')
        span_tags = soup7.find_all('span')
        for span_tag in span_tags:
            span_tag.replace_with(span_tag.text)
        soup2 = BeautifulSoup(str(container[0]), 'html.parser') #find dives that have class "db"
        divs = soup2.find_all('div', class_="db")
        #creating a blank array for extracted data.
        cleared_content = []
        for a in divs:
            soup1 = ''
            #remove <a> tags
            soup1 = BeautifulSoup(str(a), 'html.parser')
            a_tags = soup1.find_all('a')
            for a_tag in a_tags:
                a_tag.replace_with (a_tag.text)
                #remove <div> tags
            div_tags = soup1.find_all('div')
            for div_tag in div_tags:
                div_tag.replace_with (div_tag.text)
            cleared_content.append(soup1)
        #create modified files
        res = "## " + word + "{}\n".format(str(soup7))
        for b in cleared_content:
            res = res + "* " + str(b).replace(":", ".") + "\n"
        res = res + "---\n"
        return res
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)