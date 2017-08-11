from flask import Flask, request, jsonify
import json
import io
import apply_bpe

app = Flask(__name__)
config = None
models = []

@app.route('/pre', methods=['GET', 'POST'])
def preprocess():
  body = request.get_json(silent=True, force=True)
  model = None
  for m in models:
    if m['name'] == body['model']:
      model = m
  if model == None:
    return jsonify({"err": "no such model"})
  res = m['bpe'].segment(body['seg']).strip()
  return jsonify({"res": res})

def load_models(config):
  res = []
  for c in config:
    model = {}
    codes = io.open(c['codes_file'], encoding='utf-8')
    model['bpe'] = apply_bpe.BPE(codes, c['separator'], None, None)
    model['name'] = c['name']
    res.append(model)
  return res

if __name__ == '__main__':
  with open('bpe_srv.config', mode='r', encoding='utf-8') as f:
    config = json.load(f)
  models = load_models(config)
  app.run(host="0.0.0.0", port=int("9000"))

