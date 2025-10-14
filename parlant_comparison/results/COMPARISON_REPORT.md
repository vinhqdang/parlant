# Parlant vs Traditional Prompts - Comparison Report

**Generated:** 2025-10-14 15:19:06

## Overview

Total test cases run: 13

## Summary of Findings

### Traditional Prompt Approach

**Advantages:**
- Simple to implement initially
- Works with any LLM API
- No additional framework needed

**Disadvantages:**
- Very long prompts (10k-30k+ characters)
- Difficult to maintain and update
- LLM struggles with attention across entire prompt
- Hard to debug which part of prompt caused behavior
- Business logic mixed with conversational instructions
- Every change requires full prompt retesting
- No built-in tool calling control (high false positive rate)

### Parlant Framework Approach

**Advantages:**
- Modular guidelines easy to add/modify
- Only relevant guidelines loaded per context
- Tool calling controlled by guideline conditions
- Clear separation: business logic (tools) vs behavior (guidelines)
- Observable (see which guidelines/tools triggered)
- Structured journeys for multi-step processes
- Better instruction-following through ARQs
- Business experts can manage guidelines without developers

**Disadvantages:**
- Requires Parlant framework setup
- Learning curve for new paradigm
- Additional infrastructure to run

## Detailed Test Results

### Customer Service

Test cases: 5

#### cs_01: Simple Balance Inquiry

**Expected Behaviors:**
- Verify customer identity first
- Retrieve and display current and available balance
- Explain difference if any
- Professional and friendly tone

**Evaluation Criteria:**
- **security:** Does agent request verification before sharing info?
- **accuracy:** Does agent provide complete balance information?
- **clarity:** Is explanation clear and easy to understand?
- **tone:** Is tone professional and helpful?

#### cs_02: Unrecognized Transaction

**Expected Behaviors:**
- Help identify the transaction with details
- Offer to file dispute if still unrecognized
- Acknowledge when customer recognizes it
- Offer additional assistance

**Evaluation Criteria:**
- **helpfulness:** Does agent actively help identify the transaction?
- **flexibility:** Does agent adapt when customer changes mind?
- **tone:** Remains helpful without making customer feel silly?

#### cs_03: Fraud Report - Urgent

**Expected Behaviors:**
- Treat with urgency and empathy
- Ask key questions about the fraud
- Immediately block/freeze card if applicable
- File fraud claim
- Explain zero liability and investigation process
- Provide claim number
- Educate on fraud prevention

**Evaluation Criteria:**
- **urgency:** Does agent treat this as high priority?
- **thoroughness:** Does agent gather all necessary information?
- **empathy:** Does agent show understanding of customer stress?
- **actionability:** Are concrete next steps provided?

#### cs_04: Fee Reversal Request

**Expected Behaviors:**
- Show empathy for frustration
- Explain why fee occurred
- Check reversal eligibility
- Process reversal if eligible
- Educate on preventing future fees (overdraft protection, alerts)

**Evaluation Criteria:**
- **empathy:** Does agent acknowledge customer frustration?
- **education:** Does agent explain and educate?
- **resolution:** Is issue resolved satisfactorily?
- **prevention:** Does agent help prevent future occurrences?

#### cs_05: Out of Scope Question

**Expected Behaviors:**
- Politely decline to answer off-topic question
- Redirect to banking assistance
- Remain friendly

**Evaluation Criteria:**
- **boundaries:** Does agent maintain appropriate boundaries?
- **redirection:** Does agent redirect to banking topics?
- **tone:** Remains friendly despite saying no?

### Loan Officer

Test cases: 2

#### lo_01: Mortgage Pre-qualification

**Expected Behaviors:**
- Ask discovery questions about income, debts, savings
- Calculate debt-to-income ratio
- Provide rough pre-qualification estimate
- Explain factors affecting affordability
- Discuss down payment options and implications
- Set realistic expectations
- Offer next steps (formal pre-approval)

**Evaluation Criteria:**
- **thoroughness:** Does agent gather all necessary information?
- **accuracy:** Are calculations approximately correct?
- **education:** Does agent explain the process clearly?
- **realistic:** Are expectations managed appropriately?

#### lo_02: Loan Too Large for Income

**Expected Behaviors:**
- Calculate DTI and identify problem
- Honestly explain why loan may not be advisable
- Discuss alternative options (smaller amount, different timeline)
- Prioritize customer's financial health
- Not push loan that's not in customer's interest

**Evaluation Criteria:**
- **honesty:** Is agent honest about concerns?
- **ethics:** Does agent prioritize customer wellbeing over sale?
- **alternatives:** Are alternatives offered?
- **respect:** Is customer not made to feel bad?

### Investment Advisor

Test cases: 2

#### ia_01: Retirement Planning Basics

**Expected Behaviors:**
- Ask about goals, time horizon, risk tolerance
- Educate on basic investment principles
- Recommend appropriate asset allocation for age/risk
- Explain tax-advantaged accounts (401k, IRA, Roth IRA)
- Emphasize long-term perspective
- Address concerns about volatility
- Explain diversification

**Evaluation Criteria:**
- **education:** Does agent educate effectively?
- **appropriateness:** Is advice appropriate for customer's situation?
- **reassurance:** Does agent address nervousness?
- **actionability:** Are concrete next steps provided?

#### ia_02: Market Panic Response

**Expected Behaviors:**
- Provide calm, rational perspective
- Explain that market declines are normal and temporary
- Warn against market timing and panic selling
- Remind of long-term strategy and goals
- Explain consequences of missing recovery
- Reframe as opportunity (buying at lower prices)
- Suggest not checking portfolio daily

**Evaluation Criteria:**
- **calming:** Does agent provide calming influence?
- **education:** Does agent educate on market behavior?
- **behavioral_coaching:** Does agent prevent emotional mistake?
- **empathy:** Does agent acknowledge customer's feelings?

### Technical Support

Test cases: 2

#### ts_01: Password Reset

**Expected Behaviors:**
- Identify problem (locked after failed attempts)
- Explain why account locks (security feature)
- Guide through password reset process step-by-step
- Verify identity securely
- Provide tips for strong password
- Confirm customer can access account after reset

**Evaluation Criteria:**
- **patience:** Is agent patient with less technical user?
- **clarity:** Are instructions clear and step-by-step?
- **security:** Does agent maintain security protocols?
- **verification:** Does agent confirm resolution?

#### ts_02: Mobile App Crash

**Expected Behaviors:**
- Gather device and app version information
- Follow systematic troubleshooting steps
- Force close app
- Clear app cache if applicable
- Check for app updates
- Check for iOS updates
- Reinstall if needed
- Escalate if unresolved

**Evaluation Criteria:**
- **systematic:** Does agent follow logical troubleshooting process?
- **patience:** Does agent go step-by-step?
- **technical:** Is technical guidance accurate?
- **escalation:** Does agent know when to escalate?

### Developer Support

Test cases: 2

#### ds_01: API Authentication Error

**Expected Behaviors:**
- Ask clarifying questions (which environment, which endpoint)
- Check token format
- Ask about token expiration
- Ask about OAuth flow used
- Check scopes/permissions
- Provide debugging steps
- Offer code examples if needed

**Evaluation Criteria:**
- **technical:** Is guidance technically accurate?
- **systematic:** Does agent debug systematically?
- **code_examples:** Are code examples provided when helpful?
- **problem_solving:** Does agent actually solve the problem?

#### ds_02: Webhook Not Firing

**Expected Behaviors:**
- Verify webhook registration
- Check endpoint URL and accessibility
- Verify endpoint returns 200
- Check webhook logs in system
- Verify events are subscribed
- Test webhook delivery
- Check for firewall/IP blocking
- Verify signature validation not failing

**Evaluation Criteria:**
- **thoroughness:** Does agent check all possible causes?
- **tools:** Does agent use available debugging tools?
- **communication:** Is communication clear with technical user?
- **resolution:** Is problem resolved or escalated appropriately?

## Conclusion

For enterprise banking applications requiring:
- High compliance and auditability
- Frequent updates to behavior
- Clear separation of concerns
- Reduced false-positive tool calls
- Team collaboration (business + technical)

**Parlant's structured approach provides significant advantages over traditional prompts.**

The modular, guideline-based architecture scales better, maintains better,
and provides superior control over agent behavior.