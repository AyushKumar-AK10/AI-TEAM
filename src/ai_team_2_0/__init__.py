import asyncio

from langgraph.types import Command

from .graph.graph import graph


async def async_main() -> None:
    config = {"configurable": {"thread_id": "ba-session-1"}}
    result = await graph.ainvoke(
        {
            "userReq": "Build a basic hello world website. Don't ask further questions"
        },
        config=config,
    )

    while result.get("__interrupt__"):
        print(result["__interrupt__"][0].value)
        clarification = input("Your clarification: ")
        result = await graph.ainvoke(
            Command(resume=clarification),
            config=config,
        )

    print(result['devResponse'].model_dump_json(indent=2))
    print(result["testResponse"].content)
    print(result['architectReview'].content)

def main() -> None:
    asyncio.run(async_main())