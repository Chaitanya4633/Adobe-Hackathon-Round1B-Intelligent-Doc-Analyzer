#!/usr/bin/env python3
"""
Relevance Ranker
Ranks sections based on persona and job-to-be-done using TF-IDF and cosine similarity.
"""

from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RelevanceRanker:
    """Ranks sections based on persona and job-to-be-done relevance."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
    
    def calculate_relevance_scores(self, sections: List[Dict[str, Any]], 
                                 persona: str, job_to_be_done: str) -> List[Dict[str, Any]]:
        """Calculate relevance scores based on persona and job-to-be-done."""
        if not sections:
            return sections
            
        # Combine persona and job description for relevance matching
        query_text = f"{persona} {job_to_be_done}"
        
        # Prepare texts for vectorization
        section_texts = [section['full_text'] for section in sections]
        all_texts = section_texts + [query_text]
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
          
            query_vector = tfidf_matrix[-1]
            section_vectors = tfidf_matrix[:-1]
            
            similarities = cosine_similarity(section_vectors, query_vector).flatten()

            for i, section in enumerate(sections):
                section['relevance_score'] = float(similarities[i])

            sections.sort(key=lambda x: x['relevance_score'], reverse=True)
            for i, section in enumerate(sections):
                section['importance_rank'] = i + 1
                
        except Exception as e:
            print(f"Error calculating relevance scores: {e}")
            for i, section in enumerate(sections):
                section['relevance_score'] = 0.0
                section['importance_rank'] = i + 1
        
        return sections
    
    def rank_subsections(self, subsections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank subsections by their relevance scores."""
        subsections.sort(key=lambda x: x['relevance_score'], reverse=True)
        return subsections
