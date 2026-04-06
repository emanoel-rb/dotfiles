#!/usr/bin/env python3

# ==========================================================
# Weather.py - Weather.com Scraper
# ----------------------------------------------------------
# - Obtém temperatura atual, mínima e máxima de uma localização
# - Saída em JSON para integração com status bars ou scripts
# - Dependência: pyquery (pip install pyquery)
# - Mantém compatibilidade com Celsius e Fahrenheit
# ==========================================================

import json
from pyquery import PyQuery  # Biblioteca para parsing de HTML

################################### CONFIGURAÇÃO ###################################

### ID da localização no weather.com (geralmente baseado em latitude/longitude)
location_id = "294e1ac420e35622f2a093ac2951485fa4c28cd2fe5b8a01da513a1b2bb809ca"

### Unidade de temperatura: 'metric' = Celsius, 'imperial' = Fahrenheit
unit = "metric"

### Tipo de previsão (apenas referência, não usado no script)
forecast_type = "Hourly"  # 'Hourly' ou 'Daily'

########################################## MAIN ##################################

### Define idioma do site baseado na unidade de temperatura
_lang = "en-IN" if unit == "metric" else "en-US"

### Monta URL do weather.com para a localização e idioma definidos
url = f"https://weather.com/{_lang}/weather/today/l/{location_id}"

### Faz o parse do HTML da página
html_data = PyQuery(url=url)

### Pega a temperatura atual (primeiro span com data-testid='TemperatureValue')
temp = html_data("span[data-testid='TemperatureValue']").eq(0).text()

### Pega a temperatura mínima (segundo span dentro de div[data-testid='wxData'])
temp_min = (
    html_data("div[data-testid='wxData'] > span[data-testid='TemperatureValue']")
    .eq(1)
    .text()
)

### Pega a temperatura máxima (primeiro span dentro de div[data-testid='wxData'])
temp_max = (
    html_data("div[data-testid='wxData'] > span[data-testid='TemperatureValue']")
    .eq(0)
    .text()
)

### Monta JSON de saída
out_data = {
    "text": f"  {temp}C",  # Temperatura atual
    "tooltip": f"Min: {temp_min}C\nMax: {temp_max}C",  # Tooltip com min/max
}

### Imprime JSON no terminal
print(json.dumps(out_data))