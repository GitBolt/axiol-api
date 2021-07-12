import torch
import random
from fastapi import FastAPI
from pydantic import BaseModel

from chatbot.model import NeuralNet
from chatbot.utils import bag_of_words, tokenize_and_lemmatize, solve
from visuals.bargraph import BarGraph
from visuals.piechart import PieChart
from database import DB1


app = FastAPI()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

collection1 = DB1.get_collection("Col1")
alldata = list(collection1.find())


class Content(BaseModel):
    content: str

@app.get('/')
def index():
    return {
        "Rank BarGraph": "/bargraph/{serverid}",
        "Rank PieChart": "/piechart/{serverid}"
        }

    
#Returns top 10 users by default, using limit more users can be fetched
@app.get('/bargraph/{serverid}')
def index(serverid: int, limit:int=10):
    if limit > 30:
        return {"message": "You cannot get a bar graph of more than 30 users"}
    else:
        Data = BarGraph(serverid, limit)
        
        return {"message": Data}


@app.get('/piechart/{serverid}')
def index(serverid: int):
    Data = PieChart(serverid)
        
    return {"message": Data}


@app.post("/ai/chatbot")
async def chatbot(content: Content):
    FILE = "chatbot/data.pth"
    data = torch.load(FILE, map_location='cpu')

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    sentence = tokenize_and_lemmatize(content.dict()["content"])
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    print(all_words)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    print(prob.item())
    print(tag)
    if prob.item() > 0.85:
        for data in alldata:
            if tag == data["tag"]:
                if tag == "maths":
                    return {"response": solve(sentence), "tag": tag}
                else:
                    response = random.choice(data["responses"])
                    return {"response": response, "tag": tag}

    else:
        return {
            "response": random.choice([
                    "What?",
                    "Sorry what?",
                    "?",
                    "Didn't understand",
                    "Huh",
                    ":face_with_raised_eyebrow:",
                    "what",
                    "Can you say that differently?",
                    "Hmm?"
                    ]), 
                    "tag": "unknown"
                    
                    }