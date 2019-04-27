import asyncio

import worker.task_handling
import worker.context

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.context.initialize())

    try:
        loop.run_until_complete(worker.context.queue.consume(worker.task_handling.handler))
        loop.run_forever()
    finally:
        worker.context.connection.close()
