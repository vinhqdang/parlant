"""
Simple comparison script for Customer Service agent only.
This provides REAL Parlant responses vs Traditional prompts.
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys

# Add test scenarios to path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "parlant_agents"))

from test_scenarios.test_cases import get_test_cases, TestCase

# Try to import config
try:
    from config import config
    HAS_CONFIG = True
    # Set environment variable for Parlant server
    import os
    if config and config.OPENAI_API_KEY:
        os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY
except ImportError:
    HAS_CONFIG = False
    config = None

from openai import AsyncOpenAI
import parlant.sdk as p
from parlant.client import AsyncParlantClient as Client
from customer_service_agent import create_customer_service_agent


class PromptBasedAgent:
    """Traditional prompt-based agent using LLM API."""

    def __init__(self, prompt_file: Path, llm_client: AsyncOpenAI):
        """Initialize with a prompt file and LLM client."""
        self.prompt = prompt_file.read_text()
        self.conversation_history: List[Dict[str, str]] = []
        self.llm_client = llm_client

    async def send_message(self, message: str) -> str:
        """Send a message to the agent and get response."""
        self.conversation_history.append({"role": "user", "content": message})

        messages = [{"role": "system", "content": self.prompt}] + self.conversation_history
        api_response = await self.llm_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=2000
        )
        response = api_response.choices[0].message.content

        self.conversation_history.append({"role": "assistant", "content": response})
        return response


class ParlantAgentWrapper:
    """Wrapper for Parlant agent using SDK."""

    def __init__(self, agent: p.Agent, client: Client):
        """Initialize Parlant agent wrapper."""
        self.agent = agent
        self.client = client
        self.session_id = None

    async def send_message(self, message: str) -> str:
        """Send a message through Parlant framework."""
        # Create new session for each test (clean state)
        if not self.session_id:
            session = await self.client.sessions.create(
                agent_id=self.agent.id,
                allow_greeting=False,
            )
            self.session_id = session.id

        # Send customer message
        event = await self.client.sessions.create_event(
            session_id=self.session_id,
            kind="message",
            source="customer",
            message=message,
        )

        # Wait for AI agent response
        agent_messages = await self.client.sessions.list_events(
            session_id=self.session_id,
            min_offset=event.offset,
            source="ai_agent",
            kinds="message",
            wait_for_data=30,
        )

        if agent_messages:
            return agent_messages[0].model_dump().get("data", {}).get("message", "[No response]")

        return "[No response from agent]"


async def run_comparison():
    """Run comparison between traditional prompts and Parlant."""

    print("=" * 70)
    print("Customer Service Agent: Traditional Prompts vs Parlant")
    print("=" * 70)
    print()

    # Initialize OpenAI client
    if not (HAS_CONFIG and config and config.OPENAI_API_KEY):
        print("ERROR: OpenAI API key not found in config/config.py")
        return

    openai_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
    print("✓ OpenAI client initialized")

    # Start Parlant server
    port = 8800
    print(f"✓ Starting Parlant server on port {port}...")
    print("  (This may take 20-30 seconds for embedding cache initialization...)")

    server = p.Server(port=port, log_level=p.LogLevel.WARNING)
    parlant_agent = None

    async def start_server():
        nonlocal parlant_agent
        async with server:
            # Give server time to bind to port and start HTTP API
            await asyncio.sleep(5)
            print("✓ Server context ready, creating agent...")
            parlant_agent = await create_customer_service_agent(server)
            print(f"✓ Parlant agent created: {parlant_agent.name}")
            # Give extra time for embedding cache to complete
            print("  Waiting for embedding cache to complete...")
            await asyncio.sleep(10)
            print("  Agent initialization complete, HTTP API should be ready")
            # Wait forever
            await asyncio.Future()

    server_task = asyncio.create_task(start_server())

    # Wait for server to start and agent to be created
    client = Client(base_url=f"http://localhost:{port}")
    max_wait = 90  # Increased to 90 seconds for embedding cache
    print(f"  Waiting up to {max_wait} seconds for server and agent initialization...")

    # First, wait for server to be reachable
    server_ready = False
    last_error = None
    for i in range(60):  # 30 seconds for server startup
        try:
            await client.agents.list()
            server_ready = True
            print("  Server is responding, waiting for agent creation...")
            break
        except Exception as e:
            last_error = str(e)
            if i % 10 == 0 and i > 0:  # Print progress every 5 seconds
                print(f"  Still waiting for server... ({i//2}s elapsed, last error: {type(e).__name__})")
        await asyncio.sleep(0.5)

    if not server_ready:
        print("ERROR: Parlant server HTTP API did not become available")
        print(f"  Last error: {last_error}")
        print("  Server task status:", "done" if server_task.done() else "running")
        if server_task.done() and server_task.exception():
            print(f"  Server task exception: {server_task.exception()}")
        server_task.cancel()
        return

    # Then wait for agent to be created and registered
    for i in range(max_wait * 2):  # Check every 0.5 seconds
        if parlant_agent is not None:
            try:
                agents = await client.agents.list()
                if any(a.id == parlant_agent.id for a in agents):
                    print("✓ Parlant server ready and agent registered")
                    break
            except Exception as e:
                pass
        await asyncio.sleep(0.5)
    else:
        print(f"ERROR: Agent did not initialize in time (parlant_agent={'set' if parlant_agent else 'not set'})")
        server_task.cancel()
        return

    try:
        # Agent is already created above in the server context
        print(f"✓ Using agent: {parlant_agent.name}")

        # Load traditional prompt
        prompt_file = Path(__file__).parent / "prompts" / "customer_service_prompt.txt"
        traditional_agent = PromptBasedAgent(prompt_file, openai_client)
        print(f"✓ Traditional agent loaded ({len(traditional_agent.prompt)} chars)")

        # Get test cases
        test_cases = get_test_cases("customer_service")
        print(f"✓ Loaded {len(test_cases)} test cases")
        print()

        results = []

        for test_case in test_cases:
            print(f"\n{'=' * 70}")
            print(f"Test: {test_case.id} - {test_case.name}")
            print(f"{'=' * 70}\n")

            result = {
                "test_id": test_case.id,
                "test_name": test_case.name,
                "timestamp": datetime.now().isoformat(),
                "traditional": {},
                "parlant": {},
            }

            # Run with traditional prompt
            print("--- Traditional Prompt ---")
            trad_start = time.time()
            trad_responses = []
            for msg in test_case.messages:
                print(f"User: {msg}")
                response = await traditional_agent.send_message(msg)
                trad_responses.append(response)
                print(f"Agent: {response[:200]}{'...' if len(response) > 200 else ''}\n")
            trad_duration = time.time() - trad_start

            result["traditional"] = {
                "responses": trad_responses,
                "duration_seconds": trad_duration,
                "prompt_length": len(traditional_agent.prompt),
            }

            # Run with Parlant
            print("--- Parlant Framework ---")
            parlant_wrapper = ParlantAgentWrapper(parlant_agent, client)
            parlant_start = time.time()
            parlant_responses = []
            for msg in test_case.messages:
                print(f"User: {msg}")
                response = await parlant_wrapper.send_message(msg)
                parlant_responses.append(response)
                print(f"Agent: {response[:200]}{'...' if len(response) > 200 else ''}\n")
            parlant_duration = time.time() - parlant_start

            result["parlant"] = {
                "responses": parlant_responses,
                "duration_seconds": parlant_duration,
            }

            result["evaluation"] = {
                "criteria": test_case.evaluation_criteria,
                "expected_behaviors": test_case.expected_behaviors,
            }

            results.append(result)

        # Save results
        output_file = Path(__file__).parent / "results" / "REAL_customer_service_comparison.json"
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n{'=' * 70}")
        print(f"Comparison complete!")
        print(f"Results saved to: {output_file}")
        print(f"{'=' * 70}\n")

    finally:
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(run_comparison())
