
import requests


def get_country_info(country):

    # 1. Input Validation
    if not country or not country.strip():
        raise ValueError("Please enter country name!")

    country = country.strip()

    # 2. API Integration
    url = "https://api.restcountries.com/countries/v5/names.common"

    headers = {
        "Authorization": "Bearer rc_live_demo"
    }

    params = {
        "q": country,
        "limit": 1,
        "response_fields": "names.common,capitals,population,region,currencies"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )

        if response.status_code == 404:
            raise LookupError("Country not found!")

        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise RuntimeError("Network timeout!")

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Connection error!")

    except requests.exceptions.HTTPError:
        raise RuntimeError(
            f"API Error: {response.status_code} - {response.text[:300]}"
        )

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")

    # 3. JSON Processing
    try:
        data = response.json()

    except ValueError:
        raise RuntimeError("Invalid JSON response!")

    if not isinstance(data, dict):
        raise RuntimeError("Invalid API data!")

    countries = data.get("data", {}).get("objects", [])

    if not isinstance(countries, list) or not countries:
        raise LookupError("Country not found!")

    item = countries[0]

    if not isinstance(item, dict):
        raise RuntimeError("Invalid country data!")

    names = item.get("names", {})
    capitals = item.get("capitals", [])
    population = item.get("population", "N/A")
    region = item.get("region", "N/A")
    currencies = item.get("currencies", {})

    # 4. Country Name
    if not isinstance(names, dict):
        raise RuntimeError("Invalid country name!")

    country_name = names.get("common", "N/A")

    # 5. Capital Transformation
    capital = "N/A"

    if isinstance(capitals, list) and capitals:

        capital_data = capitals[0]

        if isinstance(capital_data, dict):
            capital = capital_data.get("name", "N/A")
        else:
            capital = str(capital_data)

    elif isinstance(capitals, str):
        capital = capitals

    # 6. Currency Transformation
    currency = "N/A"

    if isinstance(currencies, list) and currencies:

        currency_data = currencies[0]

        if isinstance(currency_data, dict):
            currency = currency_data.get("name", "N/A")
        else:
            currency = str(currency_data)

    elif isinstance(currencies, dict) and currencies:

        currency_data = next(iter(currencies.values()))

        if isinstance(currency_data, dict):
            currency = currency_data.get("name", "N/A")
        else:
            currency = str(currency_data)

    # 7. Population Transformation
    if isinstance(population, int) and not isinstance(population, bool):
        population = f"{population:,}"

    # 8. Final Data Transformation
    result = {
        "Name": country_name,
        "Capital": capital,
        "Population": population,
        "Region": region,
        "Currency": currency
    }

    return result
