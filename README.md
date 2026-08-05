# Alternative Lifestyle AI

**A Personal AI for Alternative Diet, Looksmaxxing, Pharmacology, and Blackpill Knowledge**

> Bernard was right. The microbe is nothing, the terrain is everything.

## DISCLAIMER

THIS IS A PERSONAL AI PROJECT.

This AI is designed for personal use and provides information on alternative lifestyle topics including:
- Alternative diet and nutrition (primal, carnivore, terrain theory)
- Looksmaxxing and physical optimization
- Pharmacology and performance enhancement
- Blackpill philosophy and manosphere analysis
- Adult industry intelligence

The views and information provided by this AI are NOT medical advice.
Consult a qualified healthcare professional before making any health-related decisions.

The AI acknowledges the existence of incel communities but does NOT endorse incel ideology.
It maintains a Faustian perspective: acknowledging struggle while emphasizing the attempt to improve rather than giving up.

## Features

- 40+ Data Sources: Websites, Reddit, Wikipedia, YouTube, Scribd, Social Media, PubMed
- Visual Knowledge Base: Thousands of indexed images with category organization
- Last Resort Handling: Incel forums used only when primary sources are insufficient
- Terminal Interface: Full CLI support for local use
- Web Interface: Streamlit-based chat interface
- API Server: FastAPI for programmatic access
- Image Support: Download, store, and reference images in responses
- Hybrid Search: Dense vector + BM25 keyword search
- Recency Weighting: Time-based relevance decay (half-life: 365 days, 20% weight)
- Metadata Filters: Filter by source, category, date, subreddit
- Grounded Generation: All claims backed by source references
- Reddit OAuth2: PRAW-based authentication with configurable credentials
- Multireddit Support: Auto-extract from user/kooky_computer1163/m/pe/
- Anti-Block Measures: User-agent rotation, jittered delays (1-3s), exponential backoff
- PubMed Connector: DOI, title, abstract, year, key findings extraction
- Structured Output: Protocols, checkpoints, risk notes in responses

## Quick Start

See START_HERE.md for comprehensive setup instructions.

## Installation

### Option 1: pip install (Recommended)

```bash
git clone https://github.com/AmazighOasisAzul/Alternative-lifestyle-AI.git
cd Alternative-lifestyle-AI
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Option 2: Direct Download

Download the repository as a ZIP file and extract it.

### Option 3: One-Click Install

Windows: Run install.bat
Linux/macOS: Run install.sh

## Usage

### Terminal AI (CLI)

```bash
# Interactive mode
python cli.py -i

# Single query
python cli.py "What is terrain theory?"

# Deep mode
python cli.py --mode deep "Explain the blackpill"

# Disable last resort sources
python cli.py --no-last-resort "Tell me about looksmaxxing"
```

### Web Interface

```bash
streamlit run web_interface.py
```

Then open http://localhost:8501 in your browser.

### API Server

```bash
uvicorn api:app --reload
```

Then send POST requests to http://localhost:8000/query

### Run Scripts

Windows: Run run.bat
Linux/macOS: Run run.sh

## First Run Setup

```bash
# Crawl all sources
python crawler.py --max-pages 100

# Index the crawled data
python indexer.py
```

## Data Sources

This AI (internally named Blackpill Lifestyle AI) scrapes content from:

### Diet & Nutrition
- aajonus.net
- jackkruse.com
- realmilk.com
- raypeat.com
- primaldiet.net
- eatwild.com
- nourishingourchildren.org

### Looksmaxxing
- looksmaxxing.com
- mewing.co
- looksmax.gg
- looksmax.org
- forum.looksmaxxing.com

### Blackpill & Manosphere
- theredarchive.com
- incels.wiki
- evolutionary.org
- masculineprinciple.blogspot.com
- harmonily.com
- scientificsean.com/wiki

### Incel Forums (LAST RESORT ONLY)
- incels.is/forums/must-read-content.23/
- schaduw.net

### Pharmacology
- examine.com
- erowid.org

### Bimbofication
- bimbolover.com
- Instagram (social media scraper)
- Twitter/X (social media scraper)

### Fitness
- smartworkout.app

### Research
- Earth.com
- Skool.com
- Nutria.onl
- PubMed (scientific papers)

### Adult Industry
- AVN Awards

### Social Media
- Scribd (document parser)

### Knowledge Bases
- Wikipedia: 50+ pages
- Reddit: 40+ subreddits
- YouTube: 9+ channels

## Technical Implementation

### RAG System
- Hybrid Search: ChromaDB (dense vectors) + rank_bm25 (keyword)
- Recency Weighting: Exponential decay with configurable half-life
- Metadata Filters: Source, category, date, subreddit filtering
- DualModeRetriever: Primary + last resort source separation

### Crawling & Scraping
- Reddit OAuth2 via PRAW
- Multireddit auto-extraction
- Anti-block: UA rotation, jittered delays, exponential backoff
- Image extraction and organization by category
- Scribd document parsing
- Social media scraping (Instagram, Twitter)

### Visual Knowledge Base
- Image indexing with metadata
- Category-based organization
- ChromaDB integration for visual search

### Generation
- Grounded claims with source references required
- Structured output: protocols, checkpoints, risk notes
- Faustian approach to sensitive topics
- NO Debate Mode

## Project Structure

Alternative-lifestyle-AI/
├── README.md                    # Project overview
├── START_HERE.md                # Comprehensive setup guide
├── LICENSE                      # MIT License
├── .gitignore
├── requirements.txt
├── config.py                    # All data source configurations
├── crawler.py                   # Multi-source web crawler
├── image_handler.py             # Image downloading and processing
├── social_media_scraper.py     # Instagram and Twitter scraper
├── scribd_parser.py             # Scribd document parser
├── visual_kb.py                 # Visual knowledge base
├── retriever.py                 # RAG retriever with last resort handling
├── generator.py                 # Response generator
├── api.py                       # FastAPI server
├── web_interface.py             # Streamlit web interface
├── cli.py                       # Terminal AI interface
├── indexer.py                   # Data indexer
├── Dockerfile
├── docker-compose.yml
├── install.bat                  # Windows one-click install
├── install.sh                   # Linux/macOS one-click install
├── run.bat                      # Windows run script
├── run.sh                       # Linux/macOS run script
├── .github/
│   └── workflows/
│       └── test.yml             # GitHub Actions
└── data/                        # Local data storage (gitignored)
    ├── vector_db/
    ├── images/
    └── visual_kb/

## Configuration

Edit config.py to:
- Add/remove data sources
- Adjust rate limits
- Change storage paths
- Configure API settings
- Set Reddit OAuth2 credentials
- Configure PubMed connector
- Adjust hybrid search weights
- Modify recency weighting parameters

## Philosophy

This AI operates on Terrain Theory principles:
- The microbe is nothing, the terrain is everything
- Genetics and biology are primary determinants
- Physical optimization through all available means
- Chemical optimization of human performance
- Alternative knowledge and unconventional approaches

Blackpill Realism: Acknowledges harsh truths while providing actionable information for those who choose to engage with reality.

Faustian Approach: When referencing difficult topics (including incel communities), the AI acknowledges the struggle but emphasizes the attempt to improve rather than giving up.

## License

MIT License - Feel free to use, modify, and distribute.

## Contributing

This is a personal project. Contributions are welcome but will be evaluated based on alignment with the project's philosophy.

## Support

This is a personal AI with no official support. Use at your own risk.