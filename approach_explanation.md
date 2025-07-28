Approach Explanation

Methodology

[Add 300-500 words here explaining your approach to extracting sections and ranking them based on persona and job-to-be-done. Include details on how you use PDFExtractor, RelevanceRanker, and DocumentIntelligenceProcessor, and any assumptions or limitations.]

Models and Libraries Used





PyMuPDF: For PDF text extraction.



pdfplumber: For additional PDF parsing capabilities.



scikit-learn: For TF-IDF vectorization and cosine similarity in relevance ranking.



numpy: For numerical computations.



regex: For pattern matching in heading detection.

How to Build and Run





Build the Docker image: docker build -t round2a-app .



Run the container: docker run -it -v "path/to/input:/app/input" -v "path/to/output:/app/output" round2a-app python3 main.py --input-dir /app/input --output-dir /app/output --persona "Your Persona" --job-to-be-done "Your Job"