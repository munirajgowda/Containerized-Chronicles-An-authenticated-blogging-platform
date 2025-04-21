from django.db import models
from django.contrib.auth.models import User

# Keyword mapping for automatic category assignment
CATEGORY_KEYWORDS = {
    "Technology": [
        "AI", "machine learning", "tech", "software", "hardware", "gadgets", "innovation", 
        "robotics", "virtual reality", "augmented reality", "automation", "big data", "cloud computing", 
        "5G", "internet of things", "smart devices", "cybersecurity", "data science", "quantum computing", 
        "blockchain", "digital transformation", "electronics", "programming", "tech startup", "AI models", 
        "computing", "wearables", "drones", "autonomous vehicles", "IoT", "computational neuroscience"
    ],
    "Health": [
        "fitness", "well-being", "diet", "exercise", "mental health", "nutrition", "lifestyle", "yoga", 
        "medications", "doctor", "wellness", "healthcare", "workout", "chronic illness", "sleep", 
        "stress management", "immune system", "weight loss", "mental wellness", "health tips", "therapy", 
        "rehabilitation", "alternative medicine", "fitness tracker", "detox", "mindfulness", "nutritionist", 
        "bodybuilding", "physical therapy", "health insurance", "medical research", "organic foods", "herbal"
    ],
    "Finance": [
        "stocks", "investment", "economy", "cryptocurrency", "savings", "retirement", "personal finance", 
        "wealth management", "financial planning", "insurance", "mutual funds", "financial advisor", 
        "real estate", "bonds", "dividends", "taxes", "financial markets", "capital gains", "debt", "loans", 
        "mortgage", "credit", "financial freedom", "trading", "forex", "econometrics", "budgeting", "crowdfunding", 
        "cryptocurrency trading", "venture capital", "fintech", "stocks market", "financial crisis"
    ],
    "Business": [
        "entrepreneurship", "startup", "management", "marketing", "leadership", "innovation", "finance", "growth", 
        "business strategy", "corporate", "B2B", "branding", "productivity", "small business", "teamwork", 
        "negotiation", "operations", "supply chain", "customer service", "customer experience", "mergers", "business model", 
        "digital marketing", "sales", "retail", "partnership", "consulting", "business development", "networking", 
        "startups", "business growth", "human resources", "corporate culture", "investors", "scaling"
    ],
    "Education": [
        "learning", "teaching", "school", "university", "online courses", "distance learning", "education technology", 
        "education system", "e-learning", "curriculum", "student", "academic", "study", "homework", "study tips", 
        "classroom", "virtual classrooms", "tutoring", "teachers", "schooling", "research", "higher education", 
        "scholarship", "college", "study abroad", "campus life", "learning resources", "SAT", "academic performance", 
        "online learning", "student loans", "degree programs", "literacy", "school projects"
    ],
    "Lifestyle": [
        "fashion", "wellness", "travel", "home decor", "relationships", "family", "culture", "self-care", "shopping", 
        "hobbies", "beauty", "luxury", "interior design", "style", "fitness", "minimalism", "vlogging", "sustainable living", 
        "mindfulness", "mental clarity", "well-being", "living well", "personal development", "fashion trends", 
        "accessories", "home organization", "luxury lifestyle", "personal growth", "creative expression", "urban lifestyle", 
        "self-love", "adventure", "beauty tips", "healthy habits"
    ],
    "Travel": [
        "destinations", "vacation", "tourism", "adventure", "sightseeing", "explore", "wanderlust", "road trips", 
        "backpacking", "holiday", "travel guides", "solo travel", "tourist attractions", "beach resorts", "cruises", 
        "nature trips", "sustainable travel", "culture trips", "airlines", "budget travel", "luxury travel", 
        "eco-tourism", "travel tips", "destinations", "expedition", "food tours", "group travel", "travel blog", 
        "road trips", "adventure tourism", "holiday destinations", "staycations", "volunteering"
    ],
    "Food": [
        "recipes", "cooking", "nutrition", "foodie", "restaurants", "diet", "healthy eating", "gourmet", 
        "vegetarian", "vegan", "organic", "baking", "grilling", "barbecue", "cooking tips", "meals", "food photography", 
        "chef", "ingredients", "meal prep", "desserts", "snacks", "food culture", "wine", "coffee", "sweets", 
        "international cuisine", "street food", "sustainable food", "food trends", "home cooking", "gourmet dishes", 
        "food blog", "food delivery", "restaurants reviews"
    ],
    "Entertainment": [
        "movies", "TV shows", "music", "celebrities", "pop culture", "theater", "video games", "streaming", 
        "concerts", "film industry", "actors", "directors", "film festivals", "gaming", "TV series", "movies reviews", 
        "musicals", "television", "entertainment news", "comedy", "music videos", "live shows", "pop culture", 
        "blockbusters", "game releases", "indie films", "gigs", "red carpet", "viral videos", "streaming platforms"
    ],
    "Sports": [
        "soccer", "basketball", "football", "tennis", "athletics", "fitness", "gym", "sports news", "Olympics", 
        "rugby", "baseball", "hockey", "cricket", "athletes", "sports events", "tournaments", "stadium", "sports leagues", 
        "track and field", "motorsports", "extreme sports", "swimming", "cycling", "fitness goals", "sports training", 
        "personal best", "championships", "coaching", "e-sports", "sports betting"
    ],
    "Science": [
        "physics", "biology", "chemistry", "space", "research", "laboratory", "scientific discoveries", 
        "innovation", "astronomy", "genetics", "biotechnology", "evolution", "neuroscience", "earth science", 
        "environmental science", "scientific method", "space exploration", "climate science", "medicine", "geology", 
        "robotics", "chemistry experiments", "AI research", "math", "quantum physics", "medical research", "genomic studies"
    ],
    "Art": [
        "painting", "sculpture", "visual arts", "drawing", "exhibitions", "artists", "creativity", "art history", 
        "art gallery", "oil painting", "watercolor", "portraiture", "abstract art", "modern art", "classical art", 
        "art techniques", "art museums", "photography", "installation art", "digital art", "art criticism", 
        "art collection", "canvas", "design", "artistic expression", "art community"
    ],
    "Environment": [
        "climate change", "sustainability", "pollution", "green energy", "recycling", "wildlife", "nature", 
        "conservation", "environmental impact", "ecosystem", "renewable energy", "climate action", "carbon footprint", 
        "ocean conservation", "biodiversity", "sustainable living", "natural resources", "greenhouse gases", 
        "environmental policy", "clean energy", "eco-friendly", "deforestation", "alternative energy", "nature reserves"
    ],
    "Politics": [
        "elections", "government", "policy", "laws", "international relations", "democracy", "politicians", 
        "news", "political parties", "presidency", "legislation", "voting", "election campaigns", "political debate", 
        "global politics", "foreign policy", "political activism", "political reform", "political discourse", 
        "human rights", "democratic process", "corruption", "international organizations", "political parties"
    ],
    "History": [
        "ancient civilizations", "world wars", "historical figures", "events", "timeline", "archaeology", "discoveries", 
        "historical documents", "empire", "medieval", "historical societies", "revolutions", "historical museums", 
        "war history", "ancient history", "history books", "artifacts", "historical research", "famous leaders", 
        "civilizations", "historical sites", "timeline of events", "historical periods", "historical studies"
    ],
    "Technology Trends": [
        "gadgets", "smartphones", "IoT", "cloud computing", "blockchain", "big data", "5G", "tech news", 
        "technology innovations", "artificial intelligence", "augmented reality", "virtual reality", "future tech", 
        "mobile apps", "wearables", "data analytics", "cybersecurity", "smart homes", "automation", "digital transformation"
    ],
    "Gaming": [
        "video games", "esports", "gaming community", "consoles", "PC gaming", "game development", "gaming events", 
        "game reviews", "game trailers", "VR games", "gaming consoles", "multiplayer", "MMORPG", "RPG", 
        "strategy games", "indie games", "game industry", "game mods", "streaming games", "gaming culture"
    ],
    "Music": [
        "rock", "pop", "jazz", "hip-hop", "classical", "concerts", "albums", "artists", "music festivals", 
        "songs", "music videos", "musicians", "genres", "pop music", "indie music", "soundtracks", "live music", 
        "musical instruments", "songs releases", "music reviews", "band", "recording artist", "producer", "album release"
    ],
    "Parenting": [
        "children", "parenting tips", "family", "parenthood", "babies", "education", "baby care", "new parents", 
        "parenting advice", "child development", "family life", "parenting styles", "discipline", "infants", 
        "parenting blog", "family activities", "positive parenting", "parenting skills", "school readiness"
    ],
    "Automotive": [
        "cars", "vehicles", "electric vehicles", "motorcycle", "auto industry", "car reviews", "driving tips", 
        "road safety", "car models", "test drive", "car maintenance", "car repairs", "car accessories", 
        "auto technology", "self-driving cars", "SUV", "sports car", "auto sales", "car dealership", "electric car", "hybrid"
    ],
    "DIY & Crafts": [
        "crafting", "handmade", "DIY projects", "home improvement", "decorating", "knitting", "sewing", 
        "embroidery", "painting", "woodworking", "upcycling", "handmade gifts", "scrapbooking", "DIY crafts", 
        "home decor", "DIY repairs", "creative projects", "craft supplies", "DIY home decor", "arts and crafts", 
        "DIY tutorial"
    ]
}

# Models
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name

STATUS_CHOICE = (
    ('draft', 'Draft'),
    ('published', 'Published')
)

class Blogs(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_image = models.ImageField(upload_to='uploads/%y/%m/%d')
    short_description = models.TextField()
    blog_body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default='draft')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'blogs'

    def __str__(self):
        return self.title

    def assign_category(self):
        category_match = None
        highest_match_count = 0

        for category_name, keywords in CATEGORY_KEYWORDS.items():
            match_count = sum(1 for keyword in keywords if keyword.lower() in self.blog_body.lower())

            if match_count > highest_match_count:
                highest_match_count = match_count
                category_match = Category.objects.filter(category_name=category_name).first()

        return category_match

    def save(self, *args, **kwargs):
        if not self.category:
            self.category = self.assign_category()
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

