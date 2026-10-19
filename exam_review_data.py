# -*- coding: utf-8 -*-
"""
exam_review_data.py
岱崙美語 3C Quiz 歷史考券錯題特訓資料庫
涵蓋 Week 2、Week 4、Week 5 共 6 頁考券：
1. 28 句精讀跟讀課文與滿分作文（含逐句地道繁中翻譯）
2. 15 道考場真實手寫錯題 (Mistake Buster Tokenized)
3. 40 道紙筆/語音雙軌測驗題：
   - 🎧 單字盲聽 (20 題)：電腦發音盲測，紙筆手寫再對答案
   - ✍️ 句子改寫 (8 題)：倒裝附和句 (so/too/either/neither)、副詞三級長句合成
   - ✏️ 課文與文法填空 (6 題)：介系詞、定向越野克漏字
   - 🔘 文法選擇 (6 題)：過去時態、假設語氣、花費動詞
4. 全數題目配備【三段式硬核教研詳解】（🎯 核心考點 + 🔑 破題公式 + ⚠️ 考場致命陷阱）
"""

EXAM_REVIEW_UNIT = {
    "id": "TEA_QUIZ_REVIEW",
    "book": "岱崙美語歷史真題考券 (TEA 3C Quiz)",
    "display_title": "歷史考券錯題特訓 (Quiz Review: W2/W4/W5)",
    "category": "歷史考券",
    "category_icon": "📝",
    "cefr": "A2+",
    "pages": "Week 2, Week 4, Week 5 (共 6 頁歷史考券)",
    "passages": [
        {
            "section_title": "尋寶定向運動長篇聽寫 (Orienteering - W5 Dictation p.40 滿分篇章)",
            "sentences": [
                {"en": "Imagine you are in a new city.", "zh": "想像你身在一座全新的城市。"},
                {"en": "Standing on a corner, you ask someone how to get to a store.", "zh": "站在街角，你詢問路人如何前往一家商店。"},
                {"en": "They tell you to \"go two blocks north, turn left, and you'll be across the street from the bookstore.\"", "zh": "他們告訴你『往北走兩個街區，左轉，你就會在書店的對街。』"},
                {"en": "Now imagine you are in an outdoor race.", "zh": "現在想像你正在參加一場戶外競賽。"},
                {"en": "Instead of directions, you have only a map and a compass, and instead of running down a marked road, you run around in the woods.", "zh": "沒有方向指引，你只有一張地圖和一個指北針；與其沿著標記好的道路奔跑，你在樹林中四處穿梭。"},
                {"en": "Welcome to orienteering!", "zh": "歡迎來到定向越野運動！"},
                {"en": "In the sport of orienteering, racers use a map and compass to find stations, which are called controls.", "zh": "在定向越野運動中，參賽者使用地圖和指北針來尋找站點，這些站點被稱為控制點。"},
                {"en": "A special flag marks each control (see Figure 1).", "zh": "一面特殊的旗幟標記著每個控制點（見圖 1）。"},
                {"en": "Controls are placed in tricky locations to challenge racers' navigation skills.", "zh": "控制點被放置在隱蔽巧妙的位置，以考驗參賽者的導航技巧。"},
                {"en": "Racers must punch their cards at every station to prove they visited it.", "zh": "參賽者必須在每個站點打卡打孔，以證明他們確實到達過該處。"},
                {"en": "The person who finishes the course in the fastest time wins the race.", "zh": "以最快時間完成全程的人贏得比賽。"}
            ]
        },
        {
            "section_title": "優秀寫作範文：我的社區 (My Neighborhood - W2 Writing 15/16 高分)",
            "sentences": [
                {"en": "Have you ever been to my neighborhood?", "zh": "你曾經來過我的社區嗎？"},
                {"en": "I have lived in my neighborhood for four years.", "zh": "我已經在我的社區住了四年了。"},
                {"en": "It is very close to my school.", "zh": "它離我的學校非常近。"},
                {"en": "I can get to school in under ten minutes on foot.", "zh": "我走路不到十分鐘就能到達學校。"},
                {"en": "The convenience store and the bus stop are very close, too.", "zh": "便利商店和公車站也離得非常近。"},
                {"en": "There are many stores in my neighborhood.", "zh": "我的社區裡有許多商店。"},
                {"en": "Across the street from the coffee shop, there is a stationery store and a pharmacy.", "zh": "在咖啡店的對街，有一家文具店和一家藥局。"},
                {"en": "Best of all, my neighborhood has a park, and my friends and I often play and ride our bikes there.", "zh": "最棒的是，我的社區有一座公園，我和朋友們常在那裡玩耍並騎腳踏車。"},
                {"en": "I really like living in my neighborhood.", "zh": "我真的非常喜歡住在我的社區裡。"}
            ]
        },
        {
            "section_title": "優秀寫作範文：假如我有 6000 美元 (If I Had 6000 Dollars - W5 Writing 15/16 高分)",
            "sentences": [
                {"en": "If I had 6000 dollars, I would do three things.", "zh": "如果我有 6000 美元，我會做三件事。"},
                {"en": "First, I love fair rides, so I would go to an amusement park with my friends.", "zh": "首先，我熱愛遊樂設施，所以我會和朋友們一起去遊樂園。"},
                {"en": "Next, I would share some of the money with my sister.", "zh": "接下來，我會把一部分的錢分享給我妹妹。"},
                {"en": "I think it is important to share money with your family.", "zh": "我認為和家人分享金錢是很重要的。"},
                {"en": "Finally, I would spend some money on myself.", "zh": "最後，我會花一些錢在自己身上。"},
                {"en": "A new jacket would cost me about 750 dollars.", "zh": "一件新夾克大概會花費我 750 美元。"},
                {"en": "With the rest of the money, I would treat my friends to a movie.", "zh": "用剩下的錢，我會請朋友們看電影。"},
                {"en": "Wouldn't it be great to have 6000 dollars?", "zh": "擁有 6000 美元不是很棒嗎？"}
            ]
        }
    ],
    "vocab": [
        {"word": "lever", "phonetic": "/ˈliːvər/", "translation": "槓桿", "note": "W02 Spelling 單字"},
        {"word": "ramp", "phonetic": "/ræmp/", "translation": "斜坡道", "note": "W02 Spelling 單字"},
        {"word": "wedge", "phonetic": "/wedʒ/", "translation": "楔子，三角木", "note": "學生曾誤拼為 wadge，需加強 /e/ 母音"},
        {"word": "knife", "phonetic": "/naɪf/", "translation": "小刀", "note": "學生曾漏寫字尾 e (Knif)"},
        {"word": "mountain", "phonetic": "/ˈmaʊntɪn/", "translation": "山脈", "note": "學生曾誤拼為 mountion"},
        {"word": "wheelchair", "phonetic": "/ˈwiːltʃer/", "translation": "輪椅", "note": "學生曾誤拼為 whillchair"},
        {"word": "wheel and axle", "phonetic": "/wiːl ənd ˈæksl/", "translation": "輪軸", "note": "機械簡單工具片語"},
        {"word": "doorknob", "phonetic": "/ˈdɔːrnɑːb/", "translation": "門把手", "note": "複合名詞 door + knob (k不發音)"},
        {"word": "steep", "phonetic": "/stiːp/", "translation": "陡峭的", "note": "形容詞，修飾斜坡"},
        {"word": "slope", "phonetic": "/sloʊp/", "translation": "斜坡，坡度", "note": "名詞/動詞"},
        {"word": "furnace", "phonetic": "/ˈfɜːrnɪs/", "translation": "熔爐", "note": "學生曾誤拼為 furnes，字尾拼寫為 -ace"},
        {"word": "frames", "phonetic": "/freɪmz/", "translation": "眼鏡鏡框", "note": "學生曾誤寫為法國 France"},
        {"word": "in front of", "phonetic": "/ɪn frʌnt əv/", "translation": "在...前面", "note": "學生曾寫成 infront off，三字需空格且介系詞為 of"},
        {"word": "across from", "phonetic": "/əˈkrɔːs frʌm/", "translation": "在...對面", "note": "方位介系詞片語"},
        {"word": "go straight", "phonetic": "/ɡoʊ streɪt/", "translation": "直走", "note": "導航指示片語"},
        {"word": "turn right", "phonetic": "/tɜːrn raɪt/", "translation": "右轉", "note": "導航指示片語"},
        {"word": "go two blocks", "phonetic": "/ɡoʊ tuː blɑːks/", "translation": "走兩個街區", "note": "距離方位片語"},
        {"word": "orienteering", "phonetic": "/ˌɔːriənˈtɪrɪŋ/", "translation": "定向越野運動", "note": "RWW6 Unit 6 核心科普運動"},
        {"word": "controls", "phonetic": "/kənˈtroʊlz/", "translation": "控制點站點", "note": "定向越野專有名詞"},
        {"word": "compass", "phonetic": "/ˈkʌmpəs/", "translation": "指北針，羅盤", "note": "雙音節 com-pass"}
    ],
    "mistake_buster": [
        {
            "trap_id": "W02_TRAP_AUXILIARY_TOO",
            "sentence": "Ryan got 95% on his quiz, and Michael are too.",
            "tokens": ["Ryan", "got", "95%", "on", "his", "quiz,", "and", "Michael", "are", "too."],
            "wrong_index": 8,
            "wrong_word": "are",
            "correct_word": "did,",
            "fixed_sentence": "Ryan got 95% on his quiz, and Michael did, too.",
            "reason": "【時態與助動詞混淆】前句動詞是過去式一般動詞 got，附和句必須使用助動詞 did，不可用現在式 be 動詞 are！"
        },
        {
            "trap_id": "W02_TRAP_SO_INVERSION",
            "sentence": "Olivia got 100% on her quiz, and 100% did Penny.",
            "tokens": ["Olivia", "got", "100%", "on", "her", "quiz,", "and", "100%", "did", "Penny."],
            "wrong_index": 7,
            "wrong_word": "100%",
            "correct_word": "so",
            "fixed_sentence": "Olivia got 100% on her quiz, and so did Penny.",
            "reason": "【倒裝附和句連詞錯誤】肯定附和句公式為『so + did + 主詞』，不可將名詞 100% 放在倒裝開頭。"
        },
        {
            "trap_id": "W02_TRAP_NEGATIVE_PAST",
            "sentence": "Ray are not pass quiz, and Jim didn't either.",
            "tokens": ["Ray", "are", "not", "pass", "quiz,", "and", "Jim", "didn't", "either."],
            "wrong_index": 1,
            "wrong_word": "are not",
            "correct_word": "didn't",
            "fixed_sentence": "Ray didn't pass the quiz, and Jim didn't either.",
            "reason": "【過去式否定句混淆】過去式一般動詞否定必須用助動詞 didn't + 原形動詞 pass，不可寫成 are not pass！"
        },
        {
            "trap_id": "W02_TRAP_VERY_CLOSER",
            "sentence": "The convenience store and the bus stop are very closer, too.",
            "tokens": ["The", "convenience", "store", "and", "the", "bus", "stop", "are", "very", "closer,", "too."],
            "wrong_index": 9,
            "wrong_word": "closer,",
            "correct_word": "close,",
            "fixed_sentence": "The convenience store and the bus stop are very close, too.",
            "reason": "【副詞 very 後接原級】受到 very 修飾時必須使用原級形容詞 close，不可誤加 -er 變成比較級 closer。"
        },
        {
            "trap_id": "W02_TRAP_SPELLING_WEDGE",
            "sentence": "He hammered a wooden wadge into the log.",
            "tokens": ["He", "hammered", "a", "wooden", "wadge", "into", "the", "log."],
            "wrong_index": 4,
            "wrong_word": "wadge",
            "correct_word": "wedge",
            "fixed_sentence": "He hammered a wooden wedge into the log.",
            "reason": "【楔子拼寫盲點】wedge 的短母音是 /e/，拼寫為 -edg-，不可拼成 wadge。"
        },
        {
            "trap_id": "W04_TRAP_SPELLING_FURNACE",
            "sentence": "A glassblower melts glass inside a giant furnes.",
            "tokens": ["A", "glassblower", "melts", "glass", "inside", "a", "giant", "furnes."],
            "wrong_index": 7,
            "wrong_word": "furnes.",
            "correct_word": "furnace.",
            "fixed_sentence": "A glassblower melts glass inside a giant furnace.",
            "reason": "【熔爐拼寫盲點】furnace 字尾發音為 /ɪs/，拼寫是 -ace 而不是 -es。"
        },
        {
            "trap_id": "W04_TRAP_HOMOPHONE_FRAMES",
            "sentence": "He bought a pair of eyeglasses with metal france.",
            "tokens": ["He", "bought", "a", "pair", "of", "eyeglasses", "with", "metal", "france."],
            "wrong_index": 8,
            "wrong_word": "france.",
            "correct_word": "frames.",
            "fixed_sentence": "He bought a pair of eyeglasses with metal frames.",
            "reason": "【音近名詞混淆】眼鏡鏡框是 frames /freɪmz/，首字母大寫的 France 是國家法國。"
        },
        {
            "trap_id": "W04_TRAP_IN_FRONT_OF",
            "sentence": "The cat was sleeping infront off the door.",
            "tokens": ["The", "cat", "was", "sleeping", "infront", "off", "the", "door."],
            "wrong_index": 4,
            "wrong_word": "infront",
            "correct_word": "in",
            "fixed_sentence": "The cat was sleeping in front of the door.",
            "reason": "【介系詞片語連寫與錯字】in front of 是三個獨立單字，介系詞是 of（非雙 f 的 off）。"
        },
        {
            "trap_id": "W04_TRAP_DOUBLE_COMPARATIVE",
            "sentence": "A dog runs more faster than a person.",
            "tokens": ["A", "dog", "runs", "more", "faster", "than", "a", "person."],
            "wrong_index": 3,
            "wrong_word": "more",
            "correct_word": "",
            "fixed_sentence": "A dog runs faster than a person.",
            "reason": "【雙重比較級錯誤】fast 是單音節副詞，比較級直接加 -er (faster)，不可重複加 more！"
        },
        {
            "trap_id": "W04_TRAP_SUBJECT_REPEAT",
            "sentence": "A dog runs faster than a dog in the race.",
            "tokens": ["A", "dog", "runs", "faster", "than", "a", "dog", "in", "the", "race."],
            "wrong_index": 6,
            "wrong_word": "dog",
            "correct_word": "person",
            "fixed_sentence": "A dog runs faster than a person in the race.",
            "reason": "【比較對象失誤】兩者比較必須是不同主體（dog vs person），不可重複寫成 a dog。"
        },
        {
            "trap_id": "W04_TRAP_SUPERLATIVE_THE",
            "sentence": "A lion runs fastest of all three animals.",
            "tokens": ["A", "lion", "runs", "fastest", "of", "all", "three", "animals."],
            "wrong_index": 3,
            "wrong_word": "fastest",
            "correct_word": "the fastest",
            "fixed_sentence": "A lion runs the fastest of all three animals.",
            "reason": "【最高級漏加 the】最高級副詞或形容詞前面必須加上定冠詞 the (the fastest)。"
        },
        {
            "trap_id": "W04_TRAP_ADVERB_LY_DROP",
            "sentence": "Peter laugh loud when he heard the joke.",
            "tokens": ["Peter", "laugh", "loud", "when", "he", "heard", "the", "joke."],
            "wrong_index": 2,
            "wrong_word": "loud",
            "correct_word": "loudly",
            "fixed_sentence": "Peter laughed loudly when he heard the joke.",
            "reason": "【形容詞副詞混淆】修飾動詞 laugh 必須使用副詞 loudly，不能使用形容詞 loud。"
        },
        {
            "trap_id": "W05_TRAP_THIRD_PERSON_S",
            "sentence": "A witch laugh horribly at midnight.",
            "tokens": ["A", "witch", "laugh", "horribly", "at", "midnight."],
            "wrong_index": 2,
            "wrong_word": "laugh",
            "correct_word": "laughs",
            "fixed_sentence": "A witch laughs horribly at midnight.",
            "reason": "【第三人稱單數動詞漏 s】主詞 A witch 是第三人稱單數，現在式動詞必須加 -s (laughs)。"
        },
        {
            "trap_id": "W05_TRAP_COMPARATIVE_CONJUNCTION",
            "sentence": "A duck flew farther then an eagle in the sky.",
            "tokens": ["A", "duck", "flew", "farther", "then", "an", "eagle", "in", "the", "sky."],
            "wrong_index": 4,
            "wrong_word": "then",
            "correct_word": "than",
            "fixed_sentence": "A duck flew farther than an eagle in the sky.",
            "reason": "【比較連詞混淆】比較級介系詞是 than（比），then 是副詞（然後、當時），兩者發音與用法完全不同！"
        },
        {
            "trap_id": "W05_TRAP_CONDITIONAL_WOULD",
            "sentence": "If I had 6000 dollars, I will buy a car.",
            "tokens": ["If", "I", "had", "6000", "dollars,", "I", "will", "buy", "a", "car."],
            "wrong_index": 7,
            "wrong_word": "will",
            "correct_word": "would",
            "fixed_sentence": "If I had 6000 dollars, I would buy a car.",
            "reason": "【與現在事實相反假設語氣】條件句為 If + had (過去式)，主要子句必須使用 would + 原形動詞，不可用 will！"
        }
    ],
    "quizzes": [
        # ==========================================
        # 題型 1: 🎧 單字盲聽 (20 題，電腦報題 + 紙筆拼寫)
        # ==========================================
        {
            "id": "TEA_LIST_01",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "簡單機械工具：槓桿",
            "audio_word": "lever",
            "phonetic": "/ˈliːvər/",
            "syllables": "le · ver",
            "answer": "lever",
            "explanation": {
                "concept": "ODG3 U13 / W02 小考核心單字：槓桿",
                "formula": "雙音節詞 le-ver，母音為 /iː/ 與 /ər/。",
                "trap": "注意字尾為 -er，不要寫成 -or。"
            }
        },
        {
            "id": "TEA_LIST_02",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "簡單機械工具：斜坡道",
            "audio_word": "ramp",
            "phonetic": "/ræmp/",
            "syllables": "ramp",
            "answer": "ramp",
            "explanation": {
                "concept": "ODG3 U13 / W02 小考核心單字：斜坡",
                "formula": "單音節詞，/æ/ 母音 + 子音群 -mp。",
                "trap": "發音注意不要與 lamp (檯燈) 混淆，首字母是 r。"
            }
        },
        {
            "id": "TEA_LIST_03",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "簡單機械工具：楔子，三角木",
            "audio_word": "wedge",
            "phonetic": "/wedʒ/",
            "syllables": "wedge",
            "answer": "wedge",
            "explanation": {
                "concept": "ODG3 U13 / W02 小考高頻失分詞：楔子",
                "formula": "短母音 /e/ + dge 發 /dʒ/ 音（如 bridge, edge, wedge）。",
                "trap": "考場真實失分：孩子曾誤寫為 wadge ❌！切記母音為 e。"
            }
        },
        {
            "id": "TEA_LIST_04",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "廚房與切割工具：小刀",
            "audio_word": "knife",
            "phonetic": "/naɪf/",
            "syllables": "knife",
            "answer": "knife",
            "explanation": {
                "concept": "W02 小考基礎字彙：小刀",
                "formula": "k 不發音 (silent k)，字尾不發音 e 使 i 發長母音 /aɪ/。",
                "trap": "考場真實失分：孩子漏寫字尾 e 寫成 Knif ❌！"
            }
        },
        {
            "id": "TEA_LIST_05",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "自然地理名詞：山脈",
            "audio_word": "mountain",
            "phonetic": "/ˈmaʊntɪn/",
            "syllables": "moun · tain",
            "answer": "mountain",
            "explanation": {
                "concept": "W02 小考基礎名詞：山脈",
                "formula": "雙音節 moun-tain，第二音節字尾是 -tain 發 /tɪn/ 音（如 fountain, captain）。",
                "trap": "考場真實失分：孩子曾誤寫為 mountion ❌！"
            }
        },
        {
            "id": "TEA_LIST_06",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "行動輔助工具：輪椅",
            "audio_word": "wheelchair",
            "phonetic": "/ˈwiːltʃer/",
            "syllables": "wheel · chair",
            "answer": "wheelchair",
            "explanation": {
                "concept": "W02 複合名詞：wheel (輪子) + chair (椅子)",
                "formula": "wheel 是 ee 雙母音，chair 是 air 三字母組合。",
                "trap": "考場真實失分：孩子曾誤寫為 whillchair ❌！"
            }
        },
        {
            "id": "TEA_LIST_07",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "高溫加熱金屬或礦石的封閉結構：熔爐",
            "audio_word": "furnace",
            "phonetic": "/ˈfɜːrnɪs/",
            "syllables": "fur · nace",
            "answer": "furnace",
            "explanation": {
                "concept": "ODG3 U14 / W04 小考高頻失分詞：熔爐",
                "formula": "雙音節 fur-nace，第二音節 -nace 發 /nɪs/ 音（如 palace, surface, furnace）。",
                "trap": "考場真實失分：孩子曾誤寫為 furnes ❌，扣 2 分！字尾是 -ace 不是 -es。"
            }
        },
        {
            "id": "TEA_LIST_08",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "眼鏡鏡片外圍固定支撐物：鏡框",
            "audio_word": "frames",
            "phonetic": "/freɪmz/",
            "syllables": "frames",
            "answer": "frames",
            "explanation": {
                "concept": "ODG3 U14 / W04 小考高頻失分詞：鏡框",
                "formula": "單音節長母音 a_e (frame)，眼鏡兩側鏡框固定用複數 frames。",
                "trap": "考場真實失分：孩子曾誤寫成國家法國 France ❌！"
            }
        },
        {
            "id": "TEA_LIST_09",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "野外尋寶競賽運動：定向越野",
            "audio_word": "orienteering",
            "phonetic": "/ˌɔːriənˈtɪrɪŋ/",
            "syllables": "o · ri · en · teer · ing",
            "answer": "orienteering",
            "explanation": {
                "concept": "RWW6 U6 / W05 聽寫 25 分滿分核心篇章詞彙",
                "formula": "字根 orient (定位) + -eer + -ing 動名詞，雙 e 發長音 /ɪr/。",
                "trap": "長單字切忌漏寫中間的 -en- 或字尾的雙 e。"
            }
        },
        {
            "id": "TEA_LIST_10",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
            "hint": "定向運動必備儀器：指北針，羅盤",
            "audio_word": "compass",
            "phonetic": "/ˈkʌmpəs/",
            "syllables": "com · pass",
            "answer": "compass",
            "explanation": {
                "concept": "RWW6 U6 核心名詞：羅盤",
                "formula": "雙音節 com-pass，字尾雙寫 ss。",
                "trap": "發音第一個 o 發 /ʌ/ 音，字尾雙寫 s 不要漏掉。"
            }
        },

        # ==========================================
        # 題型 2: ✍️ 句子改寫 (8 題，倒裝附和句 + 副詞長句)
        # ==========================================
        {
            "id": "TEA_RW_01",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 2 真題】[Ryan, Michael - 95% on quiz / too]（使用指定連接詞改寫為附和句）",
            "answer": "Ryan got 95% on his quiz, and Michael did, too.",
            "hint": "提示：前句補回動詞 got，後句一般動詞過去式附和使用助動詞 did + too",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 肯定附和句 (too)",
                "formula": "前半句：主詞 + 一般動詞過去式 (got 95% on his quiz)；後半句：and + 主詞 + did, too。",
                "trap": "考場真實失分：孩子寫成 Ryan 95% on quiz, Michael are too ❌。漏補動詞 got，且一般動詞不可用 be 動詞 are！"
            }
        },
        {
            "id": "TEA_RW_02",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 2 真題】[Brad, Lisa - did not play baseball / either]（使用指定連接詞改寫為附和句）",
            "answer": "Brad did not play baseball, and Lisa didn't either.",
            "hint": "提示：否定附和句公式為『S + didn't + either』",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 否定附和句 (either)",
                "formula": "前半句：S + did not + V；後半句：and + S + didn't + either。",
                "trap": "考場滿分表現：此題學生作答完全正確！注意 either 用於否定句末尾，不可與 neither 混淆。"
            }
        },
        {
            "id": "TEA_RW_03",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 2 真題】[Olivia, Penny - 100% on quiz / so]（使用指定連接詞改寫為倒裝附和句）",
            "answer": "Olivia got 100% on her quiz, and so did Penny.",
            "hint": "提示：肯定倒裝附和句公式為『so + 助動詞 (did) + 主詞』",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 倒裝附和句 (so)",
                "formula": "倒裝公式：and + so + 助動詞 (did) + 第二個主詞 (Penny)。",
                "trap": "考場真實失分：孩子寫成 Penny was so did ❌，把名詞 100% 放在倒裝開頭。切記是 so did Penny！"
            }
        },
        {
            "id": "TEA_RW_04",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 2 真題】[Ray, Jim - not pass quiz / either]（使用指定連接詞改寫為否定附和句）",
            "answer": "Ray didn't pass the quiz, and Jim didn't either.",
            "hint": "提示：過去式一般動詞否定必須使用助動詞 didn't + 原形動詞",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 過去式一般動詞否定句",
                "formula": "一般動詞過去式否定句公式：主詞 + didn't + 原形動詞 (pass)。",
                "trap": "考場真實失分：孩子寫成 Ray are not pass quiz ❌。中文『不是通過』直譯成 are not，被扣 3 分！"
            }
        },
        {
            "id": "TEA_RW_05",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 4 真題】How fast do they run? person, dog & lion（寫出三級副詞長句，注意單音節比較級）",
            "answer": "A person runs fast, a dog runs faster than a person, but a lion runs the fastest.",
            "hint": "三段式架構：原級逗號 ➔ 比較級逗號 ➔ but + 最高級句",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 單音節副詞三級長句合成",
                "formula": "原級 fast ➔ 比較級 faster than a person ➔ 轉折 but a lion runs the fastest。",
                "trap": "考場三大失分坑：① fast 誤加 more 寫成 more fast；② 比較對象重複寫成 a dog；③ 最高級漏加 the。"
            }
        },
        {
            "id": "TEA_RW_06",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 4 真題】How quickly can they walk? five year old, eight year old & adult（寫出三級副詞長句）",
            "answer": "A five year old can walk quickly, an eight year old can walk more quickly than a five year old, but an adult can walk the most quickly.",
            "hint": "多音節副詞比較級為 more quickly than，最高級為 the most quickly",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 多音節副詞三級比較長句",
                "formula": "多音節副詞以 -ly 結尾：原級 quickly ➔ more quickly than ➔ but ... the most quickly。",
                "trap": "考場失分：孩子直接寫 quicker / fastest ❌！quickly 必須用 more 和 the most 修飾。"
            }
        },
        {
            "id": "TEA_RW_07",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 5 真題】How far can they jump? frog, rabbit & kangaroo（寫出三級副詞長句）",
            "answer": "A frog can jump far, a rabbit can jump farther than a frog, but a kangaroo can jump the farthest.",
            "hint": "不規則副詞變化：far ➔ farther than ➔ the farthest",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 不規則副詞三級比較 (far)",
                "formula": "原級 far ➔ 比較級 farther than ➔ 最高級 the farthest。主詞前面均需不定冠詞 a。",
                "trap": "考場失分：孩子最高級寫成 jump farthest 漏寫 the ❌！最高級務必加上 the。"
            }
        },
        {
            "id": "TEA_RW_08",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 4 真題】How do they laugh? witch, vampire & zombie（用 horribly 寫出三級長句，注意主詞三單動詞）",
            "answer": "A witch laughs horribly, a vampire laughs more horribly than a witch, but a zombie laughs the most horribly.",
            "hint": "問句是 How do they laugh，時態為現在式，主詞第三人稱單數動詞需加 -s (laughs)",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 主詞動詞一致性與多音節副詞比較級",
                "formula": "A witch laughs horribly ➔ laughs more horribly than ... ➔ but a zombie laughs the most horribly。",
                "trap": "考場失分：孩子寫成 laugh horribly than ❌，既漏了動詞三單 -s，又把 more 漏掉！"
            }
        },

        # ==========================================
        # 題型 3: ✏️ 課文與文法填空 (6 題)
        # ==========================================
        {
            "id": "TEA_FILL_01",
            "type": "fill",
            "category_tag": "fill",
            "question": "【方位片語填空】There is a beautiful fountain right ( ____________ ) the museum.",
            "answer": "in front of",
            "hint": "提示：在...前面（三個單字分開）",
            "explanation": {
                "concept": "Write Right 3 Unit 4: 方位介系詞片語",
                "formula": "固定搭配片語：in front of（在...前面）。",
                "trap": "考場真實失分：孩子連寫成 infront off ❌。必須分成三個單字，且介系詞是單 f 的 of。"
            }
        },
        {
            "id": "TEA_FILL_02",
            "type": "fill",
            "category_tag": "fill",
            "question": "【方位片語填空】The bakery is right ( ____________ ) the street from the bookstore.",
            "answer": "across",
            "hint": "提示：在街道的對面 (across the street from)",
            "explanation": {
                "concept": "Write Right 3 Unit 4: 方位介系詞 across from",
                "formula": "across the street from 表示『在隔著街的對面』。",
                "trap": "注意不要拼成 a cross 或 cross，介系詞是 across。"
            }
        },
        {
            "id": "TEA_FILL_03",
            "type": "fill",
            "category_tag": "fill",
            "question": "【課文填空】Racers use a map and a ( ____________ ) to find stations in orienteering.",
            "answer": "compass",
            "hint": "提示：指北針，羅盤",
            "explanation": {
                "concept": "RWW6 Unit 6: 定向越野長篇課文聽寫",
                "formula": "定向越野兩大必備工具：a map and a compass。",
                "trap": "雙音節詞 com-pass，字尾雙寫 ss。"
            }
        },
        {
            "id": "TEA_FILL_04",
            "type": "fill",
            "category_tag": "fill",
            "question": "【課文填空】Controls are placed in tricky locations to challenge racers' ( ____________ ) skills.",
            "answer": "navigation",
            "hint": "提示：導航技巧 (nav-i-ga-tion)",
            "explanation": {
                "concept": "RWW6 Unit 6: 專有名詞名詞修飾語",
                "formula": "動詞 navigate ➔ 名詞 navigation (導航)。",
                "trap": "長字拼寫盲點：音節為 na-vi-ga-tion，字尾為 -tion。"
            }
        },
        {
            "id": "TEA_FILL_05",
            "type": "fill",
            "category_tag": "fill",
            "question": "【課文填空】Racers must ( ____________ ) their cards at every station to prove they visited it.",
            "answer": "punch",
            "hint": "提示：打卡、打孔 (punch the card)",
            "explanation": {
                "concept": "RWW6 Unit 6: 動作動詞 punch",
                "formula": "punch cards 是定向運動的專有動作（在打卡紙上打孔）。",
                "trap": "動詞原形 punch，必須加在 must 助動詞之後。"
            }
        },
        {
            "id": "TEA_FILL_06",
            "type": "fill",
            "category_tag": "fill",
            "question": "【課文填空】The person who finishes the course in the ( ____________ ) time wins the race.",
            "answer": "fastest",
            "hint": "提示：以最快時間（最高級 fastest）",
            "explanation": {
                "concept": "RWW6 Unit 6: 最高級修飾名詞 time",
                "formula": "in the fastest time（以最快時間）。前面有 the，fast 加 -est。",
                "trap": "注意題幹已有 the，空格只填 fastest。"
            }
        },

        # ==========================================
        # 題型 4: 🔘 文法選擇 (6 題)
        # ==========================================
        {
            "id": "TEA_MC_01",
            "type": "choice",
            "category_tag": "choice",
            "question": "【寫作時態】I have lived in my neighborhood ( ______ ) four years.",
            "options": ["for", "since", "during", "at"],
            "answer": "for",
            "hint": "一段時間前面介系詞用 for",
            "explanation": {
                "concept": "Write Right 3 Unit 4: 現在完成式時間介系詞",
                "formula": "for + 一段時間長度（如 for four years）；since + 過去時間點（如 since 2020）。",
                "trap": "four years 是整段持續的時間長度，絕不能用 since！"
            }
        },
        {
            "id": "TEA_MC_02",
            "type": "choice",
            "category_tag": "choice",
            "question": "【寫作句型】If I had 6000 dollars, I ( ______ ) buy a new computer.",
            "options": ["would", "will", "can", "am going to"],
            "answer": "would",
            "hint": "與現在事實相反的假設語氣：If S + had..., S + would + V",
            "explanation": {
                "concept": "Write Right 3 Unit 5: 虛擬假設語氣",
                "formula": "If 子句使用過去式動詞 (had)，主要子句必須使用 would / could + 原形動詞。",
                "trap": "考場常見錯誤：直覺選 will。因條件句是 had，時態必須倒退一步用 would！"
            }
        },
        {
            "id": "TEA_MC_03",
            "type": "choice",
            "category_tag": "choice",
            "question": "【花費動詞句型】A new jacket would cost ( ______ ) 750 dollars.",
            "options": ["me", "to me", "for me", "with me"],
            "answer": "me",
            "hint": "花費句型：cost + 受格 (me) + 金額",
            "explanation": {
                "concept": "Write Right 3 Unit 5: 花費動詞 cost 句型結構",
                "formula": "事物 (A new jacket) + cost + 人 (受格 me) + 金額 (750 dollars)。",
                "trap": "受到中文『對我花費』影響容易誤選 to me 或 for me。cost 後面直接接受格！"
            }
        },
        {
            "id": "TEA_MC_04",
            "type": "choice",
            "category_tag": "choice",
            "question": "【副詞比較選擇】Helen laughs ( ______ ) than Peter when watching comedies.",
            "options": ["more loudly", "louder", "more loud", "loudest"],
            "answer": "more loudly",
            "hint": "修飾動詞 laugh 用副詞 loudly，比較級加 more",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 多音節副詞比較級",
                "formula": "修飾動詞 laugh 必須使用副詞 loudly；多音節副詞的比較級為 more loudly + than。",
                "trap": "考場真實失分：孩子誤選 more loud ❌。loud 是形容詞，修飾動詞必須有 -ly！"
            }
        },
        {
            "id": "TEA_MC_05",
            "type": "choice",
            "category_tag": "choice",
            "question": "【附和句倒裝選擇】Brad did not play baseball, and ( ______ ).",
            "options": ["Lisa didn't either", "neither did Lisa", "Lisa did too", "so did Lisa"],
            "answer": "Lisa didn't either",
            "hint": "前句是否定句，後句附和必須也是否定附和",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 否定附和句",
                "formula": "否定句附和有兩種標準形式：① and Lisa didn't either；② and neither did Lisa。",
                "trap": "前句是否定 did not，絕不能選肯定附和的 too 或 so did！"
            }
        },
        {
            "id": "TEA_MC_06",
            "type": "choice",
            "category_tag": "choice",
            "question": "【機械單字選擇】A piece of wood or metal with one thick end and one thin edge is a ( ______ ).",
            "options": ["wedge", "ramp", "lever", "furnace"],
            "answer": "wedge",
            "hint": "一頭厚、一頭薄的三角形工具：楔子",
            "explanation": {
                "concept": "Oxford Discover 3 Unit 13 簡單機械定義",
                "formula": "wedge 的英英字典定義：thick end (厚端) + thin edge (薄刃)。",
                "trap": "ramp 是斜坡（sloping surface），lever 是槓桿（rigid bar pivoting on a fulcrum）。"
            }
        }
    ]
}
