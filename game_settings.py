import json

with open('game_variables.json') as f:
    g_vars = json.load(f)

with open('production_vars.json') as p:
    g_prod = json.load(p)
