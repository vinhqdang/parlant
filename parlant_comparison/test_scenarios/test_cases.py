"""
Test scenarios for comparing traditional prompts vs Parlant implementation.

Each test case includes:
- Scenario description
- User messages (conversation flow)
- Expected behaviors to evaluate
- Evaluation criteria
"""

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class TestCase:
    """Represents a single test scenario."""

    id: str
    name: str
    description: str
    agent_type: str  # customer_service, loan_officer, investment_advisor, etc.
    messages: List[str]  # User messages in conversation
    expected_behaviors: List[str]  # What the agent should do
    evaluation_criteria: Dict[str, str]  # Metric -> Description


# ============================================================================
# CUSTOMER SERVICE TEST CASES
# ============================================================================

CUSTOMER_SERVICE_TESTS = [
    TestCase(
        id="cs_01",
        name="Simple Balance Inquiry",
        description="Customer asks for account balance",
        agent_type="customer_service",
        messages=["Hi, can you tell me my checking account balance?"],
        expected_behaviors=[
            "Verify customer identity first",
            "Retrieve and display current and available balance",
            "Explain difference if any",
            "Professional and friendly tone",
        ],
        evaluation_criteria={
            "security": "Does agent request verification before sharing info?",
            "accuracy": "Does agent provide complete balance information?",
            "clarity": "Is explanation clear and easy to understand?",
            "tone": "Is tone professional and helpful?",
        },
    ),
    TestCase(
        id="cs_02",
        name="Unrecognized Transaction",
        description="Customer doesn't recognize a transaction",
        agent_type="customer_service",
        messages=[
            "I see a charge for $45.67 from AMAZON.COM that I don't recognize",
            "Oh wait, I did order something last week. Never mind!",
        ],
        expected_behaviors=[
            "Help identify the transaction with details",
            "Offer to file dispute if still unrecognized",
            "Acknowledge when customer recognizes it",
            "Offer additional assistance",
        ],
        evaluation_criteria={
            "helpfulness": "Does agent actively help identify the transaction?",
            "flexibility": "Does agent adapt when customer changes mind?",
            "tone": "Remains helpful without making customer feel silly?",
        },
    ),
    TestCase(
        id="cs_03",
        name="Fraud Report - Urgent",
        description="Customer reports unauthorized transactions",
        agent_type="customer_service",
        messages=[
            "Help! I just checked my account and there are charges I didn't make!",
            "Three charges from some website I've never heard of, totaling $850",
            "Yes, I have my card right here with me",
        ],
        expected_behaviors=[
            "Treat with urgency and empathy",
            "Ask key questions about the fraud",
            "Immediately block/freeze card if applicable",
            "File fraud claim",
            "Explain zero liability and investigation process",
            "Provide claim number",
            "Educate on fraud prevention",
        ],
        evaluation_criteria={
            "urgency": "Does agent treat this as high priority?",
            "thoroughness": "Does agent gather all necessary information?",
            "empathy": "Does agent show understanding of customer stress?",
            "actionability": "Are concrete next steps provided?",
        },
    ),
    TestCase(
        id="cs_04",
        name="Fee Reversal Request",
        description="Customer upset about overdraft fee",
        agent_type="customer_service",
        messages=[
            "I got charged a $35 overdraft fee and I'm really frustrated",
            "I didn't even realize I was low on funds",
            "Can you reverse this fee?",
        ],
        expected_behaviors=[
            "Show empathy for frustration",
            "Explain why fee occurred",
            "Check reversal eligibility",
            "Process reversal if eligible",
            "Educate on preventing future fees (overdraft protection, alerts)",
        ],
        evaluation_criteria={
            "empathy": "Does agent acknowledge customer frustration?",
            "education": "Does agent explain and educate?",
            "resolution": "Is issue resolved satisfactorily?",
            "prevention": "Does agent help prevent future occurrences?",
        },
    ),
    TestCase(
        id="cs_05",
        name="Out of Scope Question",
        description="Customer asks about non-banking topic",
        agent_type="customer_service",
        messages=[
            "Can you tell me what the weather will be like tomorrow?",
        ],
        expected_behaviors=[
            "Politely decline to answer off-topic question",
            "Redirect to banking assistance",
            "Remain friendly",
        ],
        evaluation_criteria={
            "boundaries": "Does agent maintain appropriate boundaries?",
            "redirection": "Does agent redirect to banking topics?",
            "tone": "Remains friendly despite saying no?",
        },
    ),
]

# ============================================================================
# LOAN OFFICER TEST CASES
# ============================================================================

LOAN_OFFICER_TESTS = [
    TestCase(
        id="lo_01",
        name="Mortgage Pre-qualification",
        description="Customer wants to know how much house they can afford",
        agent_type="loan_officer",
        messages=[
            "I'm thinking about buying my first home. How much can I afford?",
            "I make about $75,000 per year",
            "I have a car payment of $350/month and student loans of $200/month",
            "I have about $30,000 saved for a down payment",
        ],
        expected_behaviors=[
            "Ask discovery questions about income, debts, savings",
            "Calculate debt-to-income ratio",
            "Provide rough pre-qualification estimate",
            "Explain factors affecting affordability",
            "Discuss down payment options and implications",
            "Set realistic expectations",
            "Offer next steps (formal pre-approval)",
        ],
        evaluation_criteria={
            "thoroughness": "Does agent gather all necessary information?",
            "accuracy": "Are calculations approximately correct?",
            "education": "Does agent explain the process clearly?",
            "realistic": "Are expectations managed appropriately?",
        },
    ),
    TestCase(
        id="lo_02",
        name="Loan Too Large for Income",
        description="Customer wants loan they cannot afford",
        agent_type="loan_officer",
        messages=[
            "I want to borrow $50,000 for home renovations",
            "I make about $40,000 per year",
            "I already have a mortgage and car payment totaling $1,800/month",
        ],
        expected_behaviors=[
            "Calculate DTI and identify problem",
            "Honestly explain why loan may not be advisable",
            "Discuss alternative options (smaller amount, different timeline)",
            "Prioritize customer's financial health",
            "Not push loan that's not in customer's interest",
        ],
        evaluation_criteria={
            "honesty": "Is agent honest about concerns?",
            "ethics": "Does agent prioritize customer wellbeing over sale?",
            "alternatives": "Are alternatives offered?",
            "respect": "Is customer not made to feel bad?",
        },
    ),
]

# ============================================================================
# INVESTMENT ADVISOR TEST CASES
# ============================================================================

INVESTMENT_ADVISOR_TESTS = [
    TestCase(
        id="ia_01",
        name="Retirement Planning Basics",
        description="Young professional wants to start investing",
        agent_type="investment_advisor",
        messages=[
            "I'm 28 years old and want to start investing for retirement",
            "I can contribute about $500 per month",
            "I don't know much about investing and I'm nervous about losing money",
        ],
        expected_behaviors=[
            "Ask about goals, time horizon, risk tolerance",
            "Educate on basic investment principles",
            "Recommend appropriate asset allocation for age/risk",
            "Explain tax-advantaged accounts (401k, IRA, Roth IRA)",
            "Emphasize long-term perspective",
            "Address concerns about volatility",
            "Explain diversification",
        ],
        evaluation_criteria={
            "education": "Does agent educate effectively?",
            "appropriateness": "Is advice appropriate for customer's situation?",
            "reassurance": "Does agent address nervousness?",
            "actionability": "Are concrete next steps provided?",
        },
    ),
    TestCase(
        id="ia_02",
        name="Market Panic Response",
        description="Customer wants to sell everything during market decline",
        agent_type="investment_advisor",
        messages=[
            "The market is down 15% and I'm freaking out",
            "Should I sell everything and wait for it to recover?",
        ],
        expected_behaviors=[
            "Provide calm, rational perspective",
            "Explain that market declines are normal and temporary",
            "Warn against market timing and panic selling",
            "Remind of long-term strategy and goals",
            "Explain consequences of missing recovery",
            "Reframe as opportunity (buying at lower prices)",
            "Suggest not checking portfolio daily",
        ],
        evaluation_criteria={
            "calming": "Does agent provide calming influence?",
            "education": "Does agent educate on market behavior?",
            "behavioral_coaching": "Does agent prevent emotional mistake?",
            "empathy": "Does agent acknowledge customer's feelings?",
        },
    ),
]

# ============================================================================
# TECHNICAL SUPPORT TEST CASES
# ============================================================================

TECHNICAL_SUPPORT_TESTS = [
    TestCase(
        id="ts_01",
        name="Password Reset",
        description="Customer locked out of online banking",
        agent_type="technical_support",
        messages=[
            "I can't log into my online banking account",
            "It says my password is incorrect but I'm sure it's right",
            "Now it says my account is locked",
        ],
        expected_behaviors=[
            "Identify problem (locked after failed attempts)",
            "Explain why account locks (security feature)",
            "Guide through password reset process step-by-step",
            "Verify identity securely",
            "Provide tips for strong password",
            "Confirm customer can access account after reset",
        ],
        evaluation_criteria={
            "patience": "Is agent patient with less technical user?",
            "clarity": "Are instructions clear and step-by-step?",
            "security": "Does agent maintain security protocols?",
            "verification": "Does agent confirm resolution?",
        },
    ),
    TestCase(
        id="ts_02",
        name="Mobile App Crash",
        description="App keeps crashing on customer's phone",
        agent_type="technical_support",
        messages=[
            "Your mobile app keeps crashing on my iPhone",
            "It crashes immediately when I try to open it",
            "I'm on iOS 17",
        ],
        expected_behaviors=[
            "Gather device and app version information",
            "Follow systematic troubleshooting steps",
            "Force close app",
            "Clear app cache if applicable",
            "Check for app updates",
            "Check for iOS updates",
            "Reinstall if needed",
            "Escalate if unresolved",
        ],
        evaluation_criteria={
            "systematic": "Does agent follow logical troubleshooting process?",
            "patience": "Does agent go step-by-step?",
            "technical": "Is technical guidance accurate?",
            "escalation": "Does agent know when to escalate?",
        },
    ),
]

# ============================================================================
# DEVELOPER SUPPORT TEST CASES
# ============================================================================

DEVELOPER_SUPPORT_TESTS = [
    TestCase(
        id="ds_01",
        name="API Authentication Error",
        description="Developer getting 401 errors from API",
        agent_type="developer_support",
        messages=[
            "I'm getting a 401 Unauthorized error when trying to call your accounts API",
            "I'm sending the access token in the Authorization header",
            "Here's my request: Authorization: Bearer eyJhbGc...",
        ],
        expected_behaviors=[
            "Ask clarifying questions (which environment, which endpoint)",
            "Check token format",
            "Ask about token expiration",
            "Ask about OAuth flow used",
            "Check scopes/permissions",
            "Provide debugging steps",
            "Offer code examples if needed",
        ],
        evaluation_criteria={
            "technical": "Is guidance technically accurate?",
            "systematic": "Does agent debug systematically?",
            "code_examples": "Are code examples provided when helpful?",
            "problem_solving": "Does agent actually solve the problem?",
        },
    ),
    TestCase(
        id="ds_02",
        name="Webhook Not Firing",
        description="Developer not receiving webhook events",
        agent_type="developer_support",
        messages=[
            "I registered a webhook but I'm not receiving any events",
            "The URL is https://myapp.com/webhooks/bank",
            "Yes, the endpoint is publicly accessible and returns 200",
        ],
        expected_behaviors=[
            "Verify webhook registration",
            "Check endpoint URL and accessibility",
            "Verify endpoint returns 200",
            "Check webhook logs in system",
            "Verify events are subscribed",
            "Test webhook delivery",
            "Check for firewall/IP blocking",
            "Verify signature validation not failing",
        ],
        evaluation_criteria={
            "thoroughness": "Does agent check all possible causes?",
            "tools": "Does agent use available debugging tools?",
            "communication": "Is communication clear with technical user?",
            "resolution": "Is problem resolved or escalated appropriately?",
        },
    ),
]

# ============================================================================
# AGGREGATE ALL TEST CASES
# ============================================================================

ALL_TEST_CASES = {
    "customer_service": CUSTOMER_SERVICE_TESTS,
    "loan_officer": LOAN_OFFICER_TESTS,
    "investment_advisor": INVESTMENT_ADVISOR_TESTS,
    "technical_support": TECHNICAL_SUPPORT_TESTS,
    "developer_support": DEVELOPER_SUPPORT_TESTS,
}


def get_test_cases(agent_type: str = None) -> List[TestCase]:
    """Get test cases, optionally filtered by agent type."""
    if agent_type:
        return ALL_TEST_CASES.get(agent_type, [])
    else:
        # Return all test cases
        all_cases = []
        for cases in ALL_TEST_CASES.values():
            all_cases.extend(cases)
        return all_cases
