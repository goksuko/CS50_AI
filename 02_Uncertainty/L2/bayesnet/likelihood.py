from model import model

# Calculate probability for a given observation
# probability = model.probability([["none", "no", "on time", "attend"]]) # this was the code for pomegrante

probability = model.get_state_probability({"rain": "none", "maintenance": "no", "train": "on time", "appointment": "attend"}) # this is the code for pgmpy

print(probability)
