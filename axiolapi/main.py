from fastapi import FastAPI
from rank import RankBar, PieChart

app = FastAPI()


@app.get('/')
def index():
    return {
        "Welcome": "👋",
        "Rank BarGraph": "/bargraph/rank/{serverid}",
        "Rank PieChart": "/piechart/rank/{serverid}"
        }

    
#Returns top 10 users by default, using limit more users can be fetched
@app.get('/bargraph/rank/{serverid}')
def index(serverid: int, limit:int=10):
    if limit > 30:
        return {"message": "You cannot get a bar graph of more than 30 users"}
    else:
        Data = RankBar(serverid, limit)
        
        return {"message": Data}


@app.get('/piechart/rank/{serverid}')
def index(serverid: int, limit:int=10):
    if limit > 30:
        return {"message": "You cannot get a bar graph of more than 30 users"}
    else:
        Data = PieChart(serverid, limit)
        
        return {"message": Data}
