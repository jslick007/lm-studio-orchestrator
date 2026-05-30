import httpx
import asyncio


async def test_proxy():
    try:
        async with httpx.AsyncClient() as client:
            # Test if the server is up
            # Note: The server might return 404 or 500 because LM Studio isn't running,
            # but it should respond.
            response = await client.post(
                "http://localhost:8000/v1/chat/completions",
                json={"messages": [{"role": "user", "content": "Hello"}]},
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_proxy())
