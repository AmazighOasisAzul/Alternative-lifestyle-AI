# START HERE – Alternative Lifestyle AI

**Supported platforms: Windows and Mac only**

## Main way to open the AI

1. Download the ZIP from the green **Code** button -> extract the folder
2. Run the install script for your OS:
   - **Windows**: double-click `install_and_run.bat`
   - **Mac**: right-click `install_and_run.sh` -> Open (or run it in Terminal)
3. The script creates a virtual environment, installs dependencies, and launches the terminal AI.

That is the intended first-run path.

## Manual steps (if the script fails)

```bash
cd Alternative-lifestyle-AI-main   # or the name of the extracted folder
python -m venv venv

# Windows
venv\Scripts\activate

# Mac
source venv/bin/activate

pip install -r requirements.txt
python cli.py -i
```

## Optional: first data crawl + index

```bash
python crawler.py --max-pages 200
python indexer.py
```

Then run `python cli.py -i` again.

## Notes
- There is no standalone .exe yet. The install scripts are the current entry point.
- UI work is separate and not required for this step.
- Private Reddit communities only work if the authenticated account is already a member and OAuth credentials are set in config.