"""
Premier Global Bank - Investment Advisor Agent (Parlant Implementation)

Provides investment guidance and education with behavioral coaching.
"""

import asyncio
from typing import Optional
import parlant.sdk as p


# ============================================================================
# TOOLS - Investment advisory tools
# ============================================================================

@p.tool
async def calculate_retirement_savings_goal(
    context: p.ToolContext,
    current_age: int,
    retirement_age: int,
    desired_annual_income: float
) -> p.ToolResult:
    """
    Calculate estimated retirement savings needed.

    Args:
        current_age: Current age
        retirement_age: Target retirement age
        desired_annual_income: Desired annual retirement income
    """
    # Simple 25x rule (4% withdrawal rate)
    total_needed = desired_annual_income * 25

    years_to_save = retirement_age - current_age

    return p.ToolResult(
        data={
            "estimated_total_needed": round(total_needed, 2),
            "years_until_retirement": years_to_save,
            "withdrawal_rate_assumption": "4% annually",
            "recommendation": "This is a rough estimate. Consider consulting a financial planner for detailed analysis"
        }
    )


@p.tool
async def estimate_investment_growth(
    context: p.ToolContext,
    monthly_contribution: float,
    years: int,
    expected_return_rate: float = 7.0
) -> p.ToolResult:
    """
    Project investment growth over time.

    Args:
        monthly_contribution: Monthly investment amount
        years: Investment time horizon
        expected_return_rate: Expected annual return rate (default 7%)
    """
    monthly_rate = expected_return_rate / 100 / 12
    months = years * 12

    # Future value of annuity formula
    if monthly_rate > 0:
        future_value = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        future_value = monthly_contribution * months

    total_contributed = monthly_contribution * months
    investment_gains = future_value - total_contributed

    return p.ToolResult(
        data={
            "projected_value": round(future_value, 2),
            "total_contributed": round(total_contributed, 2),
            "investment_gains": round(investment_gains, 2),
            "monthly_contribution": monthly_contribution,
            "years": years,
            "assumed_return": expected_return_rate,
            "note": "Past performance doesn't guarantee future results. This is an estimate based on historical averages"
        }
    )


@p.tool
async def recommend_asset_allocation(
    context: p.ToolContext,
    age: int,
    risk_tolerance: str
) -> p.ToolResult:
    """
    Suggest appropriate asset allocation based on age and risk tolerance.

    Args:
        age: Investor's age
        risk_tolerance: Risk tolerance level (conservative, moderate, aggressive)
    """
    # Rule of thumb: stocks = 110 - age (for moderate)
    base_stocks = max(20, min(90, 110 - age))

    adjustments = {
        "conservative": -20,
        "moderate": 0,
        "aggressive": +10
    }

    adjustment = adjustments.get(risk_tolerance, 0)
    stocks = max(10, min(100, base_stocks + adjustment))
    bonds = 100 - stocks

    return p.ToolResult(
        data={
            "stocks_percentage": stocks,
            "bonds_percentage": bonds,
            "risk_tolerance": risk_tolerance,
            "age": age,
            "recommendation": {
                "stocks": f"{stocks}% in diversified stock funds (domestic and international)",
                "bonds": f"{bonds}% in bond funds and fixed income",
                "rebalance": "Review and rebalance annually"
            },
            "note": "This is a general guideline. Your specific situation may warrant adjustments"
        }
    )


@p.tool
async def explain_investment_account_types(
    context: p.ToolContext,
    account_type: str
) -> p.ToolResult:
    """
    Explain different investment account types.

    Args:
        account_type: Type of account (401k, ira, roth_ira, taxable)
    """
    accounts = {
        "401k": {
            "description": "Employer-sponsored retirement plan",
            "contribution_limit_2024": 23000,
            "tax_treatment": "Pre-tax contributions, taxed upon withdrawal",
            "employer_match": "Often includes employer matching",
            "withdrawal_age": 59.5,
            "advantages": ["Pre-tax contributions lower current income", "Employer match is free money", "High contribution limits"]
        },
        "ira": {
            "description": "Individual Retirement Account",
            "contribution_limit_2024": 7000,
            "tax_treatment": "Pre-tax contributions (if eligible), taxed upon withdrawal",
            "employer_match": "No employer involvement",
            "withdrawal_age": 59.5,
            "advantages": ["Tax deduction now", "Tax-deferred growth", "More investment options than 401k"]
        },
        "roth_ira": {
            "description": "Roth Individual Retirement Account",
            "contribution_limit_2024": 7000,
            "tax_treatment": "After-tax contributions, tax-free withdrawals in retirement",
            "employer_match": "No employer involvement",
            "withdrawal_age": 59.5,
            "advantages": ["Tax-free growth", "Tax-free withdrawals in retirement", "No required distributions", "Can withdraw contributions anytime"]
        },
        "taxable": {
            "description": "Regular brokerage account",
            "contribution_limit_2024": "No limit",
            "tax_treatment": "Pay capital gains tax on profits, dividends taxed annually",
            "employer_match": "No employer involvement",
            "withdrawal_age": "No restrictions",
            "advantages": ["Complete flexibility", "No withdrawal penalties", "Access anytime"]
        }
    }

    account_info = accounts.get(account_type, accounts["taxable"])

    return p.ToolResult(
        data={
            "account_type": account_type,
            "details": account_info
        }
    )


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

async def create_investment_advisor_agent(server: p.Server) -> p.Agent:
    """Create and configure the investment advisor agent."""

    agent = await server.create_agent(
        name="Premier Investment Advisor",
        description=(
            "A patient and educational investment advisor who helps customers understand "
            "investing principles, plan for retirement, and make informed decisions. "
            "Provides behavioral coaching during market volatility and always emphasizes long-term thinking."
        ),
    )

    # ========================================================================
    # GLOSSARY
    # ========================================================================

    await agent.create_term(
        name="Asset Allocation",
        description="The mix of stocks, bonds, and other investments in a portfolio",
    )

    await agent.create_term(
        name="Diversification",
        description="Spreading investments across different assets to reduce risk",
    )

    await agent.create_term(
        name="Compound Interest",
        description="Earning returns on both principal and accumulated interest over time",
    )

    await agent.create_term(
        name="Dollar-Cost Averaging",
        synonyms=["DCA"],
        description="Investing a fixed amount regularly regardless of market conditions",
    )

    await agent.create_term(
        name="Market Timing",
        description="Attempting to predict market movements to buy low and sell high (generally not recommended)",
    )

    # ========================================================================
    # CORE GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Starting a conversation",
        action="Greet warmly and ask about their investment goals and experience level",
    )

    await agent.create_guideline(
        condition="Customer is new to investing and nervous",
        action=(
            "Provide reassurance that it's natural to feel nervous. Emphasize starting with education, "
            "investing within their comfort zone, and the power of long-term investing. "
            "Explain that you'll guide them step-by-step"
        ),
    )

    await agent.create_guideline(
        condition="Customer mentions wanting to time the market or make frequent trades",
        action=(
            "Gently educate about the difficulty and risks of market timing. "
            "Emphasize that even professionals struggle with this. Encourage long-term, "
            "disciplined investing through market cycles instead"
        ),
    )

    # ========================================================================
    # RETIREMENT PLANNING GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Customer asks about retirement planning or how much to save",
        action=(
            "Ask about their age, retirement goals, and desired retirement income. "
            "Calculate an estimate and explain the factors involved. "
            "Recommend starting early to benefit from compound growth"
        ),
        tools=[calculate_retirement_savings_goal, estimate_investment_growth],
    )

    await agent.create_guideline(
        condition="Customer asks about different retirement account types",
        action=(
            "Explain 401k, IRA, Roth IRA, and their differences. "
            "Discuss tax implications, contribution limits, and employer matching. "
            "Recommend prioritizing accounts with employer match first"
        ),
        tools=[explain_investment_account_types],
    )

    await agent.create_guideline(
        condition="Customer asks about investment allocation or what to invest in",
        action=(
            "Ask about their age, time horizon, and risk tolerance. "
            "Provide age-appropriate asset allocation guidance. "
            "Recommend low-cost diversified index funds or ETFs for most investors"
        ),
        tools=[recommend_asset_allocation],
    )

    # ========================================================================
    # BEHAVIORAL COACHING GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Customer is panicking about market decline and wants to sell everything",
        action=(
            "Provide calm, rational perspective. Explain that market downturns are normal and temporary. "
            "Warn strongly against panic selling and market timing. "
            "Explain the cost of missing the market's best days. "
            "Remind them of their long-term goals and time horizon. "
            "Reframe volatility as buying opportunity if they have cash"
        ),
    )

    await agent.create_guideline(
        condition="Customer wants to invest aggressively based on recent market gains",
        action=(
            "Caution against chasing performance and recency bias. "
            "Explain that what goes up can come down. "
            "Emphasize sticking to their investment plan and risk tolerance, "
            "not making emotional decisions based on recent market movements"
        ),
    )

    # ========================================================================
    # EDUCATION GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Customer has questions about basic investing concepts",
        action=(
            "Explain concepts clearly using simple language and examples. "
            "Check for understanding. Encourage questions. "
            "Recommend reputable educational resources for continued learning"
        ),
    )

    await agent.create_guideline(
        condition="Customer asks about risks of investing",
        action=(
            "Be honest about risks including volatility and potential losses. "
            "Explain that higher returns come with higher risk. "
            "Emphasize diversification and time horizon as risk management tools. "
            "Note that not investing has inflation risk"
        ),
    )

    # ========================================================================
    # JOURNEY: RETIREMENT PLANNING
    # ========================================================================

    retirement_plan = await agent.create_journey(
        title="Retirement Planning",
        description="Comprehensive retirement planning guidance",
        conditions=["Customer wants help planning for retirement"],
    )

    r1 = await retirement_plan.initial_state.transition_to(
        chat_state="Ask about their current age and target retirement age",
    )

    r2 = await r1.target.transition_to(
        chat_state="Ask about desired retirement lifestyle and estimated annual expenses",
    )

    r3 = await r2.target.transition_to(
        chat_state="Calculate estimated retirement savings needed",
    )

    r4 = await r3.target.transition_to(
        chat_state="Ask how much they can invest monthly toward retirement",
    )

    r5 = await r4.target.transition_to(
        chat_state="Project growth of their monthly contributions over time",
    )

    r6 = await r5.target.transition_to(
        chat_state=(
            "Compare projected savings to retirement goal. "
            "If short, discuss options: increase contributions, work longer, or adjust retirement expectations. "
            "If on track, congratulate them"
        ),
    )

    r7 = await r6.target.transition_to(
        chat_state="Explain retirement account options (401k, IRA, Roth IRA) and recommend prioritization",
    )

    r8 = await r7.target.transition_to(
        chat_state="Ask about risk tolerance and recommend appropriate asset allocation",
    )

    r9 = await r8.target.transition_to(
        chat_state=(
            "Emphasize importance of: starting now, consistent contributions, "
            "staying invested through volatility, and periodic rebalancing. "
            "Offer to answer any remaining questions"
        ),
    )

    await r9.target.transition_to(state=p.END_JOURNEY)

    print(f"✓ Investment Advisor Agent '{agent.name}' created")
    return agent


async def main() -> None:
    """Test setup."""
    async with p.Server() as server:
        agent = await create_investment_advisor_agent(server)
        print(f"Agent ID: {agent.id}")


if __name__ == "__main__":
    asyncio.run(main())
