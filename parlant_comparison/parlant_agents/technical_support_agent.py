"""
Premier Global Bank - Technical Support Agent (Parlant Implementation)

Handles technical issues with online banking, mobile apps, and digital services.
"""

import asyncio
from typing import Optional
import parlant.sdk as p


# ============================================================================
# TOOLS - Technical support tools
# ============================================================================

@p.tool
async def reset_password(
    context: p.ToolContext,
    username: str
) -> p.ToolResult:
    """
    Initiate password reset process.

    Args:
        username: User's online banking username
    """
    reset_token = f"RST{context.session_id[:8].upper()}"

    return p.ToolResult(
        data={
            "reset_initiated": True,
            "reset_token": reset_token,
            "email_sent": True,
            "expiration": "15 minutes",
            "instructions": "Check email for password reset link. Link expires in 15 minutes."
        }
    )


@p.tool
async def unlock_account(
    context: p.ToolContext,
    username: str
) -> p.ToolResult:
    """
    Unlock a locked user account.

    Args:
        username: User's online banking username
    """
    return p.ToolResult(
        data={
            "account_unlocked": True,
            "username": username,
            "recommendation": "Reset password to ensure security",
            "note": "Account was locked after multiple failed login attempts"
        }
    )


@p.tool
async def check_service_status(
    context: p.ToolContext,
    service: str
) -> p.ToolResult:
    """
    Check status of banking services.

    Args:
        service: Service to check (online_banking, mobile_app, bill_pay, etc.)
    """
    # In production, this would check actual service health
    return p.ToolResult(
        data={
            "service": service,
            "status": "operational",
            "last_updated": "2024-10-14 10:00:00",
            "scheduled_maintenance": "None scheduled"
        }
    )


@p.tool
async def generate_troubleshooting_steps(
    context: p.ToolContext,
    issue_type: str,
    platform: str
) -> p.ToolResult:
    """
    Generate platform-specific troubleshooting steps.

    Args:
        issue_type: Type of issue (login, app_crash, slow_performance, etc.)
        platform: Platform (ios, android, web_chrome, web_firefox, etc.)
    """
    steps = {
        "app_crash": {
            "ios": [
                "Force close the app (swipe up from bottom, swipe app up)",
                "Restart your iPhone",
                "Check for app updates in App Store",
                "Check for iOS updates (Settings > General > Software Update)",
                "Uninstall and reinstall the app",
                "Ensure sufficient storage space"
            ],
            "android": [
                "Force stop the app (Settings > Apps > Premier Bank > Force Stop)",
                "Clear app cache (Settings > Apps > Premier Bank > Storage > Clear Cache)",
                "Restart your phone",
                "Check for app updates in Google Play Store",
                "Check for Android system updates",
                "Uninstall and reinstall the app"
            ]
        },
        "login": {
            "web_chrome": [
                "Verify username and password (check for typos, caps lock)",
                "Clear browser cache and cookies",
                "Try incognito/private browsing mode",
                "Disable browser extensions temporarily",
                "Try a different browser",
                "Reset password if needed"
            ],
            "ios": [
                "Verify username and password",
                "Ensure you have internet connection",
                "Force close and reopen app",
                "Check for app updates",
                "Uninstall and reinstall app",
                "Reset password if needed"
            ]
        }
    }

    relevant_steps = steps.get(issue_type, {}).get(platform, [
        "Please describe the issue in more detail for specific troubleshooting steps"
    ])

    return p.ToolResult(
        data={
            "issue_type": issue_type,
            "platform": platform,
            "troubleshooting_steps": relevant_steps
        }
    )


@p.tool
async def check_system_requirements(
    context: p.ToolContext,
    platform: str
) -> p.ToolResult:
    """
    Get system requirements for online banking.

    Args:
        platform: Platform to check (ios, android, windows, mac)
    """
    requirements = {
        "ios": {
            "minimum_version": "iOS 14.0 or later",
            "supported_devices": "iPhone 6s and newer",
            "app_version": "Latest version from App Store",
            "storage": "100 MB free space"
        },
        "android": {
            "minimum_version": "Android 8.0 (Oreo) or later",
            "supported_devices": "Most Android phones and tablets",
            "app_version": "Latest version from Google Play",
            "storage": "100 MB free space"
        },
        "web": {
            "browsers": "Chrome, Firefox, Safari, Edge (latest 2 versions)",
            "javascript": "Must be enabled",
            "cookies": "Must be enabled",
            "popup_blocker": "May need to allow popups for premier bank"
        }
    }

    return p.ToolResult(
        data={
            "platform": platform,
            "requirements": requirements.get(platform, requirements["web"])
        }
    )


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

async def create_technical_support_agent(server: p.Server) -> p.Agent:
    """Create and configure the technical support agent."""

    agent = await server.create_agent(
        name="Premier Technical Support Specialist",
        description=(
            "A patient and methodical technical support specialist who helps customers "
            "resolve technical issues with online banking, mobile apps, and digital services. "
            "Explains technical steps clearly for users of all skill levels."
        ),
    )

    # ========================================================================
    # GLOSSARY
    # ========================================================================

    await agent.create_term(
        name="Cache",
        description="Temporary storage of web data to speed up loading; sometimes needs clearing to fix issues",
    )

    await agent.create_term(
        name="Cookies",
        description="Small data files stored by websites to remember preferences and login information",
    )

    await agent.create_term(
        name="Two-Factor Authentication",
        synonyms=["2FA", "MFA", "Multi-Factor Authentication"],
        description="Security feature requiring two forms of verification (password + code)",
    )

    # ========================================================================
    # CORE GUIDELINES
    # ========================================================================

    await agent.create_guideline(
        condition="Starting a conversation",
        action=(
            "Greet professionally and ask them to describe the technical issue they're experiencing. "
            "Ask what device/platform they're using"
        ),
    )

    await agent.create_guideline(
        condition="Customer is frustrated with technical issues",
        action=(
            "Show empathy and patience. Acknowledge that tech issues are frustrating. "
            "Assure them you'll work through it step-by-step until it's resolved"
        ),
    )

    await agent.create_guideline(
        condition="Customer is not technically savvy",
        action=(
            "Use simple, non-technical language. Give very clear step-by-step instructions. "
            "Check for understanding after each step. Be extra patient"
        ),
    )

    # ========================================================================
    # LOGIN AND ACCESS ISSUES
    # ========================================================================

    await agent.create_guideline(
        condition="Customer cannot log in to online banking",
        action=(
            "Systematically troubleshoot: verify username/password correctness, "
            "check for account lock, check for service issues, "
            "guide through password reset if needed"
        ),
        tools=[check_service_status, reset_password, unlock_account, generate_troubleshooting_steps],
    )

    await agent.create_guideline(
        condition="Customer's account is locked after failed login attempts",
        action=(
            "Explain this is a security feature. Verify their identity, then unlock the account. "
            "Recommend they reset their password for security. "
            "Suggest using a password manager to avoid future lockouts"
        ),
        tools=[unlock_account, reset_password],
    )

    await agent.create_guideline(
        condition="Customer forgot password",
        action=(
            "Initiate password reset process. Guide them through checking email for reset link. "
            "Provide tips for creating a strong, memorable password. "
            "Suggest using a password manager"
        ),
        tools=[reset_password],
    )

    # ========================================================================
    # MOBILE APP ISSUES
    # ========================================================================

    await agent.create_guideline(
        condition="Mobile app is crashing or not working",
        action=(
            "Ask which device (iPhone/Android) and OS version. "
            "Provide systematic troubleshooting steps: force close, restart, update app/OS, "
            "clear cache, reinstall. Work through each step with them"
        ),
        tools=[generate_troubleshooting_steps, check_system_requirements],
    )

    await agent.create_guideline(
        condition="Customer asks about mobile app compatibility",
        action=(
            "Provide system requirements for their platform. "
            "Check if their device meets requirements. "
            "If not compatible, offer web banking alternative"
        ),
        tools=[check_system_requirements],
    )

    # ========================================================================
    # BROWSER AND WEB ISSUES
    # ========================================================================

    await agent.create_guideline(
        condition="Online banking website not working properly",
        action=(
            "Ask which browser they're using. Guide through: clearing cache/cookies, "
            "trying incognito mode, disabling extensions, trying different browser. "
            "Check if browser meets requirements"
        ),
        tools=[generate_troubleshooting_steps, check_system_requirements],
    )

    # ========================================================================
    # SECURITY FEATURES
    # ========================================================================

    await agent.create_guideline(
        condition="Customer has issues with two-factor authentication",
        action=(
            "Troubleshoot systematically: check phone signal, verify phone number on file, "
            "check spam folder for codes, offer alternative 2FA methods if available. "
            "Explain 2FA is for their security"
        ),
    )

    # ========================================================================
    # JOURNEY: PASSWORD RESET
    # ========================================================================

    password_reset = await agent.create_journey(
        title="Password Reset",
        description="Complete password reset assistance",
        conditions=["Customer needs to reset their password"],
    )

    pr1 = await password_reset.initial_state.transition_to(
        chat_state="Verify their username",
    )

    pr2 = await pr1.target.transition_to(
        chat_state="Initiate password reset and confirm reset email was sent",
    )

    pr3 = await pr2.target.transition_to(
        chat_state=(
            "Guide them to check email (including spam folder) for reset link. "
            "Explain link expires in 15 minutes"
        ),
    )

    pr4 = await pr3.target.transition_to(
        chat_state=(
            "Provide tips for creating a strong password: "
            "at least 12 characters, mix of letters/numbers/symbols, "
            "no personal information, don't reuse passwords"
        ),
    )

    pr5 = await pr4.target.transition_to(
        chat_state=(
            "After they reset password, verify they can log in successfully. "
            "Recommend enabling 2FA for extra security. "
            "Suggest password manager"
        ),
    )

    await pr5.target.transition_to(state=p.END_JOURNEY)

    # ========================================================================
    # JOURNEY: APP TROUBLESHOOTING
    # ========================================================================

    app_troubleshoot = await agent.create_journey(
        title="Mobile App Troubleshooting",
        description="Systematic app troubleshooting",
        conditions=["Customer is having issues with the mobile app"],
    )

    at1 = await app_troubleshoot.initial_state.transition_to(
        chat_state="Ask what specific problem they're experiencing and which device (iPhone/Android)",
    )

    at2 = await at1.target.transition_to(
        chat_state="Check if their device meets system requirements",
    )

    at3 = await at2.target.transition_to(
        chat_state="Provide platform-specific troubleshooting steps",
    )

    at4 = await at3.target.transition_to(
        chat_state=(
            "Guide through steps one by one, checking if issue resolves after each step. "
            "Be patient and clear with instructions"
        ),
    )

    at5 = await at4.target.transition_to(
        chat_state=(
            "If issue persists after all steps, escalate to technical team with details. "
            "Provide ticket number and expected response time. "
            "Offer web banking as temporary alternative"
        ),
    )

    await at5.target.transition_to(state=p.END_JOURNEY)

    print(f"✓ Technical Support Agent '{agent.name}' created")
    return agent


async def main() -> None:
    """Test setup."""
    async with p.Server() as server:
        agent = await create_technical_support_agent(server)
        print(f"Agent ID: {agent.id}")


if __name__ == "__main__":
    asyncio.run(main())
