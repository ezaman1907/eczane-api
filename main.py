from fastapi import FastAPI
from scraper import eczane_kazı

app = FastAPI()

@app.get("/")
def home():
    return {"mesaj": "Eczane API Hazır!"}

@app.get("/nobetci")
def verileri_ver():
    return {"data": eczane_kazı()}
