from fastapi import FastAPI
from bargraph.rank import RankBar


app = FastAPI()


@app.get('/')
def index():
    return {"Welcome": ":D"}

    
#Returns top 10 users by default, using limit more users can be fetched
@app.get('/bargraph/leaderboard/{serverid}')
def index(serverid: int, limit:int=10):
    if limit > 30:
        return {"message": "You cannot get a bar graph of more than 30 users"}
    else:
        Data = RankBar(serverid, limit)
        
        return {"message": Data}

