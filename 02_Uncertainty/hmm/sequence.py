import numpy as np
from model import create_hmm

# Observed data
observations = [
    "umbrella",
    "umbrella",
    "no umbrella",
    "umbrella",
    "umbrella",
    "umbrella",
    "umbrella",
    "no umbrella",
    "no umbrella"
]

# Create the model
model = create_hmm()

# Map observations to numerical indices
observation_map = {"umbrella": 0, "no umbrella": 1}
observed_sequence = np.array([observation_map[obs] for obs in observations]).reshape(-1, 1)

# Perform inference (Viterbi algorithm)
logprob, state_sequence = model.decode(observed_sequence)

state_names = ["sun", "rain"]
   
print()
print("Observation -> State:")
for obs, prediction in zip(observations, state_sequence):
    print(f"{obs} -> {state_names[prediction]}")
print()



# from model import model

# # Observed data
# observations = [
#     "umbrella",
#     "umbrella",
#     "no umbrella",
#     "umbrella",
#     "umbrella",
#     "umbrella",
#     "umbrella",
#     "no umbrella",
#     "no umbrella"
# ]

# # Predict underlying states
# predictions = model.predict(observations)
# for prediction in predictions:
#     print(model.states[prediction].name)
