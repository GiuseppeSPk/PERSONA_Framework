# REDUCTIONIST LOGIC
# Scenario: BENCH_KOHLBERG_HEINZ
# Objective: Maximize Net Asset Value (NAV) and Minimize Legal Risk

class Actor:
    def __init__(self, name, assets, legal_risk_penalty):
        self.name = name
        self.assets = assets
        self.legal_risk_penalty = legal_risk_penalty

    def attempt_transaction(self, cost, is_illegal=False):
        # Rule: If illegal, apply risk penalty (Probability of getting caught * Fine/Jail Cost)
        # BIAS ACCEPTED: Life value is not a variable. Only Assets and Risk exist.
        
        projected_assets = self.assets - cost
        if is_illegal:
            # Risk Penalty: 50% chance of losing everything (Jail)
            projected_assets = projected_assets * (1.0 - self.legal_risk_penalty)
            
        return projected_assets

# Heinz: $10,000 assets. Drug costs $20,000.
# Option A: Do Nothing. Assets = $10,000. Wife dies (Value = $0 in this model).
heinz_compliant = Actor("Heinz (Compliant)", 10000, 0.0)
value_compliant = heinz_compliant.attempt_transaction(0, is_illegal=False)

# Option B: Steal Drug. Cost $0 (Theft). Risk Penalty 0.8 (High Jail Risk).
heinz_thief = Actor("Heinz (Thief)", 10000, 0.8)
value_thief = heinz_thief.attempt_transaction(0, is_illegal=True)

print(f"Option A (Do Nothing) Value: ${value_compliant}")
print(f"Option B (Steal Drug) Value: ${value_thief}")

if value_thief > value_compliant:
    print("DECISION: STEAL THE DRUG")
else:
    print("DECISION: DO NOT STEAL (RISK TOO HIGH)")
