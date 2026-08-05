# START HERE - Alternative Lifestyle AI

## Quick Start (5 minutes)

### 1. Install Dependencies

Windows:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test the AI
```bash
python cli.py "What is terrain theory?"
```

### 3. Interactive Mode
```bash
python cli.py -i
```

Type 'quit' to exit.

---

## Full Setup (30-60 minutes)

### 1. Crawl Data
```bash
python crawler.py --max-pages 100
```

### 2. Index
```bash
python indexer.py
```

---

## Usage

### CLI
```bash
python cli.py -i           # Interactive
python cli.py "query"    # Single query
python cli.py --mode fast "q"  # Mode
python cli.py --no-last-resort "q"  # No incel forums
```

### Web
```bash
streamlit run web_interface.py
```

### API
```bash
uvicorn api:app --reload
```

---

## Features

- Hybrid Search (Dense + BM25)
- Recency Weighting
- Metadata Filters
- Last Resort Handling
- Grounded Claims
- Concrete Protocols
- Anti-Block Measures
- PubMed Connectors
- 40+ Multireddit Sources

---

## Configuration

Edit config.py for sources, RAG settings, Reddit OAuth.

---

## File Structure

See README.md for complete structure.

---

## Troubleshooting

- Module not found: Activate venv, pip install -r requirements.txt
- No torch: pip install torch
- Vector DB: Run crawler.py then indexer.py
- Reddit: Set REDDIT_CONFIG in config.py

---

## License

MIT License - Copyright 2026 AzulWEBG Foundation