from typing import Annotated
from fastapi import FastAPI, Depends, Response
from tts.festival import FestivalTTS
from tts.flite import FliteTTS

speak_api = FastAPI()

def flite_init():
    return FliteTTS('voices/flite')

@speak_api.get("/festival")
async def festival(text: str, voice_id: str, tts: FestivalTTS = Depends(FestivalTTS)):
    async for voice in tts.voices():
        if voice.id == voice_id:
            return Response(content=await tts.say(text, voice_id), media_type="audio/x-wav")
    return Response(content="Voice not found", status_code=400)

@speak_api.get("/flite")
async def flite(text: str, voice_id: str, tts: FliteTTS = Depends(flite_init)):
    async for voice in tts.voices():
        if voice.id == voice_id:
            return Response(content=await tts.say(text, voice_id), media_type="audio/x-wav")
    return Response(content="Voice not found", status_code=400)

@speak_api.get("/voices")
async def voices(gender: str | None = None, festival: Annotated[FestivalTTS, Depends(FestivalTTS)] = None, flite: Annotated[FliteTTS, Depends(flite_init)] = None):
    voices = {
        "festival": [voice.id async for voice in festival.voices() if gender is None or voice.gender == gender.capitalize()],
        "flite": [voice.id async for voice in flite.voices() if gender is None or voice.gender == gender.capitalize()],
    }

    return voices