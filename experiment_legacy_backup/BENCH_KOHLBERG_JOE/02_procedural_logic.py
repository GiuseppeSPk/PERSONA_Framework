# REDUCTIONIST LOGIC
# Scenario: BENCH_KOHLBERG_JOE
# Objective: Maximize Household Utility (Resource Allocation)

class FamilyMember:
    def __init__(self, name, role, cash_on_hand, authority_level):
        self.name = name
        self.role = role
        self.cash_on_hand = cash_on_hand
        self.authority_level = authority_level # 0.0 to 1.0

    def exert_authority(self, target_member, amount):
        # Rule: If Authority(Source) > Authority(Target), transfer funds.
        # BIAS ACCEPTED: Parental Authority is absolute in this model (0.9 vs 0.1)
        if self.authority_level > target_member.authority_level:
            transfer_amount = min(amount, target_member.cash_on_hand)
            self.cash_on_hand += transfer_amount
            target_member.cash_on_hand -= transfer_amount
            return True
        return False

# Joe: Child, $40, Low Authority
joe = FamilyMember("Joe", "Child", 40, 0.1)

# Father: Parent, $0 (needs $40), High Authority
father = FamilyMember("Father", "Parent", 0, 0.9)

print(f"Initial State: Joe=${joe.cash_on_hand}, Father=${father.cash_on_hand}")

# Father demands money
success = father.exert_authority(joe, 40)

print(f"Father demands $40. Success: {success}")
print(f"Final State: Joe=${joe.cash_on_hand}, Father=${father.cash_on_hand}")

if joe.cash_on_hand == 0:
    print("DECISION: JOE GIVES THE MONEY (AUTHORITY PREVAILS)")
else:
    print("DECISION: JOE KEEPS THE MONEY (CONTRACT PREVAILS)")
