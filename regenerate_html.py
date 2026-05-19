#!/usr/bin/env python3
"""
从JSON数据文件重新生成 index.html
使用: python regenerate_html.py
"""
import json
import os

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Loading data files...")
    data_dir = os.path.dirname(os.path.abspath(__file__))

    tools = load_json(os.path.join(data_dir, 'data', 'tools.json'))
    models = load_json(os.path.join(data_dir, 'data', 'models.json'))
    languages = load_json(os.path.join(data_dir, 'data', 'languages.json'))
    databases = load_json(os.path.join(data_dir, 'data', 'databases.json'))
    github = load_json(os.path.join(data_dir, 'data', 'github.json'))

    print(f"Loaded: {len(tools)} tools, {len(models)} model categories, {len(languages)} languages, {sum(len(v) for v in databases.values())} databases, {len(github)} GitHub apps")

    # TODO: Implement HTML regeneration logic
    # For now, this is a placeholder
    print("HTML regeneration not yet implemented.")
    print("Data files are ready for manual update or LLM-assisted update.")

if __name__ == '__main__':
    main()
