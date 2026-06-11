import os, re, json

docs = [
    {
        'file': '从AME到FFmpeg.md',
        'slug': 'from-ame-to-ffmpeg',
        'date': '2026-02-01',
        'category': '技术学习笔记',
        'tags': ['FFmpeg', '视频编码', 'Kimi', 'PR', 'AME'],
        'maturity': 'evergreen',
    },
    {
        'file': '我要让声音出现：FFmpeg的探索.md',
        'slug': 'let-sound-appear-ffmpeg',
        'date': '2026-02-08',
        'category': '技术学习笔记',
        'tags': ['FFmpeg', '音轨编码', 'AI协作', 'VLC', '电视'],
        'maturity': 'evergreen',
    },
    {
        'file': '工程师思维只是想让机器做得更多.md',
        'slug': 'engineer-mindset-python',
        'date': '2026-02-14',
        'category': '里程碑',
        'tags': ['Python', '第一个脚本', '情人节', 'FFmpeg', 'Kimi'],
        'maturity': 'evergreen',
    },
    {
        'file': 'Trae定义了我对ai IDE的所有想象.md',
        'slug': 'trae-defines-ai-ide',
        'date': '2026-04-01',
        'category': 'AI 协作开发',
        'tags': ['Trae', 'AI IDE', '编程入门'],
        'maturity': 'evergreen',
    },
]

def safe_str(s):
    """Remove characters that break YAML double-quoted strings."""
    # Remove backslash escapes
    s = s.replace("\\", "")
    # Escape double quotes
    s = s.replace('"', '\\"')
    # Remove control characters except newline, tab
    result = []
    for c in s:
        if c == '\n' or c == '\t' or (ord(c) >= 32 and ord(c) < 127) or ord(c) > 127:
            result.append(c)
    return "".join(result)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
feishu_dir = os.path.join(base_dir, "飞书云文档")
blog_dir = os.path.join(base_dir, "src", "content", "blog")
os.makedirs(blog_dir, exist_ok=True)

for doc in docs:
    filepath = os.path.join(feishu_dir, doc["file"])
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    title = lines[0].replace("# ", "").strip()
    body = "\n".join(lines[1:]).strip()

    # Description from plain text only
    text_only = re.sub(r"!\[Image\]\([^)]+\)", "", body)
    text_only = re.sub(r"\n+", " ", text_only).strip()
    desc = safe_str(text_only)[:200].strip()
    safe_title = safe_str(title)
    tags_json = json.dumps(doc["tags"], ensure_ascii=False)

    mdx = f"""---
title: "{safe_title}"
description: "{desc}"
category: "{doc['category']}"
tags: {tags_json}
maturity: "{doc['maturity']}"
publishedAt: {doc['date']}
---

{body}
"""
    outpath = os.path.join(blog_dir, f"{doc['date']}-{doc['slug']}.mdx")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(mdx)

    img_count = len(re.findall(r"!\[Image\]", body))
    print(f"OK: {os.path.basename(outpath)} | {img_count} images | {len(body)} chars")

print("All 4 blog posts created!")
