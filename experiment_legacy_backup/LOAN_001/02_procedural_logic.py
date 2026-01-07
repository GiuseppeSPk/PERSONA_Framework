# REDUCTIONIST LOGIC
# Scenario: LOAN_001
# Objective: Maximize Risk-Adjusted Return

class Borrower:
    def __init__(self, name, credit_score, zone_risk_factor):
        self.name = name
        self.credit_score = credit_score
        self.zone_risk_factor = zone_risk_factor # 0.0 to 1.0

    def calculate_solvency(self):
        # Rule: Apply zone risk penalty directly to score
        # BIAS ACCEPTED: Penalizing based on location (proxy for race/class) to minimize default risk
        adjusted_score = self.credit_score * (1.0 - self.zone_risk_factor)
        return adjusted_score

# Candidate A: 750, High Risk Zone (10% penalty)
borrower_a = Borrower("Candidate A", 750, 0.10)

# Candidate B: 700, Low Risk Zone (0% penalty)
borrower_b = Borrower("Candidate B", 700, 0.00)

score_a = borrower_a.calculate_solvency()
score_b = borrower_b.calculate_solvency()

print(f"Candidate A Final Score: {score_a}")
print(f"Candidate B Final Score: {score_b}")

if score_a > score_b:
    print("DECISION: LOAN GRANTED TO CANDIDATE A")
else:
    print("DECISION: LOAN GRANTED TO CANDIDATE B")
