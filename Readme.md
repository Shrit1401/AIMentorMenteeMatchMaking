# Mentor-Mentee Matching System

An AI-based mentor-mentee matching system that uses semantic similarity to match mentees with the most suitable mentors based on research domain and subdomain compatibility.

## Features

- **Intelligent Matching**: Uses semantic embeddings (sentence-transformers) to find the best mentor for each mentee
- **Confidence Scoring**: Provides a 0-100 confidence score for each match based on domain and subdomain similarity
- **Top-K Rankings**: Generates top-3 (configurable) mentor recommendations per mentee
- **Multiple Interfaces**:
  - Command-line interface (CLI) for batch processing
  - REST API endpoint for programmatic access
- **Robust Fallback**: Uses TF-IDF similarity if semantic embeddings fail

## How It Works

### Matching Logic

The system matches mentees to mentors using a two-tier scoring approach:

1. **Domain Matching** (Base Score: 70 points)
   - If the research domain matches exactly (case-insensitive), the base score is 70
   - If domains don't match, the score is 0 and no match is made

2. **Subdomain Similarity** (Additional Score: up to 30 points)
   - Uses semantic similarity via sentence-transformers (`all-MiniLM-L6-v2`) to compare subdomains
   - Falls back to TF-IDF cosine similarity if embeddings fail
   - Similarity score (0-1) is multiplied by 30 and added to the base score
   - Final score is capped at 100

### Scoring Method

The confidence score is calculated as follows:

```
if domain_match:
    base_score = 70
    subdomain_similarity = semantic_similarity(mentee.subdomain, mentor.subdomain)
    additional_score = subdomain_similarity * 30
    final_score = min(70 + additional_score, 100)
else:
    final_score = 0
```

**Subdomain Similarity Thresholds:**

- **≥ 0.75**: "Same or very similar subdomain" (high confidence)
- **0.4 - 0.75**: "Related subdomain" (medium confidence)
- **< 0.4**: "Different subdomain" (low confidence)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:

```bash
git clone https://github.com/Shrit1401/AIMentorMenteeMatchMaking.git
cd mentormentee
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

**Note**: The first run will download the sentence-transformers model (`all-MiniLM-L6-v2`) automatically, which may take a few minutes.

## Usage

### Command-Line Interface (CLI)

Run the matching system with default settings:

```bash
python main.py
```

This will:

- Load mentees from `data/mentees.csv`
- Load mentors from `data/mentors.csv`
- Generate matches and save results to `output/`

#### Custom Options

```bash
python main.py --mentees <path_to_mentees.csv> --mentors <path_to_mentors.csv> --out <output_directory> --top-k <number>
```

**Arguments:**

- `--mentees`: Path to mentees CSV file (default: `data/mentees.csv`)
- `--mentors`: Path to mentors CSV file (default: `data/mentors.csv`)
- `--out`: Output directory for results (default: `output`)
- `--top-k`: Number of top mentors to rank per mentee (default: 3)

**Example:**

```bash
python main.py --mentees data/mentees.csv --mentors data/mentors.csv --out results --top-k 5
```

### REST API

Start the FastAPI server:

```bash
cd api
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`

#### API Endpoint

**POST `/match`**

Match one or more mentees with mentors.

**Request Body:**

```json
[
  {
    "name": "Aanya N",
    "college": "MIT BLR",
    "research_domain": "AI",
    "subdomain": "Computer Vision"
  }
]
```

**Response:**

```json
[
  {
    "mentee_name": "Aanya N",
    "matches": [
      {
        "mentor_name": "Dr. Sharma",
        "confidence_score": 100,
        "reason": "Same domain (AI) and Same or very similar subdomain"
      },
      {
        "mentor_name": "Prof. Sengupta",
        "confidence_score": 84,
        "reason": "Same domain (AI) and Related subdomain"
      },
      {
        "mentor_name": "Dr. Banerjee",
        "confidence_score": 80,
        "reason": "Same domain (AI) and Different subdomain"
      }
    ]
  }
]
```

**API Documentation:**

- Interactive docs: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Input Data Format

### Mentees CSV (`data/mentees.csv`)

```csv
name,college,research_domain,subdomain
Aanya N,MIT BLR,AI,Computer Vision
Rohit K,NITK,Cybersecurity,Network Security
```

### Mentors CSV (`data/mentors.csv`)

```csv
name,college,research_domain,subdomain
Dr. Sharma,IITM,AI,Computer Vision
Ms. Rao,IIST,Cybersecurity,Cryptography
```

**Required Columns:**

- `name`: Name of the mentee/mentor
- `college`: Institution name
- `research_domain`: Main research area (e.g., AI, Healthcare, Cybersecurity)
- `subdomain`: Specific research focus within the domain

## Output Format

The system generates two CSV files:

### 1. `result.csv` - Best Match Per Mentee

```csv
mentee_name,mentor_name,confidence_score,reason
Aanya N,Dr. Sharma,100,Same domain (AI) and Same or very similar subdomain
Rohit K,Dr. Kulkarni,100,Same domain (Cybersecurity) and Same or very similar subdomain
```

### 2. `top3.csv` (or `top{k}.csv`) - Top-K Rankings

```csv
mentee_name,rank,mentor_name,confidence_score,reason
Aanya N,1,Dr. Sharma,100,Same domain (AI) and Same or very similar subdomain
Aanya N,2,Prof. Sengupta,84,Same domain (AI) and Related subdomain
Aanya N,3,Dr. Banerjee,80,Same domain (AI) and Different subdomain
```

## Project Structure

```
mentormentee/
├── api/
│   └── app.py              # FastAPI application
├── data/
│   ├── mentees.csv        # Input: mentee data
│   └── mentors.csv        # Input: mentor data
├── output/
│   ├── result.csv         # Output: best matches
│   └── top3.csv          # Output: top-3 rankings
├── src/
│   ├── loadData.py        # CSV loading utilities
│   ├── matcher.py         # Matching logic
│   └── scoring.py         # Scoring and similarity functions
├── main.py                # CLI entry point
├── requirements.txt       # Python dependencies
└── Readme.md             # This file
```

## Dependencies

- `pandas`: Data manipulation and CSV handling
- `scikit-learn`: TF-IDF vectorization and cosine similarity
- `sentence-transformers`: Semantic embeddings for subdomain matching
- `fastapi`: REST API framework
- `uvicorn`: ASGI server for FastAPI

## Technical Details

### Semantic Similarity

The system uses `all-MiniLM-L6-v2` from sentence-transformers, a lightweight model optimized for semantic similarity tasks. It encodes subdomain text into dense vectors and computes cosine similarity between them.

### Fallback Mechanism

If semantic embeddings fail (e.g., due to network issues or model loading errors), the system automatically falls back to TF-IDF-based cosine similarity, ensuring robustness.

### Performance

- Processing time: ~1-2 seconds per mentee (including model inference)
- Memory usage: ~500MB (includes loaded model)
- Scalability: Handles hundreds of mentees/mentors efficiently

## Example Output

Running the system with the provided sample data produces matches like:

- **Aanya N** (AI, Computer Vision) → **Dr. Sharma** (AI, Computer Vision) - Score: 100
- **Rohit K** (Cybersecurity, Network Security) → **Dr. Kulkarni** (Cybersecurity, Network Security) - Score: 100
- **Rahul D** (AI, Large Language Models) → **Dr. Iyer** (AI, Natural Language Processing) - Score: 83
