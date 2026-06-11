import json
import os
from pathlib import Path

# Load B站 dynamics
with open(r'D:\py_code\bilibili-knowledge-mcp\data\all_dynamics_full.json', 'r', encoding='utf-8') as f:
    dynamics = json.load(f)

def classify(item):
    title = (item.get('title', '') or '').lower()
    desc = (item.get('description', '') or '').lower()
    text = title + ' ' + desc
    tp = item.get('type', '')

    if tp == 'DYNAMIC_TYPE_FORWARD':
        return 'daily', []
    if tp == 'DYNAMIC_TYPE_AV':
        return 'creative', ['视频创作']

    tags = []

    if any(kw in text for kw in ['第一个', '完成了', '成功', '夺冠', '构建成', 'ipa', '里程碑']):
        category = 'milestone'
    elif any(kw in text for kw in ['部署', 'kavita', 'ffmpeg', '脚本', 'python', 'trae', 'claude', '编码', '开发', 'app', '代码', 'sideloady']):
        category = 'project-log'
        tags.append('技术')
    elif any(kw in text for kw in ['总结', '回顾', '这半个', '这几个月', '四月', '开学', '暑假', '期末', '月回顾']):
        category = 'review'
    elif any(kw in text for kw in ['论文', '导师', '家教', '考试', '期末', '实习', '实验', '课题']):
        category = 'academic'
    elif any(kw in text for kw in ['剪辑', '吉他', '弹唱', '视频', '演唱会']):
        category = 'creative'
    elif any(kw in text for kw in ['足球', '游戏', 'galgame', '第五人格', '音乐', '耳机', '电影', '麻将', '曼城', '瓜迪奥拉']):
        category = 'hobby'
    elif any(kw in text for kw in ['失眠', '自律', '爱情', '阶层', '孤独', '思考', '社交', '独处', '朋友', '大学生', '想象']):
        category = 'reflection'
    else:
        category = 'daily'

    return category, tags

def get_mood(desc):
    if any(kw in desc for kw in ['失眠', '破防', '难受', '焦虑', '折磨', '生气', '孤独', '痛苦']):
        return 'rainy'
    elif any(kw in desc for kw in ['还行', '一般', '有点', '但也', '乱乱', '可惜']):
        return 'cloudy'
    return 'sunny'

garden_dir = Path(r'D:\projects\garden\src\content\garden')
garden_dir.mkdir(parents=True, exist_ok=True)

count = 0
for item in dynamics:
    if item.get('type') == 'DYNAMIC_TYPE_FORWARD':
        continue

    title = item.get('title', '') or item.get('description', '')[:40] or '无标题'
    title = title.replace('"', "'").replace('\n', ' ').strip()
    if len(title) > 120:
        title = title[:120] + '...'

    date_str = item.get('date', '')[:10]
    if not date_str:
        continue

    category, tags = classify(item)
    desc = (item.get('description', '') or '').replace('\\', '\\\\').replace('"', '\\"')
    mood = get_mood(desc)

    images = [img.get('url', '') for img in item.get('all_images', [])]
    images = [url for url in images if url][:5]

    slug = f'{date_str}-{item.get("dynamic_id", "unknown")[-8:]}'

    # Build frontmatter manually
    lines = ['---']
    lines.append(f'date: {date_str}')
    lines.append(f'title: "{title}"')
    lines.append(f'category: "{category}"')
    lines.append(f'mood: "{mood}"')
    if tags:
        tag_str = json.dumps(tags, ensure_ascii=False)
        lines.append(f'tags: {tag_str}')
    b_url = item.get('url', '')
    if b_url:
        lines.append(f'bilibili_url: "{b_url}"')
    if images:
        img_str = json.dumps(images, ensure_ascii=False)
        lines.append(f'images: {img_str}')
    if desc:
        short_desc = desc[:300].strip()
        lines.append(f'description: "{short_desc}"')
    lines.append('---')
    lines.append('')
    if desc:
        lines.append(desc)

    content = '\n'.join(lines)
    filepath = garden_dir / f'{slug}.mdx'
    try:
        filepath.write_text(content, encoding='utf-8')
        count += 1
        print(f'  OK: {slug} [{category}]')
    except Exception as e:
        print(f'  FAIL: {slug}: {e}')

print(f'\nTotal garden entries created: {count}')
