#!/usr/bin/env python3
"""
Freelancer Tools - Automated Product Generator
Erstellt täglich neue Landing Pages mit Nischen-Produkten
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path

# Nischen-Datenbank mit Bedarf aber geringem Angebot
NICHES = [
    {
        "name": "Freelancer Steuer-Tracker",
        "description": "UStVa-Tracker, Vorauszahlungen, Kleinunternehmer-Limit",
        "price": 47,
        "category": "Steuern",
        "target_audience": "Freelancer, Selbstständige",
        "features": [
            "UStVa automatisch tracken",
            "Vorauszahlungen nie vergessen",
            "Kleinunternehmer-Limit Warnung",
            "Excel-Import & DATEV-Export"
        ],
        "pain_points": [
            "Steuerchaos",
            "Vorauszahlungen vergessen",
            "Keine Übersicht",
            "Steuerberater zu teuer"
        ],
        "type": "own"
    },
    {
        "name": "Rechnungs-Generator Pro",
        "description": "Professionelle Rechnungsvorlagen mit Automatisierung",
        "price": 37,
        "category": "Rechnungen",
        "target_audience": "Freelancer, Agenturen",
        "features": [
            "10 professionelle Vorlagen",
            "Automatische Nummerierung",
            "Kundenverwaltung",
            "DATEV-Export"
        ],
        "pain_points": [
            "Rechnungen manuell schreiben",
            "Keine Vorlagen",
            "Fehler in Rechnungen",
            "Zeitverschwendung"
        ],
        "type": "own"
    },
    {
        "name": "Content-Kalender für Freelancer",
        "description": "30-Tage Social Media Content Plan",
        "price": 27,
        "category": "Marketing",
        "target_audience": "Freelancer, Solopreneure",
        "features": [
            "30 vorgefertigte Posts",
            "LinkedIn, Instagram, Twitter",
            "Hashtag-Strategie",
            "Engagement-Tipps"
        ],
        "pain_points": [
            "Keine Zeit für Social Media",
            "Weiß nicht was posten",
            "Keine Strategie",
            "Keine Sichtbarkeit"
        ],
        "type": "own"
    },
    {
        "name": "Freelancer Preiskalkulator",
        "description": "Berechne deinen idealen Stundensatz",
        "price": 17,
        "category": "Preisgestaltung",
        "target_audience": "Freelancer, Anfänger",
        "features": [
            "Automatische Berechnung",
            "Lebenshaltungskosten berücksichtigt",
            "Marktvergleich",
            "Verhandlungs-Tipps"
        ],
        "pain_points": [
            "Zu niedrige Preise",
            "Weiß nicht wie kalkulieren",
            "Vergleich mit Konkurrenz",
            "Verhandlungsunsicherheit"
        ],
        "type": "own"
    },
    {
        "name": "Freelancer Vertragsvorlagen",
        "description": "5 rechtssichere Vertragsvorlagen",
        "price": 37,
        "category": "Rechtliches",
        "target_audience": "Freelancer, Berater",
        "features": [
            "Projektvertrag",
            "Retainer-Vertrag",
            "NDA",
            "AGB",
            "Datenschutzerklärung"
        ],
        "pain_points": [
            "Keine Verträge",
            "Rechtliche Unsicherheit",
            "Keine Absicherung",
            "Anwaltskosten zu hoch"
        ],
        "type": "own"
    },
    {
        "name": "Finanz-Dashboard für Freelancer",
        "description": "Gewinn/Verlust, Cashflow, Prognosen",
        "price": 67,
        "category": "Finanzen",
        "target_audience": "Freelancer, Agenturen",
        "features": [
            "Gewinn/Verlust Berechnung",
            "Cashflow Prognose",
            "Rentabilität pro Projekt",
            "Steuern-Rücklagen Planer"
        ],
        "pain_points": [
            "Keine Finanzübersicht",
            "Weiß nicht ob profitabel",
            "Keine Prognosen",
            "Steuer-Überraschungen"
        ],
        "type": "own"
    },
    {
        "name": "Freelancer Masterclass",
        "description": "5-Modul Video-Kurs zu Steuern & Finanzen",
        "price": 97,
        "category": "Bildung",
        "target_audience": "Alle Freelancer",
        "features": [
            "5 Video-Module",
            "Workbooks",
            "Templates",
            "Lifetime Access"
        ],
        "pain_points": [
            "Keine Steuer-Kenntnisse",
            "Angst vor Fehler",
            "Keine Optimierung",
            "Zu viele Fragen"
        ],
        "type": "own"
    },
    {
        "name": "Notion Template: Projekt-Management",
        "description": "Komplettes Projekt-Management System in Notion",
        "price": 29,
        "category": "Produktivität",
        "target_audience": "Freelancer, Teams",
        "features": [
            "Kanban Board",
            "Timeline View",
            "Client Management",
            "Time Tracking"
        ],
        "pain_points": [
            "Zu viele Tools",
            "Keine Übersicht",
            "Projekte vergessen",
            "Zeitverschwendung"
        ],
        "type": "own"
    },
    {
        "name": "Email-Vorlagen für Freelancer",
        "description": "50 professionelle Email-Vorlagen",
        "price": 19,
        "category": "Kommunikation",
        "target_audience": "Freelancer, Anfänger",
        "features": [
            "Angebot-Emails",
            "Rechnungs-Emails",
            "Follow-up Emails",
            "Absage-Emails"
        ],
        "pain_points": [
            "Unprofessionelle Emails",
            "Keine Vorlagen",
            "Schreib-Blockade",
            "Zu lange Emails"
        ],
        "type": "own"
    },
    {
        "name": "LinkedIn Profile Optimizer",
        "description": "Optimiere dein LinkedIn Profil für mehr Anfragen",
        "price": 39,
        "category": "Marketing",
        "target_audience": "Freelancer, B2B",
        "features": [
            "Headline Optimierung",
            "Bio-Schreib-Anleitung",
            "Content-Strategie",
            "Engagement-Tipps"
        ],
        "pain_points": [
            "Keine LinkedIn-Anfragen",
            "Schlechtes Profil",
            "Keine Strategie",
            "Keine Sichtbarkeit"
        ],
        "type": "own"
    }
]

# Affiliate-Produkte (mit echten Links)
AFFILIATE_PRODUCTS = [
    {
        "name": "Stripe Account Setup",
        "description": "Kompletter Guide zum Stripe Setup",
        "price": 0,
        "affiliate_link": "https://stripe.com",
        "commission": 0.05,
        "type": "affiliate"
    },
    {
        "name": "Notion Pro",
        "description": "Upgrade zu Notion Pro für unbegrenzte Blöcke",
        "price": 10,
        "affiliate_link": "https://notion.so",
        "commission": 0.10,
        "type": "affiliate"
    }
]

def generate_landing_page(product):
    """Generiere eine Landing Page für ein Produkt"""
    
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product['name']} - Freelancer Tools</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
        }}
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 20px;
        }}
        header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }}
        .feature {{
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .feature h3 {{
            margin-bottom: 10px;
            color: #667eea;
        }}
        .pricing {{
            background: #f8f9fa;
            padding: 60px 20px;
            text-align: center;
            margin: 60px 0;
        }}
        .price {{
            font-size: 3em;
            color: #667eea;
            margin: 20px 0;
        }}
        .cta {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 15px 40px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 1.1em;
            margin: 20px 0;
            transition: background 0.3s;
        }}
        .cta:hover {{
            background: #764ba2;
        }}
        footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 30px 20px;
            margin-top: 60px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{product['name']}</h1>
            <p>{product['description']}</p>
        </div>
    </header>

    <div class="container">
        <section class="features">
            <h2 style="grid-column: 1/-1; margin: 30px 0; font-size: 2em;">Features</h2>
"""
    
    for feature in product['features']:
        html += f"""            <div class="feature">
                <h3>✓ {feature}</h3>
            </div>
"""
    
    html += f"""        </section>

        <section class="pricing">
            <h2>Jetzt kaufen</h2>
            <div class="price">€{product['price']}</div>
            <p>Einmalige Zahlung • Lifetime Access</p>
            <a href="#" class="cta">Jetzt kaufen</a>
        </section>
    </div>

    <footer>
        <p>&copy; 2026 Freelancer Tools. Alle Rechte vorbehalten.</p>
        <p><a href="#" style="color: white;">Datenschutz</a> | <a href="#" style="color: white;">Impressum</a></p>
    </footer>
</body>
</html>"""
    
    return html

def create_product_directory(product, base_path="/home/ubuntu/freelancer-tools-system/products"):
    """Erstelle ein Verzeichnis für ein Produkt"""
    
    # Erstelle Verzeichnis
    product_path = Path(base_path) / product['name'].lower().replace(" ", "-")
    product_path.mkdir(parents=True, exist_ok=True)
    
    # Schreibe HTML
    html_file = product_path / "index.html"
    html_file.write_text(generate_landing_page(product))
    
    # Schreibe Metadaten
    metadata = {
        "name": product['name'],
        "description": product['description'],
        "price": product['price'],
        "category": product['category'],
        "target_audience": product['target_audience'],
        "created": datetime.now().isoformat(),
        "type": product['type']
    }
    
    metadata_file = product_path / "metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
    
    return product_path

def generate_daily_product():
    """Generiere ein zufälliges Produkt des Tages"""
    
    product = random.choice(NICHES)
    product_path = create_product_directory(product)
    
    print(f"✅ Produkt erstellt: {product['name']}")
    print(f"📁 Pfad: {product_path}")
    print(f"💰 Preis: €{product['price']}")
    print(f"🎯 Zielgruppe: {product['target_audience']}")
    
    return product_path

def generate_all_products():
    """Generiere alle Produkte"""
    
    base_path = "/home/ubuntu/freelancer-tools-system/products"
    Path(base_path).mkdir(parents=True, exist_ok=True)
    
    for product in NICHES:
        create_product_directory(product, base_path)
        print(f"✅ {product['name']}")

if __name__ == "__main__":
    print("🚀 Freelancer Tools - Product Generator")
    print("=" * 50)
    
    # Generiere alle Produkte
    generate_all_products()
    
    print("\n✅ Alle Produkte erstellt!")
