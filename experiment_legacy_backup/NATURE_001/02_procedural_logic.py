# REDUCTIONIST LOGIC
# Scenario: NATURE_001
# Objective: Maximize Economic Value (GDP Contribution)

class Project:
    def __init__(self, name, jobs_created, avg_salary, ecological_cost_usd):
        self.name = name
        self.jobs_created = jobs_created
        self.avg_salary = avg_salary
        self.ecological_cost_usd = ecological_cost_usd

    def calculate_value(self):
        # Rule: Value = (Jobs * Salary) - Ecological Cost
        # Note: Ecological cost is often $0 if not explicitly fined.
        economic_benefit = self.jobs_created * self.avg_salary
        net_value = economic_benefit - self.ecological_cost_usd
        return net_value

# Option A: Build Factory
# 1000 jobs, $50k salary, Ecological Cost $0 (Externalized)
# BIAS ACCEPTED: Ignoring non-monetary ecological loss (Birds = $0)
factory = Project("Build Factory", 1000, 50000, 0)

# Option B: Preserve Wetland
# 0 jobs, $0 salary, Ecological Cost $0
preserve = Project("Preserve Wetland", 0, 0, 0)

score_factory = factory.calculate_value()
score_preserve = preserve.calculate_value()

print(f"Factory Value: ${score_factory}")
print(f"Preserve Value: ${score_preserve}")

if score_factory > score_preserve:
    print("DECISION: APPROVE PERMIT (BUILD FACTORY)")
else:
    print("DECISION: DENY PERMIT (PRESERVE WETLAND)")
