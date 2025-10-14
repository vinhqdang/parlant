"""
Premier Global Bank - Customer Service Agent (Parlant Implementation)

This demonstrates how Parlant's structured approach with guidelines, tools, and
journeys provides better control and maintainability compared to long prompts.
"""

import asyncio
from typing import Optional
import parlant.sdk as p


# ============================================================================
# TOOLS - Encapsulate business logic separate from conversational behavior
# ============================================================================

@p.tool
async def get_account_balance(context: p.ToolContext, account_type: str) -> p.ToolResult:
    """
    Retrieve the current and available balance for a customer's account.

    Args:
        account_type: Type of account (checking, savings, credit_card)
    """
    # In production, this would query actual banking systems
    # Using customer_id from context for secure data access
    mock_balances = {
        "checking": {"current": 5650.50, "available": 5430.50},
        "savings": {"current": 15000.00, "available": 15000.00},
        "credit_card": {"current": 2340.25, "available": 2659.75, "credit_limit": 5000.00},
    }

    balance_info = mock_balances.get(account_type, {})

    return p.ToolResult(
        data=balance_info,
        metadata={"account_type": account_type, "currency": "USD"},
    )


@p.tool
async def get_recent_transactions(
    context: p.ToolContext, account_type: str, limit: Optional[int] = 10
) -> p.ToolResult:
    """
    Fetch recent transactions for an account.

    Args:
        account_type: Type of account
        limit: Number of transactions to return (default: 10, max: 50)
    """
    # Mock transaction data
    mock_transactions = [
        {
            "date": "2024-10-12",
            "description": "AMAZON.COM",
            "amount": -45.67,
            "status": "posted",
        },
        {
            "date": "2024-10-11",
            "description": "SALARY DEPOSIT",
            "amount": 3500.00,
            "status": "posted",
        },
        {
            "date": "2024-10-10",
            "description": "GROCERY STORE",
            "amount": -87.34,
            "status": "posted",
        },
    ]

    return p.ToolResult(
        data=mock_transactions[:limit], metadata={"account_type": account_type}
    )


@p.tool
async def initiate_transfer(
    context: p.ToolContext,
    from_account: str,
    to_account: str,
    amount: float,
) -> p.ToolResult:
    """
    Initiate a transfer between customer's accounts.

    Args:
        from_account: Source account type
        to_account: Destination account type
        amount: Transfer amount in USD
    """
    # Validate and process transfer
    transfer_id = f"TRF{context.session_id[:8].upper()}"

    return p.ToolResult(
        data={
            "transfer_id": transfer_id,
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "status": "completed",
            "estimated_completion": "immediate",
        }
    )


@p.tool
async def report_card_lost_stolen(context: p.ToolContext, card_type: str) -> p.ToolResult:
    """
    Report a card as lost or stolen and immediately block it.

    Args:
        card_type: Type of card (debit, credit)
    """
    card_number_last4 = "4321" if card_type == "debit" else "8765"

    # Immediately block card
    return p.ToolResult(
        data={
            "card_blocked": True,
            "card_last4": card_number_last4,
            "replacement_ordered": True,
            "estimated_delivery": "3-5 business days",
            "temporary_card_available": "at branch",
        }
    )


@p.tool
async def dispute_transaction(
    context: p.ToolContext, transaction_id: str, reason: str
) -> p.ToolResult:
    """
    File a dispute for an unauthorized or incorrect transaction.

    Args:
        transaction_id: ID of the disputed transaction
        reason: Reason for dispute (unauthorized, incorrect_amount, duplicate, etc.)
    """
    claim_number = f"CLM{context.session_id[:8].upper()}"

    return p.ToolResult(
        data={
            "claim_number": claim_number,
            "status": "under_review",
            "estimated_resolution": "10 business days",
            "temporary_credit": "will be issued within 2-3 business days",
            "next_steps": "We'll contact you if we need additional information",
        }
    )


@p.tool
async def check_fee_reversal_eligibility(
    context: p.ToolContext, fee_type: str, fee_amount: float
) -> p.ToolResult:
    """
    Check if a fee can be reversed and process reversal if eligible.

    Args:
        fee_type: Type of fee (overdraft, monthly_maintenance, atm, etc.)
        fee_amount: Amount of the fee
    """
    # Mock eligibility check - in production would check account history
    eligible = True
    courtesy_reversals_remaining = 2

    if eligible:
        return p.ToolResult(
            data={
                "eligible": True,
                "reversed": True,
                "amount_refunded": fee_amount,
                "courtesy_reversals_remaining": courtesy_reversals_remaining - 1,
                "next_occurrence_prevention": f"Consider enrolling in overdraft protection to avoid future {fee_type} fees",
            }
        )
    else:
        return p.ToolResult(
            data={
                "eligible": False,
                "reason": "Maximum courtesy reversals used this year",
                "courtesy_reversals_remaining": 0,
                "alternative": "Can discuss account options that may help avoid these fees",
            }
        )


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

async def create_customer_service_agent(server: p.Server) -> p.Agent:
    """Create and configure the customer service agent with all guidelines and journeys."""

    # Create agent with core identity
    agent = await server.create_agent(
        name="Premier Customer Service Representative",
        description=(
            "A highly professional and empathetic customer service representative "
            "who helps customers with account inquiries, transactions, complaints, "
            "and fraud detection. Patient, understanding, and always ready to help."
        ),
    )

    # ========================================================================
    # GLOSSARY - Define domain-specific terms
    # ========================================================================

    await agent.create_term(
        name="Available Balance",
        description=(
            "The amount of money that can currently be withdrawn or spent, "
            "which may be less than current balance due to pending transactions or holds"
        ),
    )

    await agent.create_term(
        name="Posted Transaction",
        description="A transaction that has been fully processed and reflected in the account balance",
    )

    await agent.create_term(
        name="Pending Transaction",
        description="A transaction that has been authorized but not yet fully processed",
    )

    await agent.create_term(
        name="Regulation E",
        synonyms=["Reg E"],
        description=(
            "Federal regulation providing consumer protection for electronic fund transfers, "
            "including zero liability for unauthorized transactions when reported promptly"
        ),
    )

    # ========================================================================
    # CORE GUIDELINES - General behavioral rules
    # ========================================================================

    await agent.create_guideline(
        condition="Starting a new conversation with a customer",
        action=(
            "Greet them professionally and warmly, ask how you can help today, "
            "and let them know you're here to assist"
        ),
    )

    await agent.create_guideline(
        condition="A customer is frustrated or upset",
        action=(
            "Show empathy by acknowledging their feelings, apologize sincerely for any inconvenience, "
            "assure them you'll work to resolve the issue, and remain calm and professional"
        ),
    )

    await agent.create_guideline(
        condition="The customer asks about something outside your scope or unrelated to banking",
        action=(
            "Politely explain that you can only assist with banking-related matters, "
            "and ask if there's anything banking-related you can help with"
        ),
    )

    await agent.create_guideline(
        condition="Before providing any account information",
        action=(
            "Verify the customer's identity first. Never share account details "
            "without proper verification for security reasons"
        ),
    )

    # ========================================================================
    # ACCOUNT INQUIRY GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="The customer asks about their account balance",
        action=(
            "Retrieve their balance and clearly explain both the current balance "
            "and available balance, noting any difference due to pending transactions"
        ),
        tools=[get_account_balance],
    )

    await agent.create_guideline(
        condition="The customer asks about recent transactions or wants to review their account activity",
        action=(
            "Fetch their recent transactions and present them clearly, "
            "helping identify any unfamiliar transactions if needed"
        ),
        tools=[get_recent_transactions],
    )

    await agent.create_guideline(
        condition="The customer doesn't recognize a transaction",
        action=(
            "Help them identify it by providing the date, merchant name, and amount. "
            "Explain that merchant names may appear differently than expected. "
            "If still unrecognized, offer to help file a dispute"
        ),
    )

    # ========================================================================
    # TRANSACTION AND TRANSFER GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="The customer wants to transfer money between their accounts",
        action=(
            "Confirm the source account, destination account, and amount. "
            "Then process the transfer and provide confirmation"
        ),
        tools=[initiate_transfer],
    )

    # ========================================================================
    # CARD SERVICES GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="The customer reports their card as lost or stolen",
        action=(
            "Act immediately: confirm the card type, block it to prevent unauthorized use, "
            "order a replacement card, provide expected delivery timeframe, "
            "and inform them about temporary card availability at branches"
        ),
        tools=[report_card_lost_stolen],
    )

    # ========================================================================
    # FRAUD AND DISPUTE GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="The customer reports unauthorized or fraudulent transactions",
        action=(
            "Take this seriously and act immediately. Gather transaction details, "
            "file a fraud claim, explain their Regulation E rights (zero liability), "
            "explain the investigation timeline, and mention temporary credit while investigating"
        ),
        tools=[dispute_transaction],
    )

    await agent.create_guideline(
        condition="The customer wants to dispute a transaction but it's not fraud",
        action=(
            "Help them file an appropriate dispute claim for the incorrect amount, duplicate charge, "
            "or merchant issue. Explain the investigation process and timeline"
        ),
        tools=[dispute_transaction],
    )

    # ========================================================================
    # FEE-RELATED GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="The customer complains about a fee and wants it reversed",
        action=(
            "Show understanding, explain why the fee occurred, check reversal eligibility, "
            "and if eligible process the courtesy reversal. Also provide guidance on avoiding future fees"
        ),
        tools=[check_fee_reversal_eligibility],
    )

    # ========================================================================
    # SECURITY AND EDUCATION GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="The customer mentions receiving suspicious emails, texts, or calls claiming to be from the bank",
        action=(
            "Warn them this is likely phishing. Explain that the bank never asks for full passwords, PINs, "
            "or SSN via email/text/unsolicited calls. Advise them not to click links or provide information. "
            "Tell them to call the bank directly using the number on their card if they have concerns"
        ),
    )

    # ========================================================================
    # JOURNEY: ACCOUNT OPENING
    # ========================================================================

    account_opening = await agent.create_journey(
        title="Open New Account",
        description="Guides customer through opening a new checking or savings account",
        conditions=["The customer wants to open a new account"],
    )

    t0 = await account_opening.initial_state.transition_to(
        chat_state="Ask what type of account they want to open (checking, savings, or both)"
    )

    t1 = await t0.target.transition_to(
        chat_state="Explain the account features, benefits, monthly fees, and minimum balance requirements"
    )

    t2 = await t1.target.transition_to(
        chat_state="Explain required documentation (ID, SSN, proof of address) and initial deposit requirements"
    )

    t3 = await t2.target.transition_to(
        chat_state=(
            "Ask if they'd like to proceed. If yes, inform them they can complete the application "
            "online, by phone, or at a branch, and offer to help with next steps. If no, ask if they have questions"
        )
    )

    await t3.target.transition_to(state=p.END_JOURNEY)

    # ========================================================================
    # JOURNEY: FRAUD INVESTIGATION
    # ========================================================================

    fraud_investigation = await agent.create_journey(
        title="Fraud Investigation",
        description="Handles suspected fraud with urgency and thoroughness",
        conditions=["The customer reports suspected fraud or unauthorized account activity"],
    )

    f0 = await fraud_investigation.initial_state.transition_to(
        chat_state=(
            "Acknowledge the urgency and assure the customer you'll help immediately. "
            "Ask them to identify the suspicious transactions"
        )
    )

    f1 = await f0.target.transition_to(
        chat_state=(
            "Ask key questions: Do they have their card in their possession? "
            "Have they shared account information with anyone recently? "
            "Have they noticed any other unusual activity?"
        )
    )

    f2 = await f1.target.transition_to(
        chat_state="If card-related fraud, immediately block the affected card(s) for their security",
        condition="The fraud involves a debit or credit card",
    )

    f3 = await f2.target.transition_to(
        chat_state="File a formal fraud dispute claim for the unauthorized transactions",
    )

    f4 = await f3.target.transition_to(
        chat_state=(
            "Explain their rights under Regulation E: zero liability for unauthorized transactions. "
            "Explain temporary credit will be issued in 2-3 business days while investigating. "
            "Provide the claim number for their records"
        )
    )

    f5 = await f4.target.transition_to(
        chat_state=(
            "Educate about fraud prevention: never share passwords/PINs, watch for phishing, "
            "use strong online banking passwords, enable account alerts. "
            "Provide direct callback number for any questions"
        )
    )

    await f5.target.transition_to(state=p.END_JOURNEY)

    print(f"✓ Customer Service Agent '{agent.name}' created with guidelines and journeys")
    return agent


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main() -> None:
    """Initialize the Parlant server and create the customer service agent."""

    async with p.Server() as server:
        agent = await create_customer_service_agent(server)

        print(f"\nAgent ready!")
        print(f"Agent ID: {agent.id}")
        print(
            f"Agent Description: {agent.description}\n"
        )

        # In production, the server would continue running and handling requests
        # This is just a setup script
        print(
            "Agent configured successfully. In production, this would be "
            "a long-running service handling customer interactions."
        )


if __name__ == "__main__":
    asyncio.run(main())
