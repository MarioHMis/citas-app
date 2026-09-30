from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from database import engine
from models import Cita, CitaBase, CitaConPaciente, Paciente

router = APIRouter(tags=["citas"])


@router.post("/citas", status_code=201)
def crear_cita(datos: CitaBase):
    cita = Cita.model_validate(datos)
    with Session(engine) as session:
        paciente = session.get(Paciente, datos.paciente_id)
        if paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado") 
        session.add(cita)
        session.commit()
        session.refresh(cita)
    return cita

@router.get("/citas", response_model=list[CitaConPaciente])
def listar_citas():
    with Session(engine) as session:
        resultados = session.exec(select(Cita, Paciente).join(Paciente)).all() 
        respuesta = []
        for cita, paciente in resultados:
            respuesta.append(CitaConPaciente(id=cita.id, fecha=cita.fecha, hora=cita.hora, paciente=paciente))
        return respuesta

@router.get("/citas/{cita_id}", response_model=CitaConPaciente)
def cita_por_id(cita_id: int):
    with Session(engine) as session:
        cita = session.get(Cita, cita_id)
        if cita is None:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        paciente = session.get(Paciente, cita.paciente_id)
        respuesta = CitaConPaciente(id=cita.id, fecha=cita.fecha, hora=cita.hora, paciente=paciente)
        return respuesta
    