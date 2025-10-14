# Parlant Agent Implementations

This directory contains Parlant-based implementations of the 5 banking scenarios.

## Key Advantages of Parlant Over Long Prompts

### 1. **Modularity and Maintainability**
- **Tools**: Business logic is separated into discrete, testable functions
- **Guidelines**: Behavioral rules are independent and can be added/modified without affecting others
- **Journeys**: Multi-step processes are explicitly modeled with state transitions

### 2. **Contextual Guidance**
- Parlant dynamically loads only relevant guidelines based on conversation context
- Reduces "cognitive load" on the LLM
- Better instruction-following through Attentive Reasoning Queries (ARQs)

### 3. **Tool Control**
- Tools only execute when associated guideline conditions are met
- Reduces false-positive tool calls (major LLM problem)
- Contextual tool parameterization

### 4. **Scalability**
- Easy to add new guidelines without re-testing entire system
- Guidelines can be managed by business experts (not just developers)
- Clear separation of concerns

### 5. **Debugging and Monitoring**
- Can see which guidelines triggered for each response
- Tool call history is tracked
- Journey state transitions are observable

## Agent Implementations

All 5 agents are **fully implemented** with complete tools, guidelines, and journeys:

### 1. customer_service_agent.py
- Tools for balance checking, transfers, card management, disputes
- Guidelines for various customer service scenarios
- Journeys for account opening and fraud investigation
- Security and compliance considerations

### 2. loan_officer_agent.py
- Tools for DTI calculation, mortgage affordability, payment calculations
- Guidelines for ethical lending and customer financial health
- Journey for comprehensive mortgage pre-qualification
- First-time homebuyer education

### 3. investment_advisor_agent.py
- Tools for retirement planning, asset allocation, investment growth projection
- Guidelines for behavioral coaching during market volatility
- Journey for comprehensive retirement planning
- Risk tolerance assessment and diversification strategies

### 4. technical_support_agent.py
- Tools for password resets, account unlocking, system troubleshooting
- Guidelines for patient, step-by-step technical support
- Journeys for password reset and mobile app troubleshooting
- Platform-specific guidance (iOS, Android, web browsers)

### 5. developer_support_agent.py
- Tools for API authentication, webhook debugging, error explanations
- Guidelines for systematic API debugging and code samples
- Journeys for OAuth setup and API error debugging
- Technical documentation and code generation

## Usage Pattern

All agents follow this structure:

```python
import parlant.sdk as p

# 1. Define tools (business logic)
@p.tool
async def my_tool(context: p.ToolContext, param: str) -> p.ToolResult:
    # ... implementation
    return p.ToolResult(data=result)

# 2. Create agent
async def create_agent(server: p.Server) -> p.Agent:
    agent = await server.create_agent(
        name="Agent Name",
        description="Agent personality and role"
    )

    # 3. Add domain glossary
    await agent.create_term(
        name="Term",
        description="Definition"
    )

    # 4. Add guidelines
    await agent.create_guideline(
        condition="When this happens",
        action="Do this",
        tools=[my_tool]  # Optional
    )

    # 5. Create journeys for multi-step processes
    journey = await agent.create_journey(
        title="Process Name",
        description="What this process does",
        conditions=["When to start this journey"]
    )

    return agent
```

## Comparison Metrics

The comparison script evaluates:

1. **Response Quality**: Accuracy, completeness, tone
2. **Consistency**: Same query multiple times
3. **Instruction Following**: Adherence to specific rules
4. **Error Handling**: How errors are managed
5. **Context Management**: How well context is maintained
6. **Token Efficiency**: Tokens used per interaction
