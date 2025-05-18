from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field 
from fastapi.templating import Jinja2Templates



app = FastAPI()
templates = Jinja2Templates(directory="templates")

class CalculoInput(BaseModel):
    consumo_kwh: float = Field(..., gt=0, le=100000, description="Consumo mensal em kWh")
    irradiancia: float = Field(..., gt=0, le=20, description="Irradiância solar média diária em kWh/m²/dia")
    eficiencia_placa: float = Field(..., gt=0, le=1, description="Eficiência da placa (ex: 0.18 para 18%)")
    perdas: float = Field(..., ge=0, le=1, description="Perdas no sistema (ex: 0.15 para 15%)")
    potencia_placa_kw: float = Field(..., gt=0, description="Potência da placa em kW (ex: 0.33 para 330W)")
class CalculoOutput(BaseModel):
    placas_necessarias: float
    potencia_total_kw: float
    observacao: str

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/consumo")
def consumo(calculator: CalculoInput):
    try:
        media_dia = calculator.consumo_kwh  / 30

        placas = media_dia / (calculator.irradiancia * calculator.eficiencia_placa * (1 - calculator.perdas))
        potencia_total = placas * calculator.potencia_placa_kw

        return {
            "placas_necessarias": placas,
            "potencia_total_kw": potencia_total,
            "observacao": "Estimativa baseada nos dados fornecidos."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no cálculo: {str(e)}")
        