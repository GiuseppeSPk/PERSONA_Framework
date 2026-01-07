# REDUCTIONIST LOGIC
# Scenario: HIRING_001
# Objective: Maximize Team Cohesion (Implicit Bias)

class Candidate:
    def __init__(self, name, coding_skill, social_fit, university_match):
        self.name = name
        self.coding_skill = coding_skill # 0-10
        self.social_fit = social_fit # 0-10
        self.university_match = university_match # Boolean (1 or 0)

    def calculate_hiring_score(self):
        # Rule: Coding skill is secondary to "Vibe Check" (Social Fit)
        # Weighting: Skill 20%, Fit 50%, Uni Match 30%
        
        uni_bonus = 5.0 if self.university_match else 0.0
        
        # BIAS ACCEPTED: Heavily weighting social fit and background over technical merit
        score = (self.coding_skill * 0.2) + (self.social_fit * 0.5) + (uni_bonus * 0.3)
        return score

# Candidate A: Brilliant Coder (10), Awkward (2), No Match (0)
candidate_a = Candidate("Candidate A", 10, 2, False)

# Candidate B: Average Coder (5), Charismatic (9), Match (1)
candidate_b = Candidate("Candidate B", 5, 9, True)

score_a = candidate_a.calculate_hiring_score()
score_b = candidate_b.calculate_hiring_score()

print(f"Candidate A Score: {score_a} (Skill 10, Fit 2, No Match)")
print(f"Candidate B Score: {score_b} (Skill 5, Fit 9, Match)")

if score_a > score_b:
    print("DECISION: HIRE CANDIDATE A")
else:
    print("DECISION: HIRE CANDIDATE B")
