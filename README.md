# Alternative Lifestyle AI

**A Personal AI for Alternative Diet, Looksmaxxing, Pharmacology, and Blackpill Knowledge**

> Bernard was right. The microbe is nothing, the terrain is everything.

## ⚠️ DISCLAIMER

**THIS IS A PERSONAL AI PROJECT.**

This AI is designed for **personal use** and provides information on alternative lifestyle topics including:
- Alternative diet and nutrition (primal, carnivore, terrain theory)
- Looksmaxxing and physical optimization
- Pharmacology and performance enhancement
- Blackpill philosophy and manosphere analysis
- Adult industry intelligence

**The views and information provided by this AI are NOT medical advice.**
**Consult a qualified healthcare professional before making any health-related decisions.**

**The AI acknowledges the existence of incel communities but does NOT endorse incel ideology.**
**It maintains a Faustian perspective: acknowledging struggle while emphasizing the attempt to improve rather than giving up.**

## Features

- **30+ Data Sources**: Websites, Reddit, Wikipedia, YouTube, Scribd, Social Media
- **Visual Knowledge Base**: Thousands of indexed images with category organization
- **Last Resort Handling**: Incel forums used only when primary sources are insufficient
- **Terminal Interface**: Full CLI support for local use
- **Web Interface**: Streamlit-based chat interface
- **API Server**: FastAPI for programmatic access
- **Image Support**: Download, store, and reference images in responses

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

## Usage

### Terminal AI (CLI)

```bash
# Interactive mode
python cli.py -i

# Single query
python cli.py "What is terrain theory?"

# With specific mode
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

## First Run Setup

```bash
# Crawl all sources
python crawler.py --max-pages 100

# Index the crawled data
python indexer.py
```

## Data Sources

This AI (internally named Blackpill Lifestyle AI) scrapes content from:
- **Diet**: aajonus.net, jackkruse.com, realmilk.com, raypeat.com, primaldiet.net, eatwild.com, nourishingourchildren.org
- **Looksmaxxing**: looksmaxxing.com, mewing.co, looksmax.gg, looksmax.org, forum.looksmaxxing.com
- **Blackpill**: theredarchive.com, incels.wiki, evolutionary.org, masculineprinciple.blogspot.com, harmonily.com, scientificsean.com/wiki
- **Incel Forums (Last Resort)**: incels.is, schaduw.net
- **Pharmacology**: examine.com, erowid.org
- **Bimbofication**: bimbolover.com, Instagram/Twitter
- **Fitness**: smartworkout.app
- **Research**: Earth.com, Skool.com, Nutria.onl
- **Adult Industry**: AVN Awards
- **Wikipedia**: 50+ pages
- **Reddit**: 24+ subreddits
- **YouTube**: 9+ channels
- **Scribd**: Key documents

## Philosophy

This AI operates on **Terrain Theory** principles:
- The microbe is nothing, the terrain is everything
- Genetics and biology are primary determinants
- Physical optimization through all available means
- Chemical optimization of human performance
- Alternative knowledge and unconventional approaches

**Blackpill Realism**: Acknowledges harsh truths while providing actionable information for those who choose to engage with reality.

**Faustian Approach**: When referencing difficult topics (including incel communities), the AI acknowledges the struggle but emphasizes the attempt to improve rather than giving up.

## Project Structure

```
Alternative-lifestyle-AI/
├── README.md                  # This file
├── LICENSE                    # MIT License
├── .gitignore
├── requirements.txt
├── config.py                  # All data source configurations
├── crawler.py                 # Multi-source web crawler
├── image_handler.py           # Image downloading and processing
├── social_media_scraper.py   # Instagram and Twitter scraper
├── scribd_parser.py           # Scribd document parser
├── visual_kb.py               # Visual knowledge base
├── retriever.py               # RAG retriever with last resort handling
├── generator.py               # Response generator
├── api.py                     # FastAPI server
├── web_interface.py           # Streamlit web interface
├── cli.py                     # Terminal AI interface
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── test.yml           # GitHub Actions
└── data/                      # Local data storage (gitignored)
    ├── vector_db/
    ├── images/
    └── visual_kb/
```

## Configuration

Edit `config.py` to:
- Add/remove data sources
- Adjust rate limits
- Change storage paths
- Configure API settings

## License

MIT License - Feel free to use, modify, and distribute.

## Contributing

This is a personal project. Contributions are welcome but will be evaluated based on alignment with the project's philosophy.

## Support

This is a **personal AI** with no official support. Use at your own risk.
