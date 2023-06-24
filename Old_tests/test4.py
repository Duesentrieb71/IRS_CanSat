import asyncio

async def test1():
    print("test1")
    await asyncio.sleep(2)
    print("test1")

async def test2():
    print("test2")
    await asyncio.sleep(1)
    print("test2")

async def main():
    task1 = asyncio.create_task(test1())
    task2 = asyncio.create_task(test2())
    await asyncio.gather(task1)

if __name__ == "__main__":
    asyncio.run(main())