# import pomegranate
from pgmpy.sampling import BayesianModelSampling

from collections import Counter
from model import model

# REJECTION SAMPLING EXAMPLE #

# Create a sampler object of our Bayesian model
sampler = BayesianModelSampling(model)

# Function to generate a sample
def generate_samples(num):
   # Generate samples of size num
   samples = sampler.forward_sample(size=num)
   # print(samples)
   return samples

N = 10000
samples = generate_samples(N)

# Access sample's data
samples_dict = samples.to_dict('records')

# Rejection sampling
# Compute distribution of Appointment given that train is delayeddata = []
data = []
for sample in samples_dict:
   if sample['train'] == "delayed":
       data.append(sample['appointment'])


# Count data and display resuly
print(Counter(data))


# def generate_sample():

#     # Mapping of random variable name to sample generated
#     sample = {}

#     # Mapping of distribution to sample generated
#     parents = {}

#     # Loop over all states, assuming topological order
#     for state in model.states:

#         # If we have a non-root node, sample conditional on parents
#         if isinstance(state.distribution, pomegranate.ConditionalProbabilityTable):
#             sample[state.name] = state.distribution.sample(parent_values=parents)

#         # Otherwise, just sample from the distribution alone
#         else:
#             sample[state.name] = state.distribution.sample()

#         # Keep track of the sampled value in the parents mapping
#         parents[state.distribution] = sample[state.name]

#     # Return generated sample
#     return sample

# # Rejection sampling
# # Compute distribution of Appointment given that train is delayed
# N = 10000
# data = []
# for i in range(N):
#     sample = generate_sample()
#     if sample["train"] == "delayed":
#         data.append(sample["appointment"])
# print(Counter(data))

