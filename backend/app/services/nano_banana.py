"""
Nano Banana API integration for image generation
Handles calls to Nano Banana API for AI image generation
"""

import requests
import logging
from typing import List, Dict, Any
import base64

from app.config import settings

logger = logging.getLogger(__name__)

NANO_BANANA_API_URL = "https://api.nanobana.com/v1/generate"


class NanoBananaService:
    """Nano Banana API service for image generation"""
    
    @staticmethod
    def generate_photoshoot(
        reference_images: List[str],
        article_type: str,
        style_notes: str,
        image_size: str
    ) -> Dict[str, Any]:
        """
        Generate fashion photoshoot images using Nano Banana API
        
        Args:
            reference_images: List of image URLs or base64-encoded images
            article_type: Type of article (shirt, dress, pants, etc.)
            style_notes: Style description and notes
            image_size: Output size (small: 512x512, medium: 768x768, large: 1024x1024)
            
        Returns:
            {
                "success": bool,
                "images": List[str],  # List of generated image URLs or base64
                "message": str
            }
        """
        try:
            # Map image size to dimensions
            size_map = {
                "small": "512x512",
                "medium": "768x768",
                "large": "1024x1024"
            }
            
            output_size = size_map.get(image_size, "768x768")
            width, height = output_size.split("x")
            
            # Prepare prompt
            prompt = NanoBananaService._build_prompt(
                article_type,
                style_notes,
                reference_images
            )
            
            logger.info(f"Generating photoshoot: {article_type}, size: {output_size}")
            
            # Call Nano Banana API
            payload = {
                "model_id": settings.NANO_BANANA_MODEL_ID,
                "prompt": prompt,
                "width": int(width),
                "height": int(height),
                "num_outputs": 3,  # Generate 3 images
                "num_inference_steps": 50,
                "guidance_scale": 7.5
            }
            
            headers = {
                "Authorization": f"Bearer {settings.NANO_BANANA_API_KEY}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                NANO_BANANA_API_URL,
                json=payload,
                headers=headers,
                timeout=60  # 60 second timeout for generation
            )
            
            if response.status_code != 200:
                logger.error(f"Nano Banana API error: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "images": [],
                    "message": f"API error: {response.status_code}"
                }
            
            data = response.json()
            
            # Extract image URLs/base64 from response
            images = data.get("outputs", [])
            
            if not images:
                logger.warning("No images returned from Nano Banana API")
                return {
                    "success": False,
                    "images": [],
                    "message": "No images generated"
                }
            
            logger.info(f"Successfully generated {len(images)} images")
            
            return {
                "success": True,
                "images": images,
                "message": f"Generated {len(images)} images"
            }
            
        except requests.Timeout:
            logger.error("Nano Banana API timeout (>60 seconds)")
            return {
                "success": False,
                "images": [],
                "message": "Generation timeout - taking too long"
            }
        except Exception as e:
            logger.error(f"Nano Banana API error: {str(e)}", exc_info=True)
            return {
                "success": False,
                "images": [],
                "message": f"Generation error: {str(e)}"
            }
    
    @staticmethod
    def _build_prompt(article_type: str, style_notes: str, reference_images: List[str]) -> str:
        """
        Build a detailed prompt for Nano Banana API
        
        Args:
            article_type: Type of clothing item
            style_notes: Style description
            reference_images: Reference image URLs
            
        Returns:
            Detailed prompt string
        """
        base_prompt = f"""
High-quality fashion photoshoot of a {article_type}.
Professional studio lighting, clean white background, premium fashion photography.
Article type: {article_type}
Style: {style_notes if style_notes else 'modern, professional'}

Generate multiple angles and shots:
- Front-facing shot
- Side profile
- Back view (if applicable)

Lighting: Professional studio with soft diffused lighting
Background: Clean white or neutral
Quality: 8K, high detail, professional fashion magazine quality
Style: Modern, premium, high-fashion photoshoot aesthetic
"""
        return base_prompt.strip()


class MockNanoBananaService:
    """Mock Nano Banana service for testing without API key"""
    
    @staticmethod
    def generate_photoshoot(
        reference_images: List[str],
        article_type: str,
        style_notes: str,
        image_size: str
    ) -> Dict[str, Any]:
        """
        Mock image generation for testing
        Returns placeholder image URLs
        """
        logger.info(f"MOCK: Generating photoshoot for {article_type}")
        
        # Return mock image URLs
        mock_images = [
            f"https://via.placeholder.com/768x768?text=Front+Shot",
            f"https://via.placeholder.com/768x768?text=Side+Shot",
            f"https://via.placeholder.com/768x768?text=Back+Shot"
        ]
        
        return {
            "success": True,
            "images": mock_images,
            "message": "Mock images generated (for testing)"
        }


# Use mock service if API key not configured
GenerationService = NanoBananaService if settings.NANO_BANANA_API_KEY else MockNanoBananaService
