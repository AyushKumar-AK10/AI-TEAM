import asyncio

from langgraph.types import Command

from .graph.graph import graph


async def async_main() -> None:
    config = {"configurable": {"thread_id": "ba-session-1"}}
    graph_input = {
        "userReq": "Build a website for Pokemon.No Db no reddis. Don't ask further questions"
    }

    async def run_graph(input_value):
        async for event in graph.astream(
            input_value,
            config=config,
            stream_mode="debug",
        ):
            event_type = event.get("type")
            payload = event.get("payload", {})
            node_name = payload.get("name", "unknown")

            if event_type == "task":
                print(f"Starting node: {node_name}")
            elif event_type == "task_result":
                status = "failed" if payload.get("error") else "finished"
                print(f"Node {status}: {node_name}")

        snapshot = await graph.aget_state(config)
        pending_interrupt = next(
            (
                interrupt
                for task in snapshot.tasks
                for interrupt in task.interrupts
            ),
            None,
        )
        return snapshot.values, pending_interrupt

    result, pending_interrupt = await run_graph(graph_input)
    while pending_interrupt:
        print(pending_interrupt.value)
        clarification = input("Your clarification: ")
        result, pending_interrupt = await run_graph(Command(resume=clarification))

    print(result['devResponse'].model_dump_json(indent=2))
    print(result["testResponse"].content)
    print(result['architectReview'].content)

def main() -> None:
    asyncio.run(async_main())