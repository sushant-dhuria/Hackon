from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils import get_user_chat_history
from llm.get_movies import get_response
from queries.query import fetch_results,get_movie_by_id,recommend_movie_by_id, get_playlist_by_id, get_by_plot
app = FastAPI()
origins = ["*"]  # Adjust this to specify the origins you want to allow (e.g., ["http://localhost:3000"])

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check-product")
async def check_product(request: Request):
    data = await request.json()
    chat_history = data['chatHistory']
    user_chat_history = get_user_chat_history(chat_history)
    resp = get_response(user_chat_history)
    results = fetch_results(resp)
    return {"answer": resp['answer'],'results':results}

@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int):
    return get_movie_by_id(movie_id)

@app.get("/recommendations/{movie_id}")
async def get_recommendation(movie_id: int):
    return recommend_movie_by_id(movie_id)

@app.get("/playlist/{movie_id}")
async def get_playlist(movie_id: int):
    return get_playlist_by_id(movie_id)

@app.post("/check-plot")
async def check_plot(request: Request):
    data = await request.json()
    query = data['searchQuery']
    # print(get_by_plot(query)) 
    return {'results':get_by_plot(query)}

@app.post("/search")
async def check_plot(request: Request):
    data = await request.json()
    print(data)
    # print(get_by_plot(query)) 
    return {'timestamp':0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
