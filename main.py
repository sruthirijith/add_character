from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import openai
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
from common_response import error_response,success_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase URL and Key must be set in the environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OpenAI API key must be set in the environment variables")

class Character(BaseModel):
    name: str
    details: str

@app.post("/create_character", status_code=201)
async def create_character(character: Character):
    character_name_lower = character.name.lower()
    existing_character_response = supabase.table("imaginary_characters").select("*").ilike("name", character_name_lower).execute()
    
    if existing_character_response.data:
        return error_response(400, "Character name has already been added")

    data = {"name": character.name, "details": character.details}
    
    response = supabase.table("imaginary_characters").insert(data).execute()

    if not response.data:
        logger.error("Failed to add character: %s", character.name)

        return error_response(400, "Failed to add character")
    
    character_data = {
        "id": response.data[0]["id"],
        "created_at": response.data[0]["created_at"],
        "name": response.data[0]["name"],
        "details": response.data[0]["details"]
    }
    logger.info("Character created successfully: %s", character.name)
    return success_response(201, "Character added successfully", character_data)


@app.post("/generate_story", status_code=201)
async def generate_story(character_name: str):
    response = supabase.from_("imaginary_characters").select("*").eq("name", character_name).execute()
    
    if not response.data:
        return error_response(404, "Character not found")

    character_details = response.data[0]["details"]

    try:
        prompt = f"{character_name}, {character_details}."
        story_response = openai.Completion.create(
            engine="###",
            prompt=prompt,
            max_tokens=100
        )

        if story_response.choices:
            story = story_response.choices[0].text.strip()

            update_response = supabase.table("imaginary_characters").update({
                "short_story": story
            }).eq("name", character_name).execute()

            if not update_response.data:
                return error_response(500, "Failed to update short story")
            
            return success_response(201, "Story generated and saved successfully", {"story": story})
        else:
            return error_response(500, "Failed to generate story")
    except Exception as e:
        logging.error(f"OpenAI Exception: {e}")
        return error_response(500, "Failed to generate story")


