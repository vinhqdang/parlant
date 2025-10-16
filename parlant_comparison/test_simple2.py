"""
Test using the EXACT healthcare.py pattern
"""
import asyncio
import parlant.sdk as p


async def main():
    # Use the EXACT pattern from healthcare.py
    async with p.Server(port=9999, tool_service_port=9998) as server:
        print("Server context entered")

        # Create agent
        agent = await server.create_agent(
            name="Test Agent",
            description="A test agent"
        )
        print(f"Agent created: {agent.id}")

        # Now try to interact with it using the SDK (not HTTP client)
        # This should work if the agent is properly created
        print(f"Agent name: {agent.name}")
        print(f"Agent description: {agent.description}")

        print("✓ Success! Agent created and accessible via SDK")


if __name__ == "__main__":
    asyncio.run(main())
