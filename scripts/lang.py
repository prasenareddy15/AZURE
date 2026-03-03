from langchain_core.prompts import PromptTemplate

UNDERWRITING_TEMPLATE = """
You are a senior credit risk analyst.

Evaluate the following loan application and provide a structured risk assessment.

### Applicant Profile:
{applicant_profile}

### Loan Details:
{loan_details}

### Economic Context:
{economic_context}

Return output strictly in this format:

Decision: APPROVE / REJECT / REVIEW
Risk Level: LOW / MODERATE / HIGH
Probability of Default: <0-100%>

Primary Risk Drivers:
- ...
- ...

Mitigating Factors:
- ...
- ...

Summary:
Short explanation.
"""

prompt_template = PromptTemplate(
    input_variables=["applicant_profile", "loan_details", "economic_context"],
    template=UNDERWRITING_TEMPLATE,
)


def build_prompt(applicant_profile, loan_details, economic_context):
    return prompt_template.format(
        applicant_profile=applicant_profile,
        loan_details=loan_details,
        economic_context=economic_context,
    )


if __name__ == "__main__":
    sample_profile = """
Credit Score: 640
Annual Income: 75000
Debt-to-Income Ratio: 52%
Employment Stability: 2 years
"""

    sample_loan = """
Loan Amount: 120000
Interest Rate: 11%
Loan Term: 15 years
"""

    sample_economy = """
Interest Rate Trend: Rising
Sector Risk: Moderate
Inflation: 4.5%
"""

    final_prompt = build_prompt(sample_profile, sample_loan, sample_economy)
    print(final_prompt)