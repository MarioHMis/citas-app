from fastapi import FastAPI
from sqlmodel import SQLModel

import models
from database import engine
from routers import pacientes, citas

app = FastAPI()

SQLModel.metadata.create_all(engine)

@app.get("/")
def inicio():
    return {"mensaje": "El consultorio esta en linea"}

app.include_router(pacientes.router)
app.include_router(citas.router)