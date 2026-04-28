#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = Path('/home/AF-wiki/data/fitness.db')
TARGET_DATES = ['2026-04-23', '2026-04-24', '2026-04-25', '2026-04-26']

DAY_UPDATES = {
    '2026-04-23': {
        'notes_zh': '计划槽位：周三背部 + 二头 + 下肢插入。整体状态：早餐、午餐、晚餐已记录，用户确认今天不训练。实际训练状态：确认休息 / 不训练。训练完成度：今日休息已确认，应视为已闭环日记录，而不是缺失训练日志。营养完成度：早餐、午餐、晚餐都已落地，主要剩余不确定性是具体分量以及是否还有后续补充蛋白。主要含义：由于今天确认不训练，且午餐相对偏丰盛，后续饮食应更偏简单、低油，而不是继续加重。',
        'notes_en': 'Plan slot: Wednesday back + biceps + lower-body insert. Overall status: breakfast, lunch, and dinner are recorded, and the user confirmed no training for today. Actual training status: confirmed rest / no-training day. Training completion: rest is confirmed and the day should count as closed rather than as a missing workout log. Nutrition completion: breakfast, lunch, and dinner are grounded; the main remaining uncertainty is exact portions and whether there was any later protein correction. Main implication: because today is a confirmed no-training day and lunch was relatively rich, the rest of the day should stay simpler and lower-oil rather than getting heavier.'
    },
    '2026-04-24': {
        'notes_zh': '计划槽位：周四胸 + 三头 + 核心，或等效推训练日（基于上一版有效健身计划）。整体状态：早餐未找回，午餐明确跳过，晚餐摄入偏重，应视为超量 / 需要纠偏的一天，而不是缺记录日。实际训练状态：未确认。训练完成度：仍未确认，不应推断为已训练或已休息。营养完成度：早餐仍未找回、午餐为明确跳过、晚餐已确认，因此即使没有训练，这一天的饮食记录也是落地的。主要含义：白天吃得很轻、晚餐偏重，应视为能量分配不均，而不是全天失控暴食。下一步含义：次日更适合轻一点、偏高蛋白、简单碳水、少油，而不是激进补偿。',
        'notes_en': 'Plan slot: Thursday chest + triceps + core, or an equivalent push-oriented day under the last active fitness training structure. Overall status: breakfast was not recovered, lunch was explicitly skipped, and dinner was heavier than intended, so the day should be treated as an overage / correction-needed eating day rather than as a missing-record day. Actual training status: unconfirmed. Training completion: still unconfirmed, so it should not yet be classified as either completed training or confirmed recovery. Nutrition completion: breakfast remains unrecovered, lunch is intentionally skipped, and dinner is confirmed, which means the diet record is grounded even without a workout. Main implication: daytime intake was very light but dinner overshot, so the day is better understood as uneven energy distribution rather than all-day uncontrolled overeating. Next-step implication: the following day should favor lighter, protein-forward meals with simpler carbs and less added fat rather than aggressive restriction.'
    },
    '2026-04-25': {
        'notes_zh': '计划槽位：周五肩 + 手臂 + 核心，为当前周结构中的上肢辅助强化日。整体状态：肩部 + 手臂 + 核心训练已完成；早餐和午餐已落地；晚餐及更晚摄入仍未确认。训练时间窗：11:12-11:55。实际训练状态：已完成。训练完成度：这是一次真实完成的肩 + 手臂 + 核心训练，补上了本周计划中的一个主要空缺。营养状态：早餐已确认但蛋白偏低，午餐已确认并显著改善当日蛋白情况，晚餐仍是明确未确认而非隐性缺失。主要含义：当天营养质量不再算差，但仍略不均衡，因为上午摄入偏轻，而目前唯一明确的主蛋白锚点是午餐。下一步含义：若后续找回晚餐证据，应直接合并进同一日块。',
        'notes_en': 'Plan slot: Friday shoulders + arms + core, serving as an upper-body accessory emphasis day within the current weekly pattern. Overall status: the shoulders + arms + core session was completed; breakfast and lunch are grounded; dinner and later intake remain unconfirmed. Training window: 11:12-11:55. Actual training status: completed. Training completion: this counts as a genuinely completed shoulders + arms + core session and fills one of the main remaining gaps in this week’s intended split. Nutrition status: breakfast is confirmed but protein-light, lunch is confirmed and materially improves the day’s protein situation, and dinner remains explicitly unconfirmed rather than silently missing. Main implication: the day’s nutrition quality is no longer weak overall, but it is still somewhat unbalanced because morning intake was light and the only confirmed main protein anchor is lunch. Next-step implication: if dinner evidence is recovered later, it should be appended into the same day block rather than split into a second same-day entry.'
    },
    '2026-04-26': {
        'notes_zh': '计划槽位：周日游泳 / 有氧日。整体状态：早餐记录较轻；游泳前体重已记录；上海完成了一次游泳训练。体重：74.7 kg。训练地点：上海。训练日期：2026-04-26 周日。计划执行：今天应计为完成的游泳 / 有氧日，比起在 2026-04-25 肩手臂核心训练后立刻继续上肢力量，更符合近期训练节奏。训练完成度：本次训练证据完整，应视为偏恢复型的轻中等游泳，而不是高输出进阶游泳；与 2026-04-18 相比，同样 500 m 用时更久、平均心率更低。营养状态：早餐已确认但较轻且蛋白偏低；午餐是最明确的恢复蛋白锚点；晚餐虽已落地，但因为是汉堡形式，整体不算特别精瘦。主要含义：当天摄入不再缺失，但总体仍稍偏高碳且蛋白效率不算最优，因为早餐偏轻、午餐有较大份红薯干、晚餐则用了汉堡形式。',
        'notes_en': 'Plan slot: Sunday swim / aerobic day. Overall status: breakfast was lightly logged; bodyweight was recorded before the swim; and a swim session was completed in Shanghai. Bodyweight: 74.7 kg. Training location: Shanghai. Training date: Sunday, 2026-04-26. Plan adherence: today should count as a completed swim / aerobic day, which fits the recent pattern better than repeating upper-body lifting right after the 2026-04-25 shoulders + arms + core session. Training completion: the session is fully grounded and should be treated as a lighter recovery-style swim rather than a high-output progression swim; compared with 2026-04-18, the same 500 m took longer and average heart rate was lower. Nutrition status: breakfast is confirmed but light and protein-low; lunch is the clearest recovery-protein anchor; dinner is grounded but not especially lean because the main protein came in burger form. Main implication: intake is no longer missing for the day, but the overall structure still looks somewhat carb-heavy and not maximally protein-efficient because breakfast was light, lunch included a large dried sweet potato portion, and dinner used a burger format rather than a cleaner protein plate.'
    },
}

MEAL_UPDATES = {
    ('2026-04-23', 'Breakfast'): {
        'meal_slot_zh': '早餐', 'meal_slot_en': 'Breakfast',
        'foods_text_zh': '3个鸡蛋，1碗牛奶',
        'foods_text_en': '3 eggs, 1 bowl of milk',
        'notes_zh': '与常见的简洁早餐结构一致，确认了当天早晨摄入。',
        'notes_en': 'This matches the usual simple breakfast structure and confirms morning intake for the day.'
    },
    ('2026-04-23', 'Lunch'): {
        'meal_slot_zh': '午餐', 'meal_slot_en': 'Lunch',
        'foods_text_zh': '1碗日式白米饭、1碗味噌汤（含葱和竹笋）、2块铁板汉堡肉、大量西兰花、1个生鸡蛋、3种酱料（粉色特调奶油酱、棕色烧肉风味酱、颗粒芥末酱）、一杯浅色饮料（可能是气泡水或淡饮）',
        'foods_text_en': '1 bowl of Japanese white rice, 1 bowl of miso soup (with scallion and bamboo shoots), 2 teppan hamburger patties, a large amount of broccoli, 1 raw egg, 3 sauces (pink creamy special sauce, brown yakiniku-style sauce, grainy mustard sauce), and a light-colored drink likely sparkling water or a light beverage',
        'notes_zh': '在肉肉大米用餐；这是带多种酱料的餐厅餐，隐藏脂肪和钠含量可能明显高于普通家常餐。',
        'notes_en': 'Eaten at 肉肉大米; this was a restaurant meal with multiple sauces, so hidden fat and sodium may be meaningfully higher than in a plain home-cooked meal.'
    },
    ('2026-04-23', 'Dinner'): {
        'meal_slot_zh': '晚餐', 'meal_slot_en': 'Dinner',
        'foods_text_zh': '牛肉、1碗米饭、绿色蔬菜、彩椒',
        'foods_text_en': 'Beef, 1 bowl of rice, green vegetables, and bell pepper',
        'notes_zh': '用户后续澄清了这个更简化的晚餐版本；以此作为地面真值，不默认加入红薯或四季豆等未最终确认食物。',
        'notes_en': 'The user later clarified this simpler dinner version; keep it as ground truth and do not assume sweet potato or green beans were definitely eaten.'
    },
    ('2026-04-24', 'Breakfast'): {
        'meal_slot_zh': '早餐', 'meal_slot_en': 'Breakfast',
        'foods_text_zh': '未确认 / 未找回',
        'foods_text_en': 'Unconfirmed / not recovered',
        'notes_zh': '用户要求即使非训练日也保留饮食记录；目前未找回早餐事实，因此明确标注为未确认而非省略。',
        'notes_en': 'The user asked that non-training days should still keep diet records; no breakfast fact has been recovered yet, so this remains explicitly unconfirmed rather than omitted.'
    },
    ('2026-04-24', 'Lunch'): {
        'meal_slot_zh': '午餐', 'meal_slot_en': 'Lunch',
        'foods_text_zh': '无（明确跳过）',
        'foods_text_en': 'None (explicitly skipped)',
        'notes_zh': '聊天中已明确午餐跳过；这应算作已确认的跳过餐，而不是缺失午餐记录。',
        'notes_en': 'Chat history explicitly states that lunch was skipped; this should be treated as a confirmed skipped meal, not as a missing lunch record.'
    },
    ('2026-04-24', 'Dinner'): {
        'meal_slot_zh': '晚餐', 'meal_slot_en': 'Dinner',
        'foods_text_zh': '芝士土豆饼、一大碗鸡汤、一些糯米、2瓣糖蒜、几只鸡翅、一碗炸鸡块',
        'foods_text_en': 'Cheese potato pancake, one large bowl of chicken soup, some sticky rice, 2 sugar-garlic cloves, several chicken wings, and one bowl of fried chicken pieces',
        'notes_zh': '用户明确描述这顿晚餐“有点多”；土豆饼、糯米、油炸外皮/油脂以及鸡皮等可能带来较明显的脂肪和碳水负担。',
        'notes_en': 'The user explicitly described this dinner as a bit excessive; the potato pancake, sticky rice, fried coating/oil, and chicken skin likely added meaningful fat and carb load.'
    },
    ('2026-04-25', 'Breakfast'): {
        'meal_slot_zh': '早餐', 'meal_slot_en': 'Breakfast',
        'foods_text_zh': '轻饼干，1根士力架',
        'foods_text_en': 'Light biscuits and 1 Snickers bar',
        'notes_zh': '早餐偏便利食品、蛋白偏低，不应视为当天有意义的蛋白锚点。',
        'notes_en': 'Breakfast appears convenience-based and protein-light, so it should not be treated as a meaningful protein anchor for the day.'
    },
    ('2026-04-25', 'Lunch'): {
        'meal_slot_zh': '午餐', 'meal_slot_en': 'Lunch',
        'foods_text_zh': '原味卤牛肉 250 g',
        'foods_text_en': '250 g original-flavor braised beef',
        'notes_zh': '午餐已确认吃了；确认版本里没有蔬菜，因此整体仍偏高蛋白但不算特别均衡。',
        'notes_en': 'Lunch is confirmed eaten; vegetables were not included in the confirmed version, so the meal remains protein-heavy but not especially balanced.'
    },
    ('2026-04-25', 'Dinner'): {
        'meal_slot_zh': '晚餐', 'meal_slot_en': 'Dinner',
        'foods_text_zh': '未确认',
        'foods_text_en': 'Unconfirmed',
        'notes_zh': '目前仍未从标准记录或已导出的聊天历史中找回已确认的晚餐细节。',
        'notes_en': 'No confirmed dinner detail has yet been recovered from the canonical note or the currently exported chat history.'
    },
    ('2026-04-26', 'Breakfast'): {
        'meal_slot_zh': '早餐', 'meal_slot_en': 'Breakfast',
        'foods_text_zh': '1包轻饼干，1根玉米',
        'foods_text_en': '1 pack of light biscuits and 1 corn',
        'notes_zh': '这是一次较轻的游泳前早餐，不应视为当天强蛋白锚点。',
        'notes_en': 'This is a light pre-swim breakfast and should not be treated as a strong protein anchor for the day.'
    },
    ('2026-04-26', 'Lunch'): {
        'meal_slot_zh': '午餐', 'meal_slot_en': 'Lunch',
        'foods_text_zh': '牛肉 180 g，红薯干 300 g',
        'foods_text_en': '180 g beef and 300 g dried sweet potato',
        'notes_zh': '这顿午餐目前明显是当天主要的游后恢复餐；牛肉改善了蛋白覆盖，但 300 g 红薯干也让碳水负荷偏高。',
        'notes_en': 'This lunch clearly serves as the main post-swim recovery meal so far; the beef improves protein coverage, while the 300 g dried sweet potato likely makes the carb load relatively high.'
    },
    ('2026-04-26', 'Dinner'): {
        'meal_slot_zh': '晚餐', 'meal_slot_en': 'Dinner',
        'foods_text_zh': '鳕鱼汉堡，1根玉米',
        'foods_text_en': 'A cod burger and 1 corn',
        'notes_zh': '晚餐补到了一些蛋白，但因为是汉堡形式，隐藏脂肪、酱料和精制碳水负担可能高于更简单的鳕鱼正餐。',
        'notes_en': 'Dinner adds some protein, but because it came as a burger, hidden fat, sauce, and refined-carb load may be higher than in a simpler cod-based meal.'
    },
}

SESSION_UPDATES = {
    ('2026-04-25', 1): {
        'theme_zh': '肩部 + 手臂 + 核心',
        'theme_en': 'Shoulders + arms + core',
        'intensity_zh': '中等强度',
        'intensity_en': 'Moderate',
        'evaluation_zh': '肩推在高位时略有疲劳，但侧平举和面拉稳定，二头进展顺畅，三头表现好于预期，因此这次训练应计为一次扎实完成的肩部 + 手臂 + 核心日。',
        'evaluation_en': 'Shoulder press started slightly fatigued at the top end, but lateral raise and face pull were stable, biceps work progressed cleanly, and triceps performed better than expected, so this should count as a solid completed shoulders + arms + core day.'
    },
    ('2026-04-26', 1): {
        'theme_zh': '有氧游泳',
        'theme_en': 'Aerobic swim',
        'intensity_zh': '中等强度',
        'intensity_en': 'Moderate',
        'evaluation_zh': '完成了一次中等强度、混合蛙泳和自由泳的游泳训练；整体负荷相较 2026-04-18 更轻、速度更慢，因此更适合作为恢复导向的有氧游，而不是进阶输出型游泳。',
        'evaluation_en': 'Completed a moderate swim session with mixed breaststroke and freestyle; overall load was clearly lighter and slower than on 2026-04-18, so it should be treated more as a recovery-oriented aerobic swim than as a progression swim.'
    },
}

EXERCISE_UPDATES = {
    ('2026-04-25', 'Seated shoulder press'): ('坐姿肩推', 'Seated shoulder press'),
    ('2026-04-25', 'Lateral raise'): ('侧平举', 'Lateral raise'),
    ('2026-04-25', 'Cable face pull'): ('绳索面拉', 'Cable face pull'),
    ('2026-04-25', 'Biceps machine curl'): ('器械二头弯举', 'Biceps machine curl'),
    ('2026-04-25', 'Triceps pressdown / cable triceps'): ('绳索下压 / 绳索三头', 'Triceps pressdown / cable triceps'),
    ("2026-04-25", "Captain's chair leg raise / supported leg raise"): ('队长椅举腿 / 支撑举腿', "Captain's chair leg raise / supported leg raise"),
    ('2026-04-26', 'Breaststroke'): ('蛙泳', 'Breaststroke'),
    ('2026-04-26', 'Freestyle'): ('自由泳', 'Freestyle'),
    ('2026-04-26', 'Total swim distance'): ('总游泳距离', 'Total swim distance'),
}


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    for date_text, payload in DAY_UPDATES.items():
        conn.execute(
            'update days set notes_zh=?, notes_en=? where date=?',
            (payload['notes_zh'], payload['notes_en'], date_text),
        )

    for (date_text, meal_slot), payload in MEAL_UPDATES.items():
        conn.execute(
            '''
            update meals
               set meal_slot_zh=?, meal_slot_en=?, foods_text_zh=?, foods_text_en=?, notes_zh=?, notes_en=?
             where date=? and meal_slot=?
            ''',
            (
                payload['meal_slot_zh'], payload['meal_slot_en'],
                payload['foods_text_zh'], payload['foods_text_en'],
                payload['notes_zh'], payload['notes_en'],
                date_text, meal_slot,
            ),
        )

    for (date_text, session_index), payload in SESSION_UPDATES.items():
        conn.execute(
            '''
            update training_sessions
               set theme_zh=?, theme_en=?, intensity_zh=?, intensity_en=?, evaluation_zh=?, evaluation_en=?
             where date=? and session_index=?
            ''',
            (
                payload['theme_zh'], payload['theme_en'],
                payload['intensity_zh'], payload['intensity_en'],
                payload['evaluation_zh'], payload['evaluation_en'],
                date_text, session_index,
            ),
        )

    for (date_text, exercise_name), (name_zh, name_en) in EXERCISE_UPDATES.items():
        session_ids = [row['id'] for row in conn.execute('select id from training_sessions where date=?', (date_text,))]
        for session_id in session_ids:
            conn.execute(
                '''
                update exercises
                   set exercise_name_zh=?, exercise_name_en=?
                 where session_id=? and exercise_name=?
                ''',
                (name_zh, name_en, session_id, exercise_name),
            )

    conn.commit()
    print('bilingual backfill applied for', ', '.join(TARGET_DATES))


if __name__ == '__main__':
    main()
