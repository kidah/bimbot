from rasa_core.agent import Agent
from rasa_core.channels.socketio import SocketIOInput
from rasa_core.agent import Agent
from rasa_core.utils import EndpointConfig
from rasa_core.policies.fallback import FallbackPolicy

# load action server endpoint
action_endpoint = EndpointConfig(url="http://127.0.0.1:5055/webhook")
# load your trained agent
agent = Agent.load('models/dialogue', interpreter='models/default/bimnlu', action_endpoint=action_endpoint)

input_channel = SocketIOInput(
	# event name for messages sent from the user
	user_message_evt="user_uttered",
	# event name for messages sent from the bot
	bot_message_evt="bot_uttered",
	# socket.io namespace to use for the messages
	namespace=None
)

# set serve_forever=False if you want to keep the server running
s = agent.handle_channels([input_channel], 5005, serve_forever=True)
