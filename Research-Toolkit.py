#!/usr/bin/env python3
"""
Research Toolkit
Topic Monitor • Reddit Trend Hunter • Sentiment Checker • Personal Brand Tracker • Content Ideas
"""

from duckduckgo_search import DDGS
from datetime import datetime
import time
import textwrap

# ============================================
# Einstellungen
# ============================================
MAX_RESULTS = 10
DELAY = 1.3


def clear():
    print("\n" * 2)


def search_web(query: str, max_results: int = MAX_RESULTS, news: bool = False):
    results = []
    with DDGS() as ddgs:
        if news:
            for r in ddgs.news(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "snippet": r.get("body"),
                    "date": r.get("date"),
                    "source": "News"
                })
        else:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body"),
                    "source": "Web"
                })
    return results


def print_results(results: list, title: str = "Results"):
    if not results:
        print("No results found.")
        return

    print(f"\n{'='*70}")
    print(f"  {title} ({len(results)})")
    print('='*70)

    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['title']}")
        print(f"   Source: {r.get('source', 'Web')}")
        if r.get("date"):
            print(f"   Date:   {r['date']}")
        print(f"   URL:    {r['url']}")
        print(f"   → {r['snippet'][:280]}{'...' if len(r.get('snippet','')) > 280 else ''}")


# ============================================
# 1. Topic Monitor
# ============================================
def topic_monitor():
    clear()
    print("="*60)
    print("  TOPIC MONITOR")
    print("="*60)
    query = input("\nTopic eingeben: ").strip()
    if not query:
        return

    print("\n→ Lade aktuelle News...")
    news = search_web(query, max_results=8, news=True)
    time.sleep(DELAY)

    print("→ Lade Web-Ergebnisse...")
    web = search_web(query, max_results=8)
    time.sleep(DELAY)

    print("→ Lade Twitter/X Mentions...")
    twitter = search_web(f"site:twitter.com OR site:x.com {query}", max_results=6)

    print_results(news, f"Latest News about '{query}'")
    print_results(web, f"Web Results about '{query}'")
    print_results(twitter, f"Twitter/X Mentions about '{query}'")


# ============================================
# 2. Reddit Trend Hunter
# ============================================
def reddit_trend_hunter():
    clear()
    print("="*60)
    print("  REDDIT TREND HUNTER")
    print("="*60)
    query = input("\nThema oder Subreddit-Keyword: ").strip()
    if not query:
        return

    print("\n→ Suche heiße Reddit-Posts...")
    results = search_web(f"site:reddit.com {query}", max_results=12)
    print_results(results, f"Hot Reddit Posts about '{query}'")


# ============================================
# 3. Sentiment Checker (einfach & oberflächlich)
# ============================================
def sentiment_checker():
    clear()
    print("="*60)
    print("  SENTIMENT CHECKER (Surface Level)")
    print("="*60)
    query = input("\nThema eingeben: ").strip()
    if not query:
        return

    print("\n→ Sammle aktuelle Aussagen...")
    results = search_web(query, max_results=15)
    time.sleep(DELAY)
    results += search_web(query, max_results=8, news=True)

    positive_words = ["good", "great", "love", "excellent", "amazing", "best", "positive", "win", "success",
                      "gut", "super", "toll", "liebe", "beste", "positiv", "erfolg", "stark"]
    negative_words = ["bad", "hate", "terrible", "worst", "awful", "fail", "negative", "problem", "scam",
                      "schlecht", "hasse", "schrecklich", "problem", "betrug", "negativ", "kritisch"]

    pos = neg = neutral = 0

    for r in results:
        text = (r.get("title", "") + " " + r.get("snippet", "")).lower()
        p = sum(1 for w in positive_words if w in text)
        n = sum(1 for w in negative_words if w in text)

        if p > n:
            pos += 1
        elif n > p:
            neg += 1
        else:
            neutral += 1

    total = pos + neg + neutral
    if total == 0:
        print("Keine Daten gefunden.")
        return

    print(f"\n{'='*50}")
    print(f"  Sentiment Analysis for: '{query}'")
    print(f"{'='*50}")
    print(f"Positive : {pos:3d}  ({pos/total*100:.1f}%)")
    print(f"Negative : {neg:3d}  ({neg/total*100:.1f}%)")
    print(f"Neutral  : {neutral:3d}  ({neutral/total*100:.1f}%)")
    print(f"{'='*50}")

    if pos > neg * 1.5:
        print("→ Overall Sentiment: Clearly Positive")
    elif neg > pos * 1.5:
        print("→ Overall Sentiment: Clearly Negative")
    else:
        print("→ Overall Sentiment: Mixed / Neutral")


# ============================================
# 4. Personal Brand Tracker
# ============================================
def personal_brand_tracker():
    clear()
    print("="*60)
    print("  PERSONAL BRAND TRACKER")
    print("="*60)
    name = input("\nDein Name / Username / Brand: ").strip()
    if not name:
        return

    print("\n→ Suche Erwähnungen...")
    web = search_web(name, max_results=8)
    time.sleep(DELAY)
    news = search_web(name, max_results=6, news=True)
    time.sleep(DELAY)
    twitter = search_web(f"site:twitter.com OR site:x.com \"{name}\"", max_results=6)

    print_results(news, f"News Mentions of '{name}'")
    print_results(web, f"Web Mentions of '{name}'")
    print_results(twitter, f"Twitter/X Mentions of '{name}'")


# ============================================
# 5. Content Idea Generator
# ============================================
def content_idea_generator():
    clear()
    print("="*60)
    print("  CONTENT IDEA GENERATOR")
    print("="*60)
    topic = input("\nThema eingeben: ").strip()
    if not topic:
        return

    print("\n→ Analysiere aktuelle Diskussionen...")
    results = search_web(topic, max_results=12)
    time.sleep(DELAY)
    results += search_web(f"{topic} 2025 OR 2026", max_results=6)
    results += search_web(f"site:reddit.com {topic}", max_results=6)

    print(f"\n{'='*70}")
    print(f"  Content Ideas for: '{topic}'")
    print('='*70)

    ideas = [
        f"Warum {topic} gerade so wichtig ist",
        f"Die größten Irrtümer über {topic}",
        f"Wie man mit {topic} 2026 erfolgreich wird",
        f"Vor- und Nachteile von {topic}",
        f"Persönliche Erfahrung mit {topic}",
        f"Zukunft von {topic} – was Experten sagen",
        f"Häufige Fehler bei {topic} und wie man sie vermeidet",
        f"Vergleich: {topic} vs. Alternativen",
    ]

    print("\nVorgeschlagene Content-Ideen:")
    for i, idea in enumerate(ideas, 1):
        print(f"  {i}. {idea}")

    print("\n\nAktuelle Blickwinkel aus dem Netz:")
    for i, r in enumerate(results[:8], 1):
        print(f"  → {r['title']}")


# ============================================
# Hauptmenü
# ============================================
def main():
    while True:
        clear()
        print("="*60)
        print("  RESEARCH TOOLKIT")
        print("="*60)
        print("1. Topic Monitor          – News + Web + Twitter zu einem Thema")
        print("2. Reddit Trend Hunter    – Heiße Reddit-Posts finden")
        print("3. Sentiment Checker      – Stimmung zu einem Thema prüfen")
        print("4. Personal Brand Tracker – Wer spricht über dich?")
        print("5. Content Idea Generator – Content-Ideen generieren")
        print("0. Exit")
        print("="*60)

        choice = input("\nWähle eine Option: ").strip()

        if choice == "1":
            topic_monitor()
        elif choice == "2":
            reddit_trend_hunter()
        elif choice == "3":
            sentiment_checker()
        elif choice == "4":
            personal_brand_tracker()
        elif choice == "5":
            content_idea_generator()
        elif choice == "0":
            print("\nTschüss! Happy Researching.")
            break
        else:
            print("Ungültige Auswahl.")

        input("\n[Enter drücken um zurück zum Menü zu kommen]")


if __name__ == "__main__":
    main()