#!/usr/bin/env python3
"""
Download and cache icons locally for better performance.
Usage: python download_icons.py

Features:
- Downloads from Clearbit Logo API or direct favicon URLs
- Skips already downloaded icons (progress saved)
- Fallback to alternative sources if primary fails
- Generates a manifest file for tracking downloaded icons
"""
import os
import json
import re
import hashlib
import urllib.request
import urllib.error
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ICONS_DIR = os.path.join(os.path.dirname(__file__), 'icons')
MANIFEST_FILE = os.path.join(ICONS_DIR, 'manifest.json')

# Alternative sources for icons
ICON_SOURCES = [
    'https://logo.clearbit.com/{domain}',           # Primary
    'https://www.google.com/s2/favicons?domain={domain}&sz=64',  # Google fallback
    'https://{domain}/favicon.ico',                   # Direct favicon
]

# Map of known domains to better icon sources
DOMAIN_MAP = {
    'github.githubassets.com': 'https://github.com/github.png',
    'assets.anthropic.com': 'https://anthropic.com/favicon.ico',
    'tc39.github.io': 'https://tc39.es/favicon.ico',
    'learn.microsoft.com': 'https://microsoft.com/favicon.ico',
}

def sanitize_filename(url):
    """Convert URL to safe filename"""
    if not url:
        return None

    # Handle domain mapping
    for old_domain, new_url in DOMAIN_MAP.items():
        if old_domain in url:
            url = new_url

    # Extract domain from logo.clearbit.com URL
    match = re.search(r'logo\.clearbit\.com/([^/]+)', url)
    if match:
        domain = match.group(1)
        return f"{domain}.png"

    # For GitHub user avatars
    match = re.search(r'github\.com/([^/]+)\.png', url)
    if match:
        owner = match.group(1)
        return f"github_{owner}.png"

    # For direct favicon URLs
    match = re.search(r'https?://([^/]+)', url)
    if match:
        domain = match.group(1).replace('www.', '')
        domain = re.sub(r'[^a-zA-Z0-9._-]', '_', domain)
        return f"{domain}.png"

    # Hash as fallback
    return f"{hashlib.md5(url.encode()).hexdigest()[:16]}.png"

def download_icon(url, filepath, timeout=10):
    """Download a single icon with fallback sources"""
    if not url or not isinstance(url, bool) or not url.startswith('http'):
        return False

    # Extract domain for alternative sources
    match = re.search(r'logo\.clearbit\.com/([^/]+)', url)
    if match:
        domain = match.group(1)
        sources = [
            url,
            f'https://www.google.com/s2/favicons?domain={domain}&sz=64',
            f'https://{domain}/favicon.ico',
        ]
    else:
        sources = [url]

    for source in sources:
        try:
            req = urllib.request.Request(
                source,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
                if len(data) > 500:  # Ignore tiny favicons
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    return True
        except Exception as e:
            continue

    return False

def load_manifest():
    """Load download manifest"""
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_manifest(manifest):
    """Save download manifest"""
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

def collect_icon_urls(data):
    """Recursively collect all unique icon URLs from data"""
    icons = set()
    if isinstance(data, dict):
        if 'icon' in data and data['icon']:
            icons.add(data['icon'])
        for value in data.values():
            icons.update(collect_icon_urls(value))
    elif isinstance(data, list):
        for item in data:
            icons.update(collect_icon_urls(item))
    return icons

def main():
    print("=== AIDevHub Icon Downloader ===\n")
    os.makedirs(ICONS_DIR, exist_ok=True)

    manifest = load_manifest()
    print(f"Loaded manifest: {len(manifest)} icons already downloaded\n")

    # Load all JSON data
    json_files = [
        os.path.join(DATA_DIR, 'tools.json'),
        os.path.join(DATA_DIR, 'models.json'),
        os.path.join(DATA_DIR, 'languages.json'),
        os.path.join(DATA_DIR, 'databases.json'),
        os.path.join(DATA_DIR, 'github.json'),
    ]

    all_icons = set()
    for filepath in json_files:
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        all_icons.update(collect_icon_urls(data))

    # Filter to only HTTP URLs
    icon_urls = [url for url in all_icons if url and url.startswith('http')]
    print(f"Found {len(icon_urls)} unique icon URLs\n")

    # Check which icons need downloading
    to_download = []
    for url in icon_urls:
        filename = sanitize_filename(url)
        filepath = os.path.join(ICONS_DIR, filename)
        if not os.path.exists(filepath):
            to_download.append((url, filename, filepath))
        else:
            manifest[url] = filename

    print(f"Need to download: {len(to_download)} icons")
    print(f"Already cached: {len(icon_urls) - len(to_download)} icons\n")

    if not to_download:
        print("All icons already cached!")
        return

    # Interactive confirmation
    response = input(f"Download {len(to_download)} icons? [y/N]: ").strip().lower()
    if response != 'y':
        print("Download cancelled.")
        return

    # Download icons
    success_count = 0
    for i, (url, filename, filepath) in enumerate(to_download, 1):
        print(f"[{i}/{len(to_download)}] Downloading {filename}...", end=' ')
        success = download_icon(url, filepath)
        if success:
            manifest[url] = filename
            success_count += 1
            print("OK")
        else:
            print("FAILED")
        time.sleep(0.5)  # Rate limiting

    save_manifest(manifest)

    print(f"\n=== Download Complete ===")
    print(f"Successfully downloaded: {success_count}/{len(to_download)} icons")
    print(f"Icons saved to: {ICONS_DIR}")

    # Update local paths in JSON files
    print("\nUpdating JSON files with local icon paths...")
    for filepath in json_files:
        if not os.path.exists(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        changed = False

        def update_icon_paths(obj):
            nonlocal changed
            if isinstance(obj, dict):
                if 'icon' in obj and obj['icon']:
                    url = obj['icon']
                    if url in manifest:
                        obj['icon'] = f"./icons/{manifest[url]}"
                        changed = True
                    elif url.startswith('http'):
                        filename = sanitize_filename(url)
                        if os.path.exists(os.path.join(ICONS_DIR, filename)):
                            obj['icon'] = f"./icons/{filename}"
                            changed = True
                for value in obj.values():
                    update_icon_paths(value)
            elif isinstance(obj, list):
                for item in obj:
                    update_icon_paths(item)

        update_icon_paths(data)

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Updated {os.path.basename(filepath)}")

    print("\nDone! You can now run this script again to download missing icons.")

if __name__ == '__main__':
    main()