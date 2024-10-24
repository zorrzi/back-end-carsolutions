import requests

def get_car_info(brand, model, year):
    # Chave da API fornecida
    api_key = "3wfOr7JH9UghRIIU0lPSqA==Us3CpPJPkLZ0f2Pn"
    
    # Construção da URL da API
    api_url = f"https://api.api-ninjas.com/v1/cars?make={brand}&model={model}&year={year}"

    # Cabeçalho com a chave da API
    headers = {
        'X-Api-Key': api_key
    }

    # Fazendo a requisição GET
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Levanta exceções para erros de status HTTP

        data = response.json()
        if data:
            ficha_tecnica = data[0]  # Pegando o primeiro resultado
            # removendo modelo
            ficha_tecnica.pop('model', None)
            # transformando mpg em km/l
            ficha_tecnica['city_mpg'] = round(ficha_tecnica['city_mpg'] * 0.425144, 2)
            ficha_tecnica['highway_mpg'] = round(ficha_tecnica['highway_mpg'] * 0.425144, 2)
            ficha_tecnica['combination_mpg'] = round(ficha_tecnica['combination_mpg'] * 0.425144, 2)
            ficha_tecnica['drive'] = ficha_tecnica['drive'] =  'Dianteira' if ficha_tecnica['drive'] == 'fwd' else 'Traseira' if ficha_tecnica['drive'] == 'rwd' else 'Integral'
            ficha_tecnica['transmission'] = ficha_tecnica['transmission'] = 'Automática' if ficha_tecnica['transmission'] == 'a' else 'Manual'
            ficha_tecnica['fuel_type'] = ficha_tecnica['fuel_type'] = 'Gasolina' if ficha_tecnica['fuel_type'] == 'gas' else 'Diesel' if ficha_tecnica['fuel_type'] == 'diesel' else 'Híbrido' if ficha_tecnica['fuel_type'] == 'hybrid' else 'Elétrico'
            ficha_tecnica['class'] = ficha_tecnica['class'] = 'Sedan' if ficha_tecnica['class'] == 'midsize car' else 'SUV' if ficha_tecnica['class'] == 'suv' else 'Hatchback' if ficha_tecnica['class'] == 'hatchback' else 'Picape' if ficha_tecnica['class'] == 'pickup' else 'Caminhonete' if ficha_tecnica['class'] == 'truck' else 'Van' if ficha_tecnica['class'] == 'van' else 'Esportivo' if ficha_tecnica['class'] == 'sports car' else 'Cupê' if ficha_tecnica['class'] == 'coupe' else 'Conversível' if ficha_tecnica['class'] == 'convertible' else 'Minivan' if ficha_tecnica['class'] == 'minivan' else 'Wagon' if ficha_tecnica['class'] == 'wagon' else 'Crossover' if ficha_tecnica['class'] == 'crossover' else 'Utilitário'
            return ficha_tecnica
        else:
            print("Nenhuma ficha técnica disponível.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar ficha técnica: {e}")