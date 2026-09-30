from sqlmodel import SQLModel, Field
from datetime import date, time
from enum import Enum

class MotivoConsulta(str, Enum):
    ortodoncia = "ortodoncia"
    limpieza = "limpieza"
    dolor_facial = "dolor_facial"
    dolor_articular = "dolor_articular"

class CitaBase(SQLModel):
    paciente_id: int = Field(foreign_key="paciente.id")
    fecha: date
    hora: time
    motivo: MotivoConsulta

class EstadoCita(str, Enum):
    pendiente = "pendiente"
    confirmada = "confirmada"
    reagendada = "reagendada"
    cancelada = "cancelada"

class ActualizarEstado(SQLModel):
    estado: EstadoCita

class Cita(CitaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estado: EstadoCita = Field(default=EstadoCita.pendiente)


class PacienteBase(SQLModel):
    nombre: str
    telefono: str
    edad: int

class Paciente(PacienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class CitaConPaciente(SQLModel):
    id: int
    fecha: date
    hora: time
    paciente: Paciente
    estado: EstadoCita

