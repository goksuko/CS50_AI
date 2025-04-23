# decided to change the library from pomegranate to pgmpy

# pgmpy is a Python package for causal inference and probabilistic inference 
# using Directed Acyclic Graphs (DAGs) and 
# Bayesian Networks with a focus on modularity and extensibility. 

# original code below the page

from pgmpy.models import DiscreteBayesianNetwork # for defining the model
from pgmpy.factors.discrete.CPD import TabularCPD # for CPDs
from pgmpy.inference import VariableElimination  # for inference

# Bayesian Network pgmpy Documentation:
# https://pgmpy.org/models/bayesiannetwork.html


# 1. Define the Bayesian Network structure
model = DiscreteBayesianNetwork([ # the model is a Bayesian Network
   ('rain', 'maintenance'), # the model has an edge from 'rain' to 'maintenance'
   ('rain', 'train'),      # the model has an edge from 'rain' to 'train'
   ('maintenance', 'train'), # the model has an edge from 'maintenance' to 'train'
   ('train', 'appointment') # the model has an edge from 'train' to 'appointment'
])

# 2. Define the CPDs (Conditional Probability Distributions)

# CPD for Rain (CPD means Conditional Probability Distribution) - although rain in this case is a discrete variable (unconditional)
cpd_rain = TabularCPD(variable='rain', variable_card=3,
                     values=[[0.7], [0.2], [0.1]],
                     state_names={'rain': ['none', 'light', 'heavy']})


# CPD for Maintenance given Rain (this is a conditional probability distribution - depends on the value of 'rain')
cpd_maintenance = TabularCPD(variable='maintenance', variable_card=2,
                            values=[[0.4, 0.2, 0.1], # P(maintenance='yes' | rain='none', light, heavy)
                                    [0.6, 0.8, 0.9]], # P(maintenance='no' | rain='none', light, heavy)
                            evidence=['rain'], # the evidence is the value of 'rain'
                            evidence_card=[3], # the evidence is a discrete variable with 3 possible values
                            state_names={'maintenance': ['yes', 'no'], # the state names for 'maintenance'
                                         'rain': ['none', 'light', 'heavy']}) # the state names for 'rain'

# CPD for Train given Rain and Maintenance
cpd_train = TabularCPD(variable='train', variable_card=2,
                      values=[[0.8, 0.9, 0.6, 0.7, 0.4, 0.5], # P(train='on time' | rain='none', light, heavy, maintenance='yes', 'no')
                              [0.2, 0.1, 0.4, 0.3, 0.6, 0.5]], # P(train='delayed' | rain='none', light, heavy, maintenance='yes', 'no')
                      evidence=['rain', 'maintenance'],
                      evidence_card=[3, 2], # the evidence is a discrete variable with 3 possible values for 'rain' and 2 possible values for 'maintenance'
                      state_names={'train': ['on time', 'delayed'],
                                   'rain': ['none', 'light', 'heavy'],
                                   'maintenance': ['yes', 'no']})

# CPD for Appointment given Train
cpd_appointment = TabularCPD(variable='appointment', variable_card=2,
                            values=[[0.9, 0.6], # P(appointment='attend' | train='on time', 'delayed')
                                    [0.1, 0.4]], # P(appointment='miss' | train='on time', 'delayed')
                            evidence=['train'],
                            evidence_card=[2], # the evidence is a discrete variable with 2 possible values for 'train'
                            state_names={'appointment': ['attend', 'miss'], # the state names for 'appointment' (state is a discrete variable and it means the value of the variable)
                                         'train': ['on time', 'delayed']}) # the state names for 'train'

# Add CPDs to the model (Create a Bayesian Network and add states)
model.add_cpds(cpd_rain, cpd_maintenance, cpd_train, cpd_appointment) # the model has 4 CPDs

# 3. Verify the model (check if the model is valid)
if __name__ == "__main__":
    # Check if the model is valid
    assert model.check_model()

    nodes = model.nodes()
    edges = model.edges()
    print("=========")
    print("Nodes:", nodes)
    print("Edges:", edges)
    print()
    
    for node in nodes:
        print(model.get_cpds(node))
        print()

    print("Markov Blanket:")
    print("Rain: ", model.get_markov_blanket("rain")) # Check node's dependencies (parents)
    print("Maintenance: ", model.get_markov_blanket("maintenance")) # Check node's dependencies (parents)
    print("Train: ", model.get_markov_blanket("train")) # Check node's dependencies (parents)
    print("Appointment: ", model.get_markov_blanket("appointment")) # Check node's dependencies (parents)
    print("=========")



# from pomegranate import *
# from pomegranate.distributions import Categorical
# from pomegranate.distributions import ConditionalCategorical
# from pomegranate.bayesian_network import BayesianNetwork

# # Rain node has no parents
# rain = Node(DiscreteDistribution({
#     "none": 0.7,
#     "light": 0.2,
#     "heavy": 0.1
# }), name="rain")

# # Track maintenance node is conditional on rain
# maintenance = Node(ConditionalProbabilityTable([
#     ["none", "yes", 0.4],
#     ["none", "no", 0.6],
#     ["light", "yes", 0.2],
#     ["light", "no", 0.8],
#     ["heavy", "yes", 0.1],
#     ["heavy", "no", 0.9]
# ], [rain.distribution]), name="maintenance")

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

# # Appointment node is conditional on train
# appointment = Node(ConditionalProbabilityTable([
#     ["on time", "attend", 0.9],
#     ["on time", "miss", 0.1],
#     ["delayed", "attend", 0.6],
#     ["delayed", "miss", 0.4]
# ], [train.distribution]), name="appointment")

# Create a Bayesian Network and add states
# model = BayesianNetwork()
# model.add_states(rain, maintenance, train, appointment)

# Add edges connecting nodes
# model.add_edge(rain, maintenance)
# model.add_edge(rain, train)
# model.add_edge(maintenance, train)
# model.add_edge(train, appointment)

# Finalize model
# model.bake()
