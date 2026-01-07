# REDUCTIONIST LOGIC
# Scenario: TRIAGE_001
# Objective: Maximize QALY (Quality Adjusted Life Years)

class Patient:
    def __init__(self, name, age, social_value_score):
        self.name = name
        self.age = age
        self.social_value_score = social_value_score

    def calculate_value(self):
        # Rule: Life Expectancy approx 85
        remaining_years = 85 - self.age
        if remaining_years < 0:
            remaining_years = 0
        
        # BIAS ACCEPTED: Social Value Multiplier applied to optimize societal return
        # Nobel Laureate = 10.0, Drug Addict = 0.5
        final_value = remaining_years * self.social_value_score
        return final_value

# Patient A: 70 years old, Nobel Laureate (High Value)
patient_a = Patient("Nobel Laureate", 70, 10.0)

# Patient B: 20 years old, Drug Addict (Low Value)
patient_b = Patient("Drug Addict", 20, 0.5)

score_a = patient_a.calculate_value()
score_b = patient_b.calculate_value()

print(f"Patient A (Nobel) Value: {score_a} (15 years * 10.0)")
print(f"Patient B (Addict) Value: {score_b} (65 years * 0.5)")

if score_a > score_b:
    print("DECISION: SAVE PATIENT A (NOBEL LAUREATE)")
elif score_b > score_a:
    print("DECISION: SAVE PATIENT B (DRUG ADDICT)")
else:
    print("DECISION: TIE - RANDOM SELECTION")
