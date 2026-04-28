#!/usr/bin/env python3
import argparse
import json
import re
from datetime import date, timedelta
from html import escape
from pathlib import Path

ROOT = Path('/home/AF-wiki')
README_PATH = ROOT / 'README.md'
PROFILE_ROOT = Path('/home/HaodiFan-profile')
PROFILE_README_PATH = PROFILE_ROOT / 'README.md'
LOG_PATH = ROOT / 'log.md'
AUDIT_PATH = ROOT / 'areas' / 'fitness' / '40-data' / 'latest-audit.json'
CHECKINS_DIR = ROOT / 'areas' / 'fitness' / '10-checkins'
TBODY_PATTERN = re.compile(r'(<tbody>)(.*?)(</tbody>)', re.S)
DATE_HEADING_RE = re.compile(r'^## (\d{4}-\d{2}-\d{2})(?! \()$', re.M)
LOG_DATE_RE = re.compile(r'^## (\d{4}-\d{2}-\d{2})$', re.M)
LOG_BULLET_RE = re.compile(r'^-\s+(.*)$', re.M)
MONTH_FILE_RE = re.compile(r'^(\d{4}-\d{2})\.md$')

THEME_ZH = {
    'chest + triceps + core': '胸 + 三头 + 核心',
    'shoulders + arms + core': '肩 + 手臂 + 核心',
    'back + biceps': '背 + 二头',
    'aerobic swim': '游泳',
    'moderate aerobic swim': '游泳',
}

PHRASE_REPLACEMENTS = [
    ('3 eggs', '3 个鸡蛋'),
    ('1 kiwi', '1 个猕猴桃'),
    ('milk', '1 碗牛奶'),
    ('1 bowl of milk', '1 碗牛奶'),
    ('beef 200 g', '牛肉 200 g'),
    ('beef 180 g', '牛肉 180 g'),
    ('braised beef 250 g', '卤牛肉 250 g'),
    ('original-flavor braised beef 250 g', '原味卤牛肉 250 g'),
    ('sirloin steak 200 g', '西冷牛排 200 g'),
    ('1 corn cob', '玉米 1 根'),
    ('1 corn', '玉米 1 根'),
    ('1 banana', '1 根香蕉'),
    ('cod burger', '鳕鱼汉堡'),
    ('dried sweet potato 300 g', '地瓜干 300 g'),
    ('light biscuits', '轻食饼干'),
    ('1 Snickers bar', '1 根士力架'),
    ('beef shank 256 g', '五香牛腱 256 g'),
    ('hamburger steak set', '日式汉堡排套餐'),
    ('beef, rice, vegetables', '牛肉 + 米饭 + 蔬菜'),
    ('cheese potato pancake', '土豆芝士饼'),
    ('chicken soup', '鸡汤'),
    ('sticky rice', '糯米'),
    ('chicken wings', '鸡翅'),
    ('fried chicken pieces', '炸鸡块'),
    ('sparkling water', '气泡水'),
]

EVAL_REPLACEMENTS = {
    'closed rest-day record': '当天不是空白，休息与饮食记录已闭环',
    'dinner still unconfirmed': '训练闭环已明确，但晚餐仍待确认',
    'dinner still missing': '训练闭环已明确，但晚餐仍待确认',
    'carb-heavy recovery day': '当天不是空白，但整体偏碳水高、蛋白效率一般',
    'uneven energy distribution': '当天不是空白，而是饮食已落地、训练待补确认',
    'shorter-than-target swim day': '符合游泳日方向，但训练量仍低于目标',
}


def recent_log_lines(limit: int = 6):
    if not LOG_PATH.exists():
        return []
    lines = [line.rstrip() for line in LOG_PATH.read_text(encoding='utf-8').splitlines() if line.strip()]
    return lines[:limit]


def audit_snapshot():
    if not AUDIT_PATH.exists():
        return {'status': 'missing'}
    data = json.loads(AUDIT_PATH.read_text(encoding='utf-8'))
    return {
        'generated_at': data.get('generated_at'),
        'days_checked': data.get('days_checked'),
        'complete_days': data.get('complete_days'),
        'partial_days': data.get('partial_days'),
        'incomplete_days': data.get('incomplete_days'),
    }


def parse_checkin_blocks(root: Path):
    blocks = {}
    checkins_dir = root / 'areas' / 'fitness' / '10-checkins'
    if not checkins_dir.exists():
        return blocks
    for path in sorted(checkins_dir.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        matches = list(DATE_HEADING_RE.finditer(text))
        for idx, match in enumerate(matches):
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            blocks[match.group(1)] = {'text': text[start:end].strip(), 'path': path}
    return blocks


def parse_log_blocks(root: Path):
    path = root / 'log.md'
    if not path.exists():
        return {}
    text = path.read_text(encoding='utf-8')
    matches = list(LOG_DATE_RE.finditer(text))
    blocks = {}
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        blocks[match.group(1)] = text[start:end].strip()
    return blocks


def bullet_value(text: str, label: str):
    m = re.search(rf'^- {re.escape(label)}: (.+)$', text, re.M)
    return m.group(1).strip() if m else None


def section_block(text: str, heading: str):
    pattern = rf'^### {re.escape(heading)}\n(.*?)(?=^### |\Z)'
    m = re.search(pattern, text, re.S | re.M)
    return m.group(1).strip() if m else ''


def meal_block(text: str, meal_name: str):
    meals = section_block(text, 'Meals / intake')
    if not meals:
        return ''
    pattern = rf'^- {re.escape(meal_name)}:\n(.*?)(?=^- [^\n]+:\n|\Z)'
    m = re.search(pattern, meals, re.S | re.M)
    return m.group(1).strip() if m else ''


def meal_foods(block: str, meal_name: str):
    mblock = meal_block(block, meal_name)
    if not mblock:
        return None
    m = re.search(r'^- Foods: (.+)$', mblock, re.M)
    return m.group(1).strip() if m else None


def normalize_text(text: str):
    if not text:
        return text
    out = text
    for old, new in sorted(PHRASE_REPLACEMENTS, key=lambda x: len(x[0]), reverse=True):
        out = out.replace(old, new)
    out = out.replace(' + ', ' + ')
    out = re.sub(r'\s+', ' ', out).strip()
    return out


def summarize_foods(text: str):
    if not text:
        return None
    value = normalize_text(text)
    value = value.replace('，', ' + ').replace(',', ' + ')
    value = re.sub(r'\s*\+\s*', ' + ', value)
    value = re.sub(r'(\+ 气泡水.*)$', '', value).strip()
    value = value.rstrip('+ ').strip()
    value = re.sub(r'\s+', ' ', value).strip()
    return value


def infer_checkin_link(path: Path):
    rel = path.relative_to(ROOT if str(path).startswith(str(ROOT)) else path.parents[3])
    return rel.as_posix()


def classify_training(block: str):
    training_section = section_block(block, 'Training')
    status = bullet_value(training_section, 'Status')
    theme = bullet_value(training_section, 'Theme')
    duration = bullet_value(training_section, 'Duration')
    distance = bullet_value(training_section, 'Distance')
    calories = bullet_value(training_section, 'Calories')
    avg_hr = bullet_value(training_section, 'Avg HR')
    if status == 'no training performed':
        return '🛌 恢复', '当天为意图性休息日，不算漏记。'
    if status and 'no confirmed session' in status:
        return '🏋️ 训练', '训练状态仍未确认，只能标记为 <code>unconfirmed</code>。'
    if theme:
        label = '🏊 训练' if 'swim' in theme.lower() else '💪 训练'
        zh_theme = THEME_ZH.get(theme, normalize_text(theme))
        parts = [f'{zh_theme}完成' if 'swim' in theme.lower() else f'{zh_theme}力量训练完成']
        if duration:
            parts.append(f'<code>{escape(duration.replace(" total", ""))}</code>')
        if distance:
            parts.append(f'<code>{escape(distance)}</code>')
        if calories:
            parts.append(f'<code>{escape(calories.replace(" total", ""))}</code>')
        if avg_hr:
            parts.append(f'平均心率 <code>{escape(avg_hr)}</code>')
        return label, '，'.join(parts) + '。'
    return '🏋️ 训练', '训练状态仍未确认，只能标记为 <code>unconfirmed</code>。'


def nutrition_summary(block: str):
    breakfast = meal_foods(block, 'Breakfast')
    lunch = meal_foods(block, 'Lunch')
    dinner = meal_foods(block, 'Dinner')
    pre = meal_foods(block, 'Pre-workout intake') or meal_foods(block, 'Pre-workout / intra-day intake')
    post = meal_foods(block, 'Post-workout intake')

    parts = []
    if breakfast == 'none confirmed':
        parts.append('早餐待确认')
    elif breakfast:
        parts.append(f'早餐 {summarize_foods(breakfast)}'.replace('早餐  ', '早餐 '))

    if lunch == 'none':
        parts.append('午餐明确跳过')
    elif lunch:
        parts.append(f'午餐 {summarize_foods(lunch)}'.replace('午餐  ', '午餐 ').replace('午餐 ', '午餐', 1))

    if dinner in {'unconfirmed', 'none confirmed'}:
        parts.append('晚餐仍待确认')
    elif dinner:
        parts.append(f'晚餐 {summarize_foods(dinner)}'.replace('晚餐  ', '晚餐 ').replace('晚餐 ', '晚餐', 1))

    if pre and post and summarize_foods(pre) == summarize_foods(post):
        parts.append(f'训练前后各 {summarize_foods(pre)}')
    else:
        if pre:
            parts.append(f'训练前 {summarize_foods(pre)}')
        if post:
            parts.append(f'训练后 {summarize_foods(post)}')

    return '🍽️ 营养', '、'.join(parts) + '。'


def evaluation_summary(block: str, log_block: str | None = None):
    line = None
    m = re.search(r'^- Main implication: (.+)$', block, re.M)
    if m:
        line = m.group(1).strip()
    if line and line in EVAL_REPLACEMENTS:
        line = EVAL_REPLACEMENTS[line]
    elif log_block:
        bullets = [m.group(1).strip() for m in LOG_BULLET_RE.finditer(log_block)]
        for bullet in reversed(bullets):
            if 'Overall evaluation:' in bullet:
                line = bullet.split('Overall evaluation:', 1)[1].strip()
                break
        if not line and bullets:
            line = bullets[-1]
    if not line:
        line = '当天记录已更新。'
    line = normalize_text(line)
    line = line.replace('training-unconfirmed', '训练待补确认')
    return '📝 评估', line.rstrip('。.') + '。'


def build_row_html(dt: date, training: tuple[str, str], nutrition: tuple[str, str], evaluation: tuple[str, str], link: str):
    date_cell = f'<td rowspan="3"><strong>{dt.strftime("%m-%d")}</strong></td>'
    rows = [
        '    <tr>',
        f'      {date_cell}',
        f'      <td>{training[0]}</td>',
        f'      <td>{training[1]}</td>',
        f'      <td><a href="{link}">check-in</a></td>',
        '    </tr>',
        '    <tr>',
        f'      <td>{nutrition[0]}</td>',
        f'      <td>{nutrition[1]}</td>',
        f'      <td><a href="{link}">check-in</a></td>',
        '    </tr>',
        '    <tr>',
        f'      <td>{evaluation[0]}</td>',
        f'      <td>{evaluation[1]}</td>',
        f'      <td><a href="{link}">check-in</a></td>',
        '    </tr>',
    ]
    return '\n'.join(rows)


def build_recent_updates(root: Path = ROOT, today: date | None = None):
    today = today or date.today()
    start = today - timedelta(days=6)
    checkins = parse_checkin_blocks(root)
    logs = parse_log_blocks(root)
    rows = []
    for offset in range(1, 7):
        dt = today - timedelta(days=offset)
        if dt < start:
            continue
        iso = dt.isoformat()
        item = checkins.get(iso)
        if not item:
            continue
        block = item['text']
        log_block = logs.get(iso)
        link = item['path'].relative_to(root).as_posix()
        training = classify_training(block)
        nutrition = nutrition_summary(block)
        evaluation = evaluation_summary(block, log_block)
        html = build_row_html(dt, training, nutrition, evaluation, link)
        rows.append({'date': dt.strftime('%m-%d'), 'html': html})
    return rows


def refresh_readme_recent_updates(root: Path = ROOT, today: date | None = None):
    readme_path = root / 'README.md'
    text = readme_path.read_text(encoding='utf-8')
    rows_html = '\n'.join(row['html'] for row in build_recent_updates(root, today))
    replacement = f'\\1\n{rows_html}\n  \\3'
    updated, count = TBODY_PATTERN.subn(replacement, text, count=1)
    if count != 1:
        raise ValueError('README recent updates <tbody> not found or ambiguous')
    readme_path.write_text(updated, encoding='utf-8')
    return updated


def refresh_profile_recent_updates(
    wiki_root: Path = ROOT,
    profile_readme_path: Path = PROFILE_README_PATH,
    today: date | None = None,
):
    text = profile_readme_path.read_text(encoding='utf-8')
    rows = build_recent_updates(wiki_root, today)
    sections = []
    for row in rows:
        html = row['html']
        date_label = row['date']
        dim_matches = re.findall(r'<td>([^<]+)</td>\s*<td>(.*?)</td>', html, re.S)
        if len(dim_matches) != 3:
            raise ValueError(f'unexpected recent-update row format for {date_label}')
        training, nutrition, evaluation = dim_matches
        sections.append(
            f"### {training[0]} · 2026-{date_label}\n"
            f"- {re.sub(r'<.*?>', '', training[1])}\n\n"
            f"### {nutrition[0]} · 2026-{date_label}\n"
            f"- {re.sub(r'<.*?>', '', nutrition[1])}\n\n"
            f"### {evaluation[0]} · 2026-{date_label}\n"
            f"- {re.sub(r'<.*?>', '', evaluation[1])}"
        )
    replacement = '\n\n'.join(sections)
    pattern = re.compile(r'(## Recent updates by area\n\n)(.*?)(\n\n## Featured repo)', re.S)
    updated, count = pattern.subn(rf'\1{replacement}\3', text, count=1)
    if count != 1:
        raise ValueError('Profile README recent-updates section not found or ambiguous')
    profile_readme_path.write_text(updated, encoding='utf-8')
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description='AF-wiki briefing and README recent updates helper.')
    parser.add_argument('--refresh-readme', action='store_true', help='Refresh README recent updates tbody from last 7 days of check-ins')
    parser.add_argument('--refresh-profile-readme', action='store_true', help='Refresh GitHub profile README recent updates from AF-wiki check-ins')
    parser.add_argument('--refresh-all-readmes', action='store_true', help='Refresh both wiki README and GitHub profile README recent updates')
    args = parser.parse_args()

    if args.refresh_readme or args.refresh_all_readmes:
        refresh_readme_recent_updates(ROOT)
    if args.refresh_profile_readme or args.refresh_all_readmes:
        refresh_profile_recent_updates(ROOT)

    payload = {
        'wiki': 'AF-wiki',
        'briefing': {
            'recent_log_head': recent_log_lines(),
            'fitness_audit': audit_snapshot(),
            'recent_updates_window_days': 7,
            'recent_updates_dates': [row['date'] for row in build_recent_updates(ROOT)],
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
