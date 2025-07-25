from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    google,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
    elevenlabs
)

from openai.types.beta.realtime.session import TurnDetection

from livekit.plugins.turn_detector.multilingual import MultilingualModel



from prompts import AGENT_INSTRUCTION

load_dotenv()




class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTION)


async def entrypoint(ctx: agents.JobContext):
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(
    #         voice="ash",
    #         turn_detection=TurnDetection(
    #         type="server_vad",
    #         threshold=0.5,
    #         prefix_padding_ms=300,
    #         silence_duration_ms=500,
    #         create_response=True,
    #         interrupt_response=True,
    #         )
    #     )
    # )?
    session = AgentSession(
            stt = google.STT(
    model="latest_long",
    languages=["hi-IN", "en-US"],
  ),
# stt=deepgram.STT(
#             model="telephony",
#
#             ),
            # llm=openai.LLM(model="gpt-4o-mini"),
#             tts = google.TTS(
#     gender="male",
#     voice_name="hi-IN-Chirp3-HD-Sadaltager",
#     language="hi-IN",
#   ),
tts=elevenlabs.TTS(
      voice_id="FKsP5XtKfX0pvJbzcctW",
      model="eleven_multilingual_v2"
   ),
            vad=silero.VAD.load(),
            turn_detection=MultilingualModel(),
            llm=google.LLM(
                model="gemini-2.5-flash",
                temperature=0.8,
                ), 
        )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(

            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            # noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # await session.generate_reply(
    #     instructions="Hello",
    # )

    session


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))