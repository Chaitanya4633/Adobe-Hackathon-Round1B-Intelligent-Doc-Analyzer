#!/usr/bin/env python3
"""
Document Intelligence Processor
Main orchestrator for the document intelligence system.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from .extractor import PDFExtractor
from .ranker import RelevanceRanker


class DocumentIntelligenceProcessor:
    """Main processor for document intelligence system."""
    
    def __init__(self):
        self.extractor = PDFExtractor()
        self.ranker = RelevanceRanker()
    
    def process_documents(self, pdf_paths: List[str], persona: str, 
                         job_to_be_done: str) -> Dict[str, Any]:
        """Process multiple PDF documents and extract relevant sections."""
        start_time = time.time()
        
        print(f"Starting document intelligence processing...")
        print(f"Persona: {persona}")
        print(f"Job-to-be-done: {job_to_be_done}")
        print(f"Processing {len(pdf_paths)} documents")
        
        all_sections = []
        input_files = []

        for i, pdf_path in enumerate(pdf_paths, 1):
            print(f"Processing document {i}/{len(pdf_paths)}: {Path(pdf_path).name}")
            
            try:
                pages_content = self.extractor.extract_text_from_pdf(pdf_path)
                
                if not pages_content:
                    print(f"  Warning: No content extracted from {pdf_path}")
                    continue

                sections = self.extractor.detect_sections(pages_content)
                all_sections.extend(sections)

                input_files.append({
                    'filename': Path(pdf_path).name,
                    'path': pdf_path,
                    'pages': len(pages_content),
                    'sections_found': len(sections)
                })
                
                print(f"  Extracted {len(sections)} sections from {len(pages_content)} pages")
                
            except Exception as e:
                print(f"  Error processing {pdf_path}: {e}")
                continue
        
        print(f"\nTotal sections extracted: {len(all_sections)}")
        
        if not all_sections:
            print("No sections found in any documents!")
            return self._create_empty_output(input_files, persona, job_to_be_done, start_time)

        print("Calculating relevance scores...")
        all_sections = self.ranker.calculate_relevance_scores(all_sections, persona, job_to_be_done)

        print("Extracting subsections...")
        subsections = self.extractor.extract_subsections(all_sections)
        subsections = self.ranker.rank_subsections(subsections)
        
        processing_time = round(time.time() - start_time, 2)
        print(f"Processing completed in {processing_time} seconds")
        
        output = {
            'metadata': {
                'input_files': input_files,
                'persona': persona,
                'job_to_be_done': job_to_be_done,
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': processing_time,
                'total_sections_found': len(all_sections),
                'total_documents': len(pdf_paths),
                'successful_documents': len(input_files)
            },
            'extracted_sections': [
                {
                    'document_name': section['document_name'],
                    'page_number': section['page_number'],
                    'section_title': section['section_title'],
                    'importance_rank': section['importance_rank'],
                    'relevance_score': round(section['relevance_score'], 4)
                }
                for section in all_sections[:15]  # Top 15 sections
            ],
            'subsection_analysis': [
                {
                    'document': subsection['document'],
                    'refined_text': subsection['refined_text'],
                    'page_number': subsection['page_number'],
                    'parent_section': subsection.get('parent_section', ''),
                    'relevance_score': round(subsection['relevance_score'], 4)
                }
                for subsection in subsections[:20]  
            ]
        }
        
        return output
    
    def _create_empty_output(self, input_files: List[Dict], persona: str, 
                           job_to_be_done: str, start_time: float) -> Dict[str, Any]:
        """Create empty output structure when no sections are found."""
        return {
            'metadata': {
                'input_files': input_files,
                'persona': persona,
                'job_to_be_done': job_to_be_done,
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': round(time.time() - start_time, 2),
                'total_sections_found': 0,
                'total_documents': len(input_files),
                'successful_documents': len(input_files)
            },
            'extracted_sections': [],
            'subsection_analysis': []
        }
    
    def save_output(self, output: Dict[str, Any], output_path: str) -> None:
        """Save the output to a JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to: {output_file}")