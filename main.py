#!/usr/bin/env python3
"""
Document Intelligence System - Main Entry Point
Extracts relevant sections from PDFs based on persona and job-to-be-done.
"""

import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.processor import DocumentIntelligenceProcessor


def main():
    """Main entry point for the document intelligence system."""
    parser = argparse.ArgumentParser(
        description='Document Intelligence System - Extract relevant PDF sections based on persona and job-to-be-done'
    )
    
    parser.add_argument(
        '--input-dir', 
        default='input', 
        help='Input directory containing PDF files (default: input)'
    )
    
    parser.add_argument(
        '--output-dir', 
        default='output', 
        help='Output directory for results (default: output)'
    )
    
    parser.add_argument(
        '--persona', 
        required=True, 
        help='Persona description (e.g., "Software Engineer working on ML projects")'
    )
    
    parser.add_argument(
        '--job-to-be-done', 
        required=True, 
        help='Job-to-be-done description (e.g., "Need to understand technical implementation details")'
    )
    
    parser.add_argument(
        '--max-docs', 
        type=int, 
        default=10, 
        help='Maximum number of documents to process (default: 10)'
    )
    
    args = parser.parse_args()
    input_path = Path(args.input_dir)
    if not input_path.exists():
        print(f"Error: Input directory '{input_path}' does not exist.")
        print("Please create the directory and add PDF files to process.")
        return 1

    print(f"Searching for PDF files in '{input_path}' and its subdirectories...")
    pdf_files = list(input_path.rglob('*.pdf'))
    
    if not pdf_files:
        print(f"Error: No PDF files found in '{input_path}' or its subdirectories.")
        print("Listing directory contents for debug:")
        for item in input_path.rglob('*'):
            print(f"  Found: {item} (is_dir: {item.is_dir()})")
        print("Please add PDF files (*.pdf) to the input directory or its subdirectories (e.g., Collection1).")
        return 1

    if len(pdf_files) > args.max_docs:
        print(f"Found {len(pdf_files)} PDFs, limiting to first {args.max_docs}")
        pdf_files = pdf_files[:args.max_docs]
    
    if len(pdf_files) < 3:
        print(f"Warning: Only {len(pdf_files)} PDF files found. System is optimized for 3-10 documents.")
    
    print(f"Processing {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"  - {pdf.name} (from {pdf.parent})")
    
    print(f"\nPersona: {args.persona}")
    print(f"Job-to-be-done: {args.job_to_be_done}")
    print("-" * 60)

    try:
        processor = DocumentIntelligenceProcessor()

        result = processor.process_documents(
            [str(f) for f in pdf_files],
            args.persona,
            args.job_to_be_done
        )

        output_path = Path(args.output_dir)
        output_path.mkdir(exist_ok=True)

        output_file = output_path / 'document_intelligence_output.json'
        processor.save_output(result, str(output_file))

        print("\n" + "=" * 60)
        print("PROCESSING SUMMARY")
        print("=" * 60)
        print(f"Processing time: {result['metadata']['processing_time_seconds']} seconds")
        print(f"Documents processed: {result['metadata']['successful_documents']}/{result['metadata']['total_documents']}")
        print(f"Total sections found: {result['metadata']['total_sections_found']}")
        print(f"Top sections extracted: {len(result['extracted_sections'])}")
        print(f"Subsections analyzed: {len(result['subsection_analysis'])}")

        if result['extracted_sections']:
            print(f"\nTOP 3 MOST RELEVANT SECTIONS:")
            for i, section in enumerate(result['extracted_sections'][:3], 1):
                print(f"{i}. {section['section_title'][:80]}...")
                print(f"   Document: {section['document_name']}, Page: {section['page_number']}")
                print(f"   Relevance Score: {section['relevance_score']:.4f}")
                print()
        
        print(f"Full results saved to: {output_file}")

        if result['metadata']['processing_time_seconds'] > 60:
            print("⚠️  Warning: Processing time exceeded 60 seconds target")
        else:
            print("✅ Processing completed within time constraints")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)