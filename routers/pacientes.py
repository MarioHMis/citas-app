from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from database import engine
from models import Paciente, PacienteBase

router = APIRouter(tags=["pacientes"])

@router.post("/pacientes", status_code=201)
def crear_paciente(datos: PacienteBase):
    paciente = Paciente.model_validate(datos)
    with Session(engine) as session:
        session.add(paciente)
        session.commit()
        session.refresh(paciente)
        return paciente

@router.get("/pacientes")
def listar_pacientes():
    with Session(engine) as session:
        return session.exec(select(Paciente)).all()

@router.get("/pacientes/{paciente_id}")
def paciente_por_id(paciente_id: int):
    with Session(engine) as session:
        paciente = session.get(Paciente, paciente_id)
        if paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return paciente