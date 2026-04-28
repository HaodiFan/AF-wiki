import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path('/home/AF-wiki/infra/jobs/af_wiki_briefing.py')
spec = importlib.util.spec_from_file_location('af_wiki_briefing', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


CHECKINS_TEXT = """# April 2026 Check-Ins

## 2026-04-20
### Day summary
- Overall status: chest day done

### Training
#### Session 1
- Type: traditional strength training
- Theme: chest + triceps + core
- Duration: 48:31
- Calories: 414 kcal total
- Avg HR: 128 bpm

### Meals / intake
- Breakfast:
  - Foods: 3 eggs
- Lunch:
  - Foods: beef shank 256 g
- Dinner:
  - Foods: salmon 200 g, broccoli, rice

### Coaching interpretation
- Main implication: solid push day

## 2026-04-21
### Day summary
- Overall status: pull day done

### Training
#### Session 1
- Type: traditional strength training
- Theme: back + biceps
- Duration: 42:18

### Meals / intake
- Breakfast:
  - Foods: 3 eggs, milk
- Lunch:
  - Foods: beef bowl
- Dinner:
  - Foods: beef shank, spinach, yogurt

### Coaching interpretation
- Main implication: strong substitute pull session

## 2026-04-22
### Day summary
- Overall status: swim done

### Training
#### Session 1
- Type: swim
- Theme: moderate aerobic swim
- Duration: 23:49 total / 22:51 active
- Distance: 325 m

### Meals / intake
- Breakfast:
  - Foods: 3 eggs, milk
- Pre-workout / intra-day intake:
  - Foods: 1 banana
- Lunch:
  - Foods: sirloin steak 200 g, 1 corn
- Dinner:
  - Foods: unconfirmed

### Coaching interpretation
- Main implication: shorter-than-target swim day

## 2026-04-23
### Day summary
- Overall status: rest day

### Training
- Status: no training performed
- Notes: intentional rest day

### Meals / intake
- Breakfast:
  - Foods: 3 eggs, milk
- Lunch:
  - Foods: hamburger steak set
- Dinner:
  - Foods: beef, rice, vegetables

### Coaching interpretation
- Main implication: closed rest-day record

## 2026-04-24
### Day summary
- Overall status: dinner-heavy day

### Training
- Status: no confirmed session recovered from the canonical note or currently exported chat history
- Notes: keep this day marked as training-unconfirmed rather than inferring either completion or rest

### Meals / intake
- Breakfast:
  - Foods: none confirmed
- Lunch:
  - Foods: none
  - Notes: explicitly stated in chat that lunch was skipped
- Dinner:
  - Foods: cheese potato pancake, chicken soup, sticky rice, chicken wings

### Coaching interpretation
- Main implication: uneven energy distribution

## 2026-04-25
### Day summary
- Overall status: accessory day done

### Training
#### Session 1
- Type: traditional strength training
- Theme: shoulders + arms + core
- Duration: 42:36
- Calories: 361 kcal total
- Avg HR: 126 bpm

### Meals / intake
- Breakfast:
  - Foods: light biscuits, 1 Snickers bar
- Lunch:
  - Foods: braised beef 250 g
- Dinner:
  - Foods: unconfirmed

### Coaching interpretation
- Main implication: dinner still missing

## 2026-04-26
### Day summary
- Overall status: swim done in Shanghai

### Training
#### Session 1
- Type: swim
- Theme: aerobic swim
- Duration: 38:59
- Distance: 500 m
- Calories: 218 kcal total

### Meals / intake
- Breakfast:
  - Foods: light biscuits, 1 corn
- Lunch:
  - Foods: beef 180 g, dried sweet potato 300 g
- Dinner:
  - Foods: cod burger, 1 corn

### Coaching interpretation
- Main implication: carb-heavy recovery day

## 2026-04-27
### Day summary
- Overall status: push day done in Shanghai

### Training
#### Session 1
- Type: traditional strength training
- Theme: chest + triceps + core
- Duration: 50:37
- Calories: 319 kcal total
- Avg HR: 111 bpm

### Meals / intake
- Breakfast:
  - Foods: 3 eggs, 1 kiwi
- Lunch:
  - Foods: beef 200 g, 1 corn
- Pre-workout intake:
  - Foods: 1 banana
- Post-workout intake:
  - Foods: 1 banana
- Dinner:
  - Foods: none confirmed

### Coaching interpretation
- Main implication: dinner still unconfirmed
"""

LOG_TEXT = """# AF Wiki Log

## 2026-04-27
- Fitness/Nutrition: completed chest + triceps + core strength session
- Overall evaluation: training closure is clear, but recovery closure still depends on dinner

## 2026-04-26
- Fitness: completed a lighter recovery-style swim session
- Nutrition: breakfast, lunch, and dinner are grounded
- Overall evaluation: not blank

## [2026-04-24] infra | Added Phase 1 sidecar command skeleton
- Added `infra/jobs/af_wiki_briefing.py`
"""

README_TEMPLATE = """# Demo\n\n## 📡 最近动态\n\n<table>\n  <thead>\n    <tr><th>日期</th><th>维度</th><th>状态</th><th>入口</th></tr>\n  </thead>\n  <tbody>\n    <tr><td><strong>04-01</strong></td><td>old</td><td>old</td><td>old</td></tr>\n  </tbody>\n</table>\n\n## Next\n"""

PROFILE_TEMPLATE = """# Demo Profile\n\n## Recent updates by area\n\n### Old · 2026-04-01\n- old\n\n## Featured repo\n### AF-wiki\n"""


def _write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


class BriefingTests(unittest.TestCase):
    def test_build_recent_updates_returns_only_last_7_days(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / 'wiki'
            _write(root / 'areas/fitness/10-checkins/2026-04.md', CHECKINS_TEXT)
            _write(root / 'log.md', LOG_TEXT)

            rows = module.build_recent_updates(root, today=module.date(2026, 4, 28))

            self.assertEqual([row['date'] for row in rows], ['04-27', '04-26', '04-25', '04-24', '04-23', '04-22'])
            self.assertTrue(all('04-20' not in row['html'] and '04-21' not in row['html'] for row in rows))

    def test_build_recent_updates_prefers_checkins_with_log_fallback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / 'wiki'
            _write(root / 'areas/fitness/10-checkins/2026-04.md', CHECKINS_TEXT)
            _write(root / 'log.md', LOG_TEXT)

            rows = module.build_recent_updates(root, today=module.date(2026, 4, 28))
            by_date = {row['date']: row['html'] for row in rows}

            self.assertIn('胸 + 三头 + 核心力量训练完成', by_date['04-27'])
            self.assertIn('早餐 3 个鸡蛋 + 1 个猕猴桃', by_date['04-27'])
            self.assertIn('午餐牛肉 200 g + 玉米 1 根', by_date['04-27'])
            self.assertIn('训练前后各 1 根香蕉', by_date['04-27'])
            self.assertIn('训练闭环已明确，但晚餐仍待确认', by_date['04-27'])
            self.assertIn('训练状态仍未确认', by_date['04-24'])
            self.assertIn('当天为意图性休息日', by_date['04-23'])
            self.assertIn('早餐 3 个鸡蛋 + 1 碗牛奶', by_date['04-23'])

    def test_refresh_readme_recent_updates_replaces_tbody_and_drops_old_rows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / 'wiki'
            _write(root / 'areas/fitness/10-checkins/2026-04.md', CHECKINS_TEXT)
            _write(root / 'log.md', LOG_TEXT)
            readme_path = root / 'README.md'
            _write(readme_path, README_TEMPLATE)

            updated = module.refresh_readme_recent_updates(root, today=module.date(2026, 4, 28))

            self.assertIn('<strong>04-27</strong>', updated)
            self.assertIn('<strong>04-22</strong>', updated)
            self.assertNotIn('04-21', updated)
            self.assertNotIn('04-20', updated)
            self.assertNotIn('04-01', updated)
            self.assertEqual(updated.count('<tbody>'), 1)
            self.assertEqual(updated.count('</tbody>'), 1)
            self.assertEqual(readme_path.read_text(encoding='utf-8'), updated)

    def test_refresh_profile_recent_updates_replaces_recent_updates_section(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / 'wiki'
            profile_path = Path(tmpdir) / 'HaodiFan-profile' / 'README.md'
            _write(root / 'areas/fitness/10-checkins/2026-04.md', CHECKINS_TEXT)
            _write(root / 'log.md', LOG_TEXT)
            _write(profile_path, PROFILE_TEMPLATE)

            updated = module.refresh_profile_recent_updates(root, profile_path, today=module.date(2026, 4, 28))

            self.assertIn('### 💪 训练 · 2026-04-27', updated)
            self.assertIn('### 🍽️ 营养 · 2026-04-26', updated)
            self.assertIn('### 📝 评估 · 2026-04-22', updated)
            self.assertNotIn('### Old · 2026-04-01', updated)
            self.assertIn('## Featured repo', updated)
            self.assertEqual(profile_path.read_text(encoding='utf-8'), updated)


if __name__ == '__main__':
    unittest.main()
