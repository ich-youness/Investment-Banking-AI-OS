"""
Client-based OCR using external OCR service
Based on the provided OCR function using client.files.upload and client.ocr.process
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import asyncio
import aiofiles

class ClientOCR:
    def __init__(self, client=None):
        self.logger = logging.getLogger(__name__)
        self.client = client
        
    def set_client(self, client):
        """Set the OCR client"""
        self.client = client
        
    async def ocr_pdf(self, file_path: str, output_dir: str = "Inputs") -> Dict[str, Any]:
        """
        Extract text from PDF using client-based OCR
        Based on the provided ocr_pdf function
        """
        try:
            if not self.client:
                return {
                    'success': False,
                    'error': 'OCR client not initialized',
                    'text': '',
                    'metadata': {}
                }
            
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {file_path}',
                    'text': '',
                    'metadata': {}
                }
            
            self.logger.info(f"Starting OCR for: {file_path.name}")
            
            # Upload file to OCR service
            with open(file_path, "rb") as file_content:
                uploaded_pdf = self.client.files.upload(
                    file={
                        "file_name": file_path.name,
                        "content": file_content,
                    },
                    purpose="ocr"
                )
            
            # Get signed URL
            signed_url = self.client.files.get_signed_url(file_id=uploaded_pdf.id)
            
            self.logger.info("Starting OCR request...")
            
            # Process OCR
            ocr_response = self.client.ocr.process(
                model="mistral-ocr-latest",  # You mentioned this is not available for you
                document={
                    "type": "document_url",
                    "document_url": signed_url.url,
                },
                include_image_base64=True
            )
            
            self.logger.info("OCR request completed")
            
            # Extract text from pages
            extracted_text = "\n".join([page.markdown for page in ocr_response.pages])
            
            # Save OCR response to markdown file
            output_path = Path(output_dir) / f"{file_path.stem}_ocr.md"
            async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
                await f.write(extracted_text)
            
            self.logger.info(f"OCR response saved to: {output_path}")
            
            return {
                'success': True,
                'text': extracted_text,
                'metadata': {
                    'pages': len(ocr_response.pages),
                    'extraction_method': 'client_ocr',
                    'output_file': str(output_path),
                    'text_length': len(extracted_text)
                }
            }
            
        except Exception as e:
            self.logger.error(f"OCR processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'metadata': {}
            }
    
    async def process_uploaded_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process an uploaded file with OCR
        This is the main function to call after file upload
        """
        file_path = Path(file_path)
        
        # Only process PDF files for now
        if file_path.suffix.lower() != '.pdf':
            return {
                'success': False,
                'error': f'OCR only supports PDF files, got: {file_path.suffix}',
                'text': '',
                'metadata': {}
            }
        
        return await self.ocr_pdf(str(file_path))

# Global OCR processor instance
client_ocr = ClientOCR()
