import os
import json
import logging
from dotenv import load_dotenv
from google import genai

# Cargar las variables del archivo .env a la memoria
load_dotenv()

logger = logging.getLogger(__name__)

def evaluate_adoption_quiz(answers):
    # 1. Obtenemos la llave de forma segura
    api_key = os.getenv("GEMINI_API_KEY") 

    if not api_key:
        logger.error("No se encontró GEMINI_API_KEY en el archivo .env")
        return {"score": 50, "recommendation": "Error interno: Falta configurar la llave de la API."}

    try:
        # 2. Inicializamos el cliente de Gemini
        client = genai.Client(api_key=api_key)
        
        # Usamos el modelo que ya confirmamos que funciona en tu cuenta
        model_id = "gemini-2.5-flash"
        
        prompt = f"""
        Actúa como un evaluador experto en bienestar animal para 'Huellitas Unidas'.
        Analiza este cuestionario: {json.dumps(answers, ensure_ascii=False)}
        
        Criterios: 90-100 (Ideal), 70-89 (Bueno), 50-69 (Dudoso), 0-49 (No apto).
        
        Responde ÚNICAMENTE con un JSON válido con esta estructura exacta, sin texto extra, sin saludos y sin formato Markdown:
        {{"score": 85, "recommendation": "Tu análisis aquí justificando la puntuación."}}
        """
        
        logger.info(f"Enviando evaluación a {model_id}...")
        
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        
        # Limpieza del JSON
        text = response.text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
            
        return json.loads(text)

    except Exception as e:
        logger.error(f"Error de IA capturado: {str(e)}")
        return {"score": 50, "recommendation": f"Fallo al procesar evaluación: {str(e)[:40]}"}