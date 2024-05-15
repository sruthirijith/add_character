### ###### # **Imaginary Characters API**

This API allows users to manage imaginary characters and generate short stories for them using OpenAI's GPT models.

###### Prerequisites
Before running the application, ensure you have the following installed:

--Python 3.7+
--Supabase account and project
--OpenAI API key


###### Installation
Clone the repository:

--git clone https://github.com/sruthirijith/add_character.git

###### Install dependencies:
pip install -r requirements.txt

###### Configuration

Create a .env file in the project root and add the following environment variables:


--SUPABASE_URL=your_supabase_url
--SUPABASE_KEY=your_supabase_key
--OPENAI_API_KEY=your_openai_api_key

Replace your_supabase_url, your_supabase_key, and your_openai_api_key with your Supabase project URL, Supabase key, and OpenAI API key, respectively.

###### Usage

1. Run the FastAPI server:
--uvicorn main:app --reload

2. Once the server is running, you can access the API documentation at http://localhost:8000/docs in your browser.

###### Endpoints

1. Create Character
--URL: /create_character

--Method: POST

--Description: Create a new character.

Request Body:
{
    "name": "Character Name",
    "details": "Character Details"
}
Response: Return the created character with a 201 status code.

eg: curl : curl -X 'POST' \
  'http://127.0.0.1:8000/create_character' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "spiderman",
  "details": "kids all time favourite"
}'

reponse:
   {
  "status_code": 201,
  "message": "Character added successfully",
  "data": {
    "id": 19,
    "created_at": "2024-05-15T10:45:56.536963+00:00",
    "name": "spiderman",
    "details": "kids all time favourite"
  }
}


2. Generate Story

--URL: /generate_story

--Method: POST

--Description: Generate a story for a character.

Request Body:

{
    "character_name": "Character Name"
}
Response: Return the generated story with a 201 status code.

eg:  curl  : curl -X 'POST' \
  'http://127.0.0.1:8000/generate_story' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "character_name": "spiderman"
}'

response :
{
  "status_code": 201,
  "message": "Story generated and saved successfully",
  "data": {
    "story": "Once upon a time, in a bustling city, there lived a hero named Spiderman. He was beloved by kids all around for his bravery and sense of justice. With his superpowers, he swung through the city streets, protecting the innocent from evil. Little did they know, behind the mask, he was just a regular person, trying to make the world a better place."
  }
}
