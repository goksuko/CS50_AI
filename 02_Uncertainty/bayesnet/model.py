from pomegranate import *
from pomegranate.distributions import Categorical
from pomegranate.distributions import ConditionalCategorical
from pomegranate.bayesian_network import BayesianNetwork

# # Rain node has no parents
# rain = Node(DiscreteDistribution({
#     "none": 0.7,
#     "light": 0.2,
#     "heavy": 0.1
# }), name="rain")

rain = Categorical([[0.7, 0.2, 0.1]])

# # Track maintenance node is conditional on rain
# maintenance = Node(ConditionalProbabilityTable([
#     ["none", "yes", 0.4],
#     ["none", "no", 0.6],
#     ["light", "yes", 0.2],
#     ["light", "no", 0.8],
#     ["heavy", "yes", 0.1],
#     ["heavy", "no", 0.9]
# ], [rain.distribution]), name="maintenance")

maintenance = ConditionalCategorical([
    [0.4,0.6], [0.2,0.8], [0.1,0.9]
    ])

# # Train node is conditional on rain and maintenance
# train = Node(ConditionalProbabilityTable([
#     ["none", "yes", "on time", 0.8],
#     ["none", "yes", "delayed", 0.2],
#     ["none", "no", "on time", 0.9],
#     ["none", "no", "delayed", 0.1],
#     ["light", "yes", "on time", 0.6],
#     ["light", "yes", "delayed", 0.4],
#     ["light", "no", "on time", 0.7],
#     ["light", "no", "delayed", 0.3],
#     ["heavy", "yes", "on time", 0.4],
#     ["heavy", "yes", "delayed", 0.6],
#     ["heavy", "no", "on time", 0.5],
#     ["heavy", "no", "delayed", 0.5],
# ], [rain.distribution, maintenance.distribution]), name="train")

train = ConditionalCategorical([
    [[0.8, 0.2], [0.9, 0.1]], [[0.6, 0.4], [0.7, 0.3]], [[0.4, 0.6], [0.5, 0.5]]
])

# # Appointment node is conditional on train
# appointment = Node(ConditionalProbabilityTable([
#     ["on time", "attend", 0.9],
#     ["on time", "miss", 0.1],
#     ["delayed", "attend", 0.6],
#     ["delayed", "miss", 0.4]
# ], [train.distribution]), name="appointment")

appointment = ConditionalCategorical([
    [0.9, 0.1], [0.6, 0.4]
])

# Create a Bayesian Network and add states
model = BayesianNetwork()
# model.add_states(rain, maintenance, train, appointment)
model.add_distributions([rain, maintenance, train, appointment])

# Add edges connecting nodes
model.add_edge(rain, maintenance)
model.add_edge(rain, train)
model.add_edge(maintenance, train)
model.add_edge(train, appointment)

# Finalize model
model.bake()
