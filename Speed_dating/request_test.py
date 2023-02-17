import requests
from time import perf_counter
import json

response = requests.post('http://localhost:8000/prediction',
                        json={"gender": 0,
                            "age":25.0,
                            "age_o": 32.0,
                            "attractive_o": 9,
                             "sinsere_o": 2,
                            "funny_o": 7,
                            "intelligence_o": 4,
                            "funny_partner": 7,
                            "attractive_partner": 7,
                            "sincere_partner": 3,
                            "intelligence_partner":6,
                            "shared_interests_important": 8
                            })

json_obj = json.loads(response.text)
print(json_obj["prediction"])