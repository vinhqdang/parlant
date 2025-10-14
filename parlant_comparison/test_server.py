"""Simple test to see if Parlant server can start."""
import asyncio
import sys
sys.path.insert(0, "parlant_agents")

import parlant.sdk as p
from parlant.client import AsyncParlantClient as Client
from customer_service_agent import create_customer_service_agent

async def main():
    print("Step 1: Starting Parlant HTTP server...")
    sys.stdout.flush()

    server = p.Server(port=8765, log_level=p.LogLevel.WARNING)

    async def start_server():
        async with server:
            await asyncio.Future()

    server_task = asyncio.create_task(start_server())

    print("Step 2: Waiting for server to be ready...")
    sys.stdout.flush()

    client = Client(base_url="http://localhost:8765")
    for attempt in range(60):
        try:
            await client.agents.list()
            print(f"Step 3: Server ready after {attempt+1} attempts!")
            sys.stdout.flush()
            break
        except Exception as e:
            if attempt % 10 == 0:
                print(f"  Attempt {attempt+1}/60: {type(e).__name__}")
                sys.stdout.flush()
            await asyncio.sleep(1)
    else:
        print("Step 3: FAILED - Server did not start")
        sys.stdout.flush()
        server_task.cancel()
        return

    print("Step 4: Creating test agent...")
    sys.stdout.flush()

    async with p.Server(port=8765) as setup_server:
        agent = await create_customer_service_agent(setup_server)
        print(f"Step 5: SUCCESS - Agent created with ID: {agent.id}")
        sys.stdout.flush()

    print("Step 6: Listing agents via client...")
    sys.stdout.flush()
    agents = await client.agents.list()
    print(f"Step 7: Found {len(agents)} agent(s)")
    sys.stdout.flush()

    server_task.cancel()
    print("Step 8: COMPLETE!")
    sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
