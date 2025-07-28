ractor.py
#!/usr/bin/env python3
"""
PDF Text and Section Extractor
Extracts text content and identifies sections from PDF documents.
"""

import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import fitz  
import pdfplumber
import numpy as np


class PDFExtractor:
    """Extracts text content and sections from PDF documents."""
    
    def __init__(self):
        self.heading_patterns = [
            r'^\d+\.?\s+',  
            r'^\d+\.\d+\.?\s+', 
            r'^\d+\.\d+\.\d+\.?\s+',  
            r'^[IVXLCDM]+\.?\s+',  
            r'^[A-Z]\. ',  
            r'^\([a-z]\)\s+',  
            r'^Chapter\s+\d+',  
            r'^Section\s+\d+',  
        ]
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract text content with page numbers and structure."""
        pages_content=[]
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        chars = page.chars
                        font_sizes = [char.get('size', 12) for char in chars if char.get('size')]
                        avg_font_size = np.mean(font_sizes) if font_sizes else 12
                        pages_content.append({
                            'page_number': page_num,
                            'text': text.strip(),
                            'avg_font_size': avg_font_size,
                            'chars': chars,
                            'source_file': pdf_path
                        })
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            
        return pages_content
    
    def detect_sections(self, pages_content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect sections and subsections from PDF content."""
        sections = []
        
        for page_data in pages_content:
            page_num = page_data['page_number']
            text = page_data['text']
            avg_font_size = page_data['avg_font_size']
            chars = page_data.get('chars', [])
            source_file = page_data.get('source_file', '')
            
            # Split text into lines
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line or len(line) < 3:
                    continue
                    
                # Check if line is a potential heading
                if self.is_heading(line, chars, avg_font_size):
                    # Extract surrounding context (next few lines)
                    context_lines = []
                    for j in range(i + 1, min(i + 6, len(lines))):
                        if lines[j].strip():
                            context_lines.append(lines[j].strip())
                    
                    context = ' '.join(context_lines)
                    
                    sections.append({
                        'document_name': Path(source_file).name,
                        'page_number': page_num,
                        'section_title': line,
                        'content': context,
                        'full_text': line + ' ' + context,
                        'importance_rank': 0,  # Will be calculated later
                        'relevance_score': 0.0
                    })
        
        return sections
    
    def is_heading(self, line: str, chars: List[Dict], avg_font_size: float) -> bool:
        """Determine if a line is likely a heading."""
        if len(line) > 200:
            return False
        
        for pattern in self.heading_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return True

        words = line.split()
        if len(words) > 1 and len(words) < 15:
            title_case_words = sum(1 for word in words if word and word[0].isupper())
            if title_case_words / len(words) > 0.6:
                return True

        if line.isupper() and len(line) < 100:
            return True
            
        return False
    
    def extract_subsections(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract subsections from the content of main sections."""
        subsections = []
        
        for section in sections[:10]:  
            content = section['content']

            sentences = re.split(r'[.!?]+', content)
            sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
            
            for sentence in sentences[:3]:  
                if len(sentence) > 30:  
                    subsections.append({
                        'document': section['document_name'],
                        'refined_text': sentence,
                        'page_number': section['page_number'],
                        'parent_section': section['section_title'],
                        'relevance_score': section['relevance_score'] * 0.8
                    })
        
        return subsections