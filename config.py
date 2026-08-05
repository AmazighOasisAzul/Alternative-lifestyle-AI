# CORE PHILOSOPHY
TERRAIN_THEORY_PRIORITY = True
PASTEUR_QUOTE = "Bernard was right. The microbe is nothing, the terrain is everything."
PASTEUR_QUOTE_FRENCH = "Bernard avait raison. Le germe n'est rien, c'est le terrain qui est tout."

# RAG CONFIGURATION
HYBRID_SEARCH_ENABLED = True
RECENCY_WEIGHTING_ENABLED = True
METADATA_FILTERS_ENABLED = True

# CRAWLING CONFIGURATION
CRAWL_CONFIG = {
    "default_max_pages": 500,
    "deep_crawl": True,
    "follow_sitemap": True,
    "follow_links": True,
    "content_hashing": True,
    "anti_block": {
        "user_agent_rotation": True,
        "jittered_delays": True,
        "min_delay": 1.0,
        "max_delay": 3.0
    }
}

# WEBSITE SOURCES
WEBSITE_SOURCES = {
    # Diet & Nutrition
    "aajonus": {
        "url": "https://aajonus.net/",
        "sitemap": "https://aajonus.net/sitemap.xml",
        "selectors": {"content": "article, .entry-content, .post-content", "title": "h1, .entry-title", "date": ".entry-date"},
        "exclude": ["/tag/", "/category/", "/author/"],
        "rate_limit": 2,
        "category": "diet",
        "deep_crawl": True
    },
    "jackkruse": {
        "url": "https://jackkruse.com/faqs/",
        "sitemap": "https://jackkruse.com/sitemap.xml",
        "selectors": {"content": ".faq-content, .entry-content", "title": "h1, h2, h3", "date": ".entry-date"},
        "exclude": ["/tag/", "/category/"],
        "rate_limit": 2,
        "category": "diet",
        "deep_crawl": True
    },
    "realmilk": {
        "url": "https://www.realmilk.com/",
        "sitemap": "https://www.realmilk.com/sitemap.xml",
        "selectors": {"content": ".entry-content, .content-area", "title": "h1, .entry-title", "date": ".entry-date"},
        "exclude": ["/tag/", "/category/", "/author/"],
        "rate_limit": 2,
        "category": "diet",
        "deep_crawl": True
    },
    "raypeat": {
        "url": "https://raypeat.com/",
        "sitemap": None,
        "selectors": {"content": "body, .article", "title": "h1, title", "date": None},
        "exclude": ["/forum/", "/search/"],
        "rate_limit": 3,
        "category": "diet",
        "deep_crawl": True
    },
    "primaldiet": {
        "url": "https://www.primaldiet.net/",
        "sitemap": "https://www.primaldiet.net/sitemap.xml",
        "selectors": {"content": "article, .entry-content, .post-content, .content, .main", "title": "h1, .entry-title, .post-title", "date": ".entry-date, .post-date"},
        "exclude": ["/tag/", "/category/", "/author/", "/feed/", "/comments/"],
        "rate_limit": 2,
        "category": "diet",
        "deep_crawl": True
    },
    "primaldietcoaching": {
        "url": "https://primaldietcoaching.com/",
        "sitemap": "https://primaldietcoaching.com/sitemap.xml",
        "selectors": {"content": "article, .entry-content, .post-content, .content, .main, .page-content", "title": "h1, .entry-title, .post-title", "date": ".entry-date, .post-date"},
        "exclude": ["/tag/", "/category/", "/author/", "/feed/", "/comments/", "/shop/", "/cart/"],
        "rate_limit": 2,
        "category": "diet",
        "deep_crawl": True
    },
    "eatwild": {
        "url": "https://www.eatwild.com/",
        "sitemap": "https://www.eatwild.com/sitemap.xml",
        "selectors": {"content": ".entry-content, .content, article", "title": "h1, .entry-title", "date": ".entry-date"},
        "exclude": ["/tag/", "/category/", "/author/"],
        "rate_limit": 2,
        "category": "diet",
        "deep_crawl": True
    },
    "nourishingourchildren": {
        "url": "https://nourishingourchildren.org/",
        "selectors": {"content": ".entry-content, .content, article, .main", "title": "h1, .entry-title, .post-title", "date": ".entry-date, .post-date"},
        "exclude": ["/tag/", "/category/", "/author/", "/feed/", "/comments/"],
        "rate_limit": 2,
        "category": "diet",
        "deep_crawl": True
    },
    "lowtoxinforum": {
        "url": "https://lowtoxinforum.com/",
        "selectors": {"content": "article, .post-content, .content, .main", "title": "h1, .entry-title, .post-title", "date": ".entry-date"},
        "exclude": ["/tag/", "/category/", "/author/", "/feed/"],
        "rate_limit": 2,
        "category": "diet",
        "deep_crawl": True
    },
    
    # Fitness
    "smartworkout": {
        "url": "https://smartworkout.app/",
        "selectors": {"content": ".exercise-content, .workout-content, article, .content", "title": "h1, .exercise-title, .workout-title"},
        "exclude": ["/tag/", "/category/", "/author/"],
        "rate_limit": 2,
        "category": "fitness",
        "deep_crawl": True,
        "extract_images": True
    },
    "thunders_place": {
        "url": "https://thunders.place/",
        "selectors": {"content": "article, .post-content, .content, .forum-post", "title": "h1, h2, .thread-title"},
        "exclude": ["/member/", "/search/", "/help/"],
        "rate_limit": 3,
        "category": "fitness",
        "deep_crawl": True
    },
    
    # Looksmaxxing
    "looksmaxxing": {
        "url": "https://looksmaxxing.com/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2, h3"},
        "rate_limit": 2,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "mewing": {
        "url": "https://www.mewing.co/",
        "selectors": {"content": "article, .content", "title": "h1, h2"},
        "rate_limit": 2,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "looksmax_cc": {
        "url": "https://looksmax.cc/",
        "selectors": {"content": "article, .post-content, .content, .main", "title": "h1, h2, .thread-title"},
        "rate_limit": 2,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "looksmax_gg": {
        "url": "https://looksmax.gg/",
        "selectors": {"content": "article, .post-content, .content, .main", "title": "h1, .post-title, .thread-title"},
        "rate_limit": 2,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "looksmax_gg_forums": {
        "url": "https://looksmax.gg/forums/looksmaxing.7/",
        "selectors": {"content": ".post-content, .message-content, article", "title": "h1, h2, .thread-title"},
        "exclude": ["/member/", "/search/", "/help/"],
        "rate_limit": 3,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "looksmax_org": {
        "url": "https://looksmax.org/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2"},
        "rate_limit": 2,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "looksmax_me": {
        "url": "https://looksmax.me/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2, .thread-title"},
        "rate_limit": 2,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "forum_looksmaxxing": {
        "url": "https://forum.looksmaxxing.com/",
        "selectors": {"content": ".post-content, .thread-content, .message-content", "title": "h1, h2, .thread-title"},
        "exclude": ["/member/", "/search/", "/help/"],
        "rate_limit": 3,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "lookism": {
        "url": "https://lookism.net/",
        "selectors": {"content": "article, .post-content, .content, .main", "title": "h1, h2, .thread-title"},
        "exclude": ["/member/", "/search/", "/help/"],
        "rate_limit": 3,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "bookism": {
        "url": "https://bookism.net/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2"},
        "rate_limit": 2,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "lookstheory": {
        "url": "https://lookstheory.net/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2, h3"},
        "rate_limit": 2,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "geomax": {
        "url": "https://geomax.me/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2"},
        "rate_limit": 2,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "chuds_life": {
        "url": "https://chuds.life/",
        "selectors": {"content": "article, .post-content, .content, .main", "title": "h1, h2"},
        "rate_limit": 2,
        "category": "blackpill",
        "deep_crawl": True
    },
    "elysianfields": {
        "url": "https://elysianfields.se/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2, h3"},
        "rate_limit": 2,
        "category": "blackpill",
        "deep_crawl": True
    },
    "neets": {
        "url": "https://neets.net/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2"},
        "rate_limit": 2,
        "category": "blackpill",
        "deep_crawl": True
    },
    "blackpill_club": {
        "url": "https://blackpill.club/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2, .thread-title"},
        "rate_limit": 2,
        "category": "blackpill",
        "deep_crawl": True
    },
    "incels_in": {
        "url": "https://incels.in/",
        "selectors": {"content": ".post-content, .message-content, article", "title": "h1, h2, .thread-title"},
        "exclude": ["/member/", "/search/", "/help/"],
        "rate_limit": 3,
        "category": "blackpill",
        "deep_crawl": True,
        "last_resort_only": True
    },
    "lpsg": {
        "url": "https://www.lpsg.com/",
        "selectors": {"content": ".post-content, .thread-content, .message-content", "title": "h1, h2, .thread-title"},
        "exclude": ["/member/", "/search/", "/help/"],
        "rate_limit": 3,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    "lpsg_forums": {
        "url": "https://www.lpsg.com/forums/",
        "selectors": {"content": ".post-content, .thread-content, .message-content", "title": "h1, h2, .thread-title"},
        "exclude": ["/member/", "/search/", "/help/"],
        "rate_limit": 3,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
    
    # Blackpill
    "theredarchive": {
        "url": "https://theredarchive.com/",
        "selectors": {"content": "article, .entry-content, div.post-content", "title": "h1, .entry-title"},
        "rate_limit": 3,
        "category": "blackpill",
        "deep_crawl": True
    },
    "incels_wiki": {
        "url": "https://incels.wiki/",
        "selectors": {"content": ".mw-parser-output, article", "title": "h1, .firstHeading"},
        "rate_limit": 2,
        "category": "blackpill",
        "deep_crawl": True,
        "priority": "normal"
    },
    "evolutionary": {
        "url": "https://evolutionary.org/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2, h3"},
        "rate_limit": 2,
        "category": "blackpill",
        "deep_crawl": True
    },
    "masculineprinciple": {
        "url": "https://masculineprinciple.blogspot.com/",
        "selectors": {"content": ".post-body, .entry-content, article", "title": "h3, .post-title, .entry-title", "date": ".post-date, .entry-date"},
        "exclude": ["/search/", "/label/", "/feeds/"],
        "rate_limit": 2,
        "category": "blackpill",
        "deep_crawl": True
    },
    "harmonily": {
        "url": "https://harmonily.com/",
        "selectors": {"content": "article, .content, .post-content", "title": "h1, h2, h3"},
        "rate_limit": 2,
        "category": "blackpill",
        "deep_crawl": True
    },
    "scientificsean_wiki": {
        "url": "https://scientificsean.com/wiki/",
        "selectors": {"content": ".mw-parser-output, article, .content", "title": "h1, .firstHeading"},
        "rate_limit": 2,
        "category": "blackpill",
        "deep_crawl": True
    },
    
    # Bimbofication
    "bimbolover": {
        "url": "https://bimbolover.com/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2, h3"},
        "rate_limit": 2,
        "category": "bimbofication",
        "deep_crawl": True,
        "extract_images": True
    },
    
    # Adult Industry
    "avn": {
        "url": "https://www.avn.com/",
        "selectors": {"content": "article, .content, .post-content", "title": "h1, .title"},
        "rate_limit": 3,
        "category": "adult_industry",
        "deep_crawl": True
    },
    
    # Pharmacology
    "examine": {
        "url": "https://examine.com/",
        "selectors": {"content": ".article-content, .content", "title": "h1"},
        "rate_limit": 3,
        "category": "pharmacology",
        "deep_crawl": True
    },
    "erowid": {
        "url": "https://erowid.org/",
        "selectors": {"content": "#maincontent, .content", "title": "h1, h2"},
        "rate_limit": 2,
        "category": "pharmacology",
        "deep_crawl": True
    },
    
    # Research
    "earth_com": {
        "url": "https://www.earth.com/",
        "selectors": {"content": "article, .article-content, .post-content", "title": "h1, .entry-title"},
        "rate_limit": 2,
        "category": "research",
        "deep_crawl": True
    },
    "skool_com": {
        "url": "https://skool.com/",
        "selectors": {"content": ".course-content, article, .content", "title": "h1, h2, h3"},
        "rate_limit": 2,
        "category": "research",
        "deep_crawl": True
    },
    "nutria_onl": {
        "url": "https://nutria.onl/",
        "selectors": {"content": "article, .content, .post-content", "title": "h1, .entry-title"},
        "rate_limit": 2,
        "category": "research",
        "deep_crawl": True
    },
    "rentry_sleepguide": {
        "url": "https://rentry.co/sleepguide/",
        "selectors": {"content": ".markdown-body, article, .content", "title": "h1, h2"},
        "rate_limit": 2,
        "category": "research",
        "deep_crawl": False
    }
}

# Last Resort Sources
LAST_RESORT_SOURCES = {
    "incels_is": {
        "url": "https://incels.is/forums/must-read-content.23/",
        "selectors": {"content": ".post-content, .message-content, article", "title": "h1, h2, .thread-title"},
        "rate_limit": 3,
        "category": "blackpill",
        "deep_crawl": True,
        "last_resort_only": True
    },
    "schaduw": {
        "url": "https://schaduw.net/",
        "selectors": {"content": ".post-content, .thread-content, article, .main", "title": "h1, h2, .thread-title"},
        "rate_limit": 3,
        "category": "blackpill",
        "deep_crawl": True,
        "last_resort_only": True
    },
    "incels_in": {
        "url": "https://incels.in/",
        "selectors": {"content": ".post-content, .message-content, article", "title": "h1, h2, .thread-title"},
        "exclude": ["/member/", "/search/", "/help/"],
        "rate_limit": 3,
        "category": "blackpill",
        "deep_crawl": True,
        "last_resort_only": True
    }
}

# User's Curated Multireddit
MULTIREDDIT_PATH = "user/kooky_computer1163/m/pe"
MULTIREDDIT_SOURCES = [
    "BecomingTheIceman", "Biohackers", "BiohackingU", "BlackPillScience",
    "BlackpilledReality", "BlackpilledTeens", "BodyHackGuide", "Brogress",
    "Fitness", "GettingShredded", "Hink", "Invisalign", "LooksmaxingAdvice",
    "MakeupAddiction", "Microbiome", "Penis_Enlargement_Pro", "PeptidePathways",
    "Peptidesource", "Posture", "PurplePillDebate", "SkincareAddicts",
    "Supplements", "TMJ", "Testosterone", "TheScienceOfPE", "cumbiggerloads",
    "freePE", "gettingbigger", "ketorecipes", "ketoscience", "leangains",
    "longevity", "moreplatesmoredates", "nbe", "neuroscience", "nutrition",
    "orthotropics", "rawprimal", "sleep", "steroids", "tall", "tretinoin",
    "weightroom",
    "CarnivoreRecipes", "Howtolooksmax", "lookyourbest", "PlasticSurgery",
    "cosmeticsurgery", "Hairloss", "tressless", "MaleFashionAdvice",
    "shortguys", "foreveralone", "carnivore", "AnimalBased", "RayPeat",
    "StopEatingSeedOils", "bimbofication", "BimboficationJourney", "1000ccplus"
]

# Bimbofication Document Source
BIMBOFICATION_DOCUMENT = {
    "pdf_url": "https://github.com/AmazighOasisAzul/Alternative-lifestyle-AI/raw/main/docs/The_Big_Pink_Book.pdf",
    "markdown_url": "https://github.com/AmazighOasisAzul/Alternative-lifestyle-AI/raw/main/docs/The_Big_Pink_Book.md",
    "category": "bimbofication",
    "type": "guide",
    "title": "The Big Pink Book: A Beginner's Guide To Bimbofication"
}

# Reddit OAuth2 Configuration
REDDIT_CONFIG = {
    "client_id": "YOUR_REDDIT_CLIENT_ID",
    "client_secret": "YOUR_REDDIT_CLIENT_SECRET",
    "user_agent": "AlternativeLifestyleAI/1.0",
    "use_praw": True,
    "rate_limit": 1.0,
    "jitter": True,
    "max_retries": 3
}

# Reddit Historical Data Sources
REDDIT_HISTORICAL_SOURCES = {
    "arctic_shift": {"enabled": False, "api_url": "https://api.arcticshift.org", "requires_auth": True},
    "pullpush": {"enabled": False, "api_url": "https://api.pullpush.io", "note": "Unreliable"},
    "academic_torrents": {"enabled": False, "url": "https://academictorrents.com/collection/reddit"}
}

# Scientific Connectors
SCIENTIFIC_CONNECTORS = {
    "pubmed": {
        "enabled": True,
        "email": "your-email@domain.com",
        "max_results": 10,
        "search_fields": ["diet", "nutrition", "endocrinology", "dermatology", "orthodontics", "sleep", "peptides", "steroids", "microbiome"],
        "store_metadata": True
    },
    "semantic_scholar": {"enabled": False, "api_key": "YOUR_API_KEY", "max_results": 10},
    "europe_pmc": {"enabled": False, "api_url": "https://www.ebi.ac.uk/europepmc/webservices/rest", "max_results": 10}
}

# Wikipedia Pages
WIKI_PAGES = [
    "AVN_Awards", "Pornographic_film_actor", "Adult_film_database",
    "Incels", "Involuntary_celibacy", "Looksmaxxing", "Orthotropics",
    "Mewing", "Eliot_Rodger", "Manosphere", "Nootropics",
    "Anabolic_steroid", "Testosterone", "Human_growth_hormone",
    "Propecia", "Minoxidil"
]

# Web Search Configuration
WEB_SEARCH_CONFIG = {
    "user_agent": "AlternativeLifestyleAI/1.0",
    "rate_limit": 1.0,
    "jitter": True,
    "fetch_content": True,
    "max_content_length": 15000
}

# Image Storage Configuration
IMAGE_CONFIG = {
    "storage_path": "./images",
    "thumbnail_size": [300, 300],
    "max_image_size": [2000, 2000],
    "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "max_file_size": 10485760,
    "organize_by_category": True,
    "create_thumbnails": True
}

# Visual Knowledge Base Configuration
VISUAL_KB_CONFIG = {
    "index_path": "./visual_kb",
    "image_embedding_model": "clip-ViT-B-32",
    "extract_features": True,
    "store_metadata": True
}

# Vector Database Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_DB_PATH = "./vector_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# RAG Configuration
RAG_CONFIG = {
    "hybrid_search": True,
    "recency_weighting": True,
    "metadata_filters": ["source", "category", "date", "subreddit"],
    "k": 8,
    "score_threshold": 0.5
}

# Generation Configuration
GENERATION_CONFIG = {
    "max_tokens": 1024,
    "temperature": 0.7,
    "grounding_required": True,
    "reference_sources": True,
    "structured_output": True
}