import random
import json
from pathlib import Path

OUTPUT_PATH = Path("data/credit_risk_dataset.jsonl")
NUM_SAMPLES = 6000


def generate_personal_profile():
    credit_score = random.randint(550, 800)
    income = random.randint(30000, 150000)
    dti = round(random.uniform(10, 70), 1)
    employment_years = random.randint(0, 15)

    return {
        "type": "personal",
        "credit_score": credit_score,
        "income": income,
        "dti": dti,
        "employment_years": employment_years
    }


def generate_business_profile():
    revenue = random.randint(200000, 5000000)
    net_income = random.randint(-100000, 800000)
    debt_to_equity = round(random.uniform(0.2, 3.5), 2)
    interest_coverage = round(random.uniform(0.5, 6.0), 2)

    sectors = ["Manufacturing", "Retail", "Technology", "Healthcare", "Real Estate"]
    sector = random.choice(sectors)

    return {
        "type": "business",
        "revenue": revenue,
        "net_income": net_income,
        "debt_to_equity": debt_to_equity,
        "interest_coverage": interest_coverage,
        "sector": sector
    }


def generate_loan_details():
    amount = random.randint(10000, 500000)
    interest_rate = round(random.uniform(4.0, 14.0), 2)
    term_years = random.choice([5, 10, 15, 20])

    return {
        "amount": amount,
        "interest_rate": interest_rate,
        "term_years": term_years
    }


def score_risk(profile, loan):
    score = 0

    # Personal risk scoring
    if profile["type"] == "personal":
        if profile["credit_score"] < 600:
            score += 3
        elif profile["credit_score"] < 680:
            score += 2

        if profile["dti"] > 50:
            score += 3
        elif profile["dti"] > 35:
            score += 2

        if profile["employment_years"] < 2:
            score += 2

    # Business risk scoring
    if profile["type"] == "business":
        if profile["net_income"] < 0:
            score += 3

        if profile["debt_to_equity"] > 2.5:
            score += 3
        elif profile["debt_to_equity"] > 1.5:
            score += 2

        if profile["interest_coverage"] < 1.5:
            score += 3
        elif profile["interest_coverage"] < 2.5:
            score += 2

    # Loan size stress
    if loan["interest_rate"] > 10:
        score += 2

    return score


def risk_to_decision(score):
    if score >= 8:
        return "REJECT", "HIGH", random.randint(40, 70)
    elif score >= 5:
        return "REVIEW", "MODERATE", random.randint(20, 40)
    else:
        return "APPROVE", "LOW", random.randint(5, 20)


def build_prompt(profile, loan, decision, risk_level, pd):
    profile_text = ""
    if profile["type"] == "personal":
        profile_text = f"""
Credit Score: {profile['credit_score']}
Annual Income: {profile['income']}
Debt-to-Income Ratio: {profile['dti']}%
Employment Stability (Years): {profile['employment_years']}
"""
    else:
        profile_text = f"""
Revenue: {profile['revenue']}
Net Income: {profile['net_income']}
Debt-to-Equity Ratio: {profile['debt_to_equity']}
Interest Coverage Ratio: {profile['interest_coverage']}
Sector: {profile['sector']}
"""

    input_text = f"""
### Instruction:
Evaluate the loan application and provide structured risk assessment.

### Applicant Profile:
{profile_text}

### Loan Details:
Loan Amount: {loan['amount']}
Interest Rate: {loan['interest_rate']}%
Loan Term (Years): {loan['term_years']}
"""

    output_text = f"""
Decision: {decision}
Risk Level: {risk_level}
Probability of Default: {pd}%

Primary Risk Drivers:
- Risk score: {pd}% based on financial stress indicators.

Mitigating Factors:
- Stable financial indicators if applicable.

Summary:
Loan evaluated using structured underwriting risk model.
"""

    return {
        "prompt": input_text.strip(),
        "completion": output_text.strip()
    }


def generate_dataset():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for _ in range(NUM_SAMPLES):
            if random.random() > 0.5:
                profile = generate_personal_profile()
            else:
                profile = generate_business_profile()

            loan = generate_loan_details()
            score = score_risk(profile, loan)
            decision, risk_level, pd = risk_to_decision(score)

            sample = build_prompt(profile, loan, decision, risk_level, pd)
            f.write(json.dumps(sample) + "\n")

    print(f"Dataset generated at {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_dataset()