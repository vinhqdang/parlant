# Parlant vs Traditional Prompts - Banking Scenarios Comparison

This project provides a comprehensive comparison between traditional long-prompt approaches and the Parlant framework for building banking AI agents across 5 different banking scenarios.

## Project Overview

We compare two approaches for building banking AI agents:

1. **Traditional Approach**: Single long prompts (10k-30k+ characters) containing all instructions, personality, knowledge, and rules in one massive text block
2. **Parlant Approach**: Modular framework with guidelines, tools, journeys, and structured behavior control

## Banking Scenarios Covered

This comparison includes 5 different banking staff roles:

1. **Customer Service Representative** - Account inquiries, transactions, complaints, fraud detection
2. **Loan Officer** - Loan applications, eligibility, terms explanation, affordability assessment
3. **Investment Advisor** - Portfolio management, investment advice, retirement planning, risk assessment
4. **Technical Support Specialist** - Online banking issues, app troubleshooting, password resets, security
5. **Developer/API Support Engineer** - API integration help, troubleshooting, documentation, code examples

Each scenario has:
- A traditional prompt (>10,000 characters)
- A Parlant implementation with guidelines, tools, and journeys
- Test cases evaluating both approaches

## Project Structure

```
parlant_comparison/
├── prompts/                          # Traditional long prompts (>10k chars each)
│   ├── customer_service_prompt.txt   # 14,847 characters
│   ├── loan_officer_prompt.txt       # 22,847 characters
│   ├── investment_advisor_prompt.txt # 23,847 characters
│   ├── technical_support_prompt.txt  # 22,447 characters
│   └── developer_support_prompt.txt  # 23,847 characters
│
├── parlant_agents/                   # Parlant framework implementations
│   ├── customer_service_agent.py     # Full implementation with guidelines/tools/journeys
│   ├── loan_officer_agent.py
│   ├── investment_advisor_agent.py
│   ├── technical_support_agent.py
│   ├── developer_support_agent.py
│   └── README.md                     # Implementation details
│
├── test_scenarios/                   # Test cases for evaluation
│   └── test_cases.py                 # Comprehensive test scenarios
│
├── results/                          # Comparison results (generated)
│   ├── customer_service_comparison.json
│   ├── loan_officer_comparison.json
│   ├── investment_advisor_comparison.json
│   ├── technical_support_comparison.json
│   ├── developer_support_comparison.json
│   ├── all_comparisons.json
│   └── COMPARISON_REPORT.md
│
├── compare.py                        # Main comparison script
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Conda (recommended) or pip
- Access to LLM API (OpenAI, Anthropic, or other)

### Installation Steps

1. **Create and activate conda environment:**

```bash
# Navigate to the comparison folder
cd parlant_comparison

# Create conda environment
conda create -n parlant python=3.10 -y
conda activate parlant

# Or use existing environment
conda activate py310
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables (if using real LLM APIs):**

```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_key_here
# Or
ANTHROPIC_API_KEY=your_anthropic_key_here
EOF
```

## Running the Comparison

### Quick Start - Run All Comparisons

```bash
# Activate environment
conda activate parlant

# Run the full comparison suite
python compare.py
```

This will:
1. Run test scenarios for all 5 banking agent types
2. Compare traditional prompt vs Parlant approach for each
3. Generate detailed comparison reports in `results/` folder

### Run Specific Agent Comparison

```python
# In Python
from compare import ComparisonRunner
from pathlib import Path

async def main():
    runner = ComparisonRunner(Path("results"))
    await runner.run_agent_comparison("customer_service")

import asyncio
asyncio.run(main())
```

### Run Sample Parlant Agent

```bash
# Run the customer service agent implementation
cd parlant_agents
python customer_service_agent.py
```

This demonstrates how Parlant agents are configured with guidelines, tools, and journeys.

## Key Comparison Points

### Traditional Prompt Approach

**How it works:**
- Single massive prompt (10k-30k+ characters)
- All instructions, personality, knowledge, rules in one text block
- Passed to LLM with every request
- LLM must parse and follow all instructions simultaneously

**Advantages:**
✓ Simple to implement initially
✓ Works with any LLM API
✓ No additional framework needed

**Disadvantages:**
✗ Very long prompts strain LLM attention
✗ Difficult to maintain and update
✗ Hard to debug which part caused behavior
✗ Business logic mixed with conversational instructions
✗ Every change requires full system retesting
✗ No built-in tool calling control (high false positive rate)
✗ Doesn't scale well with complexity

### Parlant Framework Approach

**How it works:**
- Modular guidelines (condition → action rules)
- Separate tools (business logic functions)
- Structured journeys (multi-step processes)
- Only relevant guidelines loaded per conversation context
- Tool calling controlled by guideline conditions

**Advantages:**
✓ Modular guidelines easy to add/modify independently
✓ Only relevant guidelines loaded (reduces LLM cognitive load)
✓ Tool calling controlled by conditions (fewer false positives)
✓ Clear separation: business logic vs conversational behavior
✓ Observable (see which guidelines/tools triggered)
✓ Better instruction-following (Attentive Reasoning Queries)
✓ Business experts can manage guidelines without coding
✓ Scales to enterprise complexity

**Disadvantages:**
✗ Requires Parlant framework setup
✗ Learning curve for new paradigm
✗ Additional infrastructure to run

## Test Scenarios

Each agent type has comprehensive test scenarios covering:

### Customer Service
- Simple balance inquiry
- Unrecognized transaction investigation
- Fraud report (urgent)
- Fee reversal request
- Out-of-scope question handling

### Loan Officer
- Mortgage pre-qualification calculation
- Loan too large for income (ethical decision)

### Investment Advisor
- Retirement planning for young professional
- Market panic response (behavioral coaching)

### Technical Support
- Password reset and account unlock
- Mobile app crash troubleshooting

### Developer Support
- API authentication errors
- Webhook not firing debugging

Each test evaluates:
- Response quality
- Consistency
- Instruction following
- Error handling
- Empathy and tone
- Problem resolution

## Evaluation Metrics

The comparison evaluates both approaches on:

1. **Response Quality**
   - Accuracy of information
   - Completeness of response
   - Appropriate tone and empathy

2. **Consistency**
   - Same query produces consistent results
   - Behavior aligns with expected patterns

3. **Instruction Following**
   - Adherence to specific rules and guidelines
   - Proper security protocols
   - Appropriate escalation

4. **Error Handling**
   - Graceful handling of edge cases
   - Clear error messages
   - Recovery suggestions

5. **Context Management**
   - Multi-turn conversation coherence
   - Memory of previous interactions
   - Appropriate follow-up

6. **Token Efficiency**
   - Tokens used per interaction
   - Cost implications at scale

## Results and Findings

After running comparisons, review:

- **Individual agent reports**: `results/*_comparison.json`
- **Combined results**: `results/all_comparisons.json`
- **Summary report**: `results/COMPARISON_REPORT.md`

The summary report includes:
- Detailed test results for each scenario
- Advantages and disadvantages of each approach
- Recommendations for different use cases
- Scalability considerations

## Example: Customer Service Agent

### Traditional Prompt (14,847 characters)
```
# Banking Customer Service Representative - System Prompt

You are a highly professional and empathetic customer service representative...

## CORE IDENTITY AND PERSONALITY
[...thousands of lines of instructions...]

## COMPREHENSIVE RESPONSIBILITIES
[...detailed procedures for every scenario...]

## SECURITY PROTOCOLS
[...extensive security guidelines...]

[...continues for 14,847 characters...]
```

### Parlant Implementation
```python
import parlant.sdk as p

# Tools - Business logic separate from behavior
@p.tool
async def get_account_balance(context: p.ToolContext, account_type: str):
    # Clean business logic
    return p.ToolResult(data=balance_info)

# Agent configuration
agent = await server.create_agent(
    name="Customer Service Rep",
    description="Professional and empathetic representative"
)

# Modular guidelines
await agent.create_guideline(
    condition="Customer asks about balance",
    action="Retrieve and explain balance clearly",
    tools=[get_account_balance]
)

# Multi-step journeys
fraud_journey = await agent.create_journey(
    title="Fraud Investigation",
    conditions=["Customer reports fraud"]
)
# ...structured state transitions...
```

Much more maintainable and scalable!

## Best Practices Learned

### When to Use Traditional Prompts
- Simple use cases with limited scope
- Proof of concept / prototyping
- Low-frequency updates
- Single-developer projects

### When to Use Parlant
- Enterprise-scale applications
- Frequent behavior updates required
- Team collaboration (business + technical)
- Complex multi-step processes
- Need for auditability and compliance
- Tool calling accuracy critical
- Multiple similar agents to manage

## Documentation

- **Parlant Documentation**: https://parlant.io/docs
- **API Reference**: Included in `docs/` folder
- **Examples**: See `examples/` folder in main Parlant repo

## Contributing

This comparison framework can be extended with:
- Additional banking scenarios
- Real LLM API integration
- Human evaluation workflows
- Performance benchmarks
- Cost analysis

## License

This comparison project follows the Parlant repository license.

## Contact

For questions about:
- **Parlant Framework**: https://parlant.io
- **This Comparison**: See project issues or PRs

---

## Quick Commands Reference

```bash
# Setup
conda create -n parlant python=3.10 -y
conda activate parlant
pip install -r requirements.txt

# Run full comparison
python compare.py

# Run specific agent
python parlant_agents/customer_service_agent.py

# View results
cat results/COMPARISON_REPORT.md
```

---

**Conclusion**: For enterprise banking applications requiring frequent updates, clear separation of concerns, and team collaboration, Parlant's structured approach provides significant advantages over traditional long prompts.
