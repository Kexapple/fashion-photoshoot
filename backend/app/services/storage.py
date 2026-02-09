"""
Firebase Storage operations
Handles image upload and retrieval from Firebase Storage
"""

import firebase_admin
from firebase_admin import storage
from datetime import datetime
import logging
from typing import Optional
import uuid

logger = logging.getLogger(__name__)


class StorageService:
    """Firebase Storage service for image management"""
    
    @staticmethod
    def upload_image(
        bucket_name: str,
        file_path: str,
        folder: str,
        uid: str,
        shoot_id: str
    ) -> Optional[str]:
        """
        Upload image to Firebase Storage
        
        Args:
            bucket_name: Firebase Storage bucket name
            file_path: Local file path
            folder: Folder in storage (uploaded-images or generated-images)
            uid: User ID or anon IP hash
            shoot_id: Photoshoot ID
            
        Returns:
            Download URL or None if failed
        """
        try:
            bucket = storage.bucket(bucket_name)
            blob_path = f"{folder}/{uid}/{shoot_id}/{uuid.uuid4().hex}.jpg"
            blob = bucket.blob(blob_path)
            
            blob.upload_from_filename(file_path)
            blob.make_public()
            
            download_url = blob.public_url
            logger.info(f"Uploaded image to {blob_path}")
            return download_url
        except Exception as e:
            logger.error(f"Failed to upload image: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def save_generated_images(
        bucket_name: str,
        images: list,
        uid: str,
        shoot_id: str
    ) -> list:
        """
        Save generated images to Firebase Storage
        
        Args:
            bucket_name: Firebase Storage bucket name
            images: List of image data (base64 or file paths)
            uid: User ID or anon IP hash
            shoot_id: Photoshoot ID
            
        Returns:
            List of download URLs
        """
        try:
            bucket = storage.bucket(bucket_name)
            download_urls = []
            
            for idx, image_data in enumerate(images):
                try:
                    # If image is already a URL (from API), store the URL
                    if isinstance(image_data, str) and image_data.startswith("http"):
                        download_urls.append(image_data)
                    else:
                        # If base64 encoded, decode and save
                        import base64
                        from io import BytesIO
                        
                        if isinstance(image_data, str):
                            image_bytes = base64.b64decode(image_data)
                        else:
                            image_bytes = image_data
                        
                        blob_path = f"generated-images/{uid}/{shoot_id}/image-{idx+1}.jpg"
                        blob = bucket.blob(blob_path)
                        blob.upload_from_string(image_bytes, content_type="image/jpeg")
                        blob.make_public()
                        
                        download_urls.append(blob.public_url)
                        logger.info(f"Saved generated image: {blob_path}")
                except Exception as e:
                    logger.error(f"Failed to save image {idx}: {str(e)}")
                    continue
            
            return download_urls
        except Exception as e:
            logger.error(f"Failed to process generated images: {str(e)}", exc_info=True)
            return []
    
    @staticmethod
    def get_download_url(bucket_name: str, blob_path: str) -> Optional[str]:
        """Get download URL for stored image"""
        try:
            bucket = storage.bucket(bucket_name)
            blob = bucket.blob(blob_path)
            if blob.exists():
                return blob.public_url
            return None
        except Exception as e:
            logger.error(f"Failed to get download URL: {str(e)}")
            return None
    
    @staticmethod
    def delete_image(bucket_name: str, blob_path: str) -> bool:
        """Delete image from Firebase Storage"""
        try:
            bucket = storage.bucket(bucket_name)
            bucket.delete_blob(blob_path)
            logger.info(f"Deleted image: {blob_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete image: {str(e)}")
            return False
