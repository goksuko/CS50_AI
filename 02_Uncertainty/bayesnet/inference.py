from pgmpy.inference import VariableElimination
from model import model

# Create an inference object
inference = VariableElimination(model)

# Define the evidence
evidence = {'train': 'delayed'}
# evidence = {'train': 'delayed', 'rain': 'heavy'}

print()
print("Knowing the evidence: ", evidence, " the probability of the following is: \n")

# Calculate predictions for each node given the evidence
predictions = {}
for node in model.nodes():
	if node in evidence:
		print(f"Node '{node}' is known to be '{evidence[node]}'.")
		print()
		continue

   	# Query the probability distribution for each node given the evidence
	prediction = inference.query(variables=[node], evidence=evidence)
	print(f"PREDICTION for {node}\n {prediction}")
	print()










# from model import model

# # Calculate predictions
# predictions = model.predict_proba({
#     # "rain":"heavy", 
#     "train": "delayed"

# })

# # Print predictions for each node
# for node, prediction in zip(model.states, predictions):
#     if isinstance(prediction, str):
#         print(f"{node.name}: {prediction}")
#     else:
#         print(f"{node.name}")
#         for value, probability in prediction.parameters[0].items():
#             print(f"    {value}: {probability:.4f}")
