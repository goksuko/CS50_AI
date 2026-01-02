import scipy.optimize

# LINEAR PROGRAMMING EXAMPLE

# Two machines X1 and X2. X1 costs $50/hour to run, X2 costs $80/hour to run. Goal is to minimize cost.
## Objective Function: 50x_1 + 80x_2

# X1 requires 5 units of labor per hour. X2 requires 2 units of labor per hour. Total of 20 units of labor to spend.
## Constraint 1: 5x_1 + 2x_2 <= 20

# X1 produces 10 units of output per hour. X2 produces 12 units of output per hour. Company needs 90 units of output.
## Constraint 2: -10x_1 + -12x_2 <= -90

# ub indicates upper bound constraints
result = scipy.optimize.linprog(
    [50, 80],  # Cost function: 50x_1 + 80x_2
    A_ub=[[5, 2], [-10, -12]],  # Coefficients for inequalities
    b_ub=[20, -90],  # Constraints for inequalities: 20 and -90
)

if result.success:
    print(f"X1: {round(result.x[0], 2)} hours")
    print(f"X2: {round(result.x[1], 2)} hours")
else:
    print("No solution")

