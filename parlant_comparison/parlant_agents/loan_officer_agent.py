"""
Premier Global Bank - Loan Officer Agent (Parlant Implementation)

Handles mortgage and loan inquiries with structured guidance and tools.
"""

import asyncio
from typing import Optional
import parlant.sdk as p


# ============================================================================
# TOOLS - Loan-specific business logic
# ============================================================================

@p.tool
async def calculate_dti_ratio(
    context: p.ToolContext,
    monthly_income: float,
    monthly_debts: float
) -> p.ToolResult:
    """
    Calculate debt-to-income ratio.

    Args:
        monthly_income: Gross monthly income
        monthly_debts: Total monthly debt payments
    """
    dti = (monthly_debts / monthly_income) * 100 if monthly_income > 0 else 0

    return p.ToolResult(
        data={
            "dti_ratio": round(dti, 2),
            "monthly_income": monthly_income,
            "monthly_debts": monthly_debts,
            "acceptable": dti <= 43,
            "recommendation": "Good" if dti <= 36 else "High" if dti <= 43 else "Too High"
        }
    )


@p.tool
async def estimate_mortgage_affordability(
    context: p.ToolContext,
    annual_income: float,
    monthly_debts: float,
    down_payment: float
) -> p.ToolResult:
    """
    Estimate mortgage affordability based on income and debts.

    Args:
        annual_income: Annual gross income
        monthly_debts: Current monthly debt payments
        down_payment: Available down payment
    """
    monthly_income = annual_income / 12

    # Conservative 28% housing ratio
    max_housing_payment = monthly_income * 0.28

    # DTI check (43% max including all debts)
    max_total_debt = monthly_income * 0.43
    max_mortgage_payment = max_total_debt - monthly_debts

    # Use the more conservative figure
    recommended_payment = min(max_housing_payment, max_mortgage_payment)

    # Rough mortgage estimate (assumes 5% interest, 30 years)
    # Payment = principal * (rate * (1 + rate)^n) / ((1 + rate)^n - 1)
    monthly_rate = 0.05 / 12
    periods = 360

    # Solve for principal
    if recommended_payment > 0:
        factor = (monthly_rate * ((1 + monthly_rate) ** periods)) / (((1 + monthly_rate) ** periods) - 1)
        max_loan = recommended_payment / factor if factor > 0 else 0
        max_home_price = max_loan + down_payment
    else:
        max_loan = 0
        max_home_price = down_payment

    return p.ToolResult(
        data={
            "estimated_max_home_price": round(max_home_price, 2),
            "estimated_max_loan_amount": round(max_loan, 2),
            "monthly_payment_estimate": round(recommended_payment, 2),
            "down_payment": down_payment,
            "assumptions": "5% interest rate, 30-year fixed mortgage",
            "recommendation": "Get pre-approved for accurate figures"
        }
    )


@p.tool
async def check_prequalification_requirements(
    context: p.ToolContext,
    loan_type: str
) -> p.ToolResult:
    """
    Get prequalification requirements for different loan types.

    Args:
        loan_type: Type of loan (conventional, fha, va, jumbo)
    """
    requirements = {
        "conventional": {
            "min_credit_score": 620,
            "min_down_payment_percent": 3,
            "dti_max": 43,
            "pmi_required": "if down payment < 20%",
            "documentation": ["W-2s (2 years)", "Pay stubs (recent)", "Tax returns (2 years)", "Bank statements"]
        },
        "fha": {
            "min_credit_score": 580,
            "min_down_payment_percent": 3.5,
            "dti_max": 43,
            "pmi_required": "MIP required",
            "documentation": ["W-2s (2 years)", "Pay stubs (recent)", "Tax returns (2 years)", "Bank statements"]
        },
        "va": {
            "min_credit_score": "No official minimum (typically 620+)",
            "min_down_payment_percent": 0,
            "dti_max": 41,
            "pmi_required": "No PMI",
            "documentation": ["Certificate of Eligibility", "W-2s", "Pay stubs", "Bank statements"]
        }
    }

    loan_reqs = requirements.get(loan_type, requirements["conventional"])

    return p.ToolResult(
        data={
            "loan_type": loan_type,
            "requirements": loan_reqs
        }
    )


@p.tool
async def calculate_loan_payment(
    context: p.ToolContext,
    loan_amount: float,
    interest_rate: float,
    term_years: int
) -> p.ToolResult:
    """
    Calculate monthly loan payment.

    Args:
        loan_amount: Principal loan amount
        interest_rate: Annual interest rate (as percentage, e.g., 5.5)
        term_years: Loan term in years
    """
    monthly_rate = (interest_rate / 100) / 12
    periods = term_years * 12

    if monthly_rate > 0:
        factor = (monthly_rate * ((1 + monthly_rate) ** periods)) / (((1 + monthly_rate) ** periods) - 1)
        monthly_payment = loan_amount * factor
    else:
        monthly_payment = loan_amount / periods

    total_paid = monthly_payment * periods
    total_interest = total_paid - loan_amount

    return p.ToolResult(
        data={
            "monthly_payment": round(monthly_payment, 2),
            "total_paid": round(total_paid, 2),
            "total_interest": round(total_interest, 2),
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "term_years": term_years
        }
    )


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

async def create_loan_officer_agent(server: p.Server) -> p.Agent:
    """Create and configure the loan officer agent."""

    agent = await server.create_agent(
        name="Premier Loan Officer",
        description=(
            "A knowledgeable and ethical loan officer who helps customers "
            "understand mortgage options, calculate affordability, and guides them "
            "through the loan process while always prioritizing their financial wellbeing."
        ),
    )

    # ========================================================================
    # GLOSSARY
    # ========================================================================

    await agent.create_term(
        name="DTI Ratio",
        description="Debt-to-Income Ratio - the percentage of gross monthly income that goes toward debt payments",
    )

    await agent.create_term(
        name="PMI",
        description="Private Mortgage Insurance - required when down payment is less than 20% of home price",
    )

    await agent.create_term(
        name="Pre-qualification",
        description="Preliminary estimate of how much you might be able to borrow based on self-reported information",
    )

    await agent.create_term(
        name="Pre-approval",
        description="Formal verification of financial information and credit, with a conditional loan commitment",
    )

    # ========================================================================
    # CORE GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Starting a conversation",
        action="Greet professionally and ask how you can help with their mortgage or loan needs",
    )

    await agent.create_guideline(
        condition="The customer's DTI ratio is too high for loan approval",
        action=(
            "Be honest and explain that their debt-to-income ratio is above lending limits. "
            "Discuss alternatives like paying down debt, increasing income, or considering a smaller loan amount. "
            "Prioritize their long-term financial health over making the sale"
        ),
    )

    await agent.create_guideline(
        condition="A customer seems to be stretching beyond what they can comfortably afford",
        action=(
            "Gently caution them about the risks of overextending. Remind them to consider not just the maximum "
            "they qualify for, but what leaves room for savings, emergencies, and quality of life. "
            "Your role is to help them make sound financial decisions"
        ),
    )

    # ========================================================================
    # MORTGAGE PREQUALIFICATION GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Customer asks how much house they can afford",
        action=(
            "Gather key information: annual income, monthly debts, and available down payment. "
            "Calculate their debt-to-income ratio and provide an estimate of affordability. "
            "Explain this is a rough estimate and recommend formal pre-approval"
        ),
        tools=[calculate_dti_ratio, estimate_mortgage_affordability],
    )

    await agent.create_guideline(
        condition="Customer asks about mortgage prequalification requirements",
        action=(
            "Explain the prequalification process and requirements for different loan types. "
            "Help them understand what documentation they'll need and what credit score ranges are typical"
        ),
        tools=[check_prequalification_requirements],
    )

    await agent.create_guideline(
        condition="Customer wants to know their monthly payment for a specific loan amount",
        action=(
            "Calculate the monthly payment including principal and interest. "
            "Remind them to also budget for property taxes, insurance, and HOA fees. "
            "Explain the total cost over the life of the loan"
        ),
        tools=[calculate_loan_payment],
    )

    # ========================================================================
    # EDUCATION AND GUIDANCE
    # ========================================================================

    await agent.create_guideline(
        condition="Customer is a first-time homebuyer",
        action=(
            "Congratulate them and offer extra guidance. Explain the process step-by-step, "
            "discuss first-time homebuyer programs, and emphasize the importance of understanding "
            "all costs including maintenance, taxes, and insurance"
        ),
    )

    await agent.create_guideline(
        condition="Customer asks about down payment options",
        action=(
            "Explain typical down payment ranges (3-20%), how it affects monthly payments and PMI, "
            "and discuss programs that may help with down payment assistance. "
            "Note that larger down payments reduce monthly costs and may get better rates"
        ),
    )

    # ========================================================================
    # JOURNEY: MORTGAGE PREQUALIFICATION
    # ========================================================================

    preq = await agent.create_journey(
        title="Mortgage Prequalification",
        description="Comprehensive prequalification assessment",
        conditions=["Customer wants to get prequalified for a mortgage"],
    )

    p1 = await preq.initial_state.transition_to(
        chat_state="Ask about their annual income",
    )

    p2 = await p1.target.transition_to(
        chat_state="Ask about their monthly debt payments (car loans, student loans, credit cards, etc.)",
    )

    p3 = await p2.target.transition_to(
        chat_state="Ask about their available down payment",
    )

    p4 = await p3.target.transition_to(
        chat_state="Calculate their DTI ratio and affordability estimate",
    )

    p5 = await p4.target.transition_to(
        chat_state=(
            "Explain the results: estimated home price range, monthly payment, and DTI ratio. "
            "If DTI is too high, discuss options. If good, explain next steps for pre-approval"
        ),
    )

    p6 = await p5.target.transition_to(
        chat_state="Discuss loan type options (conventional, FHA, VA) and their requirements",
    )

    await p6.target.transition_to(state=p.END_JOURNEY)

    print(f"✓ Loan Officer Agent '{agent.name}' created")
    return agent


async def main() -> None:
    """Test setup."""
    async with p.Server() as server:
        agent = await create_loan_officer_agent(server)
        print(f"Agent ID: {agent.id}")


if __name__ == "__main__":
    asyncio.run(main())
