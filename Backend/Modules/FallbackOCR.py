"""
Fallback OCR using pypdf for basic PDF text extraction
Used when the advanced OCR client is not available
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

class FallbackOCR:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF using pypdf as fallback"""
        try:
            if not PYPDF_AVAILABLE:
                return {
                    'success': False,
                    'error': 'pypdf not available. Please install: pip install pypdf',
                    'text': '',
                    'metadata': {}
                }
            
            text_content = []
            metadata = {
                'pages': 0,
                'total_text_length': 0,
                'extraction_method': 'pypdf_fallback'
            }
            
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                metadata['pages'] = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            text_content.append(f"--- Page {page_num} ---\n{page_text}")
                    except Exception as e:
                        self.logger.warning(f"Error extracting page {page_num}: {e}")
                        text_content.append(f"--- Page {page_num} ---\n[Error extracting text from this page]")
            
            full_text = "\n".join(text_content)
            metadata['total_text_length'] = len(full_text)
            
            return {
                'success': True,
                'text': full_text,
                'metadata': metadata
            }
            
        except Exception as e:
            self.logger.error(f"PDF extraction error: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'metadata': {}
            }
    
    def save_extracted_text(self, file_path: str, extracted_data: Dict[str, Any]) -> Optional[str]:
        """Save extracted text to a .txt file alongside the original file"""
        try:
            if not extracted_data.get('success', False):
                return None
            
            # Create text file path
            original_path = Path(file_path)
            text_file_path = original_path.with_suffix('.txt')
            
            # Save extracted text
            with open(text_file_path, 'w', encoding='utf-8') as f:
                f.write(f"EXTRACTED TEXT FROM: {original_path.name}\n")
                f.write("=" * 50 + "\n\n")
                f.write(extracted_data['text'])
                
                # Add metadata
                if extracted_data.get('metadata'):
                    f.write(f"\n\n--- METADATA ---\n")
                    for key, value in extracted_data['metadata'].items():
                        f.write(f"{key}: {value}\n")
            
            self.logger.info(f"Extracted text saved to: {text_file_path}")
            return str(text_file_path)
            
        except Exception as e:
            self.logger.error(f"Error saving extracted text: {e}")
            return None

# Global fallback OCR processor instance
fallback_ocr = FallbackOCR()
