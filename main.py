from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class CalculoRequest(BaseModel):
    consumo_mensal_kwh: float = Field(..., gt=0)
    irradiacao_media_diaria: float = Field(..., gt=0)
    potencia_placa_w: float = Field(default=340, gt=0)
    eficiencia_sistema: float = Field(default=0.8, gt=0, le=1)

class CalculoResponse(BaseModel):
    placas_necessarias: int
    potencia_sistema_kw: float

@app.post("/calculo-placas", response_model=CalculoResponse)  # <-- aqui corrigido
def calcula_placas(data: CalculoRequest):
    energia_diaria_necessaria = data.consumo_mensal_kwh / 30
    energia_necessaria_com_eficiencia = energia_diaria_necessaria / data.eficiencia_sistema
    placas = energia_necessaria_com_eficiencia / (data.irradiacao_media_diaria * (data.potencia_placa_w / 1000))
    placas_necessarias = int(placas) + (1 if placas % 1 > 0 else 0)

    potencia_sistema_kw = placas_necessarias * (data.potencia_placa_w / 1000)

    return CalculoResponse(
        placas_necessarias=placas_necessarias,
        potencia_sistema_kw=round(potencia_sistema_kw, 2)
    )
