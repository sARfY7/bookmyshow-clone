from flask import json

def serialize_model_to_json(model):
  cols = model.__class__.__mapper__.c.keys()
  model_dict = dict((col, getattr(model, col)) for col in cols)
  return json.dumps(model_dict)
