import requests
import json

res = requests.post('http://localhost:9000/pre', json={"model":"osub-en-small-50k", "seg": "He's ű ö not here."})
seg = json.loads(res.text)
print(seg)
