from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import date, time 
app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "El consultorio esta en linea"}


class CitaBase(SQLModel):
    paciente: str
    fecha: date
    hora: time

class Cita(CitaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

engine = create_engine("sqlite:///citas.db")

SQLModel.metadata.create_all(engine)

@app.post("/citas", status_code=201)
def crear_cita(datos: CitaBase):
    cita = Cita.model_validate(datos)
    with Session(engine) as session:
        session.add(cita)
        session.commit()
        session.refresh(cita)
    return cita

@app.get("/citas")
def listar_citas():
    with Session(engine) as session:
        return session.exec(select(Cita)).all()

@app.get("/citas/{cita_id}")
def cita_por_id(cita_id: int):
    with Session(engine) as session:
        cita = session.get(Cita, cita_id)
        if cita is None:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return cita

    


