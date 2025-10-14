"""
Premier Global Bank - Developer Support Agent (Parlant Implementation)

Assists developers with API integration, troubleshooting, and technical questions.
"""

import asyncio
from typing import Optional
import parlant.sdk as p


# ============================================================================
# TOOLS - Developer support tools
# ============================================================================

@p.tool
async def check_api_credentials(
    context: p.ToolContext,
    client_id: str
) -> p.ToolResult:
    """
    Verify API credentials status.

    Args:
        client_id: OAuth client ID
    """
    return p.ToolResult(
        data={
            "client_id": client_id,
            "status": "active",
            "environment": "sandbox",
            "scopes": ["accounts:read", "transactions:read", "transfers:write"],
            "rate_limit": "100 requests/minute",
            "last_used": "2024-10-14 09:30:00"
        }
    )


@p.tool
async def validate_token(
    context: p.ToolContext,
    token_prefix: str
) -> p.ToolResult:
    """
    Validate and inspect access token (partial).

    Args:
        token_prefix: First few characters of the token for identification
    """
    # In production, this would do actual token introspection
    return p.ToolResult(
        data={
            "token_valid": True,
            "expires_in": 3600,
            "scopes": ["accounts:read", "transactions:read"],
            "issued_at": "2024-10-14 10:00:00",
            "client_id": "client_abc123",
            "token_type": "Bearer"
        }
    )


@p.tool
async def get_api_endpoint_info(
    context: p.ToolContext,
    endpoint: str
) -> p.ToolResult:
    """
    Get information about a specific API endpoint.

    Args:
        endpoint: API endpoint path (e.g., /v1/accounts)
    """
    endpoints = {
        "/v1/accounts": {
            "method": "GET",
            "description": "List customer accounts",
            "required_scope": "accounts:read",
            "authentication": "Bearer token in Authorization header",
            "rate_limit": "100/minute",
            "response_format": "JSON",
            "common_errors": {
                "401": "Invalid or expired token",
                "403": "Insufficient scope",
                "429": "Rate limit exceeded"
            }
        },
        "/v1/transactions": {
            "method": "GET",
            "description": "List account transactions",
            "required_scope": "transactions:read",
            "authentication": "Bearer token in Authorization header",
            "rate_limit": "100/minute",
            "parameters": ["account_id", "from_date", "to_date", "limit"],
            "response_format": "JSON"
        }
    }

    endpoint_info = endpoints.get(endpoint, {
        "error": "Endpoint not found",
        "suggestion": "Check API documentation for available endpoints"
    })

    return p.ToolResult(
        data={
            "endpoint": endpoint,
            "details": endpoint_info
        }
    )


@p.tool
async def check_webhook_status(
    context: p.ToolContext,
    webhook_id: str
) -> p.ToolResult:
    """
    Check webhook registration and delivery status.

    Args:
        webhook_id: Webhook registration ID
    """
    return p.ToolResult(
        data={
            "webhook_id": webhook_id,
            "url": "https://example.com/webhooks/bank",
            "status": "active",
            "events": ["transaction.created", "account.updated"],
            "last_delivery": "2024-10-14 09:45:00",
            "last_delivery_status": "200 OK",
            "failed_deliveries_24h": 0,
            "next_retry": "N/A"
        }
    )


@p.tool
async def get_error_code_explanation(
    context: p.ToolContext,
    error_code: str
) -> p.ToolResult:
    """
    Explain API error codes and provide solutions.

    Args:
        error_code: HTTP status code or API error code
    """
    explanations = {
        "401": {
            "meaning": "Unauthorized - Authentication failed",
            "common_causes": [
                "Missing Authorization header",
                "Expired access token",
                "Invalid token format",
                "Token not yet valid"
            ],
            "solutions": [
                "Ensure Authorization header is present: 'Authorization: Bearer YOUR_TOKEN'",
                "Refresh your access token if expired",
                "Verify token format (Bearer scheme)",
                "Check system clock is accurate"
            ]
        },
        "403": {
            "meaning": "Forbidden - Insufficient permissions",
            "common_causes": [
                "Missing required OAuth scope",
                "Accessing resource outside permissions",
                "API key restrictions"
            ],
            "solutions": [
                "Verify your token has required scopes",
                "Re-authenticate with correct scopes",
                "Check resource ownership/access rights"
            ]
        },
        "429": {
            "meaning": "Too Many Requests - Rate limit exceeded",
            "common_causes": [
                "Too many API calls in short time",
                "Not implementing rate limit headers",
                "Multiple clients using same credentials"
            ],
            "solutions": [
                "Implement exponential backoff retry logic",
                "Check Rate-Limit headers in responses",
                "Cache responses where appropriate",
                "Consider pagination instead of bulk requests"
            ]
        }
    }

    explanation = explanations.get(error_code, {
        "meaning": "Unknown error code",
        "solution": "Check API documentation or provide more details"
    })

    return p.ToolResult(
        data={
            "error_code": error_code,
            "explanation": explanation
        }
    )


@p.tool
async def generate_code_sample(
    context: p.ToolContext,
    language: str,
    operation: str
) -> p.ToolResult:
    """
    Generate code sample for common operations.

    Args:
        language: Programming language (python, javascript, java, curl)
        operation: Operation to demonstrate (auth, list_accounts, create_transfer)
    """
    samples = {
        "python": {
            "auth": """
import requests

# OAuth 2.0 Authorization Code Flow
auth_url = "https://auth.premierbank.com/oauth/authorize"
token_url = "https://auth.premierbank.com/oauth/token"

# Step 1: Get authorization code (redirect user to auth_url)
# Step 2: Exchange code for token
response = requests.post(token_url, data={
    'grant_type': 'authorization_code',
    'code': 'AUTHORIZATION_CODE',
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'redirect_uri': 'YOUR_REDIRECT_URI'
})

token_data = response.json()
access_token = token_data['access_token']
""",
            "list_accounts": """
import requests

access_token = "YOUR_ACCESS_TOKEN"
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.premierbank.com/v1/accounts',
    headers=headers
)

accounts = response.json()
print(accounts)
"""
        },
        "curl": {
            "list_accounts": """
curl -X GET https://api.premierbank.com/v1/accounts \\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \\
  -H "Content-Type: application/json"
"""
        }
    }

    lang_samples = samples.get(language, {})
    code = lang_samples.get(operation, "# Sample not available for this combination")

    return p.ToolResult(
        data={
            "language": language,
            "operation": operation,
            "code_sample": code
        }
    )


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

async def create_developer_support_agent(server: p.Server) -> p.Agent:
    """Create and configure the developer support agent."""

    agent = await server.create_agent(
        name="Premier Developer Support Engineer",
        description=(
            "A highly technical support engineer who assists developers with API integration, "
            "OAuth flows, webhook setup, and troubleshooting. Provides code samples and "
            "systematic debugging guidance."
        ),
    )

    # ========================================================================
    # GLOSSARY
    # ========================================================================

    await agent.create_term(
        name="OAuth 2.0",
        description="Industry-standard protocol for authorization, used to securely access APIs",
    )

    await agent.create_term(
        name="Bearer Token",
        description="Access token passed in Authorization header as 'Bearer YOUR_TOKEN'",
    )

    await agent.create_term(
        name="Scope",
        description="Permissions granted to an access token (e.g., accounts:read, transfers:write)",
    )

    await agent.create_term(
        name="Webhook",
        description="HTTP callback that sends real-time event notifications to your server",
    )

    await agent.create_term(
        name="Rate Limiting",
        description="Restriction on number of API requests per time period to ensure fair usage",
    )

    # ========================================================================
    # CORE GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Starting a conversation",
        action=(
            "Greet professionally and ask about their integration challenge or technical issue. "
            "Ask which environment (sandbox/production) and what endpoint/operation they're working with"
        ),
    )

    await agent.create_guideline(
        condition="Developer describes a technical problem",
        action=(
            "Use systematic debugging approach: gather specifics (error messages, request IDs, timestamps), "
            "verify credentials, check token validity, review request format, examine response codes"
        ),
    )

    await agent.create_guideline(
        condition="Developer is stuck on implementation",
        action=(
            "Provide concrete code examples in their preferred language. "
            "Explain the concept clearly. Link to relevant documentation. "
            "Offer to walk through step-by-step"
        ),
    )

    # ========================================================================
    # AUTHENTICATION ISSUES
    # ========================================================================

    await agent.create_guideline(
        condition="Developer getting 401 authentication errors",
        action=(
            "Systematically debug: verify Authorization header format, "
            "check token expiration, verify token scopes, validate OAuth flow. "
            "Explain error and provide solutions"
        ),
        tools=[validate_token, get_error_code_explanation, generate_code_sample],
    )

    await agent.create_guideline(
        condition="Developer asks about OAuth implementation",
        action=(
            "Explain OAuth 2.0 Authorization Code flow step-by-step. "
            "Provide code samples for their language. "
            "Clarify difference between authorization code and access token. "
            "Explain token refresh process"
        ),
        tools=[generate_code_sample],
    )

    await agent.create_guideline(
        condition="Developer has token scope or permissions issues",
        action=(
            "Explain OAuth scopes required for their use case. "
            "Show how to request correct scopes during authorization. "
            "Verify their token has needed scopes"
        ),
        tools=[validate_token, get_api_endpoint_info],
    )

    # ========================================================================
    # API USAGE GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Developer asks about specific API endpoint",
        action=(
            "Provide endpoint documentation: HTTP method, authentication requirements, "
            "required parameters, response format, rate limits. "
            "Offer code sample if helpful"
        ),
        tools=[get_api_endpoint_info, generate_code_sample],
    )

    await agent.create_guideline(
        condition="Developer getting rate limit errors (429)",
        action=(
            "Explain rate limiting and current limits. "
            "Provide best practices: implement exponential backoff, respect Rate-Limit headers, "
            "cache when possible, use webhooks instead of polling"
        ),
        tools=[get_error_code_explanation],
    )

    # ========================================================================
    # WEBHOOK GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Developer not receiving webhook events",
        action=(
            "Systematically troubleshoot: verify webhook registration, "
            "check URL accessibility, verify endpoint returns 200 OK, "
            "check webhook logs for delivery attempts, verify event subscriptions, "
            "check for firewall/security blocking"
        ),
        tools=[check_webhook_status],
    )

    await agent.create_guideline(
        condition="Developer asks how to set up webhooks",
        action=(
            "Explain webhook registration process, endpoint requirements (HTTPS, return 200 OK), "
            "event types available, retry logic, signature verification for security. "
            "Provide code sample for webhook handler"
        ),
        tools=[generate_code_sample],
    )

    # ========================================================================
    # DEBUGGING AND ERRORS
    # ========================================================================

    await agent.create_guideline(
        condition="Developer shares an error code or error message",
        action=(
            "Explain what the error means, common causes, and specific solutions. "
            "Ask for additional context if needed (request ID, timestamp, full error response). "
            "Provide debugging steps"
        ),
        tools=[get_error_code_explanation],
    )

    # ========================================================================
    # JOURNEY: API AUTHENTICATION SETUP
    # ========================================================================

    auth_setup = await agent.create_journey(
        title="API Authentication Setup",
        description="Guide developer through OAuth setup",
        conditions=["Developer needs help setting up API authentication"],
    )

    a1 = await auth_setup.initial_state.transition_to(
        chat_state="Confirm they have registered their application and have client_id and client_secret",
    )

    a2 = await a1.target.transition_to(
        chat_state="Explain OAuth 2.0 Authorization Code flow: authorize URL, redirect, token exchange",
    )

    a3 = await a2.target.transition_to(
        chat_state="Ask their programming language preference and provide code sample for OAuth flow",
    )

    a4 = await a3.target.transition_to(
        chat_state="Explain token usage: include in Authorization header as 'Bearer TOKEN'",
    )

    a5 = await a4.target.transition_to(
        chat_state="Explain token expiration (1 hour) and refresh token process",
    )

    a6 = await a5.target.transition_to(
        chat_state="Verify they understand scopes needed for their use case",
    )

    a7 = await a6.target.transition_to(
        chat_state=(
            "Recommend testing in sandbox first. "
            "Provide sandbox endpoint URLs. "
            "Offer to help with any errors they encounter"
        ),
    )

    await a7.target.transition_to(state=p.END_JOURNEY)

    # ========================================================================
    # JOURNEY: API ERROR Debugging
    # ========================================================================

    error_debug = await agent.create_journey(
        title="API Error Debugging",
        description="Systematic API error debugging",
        conditions=["Developer is getting API errors"],
    )

    e1 = await error_debug.initial_state.transition_to(
        chat_state="Ask for specific error: status code, error message, request ID, timestamp",
    )

    e2 = await e1.target.transition_to(
        chat_state="Explain what the error means",
    )

    e3 = await e2.target.transition_to(
        chat_state="For auth errors: verify token format, check expiration, validate scopes",
        condition="Error is 401 or 403",
    )

    e4 = await e3.target.transition_to(
        chat_state="Ask them to verify request format matches documentation",
    )

    e5 = await e4.target.transition_to(
        chat_state=(
            "If issue persists, ask for sanitized request/response for deeper investigation. "
            "Provide ticket number if escalation needed"
        ),
    )

    await e5.target.transition_to(state=p.END_JOURNEY)

    print(f"✓ Developer Support Agent '{agent.name}' created")
    return agent


async def main() -> None:
    """Test setup."""
    async with p.Server() as server:
        agent = await create_developer_support_agent(server)
        print(f"Agent ID: {agent.id}")


if __name__ == "__main__":
    asyncio.run(main())
