"""
Purple Executor for DeFiGym.

Handles A2A protocol requests and delegates to the Purple Agent.
"""

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    UnsupportedOperationError,
    Task,
)
from a2a.utils import new_agent_text_message
from a2a.utils.errors import ServerError

from purple.agent import GroundtruthAgent


class PurpleExecutor(AgentExecutor):
    """
    Executor for the Groundtruth Purple Agent.

    Receives task descriptions and returns the actual exploit from DeFiHackLabs.
    """

    def __init__(self, agent: GroundtruthAgent):
        """
        Initialize executor with a Groundtruth Agent.

        Args:
            agent: The GroundtruthAgent instance
        """
        self.agent = agent

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """
        Execute the exploit generation request.

        Args:
            context: Request context containing the task description
            event_queue: Queue for emitting events
        """
        # Get the task description from the green agent
        task_description = context.get_user_input()

        # Get the groundtruth exploit
        try:
            exploit_code = await self.agent.generate_exploit(task_description)

            # Return the exploit code as a response
            response = new_agent_text_message(
                exploit_code,
                context_id=context.context_id
            )
            await event_queue.enqueue_event(response)

        except Exception as e:
            # Return error message
            error_response = new_agent_text_message(
                f"Error in groundtruth agent: {str(e)}",
                context_id=context.context_id
            )
            await event_queue.enqueue_event(error_response)
            raise

    async def cancel(
        self,
        request: RequestContext,
        event_queue: EventQueue,
    ) -> Task | None:
        """Cancel operation is not supported."""
        raise ServerError(error=UnsupportedOperationError())
