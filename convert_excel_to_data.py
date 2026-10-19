import openpyxl
import json
import os
import re

EXCEL_PATH = r"C:\@植善課業\AI\Tiger_5th 2 nd\Tiger 5th 2ndBooks.xlsx"
OUTPUT_JS_PATH = r"C:\@植善課業\AI\英語學習網頁\english_data.js"

def safe_str(val):
    if val is None:
        return ""
    return str(val).strip()

def parse_options(val):
    s = safe_str(val)
    if not s:
        return []
    # Try JSON
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return [str(x).strip() for x in parsed]
    except Exception:
        pass
    # If bracket format but failed json
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1]
        parts = [p.strip().strip('"').strip("'") for p in inner.split(",")]
        return [p for p in parts if p]
    # Comma or newline separated
    if "\n" in s:
        return [x.strip() for x in s.split("\n") if x.strip()]
    if "," in s:
        return [x.strip() for x in s.split(",") if x.strip()]
    return [s]

def parse_examples(val):
    s = safe_str(val)
    if not s:
        return []
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return [str(x).strip() for x in parsed]
    except Exception:
        pass
    if "\n" in s:
        return [x.strip() for x in s.split("\n") if x.strip()]
    return [s]

def main():
    print(f"Loading workbook from {EXCEL_PATH}...")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    
    # 1. Books
    books = []
    if "Books" in wb.sheetnames:
        sheet = wb["Books"]
        for row in sheet.iter_rows(min_row=2, values_only=True):
            b_id = safe_str(row[0])
            b_name = safe_str(row[1])
            if b_id:
                # Fix any encoding issues if present
                if "Tiger_" in b_name and "5b" in b_id:
                    b_name = "Tiger 五年級下學期單字"
                books.append({"book_id": b_id, "book_name": b_name})
    print(f"Loaded {len(books)} books.")

    # 2. Units
    units = []
    if "Units" in wb.sheetnames:
        sheet = wb["Units"]
        for row in sheet.iter_rows(min_row=2, values_only=True):
            b_id = safe_str(row[0])
            u_id = safe_str(row[1])
            u_title = safe_str(row[2])
            b_q = safe_str(row[3]) if len(row) > 3 else ""
            if b_id and u_id:
                units.append({
                    "book_id": b_id,
                    "unit_id": u_id,
                    "unit_title": u_title,
                    "big_question": b_q
                })
    print(f"Loaded {len(units)} units.")

    # 3. Reading_Content
    reading_content = []
    if "Reading_Content" in wb.sheetnames:
        sheet = wb["Reading_Content"]
        for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
            b_id = safe_str(row[0])
            u_id = safe_str(row[1])
            if not b_id or not u_id:
                continue
            seq = row[2] if len(row) > 2 and row[2] is not None else (idx + 1)
            eng = safe_str(row[3]) if len(row) > 3 else ""
            chi = safe_str(row[4]) if len(row) > 4 else ""
            exp_eng = safe_str(row[5]) if len(row) > 5 else ""
            exp_chi = safe_str(row[6]) if len(row) > 6 else ""
            reading_content.append({
                "book_id": b_id,
                "unit_id": u_id,
                "sequence": int(seq) if str(seq).isdigit() else (idx + 1),
                "eng": eng,
                "chi": chi,
                "exp_eng": exp_eng,
                "exp_chi": exp_chi
            })
    print(f"Loaded {len(reading_content)} reading content blocks.")

    # 4. Vocabulary
    vocabulary = []
    if "Vocabulary" in wb.sheetnames:
        sheet = wb["Vocabulary"]
        for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
            b_id = safe_str(row[0])
            u_id = safe_str(row[1])
            word = safe_str(row[2])
            if not b_id or not word:
                continue
            pos = safe_str(row[3]) if len(row) > 3 else ""
            chi = safe_str(row[4]) if len(row) > 4 else ""
            breakdown = safe_str(row[5]) if len(row) > 5 else ""
            trick = safe_str(row[6]) if len(row) > 6 else ""
            scene = safe_str(row[7]) if len(row) > 7 else ""
            collocation = safe_str(row[8]) if len(row) > 8 else ""
            img = safe_str(row[9]) if len(row) > 9 else "📝"
            context_eng = safe_str(row[10]) if len(row) > 10 else ""
            context_chi = safe_str(row[11]) if len(row) > 11 else ""
            chant = safe_str(row[12]) if len(row) > 12 else ""
            compare = safe_str(row[13]) if len(row) > 13 else ""
            vocabulary.append({
                "id": f"voc_{idx+1}",
                "book_id": b_id,
                "unit_id": u_id,
                "word": word,
                "pos": pos,
                "chi": chi,
                "breakdown": breakdown,
                "trick": trick,
                "scene": scene,
                "collocation": collocation,
                "img": img,
                "context_eng": context_eng,
                "context_chi": context_chi,
                "chant": chant,
                "compare": compare
            })
    print(f"Loaded {len(vocabulary)} vocabulary words.")

    # 5. Grammar
    grammar_rules = []
    if "Grammar" in wb.sheetnames:
        sheet = wb["Grammar"]
        for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
            b_id = safe_str(row[0])
            u_id = safe_str(row[1])
            rule_title = safe_str(row[2])
            if not b_id or not rule_title:
                continue
            eng_exp = safe_str(row[3]) if len(row) > 3 else ""
            chi_exp = safe_str(row[4]) if len(row) > 4 else ""
            examples = parse_examples(row[5]) if len(row) > 5 else []
            grammar_rules.append({
                "id": f"gra_{idx+1}",
                "book_id": b_id,
                "unit_id": u_id,
                "rule_title": rule_title,
                "eng_exp": eng_exp,
                "chi_exp": chi_exp,
                "examples": examples
            })
    print(f"Loaded {len(grammar_rules)} grammar rules.")

    # 6. Quizzes: Reading, Grammar, Vocab
    quizzes = []
    q_counter = 0

    quiz_types = [
        ("Reading_Quiz", "reading"),
        ("Grammar_Quiz", "grammar"),
        ("Vocab_Quiz", "vocab")
    ]

    for sheet_name, q_type in quiz_types:
        if sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            for row in sheet.iter_rows(min_row=2, values_only=True):
                b_id = safe_str(row[0])
                u_id = safe_str(row[1])
                question = safe_str(row[2])
                if not b_id or not question:
                    continue
                q_counter += 1
                options = parse_options(row[3]) if len(row) > 3 else []
                answer = safe_str(row[4]) if len(row) > 4 else ""
                diff = safe_str(row[5]) if len(row) > 5 else "★★★☆☆"
                explanation = safe_str(row[6]) if len(row) > 6 else ""
                
                quizzes.append({
                    "id": f"q_{q_counter:04d}",
                    "book_id": b_id,
                    "unit_id": u_id,
                    "type": q_type,
                    "question": question,
                    "options": options,
                    "answer": answer,
                    "difficulty": diff if diff else "★★★☆☆",
                    "explanation": explanation
                })
    print(f"Loaded {len(quizzes)} quiz questions.")

    # 7. Add Brain Gym questions (晨間純腦力體操 1★~10★)
    brain_gym_questions = [
        {
            "id": "bg_001",
            "book_id": "od3",
            "unit_id": "od3_1",
            "type": "brain_gym",
            "star": 1,
            "question": "The volleyball match was really ______! All the players were ______ after running for 2 hours.",
            "options": ["exciting; tired", "excited; tiring", "exciting; tiring", "excited; tired"],
            "answer": "exciting; tired",
            "difficulty": "★☆☆☆☆",
            "explanation": "🟢 正確思維：球賽 (match) 是事物本身特質，使用 -ing (exciting)；球員 (players) 是人的心理/身體感受，使用 -ed (tired)。\\n🔴 盲點警示：不可將人的感受誤用 -ing (tiring 指令人疲累的事物)。"
        },
        {
            "id": "bg_002",
            "book_id": "od3",
            "unit_id": "od3_1",
            "type": "brain_gym",
            "star": 2,
            "question": "Which sentence expresses a pure FACT, NOT an opinion?",
            "options": [
                "The first team to reach a score of 25 is the winner.",
                "I think jogging in the park is the most fun sport.",
                "A wedding in Egypt is always a wonderful celebration.",
                "Blue and white are the nicest colors for team uniforms."
            ],
            "answer": "The first team to reach a score of 25 is the winner.",
            "difficulty": "★★☆☆☆",
            "explanation": "🟢 正確思維：排球規則「先得 25 分為勝方」是客觀競賽事實 (Fact)。\\n🔴 盲點警示：I think、wonderful、nicest 皆屬於個人主觀判斷與審美觀點 (Opinion)。"
        },
        {
            "id": "bg_003",
            "book_id": "od3",
            "unit_id": "od3_1",
            "type": "brain_gym",
            "star": 3,
            "question": "Husani called his cousin in London ______ Sunday afternoon to talk about the soccer game.",
            "options": ["on", "in", "at", "during"],
            "answer": "on",
            "difficulty": "★★★☆☆",
            "explanation": "🟢 正確思維：特定某一天或某個星期的上午/下午 (Sunday afternoon)，介系詞必須固定搭配 on。\\n🔴 盲點警示：一般上午 in the afternoon 用 in，但一旦前面加上具體星期 (Sunday)，必須受星期主導改用 on！"
        },
        {
            "id": "bg_004",
            "book_id": "od3",
            "unit_id": "od3_1",
            "type": "brain_gym",
            "star": 4,
            "question": "In the sentence 'The children love the pony ride at the fair,' what part of speech is the word 'ride'?",
            "options": ["Noun (名詞)", "Verb (動詞)", "Adjective (形容詞)", "Adverb (副詞)"],
            "answer": "Noun (名詞)",
            "difficulty": "★★★★☆",
            "explanation": "🟢 正確思維：前面有冠詞 the 與定語 pony，且作為及物動詞 love 的受詞，此處 ride 為名詞 (乘騎體驗)。\\n🔴 盲點警示：若是 'Children love to ride ponies'，則 ride 為動詞。"
        },
        {
            "id": "bg_005",
            "book_id": "od3",
            "unit_id": "od3_1",
            "type": "brain_gym",
            "star": 5,
            "question": "Tom ______ pizza with his family last night, and this morning he ______ a race.",
            "options": ["ate; ran", "eats; runs", "ate; runs", "was eating; ran"],
            "answer": "ate; ran",
            "difficulty": "★★★★★",
            "explanation": "🟢 正確思維：last night 與 this morning (若說話時已是下午) 均為明確過去時間副詞，動詞需統一使用過去式 (ate, ran)。\\n🔴 盲點警示：不可前後時態割裂或動詞三態記錯。"
        }
    ]
    quizzes.extend(brain_gym_questions)

    # 8. Assemble Full Data Object
    full_data = {
        "metadata": {
            "version": "1.0.0",
            "generated_at": "2026-10-18",
            "total_books": len(books),
            "total_units": len(units),
            "total_vocab": len(vocabulary),
            "total_grammar": len(grammar_rules),
            "total_reading": len(reading_content),
            "total_quizzes": len(quizzes)
        },
        "books": books,
        "units": units,
        "reading_content": reading_content,
        "vocabulary": vocabulary,
        "grammar": grammar_rules,
        "quizzes": quizzes
    }

    # 9. Output to JS file
    print(f"Writing to {OUTPUT_JS_PATH}...")
    js_content = "/**\n * 六年級英語特訓系統 — 全域資料層\n * 自動由 Tiger 5th 2ndBooks.xlsx 解析並融合雙層教研規格生成\n */\n"
    js_content += "const ENGLISH_DATA = " + json.dumps(full_data, ensure_ascii=False, indent=2) + ";\n\n"
    js_content += "if (typeof module !== 'undefined' && module.exports) {\n  module.exports = ENGLISH_DATA;\n}\n"

    with open(OUTPUT_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)
    
    file_size = os.path.getsize(OUTPUT_JS_PATH)
    print(f"Done! File generated: {OUTPUT_JS_PATH} ({file_size} bytes)")

if __name__ == "__main__":
    main()
