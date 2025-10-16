"""
Simple test to verify Parlant server and client work together
"""
import asyncio
import parlant.sdk as p
from parlant.client import AsyncParlantClient as Client


async def main():
    # Use a simple port
    port = 8888
    tool_port = 8889

    print(f"Starting Parlant server on port {port}...")

    # Create server
    server = p.Server(port=port, tool_service_port=tool_port, log_level=p.LogLevel.INFO)

    # Server task
    async def run_server():
        async with server:
            # Create a simple agent
            print("Creating test agent...")
            agent = await server.create_agent(
                name="Test Agent",
                description="A simple test agent"
            )
            print(f"✓ Agent created with ID: {agent.id}")

            # Keep server running - HTTP server is now accepting connections
            print("Server ready, HTTP endpoint active, waiting forever...")
            await asyncio.Future()

    # Start server in background
    server_task = asyncio.create_task(run_server())

    # Connect with client
    print("Connecting client...")
    client = Client(base_url=f"http://localhost:{port}")

    # Wait for server to be ready by polling (like SDK tests do)
    print("Waiting for server to be ready...")
    for attempt in range(60):  # Increased from 30 to 60
        # Check if server task failed
        if server_task.done():
            try:
                server_task.result()
            except Exception as e:
                print(f"⚠ Server task failed: {e}")
                import traceback
                traceback.print_exc()
                return

        try:
            agents = await client.agents.list()
            print(f"✓ Server ready after {attempt+1} attempts ({(attempt+1)*0.5:.1f}s)")
            break
        except Exception as e:
            if attempt % 10 == 0:
                print(f"  Attempt {attempt+1}/60: {type(e).__name__} (waiting for HTTP server...)")
            await asyncio.sleep(0.5)
    else:
        print("⚠ Server did not start in time")
        server_task.cancel()
        return

    # List agents
    print(f"Listing agents (found {len(agents)})...")
    print(f"✓ Found {len(agents)} agent(s)")

    if agents:
        agent = agents[0]
        print(f"  Agent: {agent.name} (ID: {agent.id})")

        # Create session
        print("Creating session...")
        session = await client.sessions.create(
            agent_id=agent.id,
            allow_greeting=False
        )
        print(f"✓ Session created: {session.id}")

        # Send message
        print("Sending message...")
        event = await client.sessions.create_event(
            session_id=session.id,
            kind="message",
            source="customer",
            message="Hello!"
        )
        print(f"✓ Message sent")

        # Get response
        print("Waiting for response...")
        agent_messages = await client.sessions.list_events(
            session_id=session.id,
            min_offset=event.offset,
            source="ai_agent",
            kinds="message",
            wait_for_data=30
        )

        if agent_messages:
            response = agent_messages[0].model_dump().get("data", {}).get("message", "")
            print(f"✓ Got response: {response}")
        else:
            print("⚠ No response received")

    # Cleanup
    print("Cleaning up...")
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

    print("✓ Test complete!")


if __name__ == "__main__":
    asyncio.run(main())
