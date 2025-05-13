

import logging
from dotenv import load_dotenv

# Load environment variables (your API keys should be in .env)
_ = load_dotenv(override=True)

# Set up logging
logger = logging.getLogger("voice-ai-agent")
logger.setLevel(logging.INFO)

# Import LiveKit and plugin tools
from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, jupyter
from livekit.plugins import openai, elevenlabs, silero

# Define your custom assistant agent
class Assistant(Agent):
    def __init__(self) -> None:
        # Load your preferred models
        llm = openai.LLM(model="gpt-4o")        # GPT-4o for fast multi-modal responses
        stt = openai.STT()                      # OpenAI Whisper for speech-to-text
        tts = elevenlabs.TTS()                  # ElevenLabs for realistic voice
        # tts = elevenlabs.TTS(voice_id="CwhRBWXzGAHq8TQ4Fs17")  # Custom voice (optional)
        vad = silero.VAD.load()                 # Voice activity detection

        # Initialize the agent with instructions
        super().__init__(
            instructions="""
                You are a helpful assistant communicating via voice.
                Answer clearly, concisely, and with a friendly tone.
            """,
            stt=stt,
            llm=llm,
            tts=tts,
            vad=vad,
        )

# Entry point for LiveKit Agent
async def entrypoint(ctx: JobContext):
    await ctx.connect()                         # Connect to the LiveKit infrastructure

    session = AgentSession()                    # Create a new agent session

    await session.start(
        room=ctx.room,                          # Connect the session to the room
        agent=Assistant(),                      # Use the assistant agent defined above
    )

# Run the agent app with Jupyter for testing/demo
jupyter.run_app(
    WorkerOptions(entrypoint_fnc=entrypoint),
    jupyter_url="https://jupyter-api-livekit.vercel.app/api/join-token"  # Demo URL or your own server
)
