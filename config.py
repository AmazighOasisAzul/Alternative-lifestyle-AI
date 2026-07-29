# CORE PHILOSOPHY
TERRAIN_THEORY_PRIORITY = True
PASTEUR_QUOTE = "Bernard was right. The microbe is nothing, the terrain is everything."
PASTEUR_QUOTE_FRENCH = "Bernard avait raison. Le germe n'est rien, c'est le terrain qui est tout."

# ALL SOURCES - Comprehensive alternative knowledge
SOURCES = {
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
    "smartworkout": {
        "url": "https://smartworkout.app/",
        "selectors": {"content": ".exercise-content, .workout-content, article, .content", "title": "h1, .exercise-title, .workout-title"},
        "exclude": ["/tag/", "/category/", "/author/"],
        "rate_limit": 2,
        "category": "fitness",
        "deep_crawl": True,
        "extract_images": True
    },
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
    "looksmax_gg": {
        "url": "https://looksmax.gg/",
        "selectors": {"content": "article, .post-content, .content, .main", "title": "h1, .post-title, .thread-title"},
        "rate_limit": 2,
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
    "bimbolover": {
        "url": "https://bimbolover.com/",
        "selectors": {"content": "article, .post-content, .content", "title": "h1, h2, h3"},
        "rate_limit": 2,
        "category": "bimbofication",
        "deep_crawl": True,
        "extract_images": True
    },
    "forum_looksmaxxing": {
        "url": "https://forum.looksmaxxing.com/",
        "selectors": {"content": ".post-content, .thread-content, .message-content", "title": "h1, h2, .thread-title"},
        "exclude": ["/member/", "/search/", "/help/"],
        "rate_limit": 3,
        "category": "looksmaxxing",
        "deep_crawl": True
    },
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
    },
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
    "avn": {
        "url": "https://www.avn.com/",
        "selectors": {"content": "article, .content, .post-content", "title": "h1, .title"},
        "rate_limit": 3,
        "category": "adult_industry",
        "deep_crawl": True
    },
    "incels_is": {
        "url": "https://incels.is/forums/must-read-content.23/",
        "selectors": {"content": ".post-content, .message-content, article", "title": "h1, h2, .thread-title"},
        "rate_limit": 3,
        "category": "blackpill",
        "deep_crawl": True,
        "priority": "last_resort",
        "last_resort_only": True
    },
    "schaduw": {
        "url": "https://schaduw.net/",
        "selectors": {"content": ".post-content, .thread-content, article, .main", "title": "h1, h2, .thread-title"},
        "rate_limit": 3,
        "category": "blackpill",
        "deep_crawl": True,
        "priority": "last_resort",
        "last_resort_only": True
    }
}

SOCIAL_MEDIA_SOURCES = {
    "instagram": {
        "accounts": ["bimbofication", "looksmaxxing", "mewing", "orthotropics", "primal_diet", "carnivore_diet"],
        "category": "bimbofication",
        "extract_images": True,
        "extract_videos": True
    },
    "twitter": {
        "accounts": ["BlackPillScience", "LooksMaxxing", "MewingScience", "PrimalDiet", "CarnivoreDiet"],
        "category": "blackpill",
        "extract_images": True,
        "extract_videos": True
    }
}

SCRIBD_DOCUMENTS = [
    {"url": "https://www.scribd.com/document/.../The-Art-of-Frame", "title": "The Art of Frame", "category": "blackpill"},
    {"url": "https://www.scribd.com/document/.../Bonesmashing-Guide", "title": "Bonesmashing Guide", "category": "looksmaxxing"}
]

REDDIT_SOURCES = {
    "bimbofication": {"subreddit": "BimboficationJourney", "category": "looksmaxxing", "limit": 1000},
    "looksmaxxing": {"subreddit": "looksmaxxing", "category": "looksmaxxing", "limit": 1000},
    "incels": {"subreddit": "incels", "category": "blackpill", "limit": 1000},
    "blackpillscience": {"subreddit": "BlackPillScience", "category": "blackpill", "limit": 1000}
}

ADDITIONAL_REDDIT_SOURCES = {
    "redpill": {"subreddit": "TheRedPill", "category": "blackpill", "limit": 1000},
    "blackpill": {"subreddit": "BlackPill", "category": "blackpill", "limit": 1000},
    "looksmax": {"subreddit": "looksmax", "category": "looksmaxxing", "limit": 1000},
    "mewing": {"subreddit": "mewing", "category": "looksmaxxing", "limit": 1000},
    "orthotropics": {"subreddit": "orthotropics", "category": "looksmaxxing", "limit": 1000},
    "incel": {"subreddit": "incel", "category": "blackpill", "limit": 1000},
    "mgtow": {"subreddit": "MGTOW", "category": "blackpill", "limit": 1000},
    "mgtow2": {"subreddit": "MGTOW2", "category": "blackpill", "limit": 1000},
    "femaleleveluprstrategy": {"subreddit": "FemaleLevelUpStrategy", "category": "blackpill", "limit": 1000},
    "femaledatingstrategy": {"subreddit": "FemaleDatingStrategy", "category": "blackpill", "limit": 1000},
    "asktrp": {"subreddit": "askTRP", "category": "blackpill", "limit": 1000},
    "marriagedredd": {"subreddit": "MarriageDredd", "category": "blackpill", "limit": 1000},
    "deadbedrooms": {"subreddit": "DeadBedrooms", "category": "blackpill", "limit": 1000},
    "whereareallthegoodmen": {"subreddit": "whereareallthegoodmen", "category": "blackpill", "limit": 1000},
    "pussypassdenied": {"subreddit": "PussyPassDenied", "category": "blackpill", "limit": 1000},
    "twoxchromosomes": {"subreddit": "TwoXChromosomes", "category": "blackpill", "limit": 1000},
    "thebluepill": {"subreddit": "TheBluePill", "category": "blackpill", "limit": 1000},
    "braincels": {"subreddit": "Braincels", "category": "blackpill", "limit": 1000},
    "inceltears": {"subreddit": "IncelTears", "category": "blackpill", "limit": 1000},
    "trufemcels": {"subreddit": "TruFemcels", "category": "blackpill", "limit": 1000},
    "femcels": {"subreddit": "Femcels", "category": "blackpill", "limit": 1000}
}

WIKI_PAGES = [
    "AVN_Awards", "Pornographic_film_actor", "Adult_film_database", "Incels",
    "Involuntary_celibacy", "Looksmaxxing", "Orthotropics", "Mewing", "Eliot_Rodger",
    "Manosphere", "Nootropics", "Anabolic_steroid", "Testosterone",
    "Human_growth_hormone", "Propecia", "Minoxidil"
]

WEB_SEARCH_CONFIG = {
    "pubmed_email": "your-email@domain.com",
    "max_results": 8,
    "user_agent": "AlternativeLifestyleAI/1.0",
    "rate_limit": 1.0,
    "fetch_content": True,
    "max_content_length": 15000
}

IMAGE_CONFIG = {
    "storage_path": "./images",
    "thumbnail_size": [300, 300],
    "max_image_size": [2000, 2000],
    "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "max_file_size": 10485760,
    "organize_by_category": True,
    "create_thumbnails": True
}

VISUAL_KB_CONFIG = {
    "index_path": "./visual_kb",
    "image_embedding_model": "clip-ViT-B-32",
    "extract_features": True,
    "store_metadata": True
}

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_DB_PATH = "./vector_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200