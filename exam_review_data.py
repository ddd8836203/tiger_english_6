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
    "display_title": "歷史考券錯題特訓 (Quiz Review: W2/W4/W5/W6/W7)",
    "category": "歷史考券",
    "category_icon": "📝",
    "cefr": "A2+",
    "pages": "Week 2, 4, 5, 6, 7 (共 10 頁歷史考券)",
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
        },
        {
            "section_title": "短文改錯滿分訂正版：假如我有 3000 美元 (If I Had 3000 Dollars - W6 Proofreading p.10)",
            "sentences": [
                {"en": "If I had 3000 dollars, I would do three things.", "zh": "如果我有 3000 美元，我會做三件事。"},
                {"en": "First, my family loves baseball, so I would go to a baseball game with them.", "zh": "首先，我的家人熱愛棒球，所以我會和他們一起去看一場棒球賽。"},
                {"en": "Next, I would buy a fish tank for my class.", "zh": "接下來，我會為我的班級買一個魚缸。"},
                {"en": "I think it would brighten up our classroom.", "zh": "我認為它會讓我們的教室變得更有朝氣。"},
                {"en": "Finally, I would spend some money on myself.", "zh": "最後，我會花一些錢在自己身上。"},
                {"en": "I would buy some comic books.", "zh": "我會買一些漫畫書。"},
                {"en": "They would cost me about 300 dollars.", "zh": "它們大約會花費我 300 美元。"},
                {"en": "With the rest of the money, I would treat my friends to lunch.", "zh": "用剩下的錢，我會請我的朋友們吃午餐。"}
            ]
        },
        {
            "section_title": "容器計量詞與可數不可數問答 (Measure Words & Quantifiers - W6 & W7 p.10-11 必考句)",
            "sentences": [
                {"en": "There is a slice of pizza and a carton of milk.", "zh": "那裡有一片披薩和一紙盒牛奶。"},
                {"en": "There are six bottles of water and two cans of tomatoes.", "zh": "那裡有六瓶水和兩罐番茄罐頭。"},
                {"en": "There is a bar of chocolate and a jar of honey.", "zh": "那裡有一條巧克力和一玻璃罐蜂蜜。"},
                {"en": "There are seven slices of bread and two cups of tea.", "zh": "那裡有七片吐司和兩杯茶。"},
                {"en": "How much trash is there? There is a lot of trash.", "zh": "那裡有多少垃圾？那裡有許多垃圾。"},
                {"en": "How many plastic bottles are there? There are a few plastic bottles.", "zh": "那裡有幾個寶特瓶？那裡有幾個寶特瓶。"}
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
        {"word": "compass", "phonetic": "/ˈkʌmpəs/", "translation": "指北針，羅盤", "note": "雙音節 com-pass"},
        {"word": "nectar", "phonetic": "/ˈnektər/", "translation": "花蜜", "note": "W06 學生曾誤拼為 nector，字尾為 -ar"},
        {"word": "petals", "phonetic": "/ˈpetlz/", "translation": "花瓣", "note": "W06 學生曾誤拼為 patels，首音節為 pe-"},
        {"word": "pollen", "phonetic": "/ˈpɑːlən/", "translation": "花粉", "note": "OD3 U15 植物授粉核心單字"},
        {"word": "oxygen", "phonetic": "/ˈɑːksɪdʒən/", "translation": "氧氣", "note": "OD3 U15 植物光合作用單字"},
        {"word": "language", "phonetic": "/ˈlæŋɡwɪdʒ/", "translation": "語言", "note": "W06 學生曾誤拼為 langauges，注意 -gua- 順序"},
        {"word": "official", "phonetic": "/əˈfɪʃl/", "translation": "官方的、正式的", "note": "W06 學生曾漏 i 寫成 offical"},
        {"word": "government", "phonetic": "/ˈɡʌvərnmənt/", "translation": "政府", "note": "W06 學生曾漏 n 寫成 goverment (govern+ment)"},
        {"word": "French", "phonetic": "/frentʃ/", "translation": "法語、法國的", "note": "W06 學生曾寫成 franch，首字母需大寫 F"},
        {"word": "countries", "phonetic": "/ˈkʌntriz/", "translation": "國家(複數)", "note": "W06 學生曾漏 u 寫成 contries"},
        {"word": "example", "phonetic": "/ɪɡˈzæmpl/", "translation": "例子、範例", "note": "W06 學生曾誤寫為 exemple"},
        {"word": "Mandarin", "phonetic": "/ˈmændərɪn/", "translation": "中文普通話、國語", "note": "W06 學生曾誤寫為 manderin，首字母 M 大寫"},
        {"word": "thousand", "phonetic": "/ˈθaʊznd/", "translation": "一千", "note": "W06 學生曾誤寫為 thoudnd (thou+sand)"},
        {"word": "in fact", "phonetic": "/ɪn fækt/", "translation": "事實上", "note": "W06 學生曾聽音硬拼成單字 infecte，實為兩個字"}
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
            "sentence": "Ray are not pass the quiz, and Jim didn't either.",
            "tokens": ["Ray", "are not", "pass", "the", "quiz,", "and", "Jim", "didn't", "either."],
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
            "tokens": ["The", "cat", "was", "sleeping", "infront off", "the", "door."],
            "wrong_index": 4,
            "wrong_word": "infront off",
            "correct_word": "in front of",
            "fixed_sentence": "The cat was sleeping in front of the door.",
            "reason": "【介系詞片語連寫與錯字】in front of 是三個獨立單字，介系詞是 of（非雙 f 的 off）。"
        },
        {
            "trap_id": "W04_TRAP_DOUBLE_COMPARATIVE",
            "sentence": "A dog runs more faster than a person.",
            "tokens": ["A", "dog", "runs", "more faster", "than", "a", "person."],
            "wrong_index": 3,
            "wrong_word": "more faster",
            "correct_word": "faster",
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
            "sentence": "Peter laughed loud when he heard the joke.",
            "tokens": ["Peter", "laughed", "loud", "when", "he", "heard", "the", "joke."],
            "wrong_index": 2,
            "wrong_word": "loud",
            "correct_word": "loudly",
            "fixed_sentence": "Peter laughed loudly when he heard the joke.",
            "reason": "【形容詞副詞混淆】修飾動詞 laughed 必須使用副詞 loudly，不能使用形容詞 loud。"
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
            "wrong_index": 6,
            "wrong_word": "will",
            "correct_word": "would",
            "fixed_sentence": "If I had 6000 dollars, I would buy a car.",
            "reason": "【與現在事實相反假設語氣】條件句為 If + had (過去式)，主要子句必須使用 would + 原形動詞，不可用 will！"
        },
        {
            "trap_id": "W06_TRAP_GO_TO_GAME",
            "sentence": "First, my family loves baseball, so I would go a baseball game with them.",
            "tokens": ["First,", "my", "family", "loves", "baseball,", "so", "I", "would", "go", "a", "baseball", "game", "with", "them."],
            "wrong_index": 8,
            "wrong_word": "go",
            "correct_word": "go to",
            "fixed_sentence": "First, my family loves baseball, so I would go to a baseball game with them.",
            "reason": "【W6 真題漏抓：不及物動詞 go 漏介系詞 to】go 後接活動或地點名詞 (a baseball game) 必須加介系詞 to！"
        },
        {
            "trap_id": "W06_TRAP_WOULD_BY_BUY",
            "sentence": "I would by some comic books at the bookstore.",
            "tokens": ["I", "would", "by", "some", "comic", "books", "at", "the", "bookstore."],
            "wrong_index": 2,
            "wrong_word": "by",
            "correct_word": "buy",
            "fixed_sentence": "I would buy some comic books at the bookstore.",
            "reason": "【W6 真題漏抓：同音異字 by vs. buy】助動詞 would 後面必須接原形動詞 buy（購買），by 是介系詞！"
        },
        {
            "trap_id": "W06_TRAP_REST_OF_MONEY",
            "sentence": "With rest of the money, I would treat my friends to lunch.",
            "tokens": ["With", "rest", "of", "the", "money,", "I", "would", "treat", "my", "friends", "to", "lunch."],
            "wrong_index": 1,
            "wrong_word": "rest",
            "correct_word": "the rest",
            "fixed_sentence": "With the rest of the money, I would treat my friends to lunch.",
            "reason": "【W6 真題失分：With the rest of the money 漏 the】表示『用剩下的錢』固定片語前後都需要定冠詞 the！"
        },
        {
            "trap_id": "W06_TRAP_US_CLASSROOM",
            "sentence": "I think a new fish tank would brighten up us's classroom.",
            "tokens": ["I", "think", "a", "new", "fish", "tank", "would", "brighten", "up", "us's", "classroom."],
            "wrong_index": 9,
            "wrong_word": "us's",
            "correct_word": "our",
            "fixed_sentence": "I think a new fish tank would brighten up our classroom.",
            "reason": "【W6 真題代名詞所有格】修飾名詞 classroom 必須用所有格代名詞 our（我們的），英文沒有 us's 或 our's！"
        },
        {
            "trap_id": "W07_TRAP_SEVEN_SLICE_BREAD",
            "sentence": "There are seven packet of breads on the table.",
            "tokens": ["There", "are", "seven", "packet of breads", "on", "the", "table."],
            "wrong_index": 3,
            "wrong_word": "packet of breads",
            "correct_word": "slices of bread",
            "fixed_sentence": "There are seven slices of bread on the table.",
            "reason": "【W7 真題三連錯】① 切片吐司量詞用 slice；② seven 後量詞加 -s (slices)；③ 不可數名詞 bread 永遠不可加 -s！"
        },
        {
            "trap_id": "W07_TRAP_FUTURE_SO_WILL",
            "sentence": "Roger will see a new movie tomorrow, and so do Sean.",
            "tokens": ["Roger", "will", "see", "a", "new", "movie", "tomorrow,", "and", "so", "do", "Sean."],
            "wrong_index": 9,
            "wrong_word": "do",
            "correct_word": "will",
            "fixed_sentence": "Roger will see a new movie tomorrow, and so will Sean.",
            "reason": "【W7 真題未來式倒裝附和】前句含有時間 tomorrow 為未來式 will see，倒裝附和必須對齊助動詞 so will Sean！"
        },
        {
            "trap_id": "W07_TRAP_3RD_PERSON_DOESNT",
            "sentence": "Rachel do not learn to play the piano, and Nicole doesn't, either.",
            "tokens": ["Rachel", "do not", "learn", "to", "play", "the", "piano,", "and", "Nicole", "doesn't,", "either."],
            "wrong_index": 1,
            "wrong_word": "do not",
            "correct_word": "doesn't",
            "fixed_sentence": "Rachel doesn't learn to play the piano, and Nicole doesn't, either.",
            "reason": "【W7 真題單三否定助動詞】Rachel 是第三人稱單數，現在式否定必須用 doesn't (does not)，不可用 do not！"
        },
        {
            "trap_id": "W07_TRAP_MODAL_NEITHER_CAN",
            "sentence": "Penguins can't fly in the sky, and neither do ostriches.",
            "tokens": ["Penguins", "can't", "fly", "in", "the", "sky,", "and", "neither", "do", "ostriches."],
            "wrong_index": 8,
            "wrong_word": "do",
            "correct_word": "can",
            "fixed_sentence": "Penguins can't fly in the sky, and neither can ostriches.",
            "reason": "【W7 真題情態助動詞附和】前句是情態助動詞 can't，倒裝附和必須沿用 can (neither can ostriches)，不可慣性寫 do！"
        },
        {
            "trap_id": "W07_TRAP_SUPERLATIVE_VERB_IS",
            "sentence": "Penny sings more beautifully than Eric, but Anne is the most beautifully.",
            "tokens": ["Penny", "sings", "more", "beautifully", "than", "Eric,", "but", "Anne", "is", "the", "most", "beautifully."],
            "wrong_index": 8,
            "wrong_word": "is",
            "correct_word": "sings",
            "fixed_sentence": "Penny sings more beautifully than Eric, but Anne sings the most beautifully.",
            "reason": "【W7 真題高頻失分：最高級子句把一般動詞換成 is】修飾唱歌 beautifully 必須搭配一般動詞 sings (Anne sings the most beautifully)，絕不能寫 Anne is！"
        },
        {
            "trap_id": "W07_TRAP_WELL_BETTER_WILL",
            "sentence": "Ingrid did will on her homework than Hank, but Jeremy did the best.",
            "tokens": ["Ingrid", "did", "will", "on", "her", "homework", "than", "Hank,", "but", "Jeremy", "did", "the", "best."],
            "wrong_index": 2,
            "wrong_word": "will",
            "correct_word": "better",
            "fixed_sentence": "Ingrid did better on her homework than Hank, but Jeremy did the best.",
            "reason": "【W7 真題不規則副詞 well】well 的比較級是不規則變化 better（well ➔ better ➔ the best），不可寫成 will！"
        },
        {
            "trap_id": "W07_TRAP_EASILY_EASILIER",
            "sentence": "I can learn science easilier than maths, but I learn Chinese the most easily.",
            "tokens": ["I", "can", "learn", "science", "easilier", "than", "maths,", "but", "I", "learn", "Chinese", "the", "most", "easily."],
            "wrong_index": 4,
            "wrong_word": "easilier",
            "correct_word": "more easily",
            "fixed_sentence": "I can learn science more easily than maths, but I learn Chinese the most easily.",
            "reason": "【W7 真題自創字錯誤】副詞 easily 以 -ly 結尾，比較級與最高級必須用 more easily / the most easily，沒有 easilier 這個字！"
        },
        {
            "trap_id": "W07_TRAP_BADLY_WORSE_WORST",
            "sentence": "Ted plays the electric guitar badly than Fred, but Bill plays the worst.",
            "tokens": ["Ted", "plays", "the", "electric", "guitar", "badly", "than", "Fred,", "but", "Bill", "plays", "the", "worst."],
            "wrong_index": 5,
            "wrong_word": "badly",
            "correct_word": "worse",
            "fixed_sentence": "Ted plays the electric guitar worse than Fred, but Bill plays the worst.",
            "reason": "【W7 真題不規則副詞 badly】badly 的三級變化為 badly ➔ worse ➔ the worst，看到後方有 than 必須用比較級 worse！"
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
            "options": ["Lisa didn't, either", "neither didn't Lisa", "Lisa did, too", "so did Lisa"],
            "answer": "Lisa didn't, either",
            "hint": "前句是否定句，後句附和必須也是否定附和（注意 neither 後不可用 didn't）",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 否定附和句",
                "formula": "否定句附和標準形式：① Lisa didn't, either；② neither did Lisa（助動詞必須為肯定形 did）。",
                "trap": "neither didn't Lisa 犯了雙重否定錯誤 ❌；too 與 so did 則是肯定附和 ❌。"
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
        },
        # ==========================================
        # 新增 Week 6 & Week 7 真實考券盲點與錯題 (TEA_W6_W7)
        # ==========================================
        {
            "id": "TEA_LIST_11",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個植物單字：",
            "hint": "花朵吸引蜜蜂的甜液：花蜜",
            "audio_word": "nectar",
            "phonetic": "/ˈnektər/",
            "syllables": "nec · tar",
            "answer": "nectar",
            "explanation": {
                "concept": "Discover 3 Unit 15 / Week 6 單字聽寫",
                "formula": "nec-tar，注意字尾是 -tar 而非 -tor。",
                "trap": "Rex 考場原答寫成 nector ❌！切記字尾母音為 a (nectar)。"
            }
        },
        {
            "id": "TEA_LIST_12",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個植物單字：",
            "hint": "花朵色彩鮮豔的部分：花瓣 (複數)",
            "audio_word": "petals",
            "phonetic": "/ˈpetlz/",
            "syllables": "pet · als",
            "answer": "petals",
            "explanation": {
                "concept": "Discover 3 Unit 15 / Week 6 單字聽寫",
                "formula": "第一音節為短母音 /e/ (pet-)，第二音節為 -als。",
                "trap": "Rex 考場原答把 e 跟 a 對調寫成 patels ❌！"
            }
        },
        {
            "id": "TEA_LIST_13",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個核心單字：",
            "hint": "人類溝通使用的：語言",
            "audio_word": "language",
            "phonetic": "/ˈlæŋɡwɪdʒ/",
            "syllables": "lan · guage",
            "answer": "language",
            "explanation": {
                "concept": "RWW6 Unit 7 / Week 6 單字聽寫失分題",
                "formula": "lan + gua + ge，g 後面固定接 ua 發 /ɡwɪ/。",
                "trap": "Rex 考場原答寫成 langauges ❌（把 ua 寫反成 au 且多加 s）！"
            }
        },
        {
            "id": "TEA_LIST_14",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個核心單字：",
            "hint": "政府或國家認定的：官方的、正式的",
            "audio_word": "official",
            "phonetic": "/əˈfɪʃl/",
            "syllables": "of · fi · cial",
            "answer": "official",
            "explanation": {
                "concept": "RWW6 Unit 7 / Week 6 單字聽寫失分題",
                "formula": "office (辦公室) 去 e + ial = official，字尾 -cial 發 /ʃəl/。",
                "trap": "Rex 考場原答漏寫 i 寫成 offical ❌！"
            }
        },
        {
            "id": "TEA_LIST_15",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個核心單字：",
            "hint": "治理國家的機構：政府",
            "audio_word": "government",
            "phonetic": "/ˈɡʌvərnmənt/",
            "syllables": "gov · ern · ment",
            "answer": "government",
            "explanation": {
                "concept": "RWW6 Unit 7 / Week 6 單字聽寫必考陷阱",
                "formula": "動詞 govern (統治) + 名詞字尾 -ment = government。",
                "trap": "Rex 考場原答漏掉中間的 n 寫成 goverment ❌！務必記住 govern 有 n。"
            }
        },
        {
            "id": "TEA_LIST_16",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個語言名稱：",
            "hint": "法國人說的語言：法語（注意首字母大小寫）",
            "audio_word": "French",
            "phonetic": "/frentʃ/",
            "syllables": "French",
            "answer": "French",
            "explanation": {
                "concept": "RWW6 Unit 7 / Week 6 專有名詞聽寫",
                "formula": "國家與語言名稱屬於專有名詞，首字母 F 永遠大寫，母音為 e。",
                "trap": "Rex 考場原答寫成小寫 franch ❌！"
            }
        },
        {
            "id": "TEA_LIST_17",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個名詞複數：",
            "hint": "世界上的許多：國家（複數）",
            "audio_word": "countries",
            "phonetic": "/ˈkʌntriz/",
            "syllables": "coun · tries",
            "answer": "countries",
            "explanation": {
                "concept": "RWW6 Unit 7 / Week 6 單字聽寫失分題",
                "formula": "coun-try 去 y 加 ies ➔ countries，首音節為 coun- (ou)。",
                "trap": "Rex 考場原答漏寫 u 寫成 contries ❌！"
            }
        },
        {
            "id": "TEA_LIST_18",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個核心單字：",
            "hint": "用來說明的：例子、範例",
            "audio_word": "example",
            "phonetic": "/ɪɡˈzæmpl/",
            "syllables": "ex · am · ple",
            "answer": "example",
            "explanation": {
                "concept": "RWW6 Unit 7 / Week 6 單字聽寫失分題",
                "formula": "ex + am + ple，第二音節為短母音 /æ/ (am)。",
                "trap": "Rex 考場原答寫成 exemple ❌！"
            }
        },
        {
            "id": "TEA_LIST_19",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個語言名稱：",
            "hint": "世界上最多母語人士說的：中文普通話、國語（注意首字母）",
            "audio_word": "Mandarin",
            "phonetic": "/ˈmændərɪn/",
            "syllables": "Man · da · rin",
            "answer": "Mandarin",
            "explanation": {
                "concept": "RWW6 Unit 7 / Week 6 專有名詞聽寫",
                "formula": "Man-da-rin，首字母 M 大寫，前兩個音節母音都是 a！",
                "trap": "Rex 考場原答寫成小寫 manderin ❌！"
            }
        },
        {
            "id": "TEA_LIST_20",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個數字單位：",
            "hint": "十個一百：一千 (1,000)",
            "audio_word": "thousand",
            "phonetic": "/ˈθaʊznd/",
            "syllables": "thou · sand",
            "answer": "thousand",
            "explanation": {
                "concept": "RWW6 Unit 7 / Week 6 單字聽寫失分題",
                "formula": "拆字記憶法：thou + sand (沙子) = thousand。",
                "trap": "Rex 考場原答漏寫 sa 寫成 thoudnd ❌！"
            }
        },
        {
            "id": "TEA_LIST_21",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "【W6 真題錯字重測】請聽電腦發音，拼寫出這個雙字轉折片語：",
            "hint": "用來補充真實情況：事實上（兩個單字）",
            "audio_word": "in fact",
            "phonetic": "/ɪn fækt/",
            "syllables": "in · fact",
            "answer": "in fact",
            "explanation": {
                "concept": "RWW6 Unit 8 / Week 6 片語聽寫失分題",
                "formula": "介系詞 in + 名詞 fact (事實) = in fact（事實上）。",
                "trap": "Rex 考場原答把兩個字連起來聽音硬拼成 infecte ❌！"
            }
        },
        {
            "id": "TEA_RW_09",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 7 真題】[Roger, Sean – see new Iron Man movie tomorrow / so]（注意時間副詞 tomorrow 的時態！）",
            "answer": "Roger will see a new Iron Man movie tomorrow, and so will Sean.",
            "hint": "看到 tomorrow 必須用未來式 will see，倒裝附和用 so will Sean",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 未來式肯定倒裝附和句",
                "formula": "S1 + will + V ... tomorrow, and so + will + S2。",
                "trap": "Rex 考場原答：Roger see..., so do Sean ❌！忽略 tomorrow 未來式，導致前後都漏了 will。"
            }
        },
        {
            "id": "TEA_RW_10",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 7 真題】[Rachel, Nicole – not learn to play the piano / either]（注意單數人名的否定助動詞！）",
            "answer": "Rachel doesn't learn to play the piano, and Nicole doesn't, either.",
            "hint": "Rachel 與 Nicole 皆為第三人稱單數，現在式否定用 doesn't",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 第三人稱單數否定附和句",
                "formula": "S1 + doesn't + V ..., and S2 + doesn't, either。",
                "trap": "Rex 考場原答：Rachel do not..., Nicole do not... ❌！單數主詞絕對不能用 do not。"
            }
        },
        {
            "id": "TEA_RW_11",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 7 真題】[penguins, ostriches – can't fly / neither]（注意情態助動詞 can't 的倒裝對應！）",
            "answer": "Penguins can't fly, and neither can ostriches.",
            "hint": "前句是 can't，後面 neither 倒裝必須用 can (neither can ostriches)",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 情態助動詞 can 否定倒裝附和",
                "formula": "S1 + can't + V, and neither + can + S2。",
                "trap": "Rex 考場原答：neither do ostriches ❌！前句是 can't，附和必須用 can 而非 do。"
            }
        },
        {
            "id": "TEA_RW_12",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 7 真題】How beautifully do they sing? Singing Scores: Anne: 10/10, Penny: 9/10 & Eric: 8/10",
            "answer": "Eric sings beautifully, Penny sings more beautifully than Eric, but Anne sings the most beautifully.",
            "hint": "最高級子句主詞 Anne 後面必須保留一般動詞 sings，不可寫 Anne is！",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 多音節副詞三級比較問答",
                "formula": "Penny sings more beautifully than Eric, but Anne sings the most beautifully.",
                "trap": "Rex 考場原答寫成 but Anne is the most beautifully ❌！副詞修飾唱歌動作，動詞必須是 sings 而非 is。"
            }
        },
        {
            "id": "TEA_RW_13",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 7 真題】How well did they do their homework? Jeremy: 100%, Ingrid: 95% & Hank: 90%",
            "answer": "Hank did his homework well, Ingrid did better than Hank, but Jeremy did the best.",
            "hint": "題幹 did 為過去式，且 well 的比較級與最高級為 better / the best",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 不規則副詞 well 過去式三級比較",
                "formula": "過去式 did + well ➔ did better than ➔ but Jeremy did the best。",
                "trap": "Rex 考場原答：Ingrid did will than Hana, but Jeremy do the best ❌（better 寫成 will、過去式 did 寫成現在式 do）！"
            }
        },
        {
            "id": "TEA_RW_14",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 7 真題】How easily do you learn: Chinese, science & maths?",
            "answer": "I learn maths easily, I learn science more easily than maths, but I learn Chinese the most easily.",
            "hint": "主詞動詞為 I learn，且副詞 easily 比較級為 more easily、最高級為 the most easily",
            "explanation": {
                "concept": "Grammar 3 Unit 14: -ly 副詞 (easily) 比較級與最高級",
                "formula": "I learn + 科目 + more easily than ..., but I learn + 科目 + the most easily。",
                "trap": "Rex 考場原答：Science is easilier than maths, but Chinese is the easiliest ❌！把副詞 easily 當形容詞自創字且漏了 I learn。"
            }
        },
        {
            "id": "TEA_RW_15",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 7 真題】How badly do they play the electric guitar? Guitar Scores: Bill: 1/10, Ted: 3/10 & Fred: 5/10",
            "answer": "Fred plays the electric guitar badly, Ted plays worse than Fred, but Bill plays the worst.",
            "hint": "badly 的比較級是 worse，最高級是 the worst；1/10 分最低代表彈得最差 (plays the worst)！",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 不規則副詞 badly 三級變化",
                "formula": "badly (原級) ➔ worse than (比較級) ➔ the worst (最高級)。",
                "trap": "Rex 考場原答：Ted plays badly than Fred, but Bill play the most badly ❌！badly 是不規則變化 worse / the worst。"
            }
        },
        {
            "id": "TEA_RW_16",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": "【Week 7 真題】How early did they get up? Elizabeth: 5:30 a.m., Caroline: 6:00 a.m. & Melanie: 6:30 a.m.",
            "answer": "Melanie got up early, Caroline got up earlier than Melanie, but Elizabeth got up the earliest.",
            "hint": "early 比較級為 earlier、最高級為 the earliest；最高級主詞 Elizabeth 後面動詞不可寫 is！",
            "explanation": {
                "concept": "Grammar 3 Unit 14: -y 結尾雙音節副詞 early 三級變化",
                "formula": "early ➔ earlier than ➔ the earliest；動詞須維持 got up / gets up。",
                "trap": "Rex 考場原答：but Elizebeth is the earliest ❌！再次把動作動詞 get up 誤寫成 be 動詞 is。"
            }
        },
        {
            "id": "TEA_FILL_07",
            "type": "fill",
            "category_tag": "fill",
            "question": "【W7 量詞真題】6. bread (7 片吐司)：There are seven ( ____________ ) of ( ____________ ).",
            "answer": "slices of bread",
            "hint": "切片吐司量詞用 slice 複數，不可數名詞 bread 絕不加 s（請填 slices of bread）",
            "explanation": {
                "concept": "Grammar 3 Unit 15: 不可數食物計量詞搭配",
                "formula": "數字 (seven) + 複數容器量詞 (slices) + of + 不可數名詞原形 (bread)。",
                "trap": "Rex 考場原答寫成 seven packet of breads ❌，同時錯了量詞、漏複數 s、又給不可數 bread 加上 s！"
            }
        },
        {
            "id": "TEA_FILL_08",
            "type": "fill",
            "category_tag": "fill",
            "question": "【W6 改錯真題】With ( ____________ ) of the money, I would treat my friends to lunch.",
            "answer": "the rest",
            "hint": "用剩下的錢：With the rest of the money",
            "explanation": {
                "concept": "Write Right 3 Unit 5: 假設語氣金額分配固定片語",
                "formula": "With the rest of the money（用剩下的那筆錢），兩個 the 缺一不可。",
                "trap": "Rex 考場原答只補了後面 the money，漏了前面 the rest 的 the ❌！"
            }
        },
        {
            "id": "TEA_MC_07",
            "type": "choice",
            "category_tag": "choice",
            "question": "【W7 真題盲點秒殺】Penny sings more beautifully than Eric, but Anne ( ______ ) the most beautifully.",
            "options": ["sings", "is", "does", "sing"],
            "answer": "sings",
            "hint": "副詞 the most beautifully 用來修飾唱歌動作，主詞 Anne 為第三人稱單數",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 最高級副詞子句動詞搭配",
                "formula": "主詞 (Anne) + 一般動詞三單 (sings) + 最高級副詞 (the most beautifully)。",
                "trap": "Rex 在 W7 考卷連錯兩題：誤把最高級子句的動作動詞換成 be 動詞 is ❌！"
            }
        },
        {
            "id": "TEA_MC_08",
            "type": "choice",
            "category_tag": "choice",
            "question": "【W7 真題盲點秒殺】Ted plays the electric guitar ( ______ ) than Fred, but Bill plays ( ______ ).",
            "options": ["worse / the worst", "more badly / the most badly", "badlier / the badliest", "badly / the worst"],
            "answer": "worse / the worst",
            "hint": "badly 是不規則變化副詞！",
            "explanation": {
                "concept": "Grammar 3 Unit 14: 不規則副詞 badly 三級變化",
                "formula": "badly (原級) ➔ worse (比較級) ➔ the worst (最高級)。",
                "trap": "Rex 考場原答寫成 badly than Fred 與 the most badly ❌！切記 badly 不加 more/most。"
            }
        },
        {
            "id": "TEA_MC_09",
            "type": "choice",
            "category_tag": "choice",
            "question": "【W7 真題盲點秒殺】Penguins can't fly, and ( ______ ) ostriches.",
            "options": ["neither can", "neither do", "neither can't", "either can"],
            "answer": "neither can",
            "hint": "前句助動詞為 can't，否定倒裝用 neither + 肯定助動詞",
            "explanation": {
                "concept": "Grammar 3 Unit 13: 情態助動詞 can 否定倒裝附和",
                "formula": "前句 can't ➔ 後句 neither + can + 主詞。",
                "trap": "Rex 考場原答誤選 neither do ❌！必須看前句是哪個助動詞就用哪個助動詞。"
            }
        },
        {
            "id": "TEA_MC_10",
            "type": "choice",
            "category_tag": "choice",
            "question": "【W7 真題盲點秒殺】There are seven ( ______ ) on the kitchen table.",
            "options": ["slices of bread", "packet of breads", "slices of breads", "slice of bread"],
            "answer": "slices of bread",
            "hint": "seven 後接複數量詞 slices，bread 不可數永遠不加 s",
            "explanation": {
                "concept": "Grammar 3 Unit 15: 容器量詞與不可數名詞",
                "formula": "seven + slices (複數) + of + bread (不可數原形)。",
                "trap": "Rex 考場原答寫成 seven packet of breads ❌！"
            }
        }
    ]
}
