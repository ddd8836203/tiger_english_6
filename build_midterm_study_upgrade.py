# -*- coding: utf-8 -*-
"""
build_midterm_study_upgrade.py
將英語學習網頁的 `english_data.js` 全面升級為「六上期中考 5 大書系 12 單元優先」架構：
1. 頂部書籍與單元清單重組：將六上期中考 5 大書系 12 單元置頂，並標註 `is_midterm: True` 與對應 `midterm_unit_id`。
2. 清除空白佔位單元（避免選單點進去無內容）。
3. 為全數 12 個期中考單元注入【100% 課本完整原文段落 (Full Unabridged Passages)】，並附帶 `key_sentences`（必考重點句標註與解析）。
4. 為原本缺少資料的 5 個期中考單元（`rw6_5`, `rw6_6`, `rw6_7`, `rw6_8`, `tea_midterm_1`）補齊完整「7 大錨點單字卡」（字根拆解、諧音聯想、情境畫面、搭配用法、記憶口訣、易混比較、課文例句）、文法規則與避坑卡、以及雙軌測驗題庫。
5. 為既有的 7 個期中考單元（`gra3_13~15`, `wr3_4~5`, `rd6_4~5`）升級完整課文段落、必考句標註與岱崙考卷避坑提示。
6. 打造 50 題「六上期中考專屬 1★~10★ 晨間體操語感秒殺題庫」（含 🟢 正確語感直覺 vs 🔴 誘答盲點排除）。
"""

import json
import os

WORKSPACE = r"c:\@植善課業\AI\英語學習網頁"
ENGLISH_DATA_PATH = os.path.join(WORKSPACE, "english_data.js")


def load_existing_english_data():
    with open(ENGLISH_DATA_PATH, "r", encoding="utf-8") as f:
        txt = f.read()
    start = txt.find("{")
    end = txt.rfind("};") + 1
    return json.loads(txt[start:end])


# ==============================================================================
# 1. 12 個期中考單元的【完整課文段落 + 必考重點句標註】
# ==============================================================================
MIDTERM_FULL_READINGS = {
    "gra3_13": [
        {
            "sequence": 1,
            "section_title": "📖 課本主課文 (p.67)：The History of the Telephone (電話發明史與專利之爭)",
            "eng": "In the 19th century, Alexander Graham Bell was working on a new invention. He was trying to invent a telephone. Other scientists were trying to invent telephones, too. Antonio Meucci and Johann Philipp Reis made telephone machines. So did Elisha Gray.",
            "chi": "在 19 世紀，亞歷山大·葛拉漢·貝爾正致力於一項新發明。他當時正試圖發明電話。其他科學家當時也正試圖發明電話。安東尼奧·梅烏奇與約翰·菲利普·雷斯製作了電話機器。以利沙·格雷也是如此。",
            "key_sentences": [
                {
                    "sentence": "Other scientists were trying to invent telephones, too.",
                    "tag": "⭐ 肯定句尾附和 (too)",
                    "note": "前句是過去進行式肯定句 (was trying)，附和句在句尾逗號後加上 too。"
                },
                {
                    "sentence": "So did Elisha Gray.",
                    "tag": "🔥 岱崙必考倒裝 (So did + S)",
                    "note": "前句動詞為一般動詞過去式 (made)，句首倒裝附和必用『So + did + 主詞』，千萬不可寫成 So was！"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本主課文 (p.67)：The Race to the Patent Office (專利局搶先之戰)",
            "eng": "On February 14, 1876, Gray's invention was ready. Bell's invention was ready, too. Gray hurried to the U.S. Patent Office to get a licence for his invention. So did Bell. But Bell got there first.",
            "chi": "1876 年 2 月 14 日，格雷的發明準備好了。貝爾的發明也準備好了。格雷匆忙趕往美國專利局，為他的發明申請專利許可證。貝爾也是如此。但貝爾搶先一步抵達了那裡。",
            "key_sentences": [
                {
                    "sentence": "Gray hurried to the U.S. Patent Office to get a licence for his invention. So did Bell.",
                    "tag": "🔥 過去式一般動詞倒裝",
                    "note": "hurried 是過去式一般動詞，因此簡短倒裝附和用『So did Bell.』。"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 課本主課文 (p.67)：Remembering the Inventors (銘記歷史發明家)",
            "eng": "Gray did not become rich and famous. Meucci didn't become rich and famous, either. Neither did Reis. But we remember them today as important people in the history of the telephone.",
            "chi": "格雷並未因此變得富有和出名。梅烏奇也沒有變得富有和出名。雷斯也是如此。但今天我們將他們銘記為電話歷史上的重要人物。",
            "key_sentences": [
                {
                    "sentence": "Meucci didn't become rich and famous, either.",
                    "tag": "⭐ 否定句尾附和 (either)",
                    "note": "否定句（含 didn't）表示『也沒有』時，句尾逗號後必須用 either，不可用 too！"
                },
                {
                    "sentence": "Neither did Reis.",
                    "tag": "🔥 否定倒裝大魔王 (Neither + 肯定助動詞)",
                    "note": "Neither 本身已含 not，後面助動詞必須用肯定形 did（Neither did Reis），嚴禁寫成 Neither didn't！"
                }
            ]
        },
        {
            "sequence": 4,
            "section_title": "💬 課本實戰對話 (p.69)：Rosa & Carlos Discuss Alexander Graham Bell",
            "eng": "Rosa: What do you know about Alexander Graham Bell, Carlos?\nCarlos: I know that he helped deaf people. His father helped deaf people, too. Bell's mother was deaf. So was his wife.\nRosa: Really? Was Bell a doctor?\nCarlos: No, he wasn't. He was a teacher. His father was a teacher, too.\nRosa: Was Bell from the U.K.?\nCarlos: Yes, he was. But he moved to Canada in 1870. So did his parents. Bell started his work on the telephone in Canada.\nRosa: In the 1870s, people didn't have telephones. They didn't have computers, either.\nCarlos: That's right. Houses didn't have telephones then. Neither did offices. But Bell changed that with his amazing invention.",
            "chi": "Rosa：卡洛斯，你對亞歷山大·葛拉漢·貝爾了解多少？\nCarlos：我知道他幫助聽障人士。他的父親也幫助聽障人士。貝爾的母親是聽障者。他的妻子也是。\nRosa：真的嗎？貝爾是醫生嗎？\nCarlos：不，他不是。他是一位老師。他的父親也是一位老師。\nRosa：貝爾來自英國嗎？\nCarlos：是的。但他在 1870 年搬到了加拿大。他的父母也是。貝爾在加拿大開始了他對電話的研究。\nRosa：在 1870 年代，人們沒有電話。他們也沒有電腦。\nCarlos：沒錯。當時住家裡沒有電話。辦公室裡也沒有。但貝爾用他驚人的發明改變了這一切。",
            "key_sentences": [
                {
                    "sentence": "Bell's mother was deaf. So was his wife.",
                    "tag": "🔥 Be 動詞 vs 一般動詞辨析",
                    "note": "前句是 be 動詞 was，倒裝附和必須對應使用『So was his wife』，不可用 did！"
                },
                {
                    "sentence": "Houses didn't have telephones then. Neither did offices.",
                    "tag": "⭐ 課本改寫原題",
                    "note": "可與『Offices didn't, either.』雙向互換改寫！"
                }
            ]
        },
        {
            "sequence": 5,
            "section_title": "📖 課本第二篇長文 (p.70)：Inventing the Light Bulb — Edison & Swan (電燈泡發明歷程)",
            "eng": "In 1878, Thomas Edison was trying to invent a light bulb. Joseph Swan was trying to invent a light bulb, too. Edison and Swan weren't the only scientists to experiment with light bulbs. Other scientists were experimenting with light bulbs, too. British inventor Humphry Davy invented a light bulb. So did Canadian inventor Henry Woodward. But their light bulbs were not very successful. Swan's light bulb was a success. So was Edison's light bulb. Swan's light bulb worked for a long time. So did Edison's light bulb. Swan got a patent for his invention. Edison got a patent, too. Swan wasn't happy about this. Edison wasn't happy, either. Swan and Edison weren't friends, but their inventions changed the world!",
            "chi": "1878 年，湯瑪斯·愛迪生正試圖發明電燈泡。約瑟夫·斯旺當時也正試圖發明電燈泡。愛迪生和斯旺並不是唯一實驗電燈泡的科學家。其他科學家當時也正在實驗電燈泡。英國發明家漢弗里·戴維發明了電燈泡。加拿大發明家亨利·伍德沃德也是。但他們的電燈泡並不是很成功。斯旺的電燈泡獲得了成功。愛迪生的電燈泡也是。斯旺的電燈泡運作了很長時間。愛迪生的電燈泡也是。斯旺為他的發明取得了專利。愛迪生也取得了專利。斯旺對此並不開心。愛迪生也不開心。斯旺和愛迪生並不是朋友，但他們的發明改變了世界！",
            "key_sentences": [
                {
                    "sentence": "Swan's light bulb was a success. So was Edison's light bulb.",
                    "tag": "🔥 對比陷阱 (was vs did)",
                    "note": "注意這兩句連著考：『was a success』用『So was...』；下一句『worked for a long time』是一般動詞，改用『So did...』！"
                },
                {
                    "sentence": "Swan's light bulb worked for a long time. So did Edison's light bulb.",
                    "tag": "🔥 一般動詞過去式附和",
                    "note": "worked 是過去式一般動詞，附和句必用 So did。"
                }
            ]
        }
    ],
    "gra3_14": [
        {
            "sequence": 1,
            "section_title": "📖 課本四格漫畫全文 (p.71)：The Wright Brothers' Dream of Flight (萊特兄弟飛行夢)",
            "eng": "Orville and Wilbur Wright wanted to fly when they were small boys. They liked to play with flying toys. When the boys were older, they decided to make a flying machine. In 1900, they built a glider. It didn't fly very quickly, and it didn't fly very far.",
            "chi": "奧維爾和威爾伯·萊特小時候就想要飛行。他們喜歡玩飛行玩具。當男孩們長大後，他們決定製造一架飛行機器。1900 年，他們造了一架滑翔機。它飛得不是很快，也飛得不是很遠。",
            "key_sentences": [
                {
                    "sentence": "It didn't fly very quickly, and it didn't fly very far.",
                    "tag": "⭐ 副詞原級修飾動詞",
                    "note": "quickly（規則副詞 +ly）與 far（不規則同形副詞）皆用來修飾動詞 fly。"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本四格漫畫全文 (p.71)：The First Airplane in 1903 & Best Machine in 1908",
            "eng": "In 1903, Orville and Wilbur successfully made the world's first airplane flight. Their plane flew further than the glider. It flew more quickly than the glider, too. But it only stayed in the sky for one minute. The Wright brothers made another plane in 1908. It was their best machine. It flew the most quickly. It flew the furthest, too. People watched excitedly as the plane stayed in the air for thirty minutes. It was a wonderful sight!",
            "chi": "1903 年，奧維爾與威爾伯成功完成了世界上第一次飛機飛行。他們的飛機比滑翔機飛得更遠。它飛得也比滑翔機更快。但它只在空中停留了一分鐘。萊特兄弟在 1908 年又製造了另一架飛機。那是他們最好的機器。它飛得最快。它飛得也最遠。當飛機在空中停留三十分鐘時，人們興奮地注視著。那是一幅美妙的景象！",
            "key_sentences": [
                {
                    "sentence": "Their plane flew further than the glider. It flew more quickly than the glider, too.",
                    "tag": "🔥 副詞比較級雙公式",
                    "note": "不規則副詞 far ➔ further than (或 farther than)；多音節副詞 quickly ➔ more quickly than（嚴禁寫 quicker）！"
                },
                {
                    "sentence": "It flew the most quickly. It flew the furthest, too.",
                    "tag": "🔥 副詞最高級必加 the",
                    "note": "最高級前面務必加上定冠詞 the：the most quickly / the furthest。"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 課本篇章填空全文 (p.72)：Testing the First Plane on December 17, 1903",
            "eng": "On December 17, 1903, the Wright brothers tested their first plane. They shook hands nervously as Orville got into the plane. The plane started to move slowly along the ground. Then the plane started to move quickly and after a moment, it suddenly lifted up into the air. Orville was lying on the bottom wing of the plane. He was holding onto the plane tightly and he was watching the people on the ground. The people were cheering loudly and waving at Orville excitedly. After about a minute, the plane landed. Orville stood up proudly and Wilbur ran to him. The first flight was a success!",
            "chi": "1903 年 12 月 17 日，萊特兄弟測試了他們的第一架飛機。當奧維爾登上飛機時，他們緊張地握手。飛機開始沿著地面緩慢移動。接著飛機開始快速移動，片刻之後，它突然升空。奧維爾趴在飛機的下機翼上。他緊緊抓著飛機，看著地面上的人們。人們大聲歡呼，興奮地向奧維爾揮手。大約一分鐘後，飛機降落了。奧維爾自豪地站起來，威爾伯跑向他。第一次飛行大獲成功！",
            "key_sentences": [
                {
                    "sentence": "The people were cheering loudly and waving at Orville excitedly.",
                    "tag": "⭐ 岱崙小考常考副詞轉換",
                    "note": "修飾動作 cheering 與 waving 必須加 -ly 變成副詞 loudly, excitedly（Rex 在小考曾誤寫成 laughed loud ❌）。"
                }
            ]
        },
        {
            "sequence": 4,
            "section_title": "💬 課本實戰對話 (p.73)：Nada & Ali Talk About Computers and the Internet",
            "eng": "Nada: What's your favorite invention, Ali?\nAli: I love computers. They're brilliant. Computers help us do everything more easily.\nNada: What was the world like before computers?\nAli: Well, I think children did their homework more slowly than we do, because they didn't have the Internet!\nNada: That's true. Today, we can find information more quickly than people in the past. Do you use the Internet regularly?\nAli: I use it more regularly than my brother. He never goes online. But my sister uses the Internet the most regularly. She's always online!\nNada: Is she? Can you type fast on your computer?\nAli: Yes, I can. I can type the fastest of all the children in my class!",
            "chi": "Nada：阿里，你最喜歡的發明是什麼？\nAli：我熱愛電腦。它們太棒了。電腦幫助我們更輕鬆地完成所有事。\nNada：在有電腦之前，世界是什麼樣子？\nAli：嗯，我想以前的孩子做作業比我們更慢，因為他們沒有網路！\nNada：沒錯。今天我們能比過去的人更快找到資訊。你經常使用網路嗎？\nAli：我比我弟弟更常使用網路。他從不上網。但我姊姊最常使用網路。她總是掛在網上！\nNada：是嗎？你在電腦上打字快嗎？\nAli：是的，我很快。我是我們班所有孩子當中打字最快的！",
            "key_sentences": [
                {
                    "sentence": "Computers help us do everything more easily.",
                    "tag": "⭐ 去 y 變 i 加 ly 的比較級",
                    "note": "easy ➔ easily ➔ more easily（絕對不是 easier，因為修飾動詞 do）。"
                },
                {
                    "sentence": "I can type the fastest of all the children in my class!",
                    "tag": "🔥 不規則同形副詞 fast",
                    "note": "fast 本身就是副詞（無 fastly），比較級 faster，最高級 the fastest（嚴禁寫 more faster）！"
                }
            ]
        },
        {
            "sequence": 5,
            "section_title": "📖 課本科學史短文 (p.73)：The Invention of Telescopes (望遠鏡演進史)",
            "eng": "Hans Lippershey invented the first telescope in 1608. He couldn't see very far with his telescope, but he could see things quite clearly. In 1609, Galileo made another telescope. Galileo could see things more clearly with his telescope than he could with Lippershey's telescope. Galileo could see further with his telescope, too. He used his telescope to look into space and see the surface of the moon! Isaac Newton invented a new kind of telescope in 1670. With his new telescope, he could see the furthest of all, and he could see things the most clearly. Newton used his telescope to study the planets.",
            "chi": "漢斯·利伯希在 1608 年發明了第一架望遠鏡。用他的望遠鏡看不太遠，但他能把東西看得很清楚。1609 年，伽利略造了另一架望遠鏡。伽利略用他的望遠鏡比用利伯希的望遠鏡能看得更清晰。伽利略用他的望遠鏡也能看得更遠。他用望遠鏡觀測太空，並看見了月球表面！艾薩克·牛頓在 1670 年發明了一種新型望遠鏡。用他的新望遠鏡，他看得最遠，也看得最清晰。牛頓用他的望遠鏡來研究行星。",
            "key_sentences": [
                {
                    "sentence": "With his new telescope, he could see the furthest of all, and he could see things the most clearly.",
                    "tag": "🔥 課本三級比較總結句",
                    "note": "far ➔ further ➔ the furthest；clearly ➔ more clearly ➔ the most clearly。"
                }
            ]
        }
    ],
    "gra3_15": [
        {
            "sequence": 1,
            "section_title": "📖 課本食譜全文 (p.76)：HOW TO MAKE EASY MINI PIZZAS — Ingredients (食材清單)",
            "eng": "HOW TO MAKE EASY MINI PIZZAS — Ingredients: 8 tomatoes, cut into slices; 4 cups of grated cheese; 1 can of chopped tomatoes; some dough; 1 tablespoon of olive oil; 1 teaspoon of oregano; and some olives.",
            "chi": "如何製作簡單迷你披薩 —— 食材清單：8 顆番茄（切片）、4 杯刨絲起司、1 罐切碎的番茄罐頭、一些披薩麵團、1 大匙橄欖油、1 茶匙牛至香草粉（奧勒岡草），以及一些橄欖。",
            "key_sentences": [
                {
                    "sentence": "4 cups of grated cheese; 1 can of chopped tomatoes; some dough; 1 tablespoon of olive oil",
                    "tag": "🔥 可數 vs 不可數食材分類",
                    "note": "課本分類必背：可數 (tomatoes, olives, mini pizzas)；不可數 (cheese, dough, olive oil, oregano)。"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本食譜步驟全文 (p.76)：Instructions for Mini Pizzas (六步驟料理說明)",
            "eng": "First, put a piece of baking paper on a baking tray. Spread the olive oil on the baking paper. Second, cut two or three rounds of dough and put them on the baking paper. Third, put some chopped tomatoes on each round of dough. Fourth, put a slice of tomato, some cheese, a little oregano, and a few olives on each round. Fifth, cook the mini pizzas in the oven for ten minutes. Finally, eat your mini pizzas!",
            "chi": "第一，在烤盤上鋪一張烘焙紙。把橄欖油塗抹在烘焙紙上。第二，切出兩到三個圓形麵團並放在烘焙紙上。第三，在每個圓形麵團上放一些切碎的番茄。第四，在每個圓麵團上放一片番茄、一些起司、一點點牛至香草粉和幾顆橄欖。第五，將迷你披薩放進烤箱烤十分鐘。最後，享用你的迷你披薩！",
            "key_sentences": [
                {
                    "sentence": "Fourth, put a slice of tomato, some cheese, a little oregano, and a few olives on each round.",
                    "tag": "⭐ 量詞與數量詞精準搭配",
                    "note": "a little + 不可數名詞 (oregano)；a few + 可數複數名詞 (olives)；a slice of + 切片食物。"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 課本廚房情境短文 (p.78)：Emily in the Kitchen (艾蜜莉的廚房量詞觀察)",
            "eng": "Emily is in the kitchen. There's a bowl of apples on the table and there's a bar of chocolate on the table, too. There are some slices of bread on a plate. There's a bag of flour and a jar of honey in the cupboard. There's a bottle of water in the fridge and there's a carton of milk in the fridge, too. Emily is drinking a glass of milk because she's thirsty.",
            "chi": "艾蜜莉在廚房裡。餐桌上有一碗蘋果，桌上還有一塊（條）巧克力。盤子裡有一些切片麵包。櫥櫃裡有一袋麵粉和一罐蜂蜜。冰箱裡有一瓶水，冰箱裡還有一盒牛奶。艾蜜莉正在喝一杯牛奶，因為她口渴了。",
            "key_sentences": [
                {
                    "sentence": "There are some slices of bread on a plate. There's a bag of flour and a jar of honey in the cupboard.",
                    "tag": "🔥 14 大容器量詞必背句",
                    "note": "bread, flour, honey 都是不可數名詞，絕不可加 s！複數必須加在量詞上（some slices of bread）。"
                }
            ]
        },
        {
            "sequence": 4,
            "section_title": "💬 課本實戰對話 (p.79)：Karima & Tarik Bake a Cake for Grandma and Grandpa",
            "eng": "Karima: Let's make a cake for Grandma and Grandpa.\nTarik: That's a good idea. What do we need?\nKarima: We need a carton of eggs, and some butter.\nTarik: OK. Do we need a bag of flour?\nKarima: No. There's a lot of flour in the cupboard. But we need a bar of chocolate for the cake.\nTarik: OK. Do we need a carton of milk?\nKarima: No. We've got some milk in the fridge. But we need some coffee.\nTarik: Why? Are we making a coffee cake?\nKarima: No. But Grandma always drinks a cup of coffee when she eats a piece of cake!",
            "chi": "Karima：我們來為爺爺和奶奶做一個蛋糕吧。\nTarik：好主意。我們需要什麼？\nKarima：我們需要一盒雞蛋，還有一些奶油。\nTarik：好的。我們需要一袋麵粉嗎？\nKarima：不用。櫥櫃裡有很多麵粉。但我們需要一塊做蛋糕用的巧克力。\nTarik：好的。我們需要一盒牛奶嗎？\nKarima：不用。我們冰箱裡有一些牛奶。但我們需要一些咖啡。\nTarik：為什麼？我們要做咖啡蛋糕嗎？\nKarima：不是。但奶奶吃一塊蛋糕時，總是會喝一杯咖啡！",
            "key_sentences": [
                {
                    "sentence": "Grandma always drinks a cup of coffee when she eats a piece of cake!",
                    "tag": "⭐ 容器量詞經典組合",
                    "note": "a carton of eggs/milk（一盒蛋/奶）、a bag of flour（一袋麵粉）、a bar of chocolate（一塊巧克力）、a cup of coffee（一杯咖啡）、a piece of cake（一片蛋糕）。"
                }
            ]
        }
    ],
    "wr3_4": [
        {
            "sequence": 1,
            "section_title": "📖 課本範文全文 (p.31)：Cynthia's Story — My Neighborhood (辛西婭的社區範文)",
            "eng": "Have you ever been to my neighborhood?\nI have lived in my neighborhood for three years. It is very close to my school. I can get to school in ten minutes on foot. The subway station and the bus stop are very close, too.\nThere are many stores in my neighborhood. The grocery store is two blocks from my house. Across the street from the grocery store, there is a hair salon, a dry cleaner's and a bank. Best of all, my neighborhood has a park. My friends and I often have lunch there.\nI really like living in my neighborhood!",
            "chi": "你曾經來過我的社區嗎？\n我已經在我的社區住了三年了。它離我的學校非常近。我步行十分鐘就能到達學校。地鐵站和公車站也非常近。\n我的社區裡有許多商店。雜貨店距離我家兩個街區。在雜貨店的對街，有一家美髮沙龍、一家乾洗店和一家銀行。最棒的是，我的社區有一座公園。我和朋友們經常在那裡吃午餐。\n我真的很喜歡住在我的社區裡！",
            "key_sentences": [
                {
                    "sentence": "I have lived in my neighborhood for three years.",
                    "tag": "🔥 現在完成式持續時間 (have lived ... for)",
                    "note": "從過去搬來一直住到現在，用 have/has lived + for + 一段時間（嚴禁在句尾加 ago）！"
                },
                {
                    "sentence": "I can get to school in ten minutes on foot.",
                    "tag": "🔥 交通時間與步行介系詞",
                    "note": "花費時間用『in + 時間』；走路必用『on foot』（搭車才用 by bus / by subway）。"
                },
                {
                    "sentence": "The subway station and the bus stop are very close, too.",
                    "tag": "⚠️ 岱崙小考真實失分句",
                    "note": "Rex 在 Week 2 作文將 very close 誤寫成 very closer ❌！very 後面必須接原級形容詞 close。"
                },
                {
                    "sentence": "Across the street from the grocery store, there is a hair salon, a dry cleaner's and a bank.",
                    "tag": "⭐ 空間方位與存在句",
                    "note": "Across the street from（在...對街），後接 there is（靠近單數名詞 a hair salon）。"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本方位與句型總覽 (p.33-p.35)：Neighborhood Locations & Activities",
            "eng": "The grocery store is two blocks from my house. The stationery store is next to the gas station. The hair salon is across the street from the dry cleaner's. The Internet café is down the street from the grocery store. The coffee shop is around the corner from the hair salon. The bus stop is in front of the park.\nMy neighborhood has a park. My friends and I have lunch there. My neighborhood has a grocery store. My mother buys food there. My neighborhood has a bank. I keep my money there. My neighborhood has a hair salon. I get my hair cut there. My neighborhood has a dry cleaner's. My father has his suits cleaned there. My neighborhood has a stationery store. I buy my school supplies there.",
            "chi": "雜貨店距離我家兩個街區。文具店在加油站隔壁。美髮沙龍在乾洗店對街。網咖沿著雜貨店這條街走下去就到了。咖啡店在美髮沙龍轉角處。公車站在公園正前方。\n我的社區有一座公園，我和朋友在那裡吃午餐。我的社區有一家雜貨店，我媽媽在那裡買食物。我的社區有一家銀行，我在那裡存錢。我的社區有一家美髮沙龍，我在那裡剪頭髮。我的社區有一家乾洗店，我爸爸把西裝送去那裡清洗。我的社區有一家文具店，我在那裡買學用品。",
            "key_sentences": [
                {
                    "sentence": "I get my hair cut there. / My father has his suits cleaned there.",
                    "tag": "⭐ 使役被動句型 (get/have + 物 + V-p.p.)",
                    "note": "讓別人幫自己剪頭髮 (get my hair cut)、送洗西裝 (have his suits cleaned) 是高分寫作必備句型！"
                }
            ]
        }
    ],
    "wr3_5": [
        {
            "sequence": 1,
            "section_title": "📖 課本範文全文 (p.39)：Nathan's Story — If I Had 300 Dollars (奈森的假設語氣範文)",
            "eng": "If I had 300 dollars, I would do three things.\nWith the first 100 dollars, I would buy a nice present for my mom. My mom loves scarves, so I would get her a beautiful scarf.\nNext, I would donate 100 dollars to a charity group. I think you should help other people whenever you can.\nFinally, I would spend 100 dollars on myself. A baseball glove and some comic books would cost me about 70 dollars. With the rest of the money, I would treat my friends to lunch.\nWouldn't it be great to have 300 dollars?",
            "chi": "如果我有 300 美元，我會做三件事。\n用第一個 100 美元，我會買一份精美的禮物送給媽媽。我媽媽喜愛圍巾，所以我會買一條美麗的圍巾給她。\n接下來，我會捐贈 100 美元給慈善團體。我認為只要你有能力，隨時都應該幫助別人。\n最後，我會花 100 美元在自己身上。一個棒球手套和幾本漫畫書大約會花費我 70 美元。用剩下的錢，我會請我的朋友們吃午餐。\n擁有 300 美元難道不是很棒嗎？",
            "key_sentences": [
                {
                    "sentence": "If I had 300 dollars, I would do three things.",
                    "tag": "🔥 與現在事實相反假設語氣",
                    "note": "If 子句用過去式 had，主要子句必用『would + 原形動詞』，絕對不能寫 will！"
                },
                {
                    "sentence": "With the first 100 dollars, I would buy a nice present for my mom.",
                    "tag": "🔥 買東西給某人介系詞 (buy ... for)",
                    "note": "buy + 物 + for + 人（課本改錯必考：不可寫 buy a present to my mom ❌）！"
                },
                {
                    "sentence": "A baseball glove and some comic books would cost me about 70 dollars.",
                    "tag": "🔥 花費動詞四大天王 (spend vs cost)",
                    "note": "人 + spend + 錢 + on + 物；物 + cost + 人 + 錢。"
                },
                {
                    "sentence": "Wouldn't it be great to have 300 dollars?",
                    "tag": "⭐ 結尾反問句 (Wouldn't it be + adj.)",
                    "note": "助動詞 Wouldn't 後方必須保留原形動詞 be，不可漏掉 be 寫成 Wouldn't it great ❌！"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本寫作句型庫全文 (p.41-p.43)：Spending, Costing & Sharing Money",
            "eng": "If I had a lot of money, I would open up a bank account. I think you should save your money. I would have a meal at a fancy restaurant. I think you should enjoy good food. I would share the money with my sister. I would give the money to a homeless person.\nMy dad loves ties, so I would get him a tie. My brother enjoys computer games, so I would get him a computer game. My sister likes mystery novels, so I would get her a mystery novel.\nWith some of the money, I would treat my friends to lunch. With most of the money, I would open up a bank account. With half of the money, I would buy dinner for my family. If I were a millionaire, I would travel around the world!",
            "chi": "如果我有很多錢，我會開立一個銀行帳戶。我認為你應該存錢。我會在高級餐廳享用大餐。我認為你應該享受美食。我會把錢和妹妹分享。我會把錢給無家可歸的人。\n我爸爸喜歡領帶，所以我會買一條領帶給他。我哥哥喜歡電腦遊戲，所以我會買一款電腦遊戲給他。我姊姊喜歡推理小說，所以我會買一本推理小說給她。\n用其中一些錢，我會請朋友吃午餐。用大部分的錢，我會開一個銀行帳戶。用一半的錢，我會買晚餐給家人吃。如果我是百萬富翁，我就會環遊世界！",
            "key_sentences": [
                {
                    "sentence": "If I were a millionaire, I would travel around the world!",
                    "tag": "🔥 假設語氣 Be 動詞一律用 were",
                    "note": "在與現在事實相反的 If 子句中，不論主詞是 I / he / she，be 動詞正式用法一律用 were！"
                }
            ]
        }
    ],
    "rw6_5": [
        {
            "sequence": 1,
            "section_title": "📖 課本單元導讀 (p.35)：Topic 3 Intro — The Mighty Compass (神奇的指北針)",
            "eng": "The first compasses were used about eight hundred years ago. A compass is an instrument you use to tell direction. It has a small, pointed magnet that always points north. If you know where north is, you can always find south, west, and east. Use a compass with a map, and you can find your way anywhere!",
            "chi": "最早的指北針大約在八百年前開始被使用。指北針是一種用來辨別方向的儀器。它裡面有一根細小、尖端的磁鐵，永遠指向北方。如果你知道北方在哪裡，你就能隨時找出南方、西方和東方。將指北針搭配地圖一起使用，你就能在任何地方找到路！",
            "key_sentences": [
                {
                    "sentence": "It has a small, pointed magnet that always points north.",
                    "tag": "⭐ 科普細節必考句",
                    "note": "指北針內部的指針是一塊小磁鐵 (magnet)，永遠指向北方 (north)。"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本主課文全文 Part 1 (p.36)：Lost and Found — Missing the Turn in the Fog",
            "eng": "Jaya and her family went hiking one foggy morning. Their goal was a hill with a tall, crooked tree on top. They liked to picnic there.\n\"I think we missed our turn,\" said Jaya. She pointed to a log bench on the left side of the trail.\n\"Yeah, I don't remember this bench. There's a place we should have turned right, but I think we went straight,\" said her brother, Manoj.\nTheir mom looked at her watch, and added, \"And it's noon. We should be there by now.\"",
            "chi": "一個起霧的早晨，佳雅（Jaya）和她的家人去健行。他們的目標是一座山頂上有一棵高大彎曲樹木的山丘。他們喜歡在那裡野餐。\n「我想我們錯過轉彎處了，」佳雅說。她指著步道左側的一張原木長凳。\n「對啊，我不記得有這張長凳。有一個地方我們本來應該右轉，但我想我們卻直走了，」她的弟弟馬諾傑（Manoj）說。\n他們的媽媽看了看手錶補充道：「而且現在已經正午十二點了。我們現在應該已經到那裡了才對。」",
            "key_sentences": [
                {
                    "sentence": "Jaya and her family went hiking one foggy morning. Their goal was a hill with a tall, crooked tree on top.",
                    "tag": "🔥 閱讀策略：Setting (時空背景)",
                    "note": "時間與天氣：one foggy morning（起霧的早晨）；目的地：山頂有棵高大彎曲樹 (crooked tree) 的山丘。"
                },
                {
                    "sentence": "There's a place we should have turned right, but I think we went straight,",
                    "tag": "🔥 迷路原因必考細節",
                    "note": "為什麼迷路？因為濃霧中他們本來應該右轉 (turned right)，卻誤直走了 (went straight)！"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 課本主課文全文 Part 2 (p.37)：Lost and Found — Above the Sea of Clouds",
            "eng": "They stopped and looked around at the trees. Jaya realized they were next to a different, smaller hill. She said, \"Before we go back down the trail, we should hike up the hill and take a look around!\"\n\"I'm tired,\" said Manoj. \"I don't want to climb an extra hill.\"\n\"Why not? Let's go!\" said their mom. So they walked up, and they discovered the top of the hill was above the fog. \"Nice!\" Mom said. \"We know how to read a map, so let's look. There's the lighthouse near town. We know that's south, and I think we're on a hill between the lighthouse and our usual picnic spot.\"\nThey looked at the map. Then they looked around and saw the top of another hill to the northeast. It had a tall, crooked tree on top.\n\"There it is!\" said Jaya. \"It looks like an island in a sea of clouds.\"",
            "chi": "他們停下腳步，環顧四周的樹木。佳雅意識到他們正位於另一座比較小的山丘旁邊。她說：「在我們沿著步道折返下山之前，我們應該爬上這座山丘四處看看！」\n「我累了，」馬諾傑說。「我不想多爬一座山。」\n「有何不可？我們走吧！」媽媽說。於是他們往上走，並發現山頂高於濃霧之上。「太棒了！」媽媽說。「我們會看地圖，所以來看看吧。那是城鎮附近的燈塔。我們知道那是南方，我想我們現在所在的山丘，剛好介於燈塔和我們平常野餐地點之間。」\n他們看了看地圖。接著他們環顧四周，看見東北方另一座山丘的山頂。上面有一棵高大彎曲的樹。\n「就在那裡！」佳雅說。「它看起來就像雲海中的一座島嶼。」",
            "key_sentences": [
                {
                    "sentence": "So they walked up, and they discovered the top of the hill was above the fog.",
                    "tag": "🔥 課本選擇題必考陷阱",
                    "note": "山頂在濃霧之上 (above the fog)，所以濃霧是在山下 (at the bottom of the hill)，視野才豁然開朗！"
                },
                {
                    "sentence": "There's the lighthouse near town. We know that's south, and I think we're on a hill between the lighthouse and our usual picnic spot.",
                    "tag": "⭐ 空間方位定位邏輯",
                    "note": "燈塔在南方 (south)，野餐山頭在東北方 (northeast)，一家人位在兩者之間 (between A and B)。"
                }
            ]
        },
        {
            "sequence": 4,
            "section_title": "📖 課本練習短文與副篇 (p.39)：Hiking in the Park & Warning! Warning! (燈塔科普)",
            "eng": "My mom, my sister, and I went hiking in our favorite park last weekend. We usually turn right at a place where the main trail splits. On this trip, we decided to go straight instead of turning. We knew where we were going, so we didn't need to read a map. Our plan was to go back to an old, giant tree we once found by accident. We walked until we saw a bench on the left side of the trail, near a tall hill. We were going to hike up the hill, but it was a long climb, so we rested. I sat down next to my sister on the bench. Mom sat down between us. But after only one minute, she asked, \"Are you ready to hike?\"\n\nWarning! Warning!\nA lighthouse is a tall tower built on the coast. The top of a lighthouse has a huge lamp and a very loud horn. The light from the lamp can be seen far out on the ocean. The horn can be heard far away. When fog forms, someone goes to the lighthouse and turns on the light and horn. This warns people in ships where the land is, telling them which direction not to go.",
            "chi": "上週末，我媽媽、我姊姊和我去我們最喜歡的公園健行。我們通常在主步道分岔的地方右轉。這趟旅程中，我們決定直走而不轉彎。我們知道要去哪裡，所以不需要看地圖。我們的計畫是折返去一棵我們曾偶然發現的古老巨樹。我們一直走到看見步道左側有一張長凳，靠近一座高山丘。我們原本打算爬上山丘，但路途漫長，所以我們休息了一下。我坐在長凳上我姊姊旁邊。媽媽坐在我們兩人之間。但才過了一分鐘，她就問：「你們準備好健行了嗎？」\n\n警告！警告！（燈塔科普）\n燈塔是建造在海岸邊的高塔。燈塔頂端有一盞巨大的燈和一個非常響亮的號角（霧角）。燈光可以在遙遠的海面上被看見。號角聲可以在很遠的地方被聽見。當濃霧形成時，會有人前往燈塔打開巨燈與號角。這能警告船隻上的人們陸地在哪裡，告訴他們哪個方向不能去。",
            "key_sentences": [
                {
                    "sentence": "When fog forms, someone goes to the lighthouse and turns on the light and horn. This warns people in ships where the land is,",
                    "tag": "⭐ 副篇閱讀理解必考",
                    "note": "起霧時燈塔會開啟巨燈 (lamp) 與霧角 (horn)，警告船上的人們 (people in ships) 陸地位置。"
                }
            ]
        }
    ],
    "rw6_6": [
        {
            "sequence": 1,
            "section_title": "📖 課本主課文全文 Part 1 (p.40)：The World of Orienteering (岱崙 W5 聽寫 25 分原篇！)",
            "eng": "Imagine you are in a new city. Standing on a corner, you ask someone how to get to a store. They tell you to \"go two blocks north, turn left, and you'll be across the street from the bookstore.\" Now imagine you are in an outdoor race. Instead of directions, you have only a map and a compass, and instead of running down a marked road, you run around in the woods. Welcome to orienteering!\nIn the sport of orienteering, racers use a map and compass to find stations, which are called controls. A special flag marks each control (see Figure 1). Controls are placed so you can't see them easily from all directions. They may be in front of a big rock or behind a tree, which means racers must use their maps and compasses to find controls.",
            "chi": "想像你身在一座陌生的城市。站在街角，你向路人詢問如何前往一家商店。他們告訴你：「往北走兩個街區，左轉，你就會在書店的對街。」現在想像你正在參加一場戶外競賽。沒有方向指引，你只有一張地圖和一個指北針；而且不是沿著標示好的馬路跑，你是在樹林裡四處奔跑。歡迎來到定向越野運動！\n在定向越野這項運動中，參賽者使用地圖和指北針來尋找稱為「控制點（controls）」的站點。一面特殊的旗幟標記著每個控制點（見圖 1）。控制點的放置方式讓你無法輕易從各個方向看見它們。它們可能位於巨石前方或大樹後面，這意味著參賽者必須運用地圖和指北針才能找到控制點。",
            "key_sentences": [
                {
                    "sentence": "Instead of directions, you have only a map and a compass, and instead of running down a marked road, you run around in the woods.",
                    "tag": "🔥 岱崙 W5 聽寫考卷原句",
                    "note": "注意介系詞片語 instead of + N/V-ing（代替/而不是），以及必備工具 a map and a compass（缺一不可）。"
                },
                {
                    "sentence": "They may be in front of a big rock or behind a tree,",
                    "tag": "⚠️ 岱崙 W4 小考真實失分片語",
                    "note": "in front of 是三個獨立單字，介系詞是單 f 的 of（Rex 曾誤寫成 infront off ❌）！"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本主課文全文 Part 2 (p.41)：The World of Orienteering — Control Cards & Winning Rules",
            "eng": "At each control, racers mark a card they carry with them (see Figure 2). The cards are very important because racers must find all the controls to win. If someone misses a control, they won't have that mark on their card. They might cross the finish line first, but the next person to finish with a full card will win the race.\nIn a race in a city, you might only need to cross the street to get to the finish line. In orienteering, you will likely run along a river, climb over rocks, and go up and down hills. And, after all that, you still have to use your compass to find the finish line!\n[Visual Info — Figure 1: A bright red-and-white triangular control flag hanging behind a tree. Figure 2: Orienteering Control Card with 18 numbered boxes for punching marks.]",
            "chi": "在每個控制點，參賽者會在隨身攜帶的卡片上做記號（見圖 2）。這些卡片非常重要，因為參賽者必須找到所有的控制點才能獲勝。如果有人漏掉了一個控制點，他們的卡片上就不會有那個記號。他們也許會第一個衝過終點線，但下一位打滿整張卡片並完成比賽的人才會贏得比賽。\n在城市裡的比賽，你計算也許只需要過馬路就能抵達終點線。但在定向越野中，你很可能會沿著河邊奔跑、爬過岩石，並在山丘間上下穿梭。而且在經歷這一切之後，你仍然必須使用指北針來找到終點線！\n【視覺圖表補充 —— 圖 1：掛在樹後的紅白相間三角形控制旗。圖 2：共有 18 個編號打卡格的定向越野控制卡。】",
            "key_sentences": [
                {
                    "sentence": "They might cross the finish line first, but the next person to finish with a full card will win the race.",
                    "tag": "🔥 閱讀理解最大陷阱：誰才會贏？",
                    "note": "第一個衝過終點線的人不一定贏！必須『打滿全卡所有控制點 (with a full card — 共 18 點)』且最快完成的人才獲勝！"
                },
                {
                    "sentence": "In orienteering, you will likely run along a river, climb over rocks, and go up and down hills.",
                    "tag": "⭐ 地形移動片語三連發",
                    "note": "along a river（沿著河）、climb over rocks（爬過岩石）、go up and down hills（上下山丘）。"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 課本副篇短文全文 (p.43)：Treasure Hunt (公園尋寶派對)",
            "eng": "Treasure Hunt\nMy friend Bayani had the best party this weekend! He lives across the street from the park, and his family made a treasure hunt for us to do there. They gave us maps, compasses, and directions. My team's first direction said, \"Start at the north corner of the swings. Then walk east for 50 steps.\" We were the first group to find a treasure! We ate them before we got back to Bayani's house.",
            "chi": "尋寶遊戲\n我的朋友巴亞尼（Bayani）這個週末舉辦了最棒的派對！他家住在公園對街，他的家人為我們在公園裡設計了一場尋寶遊戲。他們發給我們地圖、指北針和方向指引。我們這隊的第一條指引寫著：「從鞦韆的北角出發。然後向東走 50 步。」我們是第一組找到寶藏的隊伍！在回到巴亞尼家之前，我們就把寶藏吃光了。",
            "key_sentences": [
                {
                    "sentence": "He lives across the street from the park, and his family made a treasure hunt for us to do there.",
                    "tag": "⭐ 副篇細節推理",
                    "note": "Bayani 家在公園對面 (across from the park)；且因為『We ate them』加上插圖餅乾盒，可推論寶藏是 cookies！"
                }
            ]
        }
    ],
    "rw6_7": [
        {
            "sequence": 1,
            "section_title": "📖 課本單元導讀 (p.49)：Topic 4 Intro — How We Talk & Sign Languages (手語溝通)",
            "eng": "There are many languages around the world. People who can't hear or speak use special languages called sign languages.\nIn sign languages, people \"talk\" using their hands to make signals. They also communicate by making different faces and moving their bodies. In American sign language, for instance, you can say \"thank you\" by putting your fingers on your chin and moving your hand out. This is also the sign for \"you're welcome.\"",
            "chi": "世界上有許多種語言。聽不見或無法說話的人使用稱為「手語（sign languages）」的特殊語言。\n在手語中，人們運用雙手比出訊號來「交談」。他們也會透過做出不同臉部表情和身體動作來溝通。舉例來說，在美國手語中，你可以把手指放在下巴並將手向外移來表達「謝謝你」。這同時也是「不客氣」的手勢。",
            "key_sentences": [
                {
                    "sentence": "People who can't hear or speak use special languages called sign languages.",
                    "tag": "⭐ 導讀核心概念",
                    "note": "手語 (sign language) 透過手勢訊號 (signals)、臉部表情與肢體動作進行溝通。"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本主課文全文 Part 1 (p.50)：Languages We Use — Native vs. Official Languages",
            "eng": "Everyone is a native speaker of their first language. This is the language you learned and speak at home. An official language is the one used by the government of a country. Most people learn this in school. A country has to pass a law to make a language official.\nSome countries have no official language. Mexico is one example. Most people there speak Spanish. Many Mexican people speak native languages, too. But Mexico never passed a law to make any language official.\nIn many countries, most of the people have the same native language. This often becomes the official one as well. For example, most people in France speak French as their native language. French is also the official language.",
            "chi": "每個人都是自己第一語言的母語使用者（native speaker）。這是你在家裡習得並使用的語言。官方語言（official language）則是一國政府所使用的語言。大多數人在學校學習這種語言。一個國家必須通過法律（pass a law），才能使一種語言成為官方語言。\n有些國家沒有官方語言。墨西哥就是一個例子。那裡的大多數人說西班牙語。許多墨西哥人也說當地原住民母語。但墨西哥從未通過法律將任何語言定為官方語言。\n在許多國家，大多數人擁有相同的母語。這通常也會成為官方語言。例如，法國大多數人以法語作為母語，而法語同時也是法國的官方語言。",
            "key_sentences": [
                {
                    "sentence": "A country has to pass a law to make a language official.",
                    "tag": "🔥 官方語言成立的唯一法定條件",
                    "note": "必須『通過法律 (pass a law)』才算官方語言！墨西哥雖普遍說西班牙語、美國雖普遍說英語，但因未立法，皆屬於『無官方語言 (0 official languages)』！"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 課本主課文全文 Part 2 & 長條圖 (p.51)：Zimbabwe, China, India & 196 Countries Bar Graph",
            "eng": "A small country like Zimbabwe can have many official languages. There are four other countries around Zimbabwe, so people speak different languages from those countries. Zimbabwe has the most official languages in the world—sixteen!\n[Bar Graph — Official Languages for 196 Countries: 0 official languages = 8 countries; 1 official language = 110 countries; 2 official languages = 48 countries; 3 official languages = 16 countries; 4+ official languages = 14 countries.]\nA large country like China may have only a few official languages. China is one of the biggest countries in the world. Every day, people in China use over a hundred languages. But most people just use one Chinese language to talk with each other. It's called Mandarin.\nIndia is another huge country. Many people in India speak Hindi. It's a native language. But Hindi and English are the two official languages of India. In fact, people in India speak more than a thousand native languages in all!",
            "chi": "像辛巴威（Zimbabwe）這樣的小國卻可能擁有許多官方語言。辛巴威周圍環繞著另外四個國家，因此人們說著來自那些國家的不同語言。辛巴威擁有全世界最多的官方語言——高達 16 種！\n【長條圖數據 —— 全球 196 國官方語言統計：0 種官方語言 = 8 國；1 種官方語言 = 110 國（最多）；2 種官方語言 = 48 國；3 種官方語言 = 16 國；4 種以上官方語言 = 14 國（含辛巴威）。】\n像中國這樣的大國可能只有少數幾種官方語言。中國是世界上最大的國家之一。每天在中國有超過一百種語言被使用。但大多數人只使用一種中文來彼此交談，稱為華語（Mandarin）。\n印度是另一個龐大的國家。印度有許多人說印地語（Hindi），那是一種母語。但印地語和英語是印度的兩種官方語言。事實上，印度人總共說著超過一千種以上的母語！",
            "key_sentences": [
                {
                    "sentence": "Zimbabwe has the most official languages in the world—sixteen!",
                    "tag": "🔥 國家案例與長條圖交叉必考",
                    "note": "辛巴威有 16 種官方語言（世界第一，對應長條圖 4+ 的 14 國）；法國有 1 種（對應 110 國）；印度有 2 種（Hindi & English）；墨西哥與美國為 0 種（對應 8 國）。"
                }
            ]
        },
        {
            "sequence": 4,
            "section_title": "📖 課本練習與副篇全文 (p.53)：Languages in North America & Tawanda's Story (My Languages)",
            "eng": "A long time ago, people from Spain brought their language to Mexico. Today, Mexican people speak Spanish. Similarly, language traveled from England to the United States, so many people in the United States speak English. Most people in the United States and Mexico are native speakers of either English or Spanish. People from all over the world have moved to these countries, too. People from China brought the Chinese language with them. Many people from India brought Hindi. People from France brought their native language, French. And yet the United States and Mexico are countries with no official languages! Neither country has passed a law to make one.\n\nMy Languages\nMy name is Tawanda. I grew up in a small village in Zimbabwe. The country has sixteen official languages. My native language is called Shona, and I also learned English in school. I know a few words in other languages, but don't speak or read them. When I was nineteen years old, I moved to Tanzania, a country near Zimbabwe. English and Swahili are the official languages here. So I'm learning Swahili now, too.",
            "chi": "很久以前，來自西班牙的人們把他們的語言帶到了墨西哥。今天，墨西哥人說西班牙語。同樣地，語言從英國傳到了美國，所以許多美國人說英語。美國和墨西哥的大多數人不是英語就是西班牙語的母語使用者。世界各地的人們也移居到這些國家。來自中國的人帶來了中文，許多來自印度的人帶來了印地語，來自法國的人帶來了他們的母語法語。然而，美國和墨西哥卻都是沒有官方語言的國家！這兩個國家都沒有通過法律來制定官方語言。\n\n我的語言（Tawanda 的故事）\n我的名字叫塔萬達（Tawanda）。我在辛巴威的一個小村莊長大。這個國家有 16 種官方語言。我的母語叫做修納語（Shona），而且我在學校也學了英語。我知道其他語言的幾個單字，但不會說也不會讀。當我十九歲時，我搬到了辛巴威附近的國家坦尚尼亞（Tanzania）。英語和史瓦希里語（Swahili）是這裡的官方語言。所以我現在也正在學史瓦希里語。",
            "key_sentences": [
                {
                    "sentence": "And yet the United States and Mexico are countries with no official languages! Neither country has passed a law to make one.",
                    "tag": "⭐ 結合 U13 Neither 文法與 U7 社科知識",
                    "note": "注意 Neither country has passed a law（兩國皆未立法），呼應 Grammar U13 否定句型！"
                }
            ]
        }
    ],
    "rw6_8": [
        {
            "sequence": 1,
            "section_title": "📖 課本主課文全文 Part 1 (p.54)：So Many Questions — Meeting Rosa at the Door",
            "eng": "\"Can you hold the door?\" the girl asked Erico in Italian. \"No problem,\" he replied in English, pushing the door open and holding it there.\nThe girl walked through, carrying a big pile of drawing paper and other supplies. \"Hi, I'm Rosa,\" she said as she struggled to hold onto the supplies. \"Are you the new student from Italy?\"\n\"No,\" he replied. \"I mean, I only lived there three months, but yes, I'm new here.\" \"You sound like you have a British accent, but you have an Italian name. Did you live in England, too?\" asked Rosa. \"Sorry, my friends say I ask a lot of questions. I hope you don't mind. But I speak Italian at home, and I thought you might, too.\" It was the second day of summer school and Erico's second month in the United States. He enjoyed meeting new people, even if they did ask a lot of questions.",
            "chi": "「你可以幫我扶著門嗎？」女孩用義大利語問艾里코（Erico）。「沒問題，」他用英語回答，一邊把門推開並扶著。\n女孩走了過去，手裡抱著一大疊圖畫紙和其他美術用品。「嗨，我是蘿莎（Rosa），」她一邊吃力地抓緊手上的用品一邊說。「你是從義大利來的新學生嗎？」\n「不是，」他回答。「我的意思是，我只在那裡住了三個月，但沒錯，我是新來的。」「你聽起來有英國腔調，但你卻有個義大利名字。你也住過英國嗎？」蘿莎問。「抱歉，我朋友都說我問題很多。希望你別介意。但我在家說義大利語，我以為你也是。」那天是暑期學校的第二天，也是艾里柯來到美國的第二個月。他很喜歡認識新朋友，就算他們真的問了一大堆問題。",
            "key_sentences": [
                {
                    "sentence": "The girl walked through, carrying a big pile of drawing paper and other supplies.",
                    "tag": "🔥 閱讀策略：Make Predictions (線索預測)",
                    "note": "從『drawing paper, paint brushes, colored pencils』這些線索，可預測 Rosa 正要去上美術課 (art class)！"
                },
                {
                    "sentence": "You sound like you have a British accent, but you have an Italian name.",
                    "tag": "⭐ 角色背景細節辨析",
                    "note": "Rosa 第一句話講的是義大利語 (Italian)；Erico 說話帶有英國腔 (British accent)，不是澳洲腔！"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本主課文全文 Part 2 (p.55)：So Many Questions — Multicultural Family & Friendly Help",
            "eng": "\"My name is Portuguese, but my family's from Australia. My dad moved there from Brazil, and my mom's from Portugal ...\"\n\"Oh!\" Rosa interrupted. \"Do they speak Portuguese and English? Are they bilingual? Are you? Do your parents have Australian accents? Does speaking Portuguese help you learn Italian at all? Wait—why do you sound British?\"\nRosa asked all of these questions very quickly and dropped her supplies while she was talking. Erico realized that asking so many questions was Rosa's way of being friendly, and he helped her pick up her paper, paint brushes, and colored pencils.\n\"Yes, Portuguese did help me learn some Italian,\" he said. \"As for my British accent, do you want to hear a long story?\"",
            "chi": "「我的名字是葡萄牙語，但我的家人來自澳洲。我爸爸從巴西搬去那裡，而我媽媽來自葡萄牙……」\n「噢！」蘿莎插話道。「他們說葡萄牙語和英語嗎？他們是雙語人士（bilingual）嗎？你也是嗎？你父母有澳洲腔嗎？說葡萄牙語對你學義大利語有幫助嗎？等等——那你為什麼聽起來像英國人？」\n蘿莎連珠砲似地飛快問完這些問題，說話時還把美術用品掉了一地。艾里柯明白，問這麼多問題是蘿莎展現友善的方式，於是他幫她撿起圖畫紙、畫筆和色鉛筆。\n「對，葡萄牙語確實幫我學會了一些義大利語，」他說。「至於我的英國腔，你想聽一個長長的故事嗎？」",
            "key_sentences": [
                {
                    "sentence": "My name is Portuguese, but my family's from Australia. My dad moved there from Brazil, and my mom's from Portugal ...",
                    "tag": "🔥 Erico 跨國家庭背景必考題",
                    "note": "Erico 出生/家庭來自澳洲 (Australia)；爸爸來自巴西 (Brazil)；媽媽來自葡萄牙 (Portugal)；在義大利住過 3 個月；現在在美國上暑期學校！"
                },
                {
                    "sentence": "Erico realized that asking so many questions was Rosa's way of being friendly,",
                    "tag": "⭐ 人物性格與態度題",
                    "note": "Erico 並不覺得 Rosa 沒禮貌或不友善 (unfriendly)，反而理解這是她表達友善 (friendly) 的方式。"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 課本副篇短訊全文 (p.57)：Hey, Friends! (跨國搬家後的雙語生活)",
            "eng": "Hey, Friends!\nJane and Tomi, I really miss you, my friends! We'll have to do a video call soon. I miss Mexico, but we're having fun in California. Also, it's nice to speak English again every day. Although some days it's hard to remember which conversations I've had in which language! My sister has already made some new friends—oops, I just sat down to write this, but I hear my dad calling, saying dinner's ready. I'll be back later!",
            "chi": "嘿，朋友們！\n珍（Jane）和湯米（Tomi），我好想念你們，我的朋友們！我們很快一定要來視訊通話。我想念墨西哥，但我們在加州玩得很開心。此外，每天能再次說英語真好。雖然有幾天很難記住我到底是用哪種語言進行了哪些對話！我妹妹已經交到一些新朋友了——哎呀，我才剛坐下來寫這封信，但就聽到我爸在叫我，說晚餐準備好了。我晚點再回來！",
            "key_sentences": [
                {
                    "sentence": "I just sat down to write this, but I hear my dad calling, saying dinner's ready. I'll be back later!",
                    "tag": "⭐ 預測下一秒動作題",
                    "note": "爸爸喊 dinner's ready，所以作者發出訊息後接下來會去吃晚餐 (go eat dinner)！"
                }
            ]
        }
    ],
    "rd6_4": [
        {
            "sequence": 1,
            "section_title": "📖 課本全文第 1 節 (p.16)：Chapter 4: Rocks and Ice — Asteroid Belt & Kuiper Belt",
            "eng": "There are two rings around the Sun, called the asteroid belt and the Kuiper belt. The asteroid belt is between Mars and Jupiter. It's made of rocks called asteroids. The Kuiper belt is further away than Neptune. It's made of pieces of ice.\n\nAsteroids\nSome rocks in the asteroid belt are the size of houses, but others are many kilometers across. When planets come near them, or other asteroids hit them, these rocks can leave the asteroid belt. Sometimes, they travel toward the inner planets.",
            "chi": "太陽周圍有兩個環帶，稱為小行星帶（asteroid belt）和古柏帶（Kuiper belt）。小行星帶位於火星和木星之間。它是由稱為小行星（asteroids）的岩石組成的。古柏帶則比海王星更遙遠。它是由碎冰塊組成的。\n\n小行星（Asteroids）\n小行星帶中的一些岩石有房子那麼大，但其他的則有好幾公里寬。當行星靠近它們，或者其他小行星撞擊它們時，這些岩石就可能離開小行星帶。有時候，它們會朝著內側行星移動。",
            "key_sentences": [
                {
                    "sentence": "The asteroid belt is between Mars and Jupiter. It's made of rocks called asteroids. The Kuiper belt is further away than Neptune. It's made of pieces of ice.",
                    "tag": "🔥 兩大環帶位置與成分對比（必考！）",
                    "note": "小行星帶：火星與木星之間 (between Mars and Jupiter)，由岩石 (rocks) 組成；古柏帶：海王星之外 (further away than Neptune)，由冰塊 (pieces of ice) 組成。"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本全文第 2 節 (p.17)：Comets & Halley's Comet (彗星、彗尾成因與哈雷彗星)",
            "eng": "Comets\nComets are huge pieces of ice and dust, and some of them are 50 kilometers across. Comets come from the Kuiper belt, or from further away in space, but sometimes their orbits bring them nearer Earth and the Sun. When comets come nearer the Sun, they become hotter and they leave pieces of ice and dust behind them. This is called a comet's tail and it can be millions of kilometers long!\n\n[Discover! Box]\nHalley's Comet is a famous comet. It comes near Earth every 75 or 76 years. We will see it again in 2061.",
            "chi": "彗星（Comets）\n彗星是巨大的冰塊和塵埃，其中一些寬達 50 公里。彗星來自古柏帶，或來自太空更遙遠的地方，但有時它們的軌道會將它們帶到靠近地球和太陽的地方。當彗星靠近太陽時，它們會變得更熱，並在身後留下冰塊和塵埃碎片。這被稱為彗星的尾巴（comet's tail），它可以長達數百萬公里！\n\n【探索專欄 Discover!】\n哈雷彗星（Halley's Comet）是一顆著名的彗星。它每 75 或 76 年靠近地球一次。我們將在 2061 年再次看到它。",
            "key_sentences": [
                {
                    "sentence": "When comets come nearer the Sun, they become hotter and they leave pieces of ice and dust behind them. This is called a comet's tail",
                    "tag": "🔥 彗尾形成科學原理",
                    "note": "彗星靠近太陽時會變熱 (become hotter，不是 colder！)，釋放冰與塵埃形成長達數百萬公里的彗尾。"
                },
                {
                    "sentence": "Halley's Comet is a famous comet. It comes near Earth every 75 or 76 years. We will see it again in 2061.",
                    "tag": "⭐ 數據必記題",
                    "note": "哈雷彗星週期為 75~76 年，下次造訪為 2061 年。"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 課本全文第 3 節 (p.18)：Meteors, Meteorites & Craters (流星、隕石與木星撞擊事件)",
            "eng": "Meteors and Meteorites\nMeteors are pieces of rock, dust, or ice that enter a planet's atmosphere. They come from asteroids and comets.\nMost meteors burn when they enter the atmosphere, but sometimes pieces hit a planet's surface and these pieces are called meteorites. More than 1,000 metric tons of ice, dust, and rocks from space land on Earth every year, but most of these pieces are very small.\nSometimes big meteorites hit Earth and make a huge hole called a crater. Big meteorites don't hit planets very often, but they are very dangerous. In 1994, 21 pieces of a comet hit Jupiter. Some of the explosions were bigger than our planet Earth!",
            "chi": "流星與隕石（Meteors and Meteorites）\n流星（Meteors）是進入行星大氣層的岩石、塵埃或冰塊碎片。它們來自小行星和彗星。\n大多數流星在進入大氣層時就會燃燒殆盡，但有時碎片會撞擊行星表面，這些撞擊地面的碎片被稱為隕石（meteorites）。每年有超過 1,000 公噸來自太空的冰、塵埃和岩石降落在地球上，但其中大多數碎片都非常微小。\n有時巨大的隕石撞擊地球，會打出一個稱為隕石坑（crater）的巨大坑洞。大隕石並不常撞擊行星，但它們非常危險。1994 年，一顆彗星的 21 塊碎片撞擊了木星。其中一些爆炸規模比我們的地球還要大！",
            "key_sentences": [
                {
                    "sentence": "Most meteors burn when they enter the atmosphere, but sometimes pieces hit a planet's surface and these pieces are called meteorites.",
                    "tag": "🔥 Meteor vs. Meteorite 終極辨析",
                    "note": "進入大氣層燃燒發光的是流星 (meteor)；沒燒完撞上星球表面的石頭才是隕石 (meteorite)！"
                }
            ]
        },
        {
            "sequence": 4,
            "section_title": "📖 課本全文第 4 節 (p.19)：Tunguska Explosion (1908) & Chicxulub Dinosaur Extinction",
            "eng": "[Discover! Box]\nIn 1908, a meteorite exploded in the sky above the Tunguska River, in Siberia in Russia. No one lived there, but a forest of 80 million trees was burned.\n\nAbout 65 million years ago, there were no people on Earth, and the animals were different, too. Dinosaurs lived here. Then one day a bright light appeared in the sky. It was a huge meteorite. Some of it burned in the atmosphere, but a piece hit Earth – it was about 20 kilometers long. The meteorite crater is in Chicxulub, in the Yucatan in Mexico, and it's 180 kilometers across!\nWhen the meteorite hit Earth, there was a huge explosion. Scientists think that fires and acid destroyed most of the world's forests. Clouds of dust covered the sky, and light from the Sun didn't reach Earth's surface. It became very cold for many years. At about the same time, the dinosaurs and 70% of all the plants and other animals on Earth died.",
            "chi": "【探索專欄 Discover!】\n1908 年，一顆隕石在俄羅斯西伯利亞通古斯河（Tunguska River）上空爆炸。那裡沒有人居住，但有一片由 8,000 萬棵樹木組成的森林被燒毀。\n\n大約 6,500 萬年前，地球上還沒有人類，動物也與現在不同。恐龍住在這裡。突然有一天，天空中出現一道強光。那是一顆巨大的隕石。它的一部分在大氣層中燃燒，但有一塊碎片撞擊了地球——它大約有 20 公里長。這個隕石坑位於墨西哥尤卡坦半島的希克蘇魯伯（Chicxulub），寬達 180 公里！\n當隕石撞擊地球時，發生了巨大的爆炸。科學家認為大火和酸雨摧毀了世界上大部分的森林。塵埃雲遮蔽了天空，來自太陽的光線無法照到地球表面。地球變得極度寒冷長達好幾年。大約在同一時間，恐龍以及地球上 70% 的植物和其他動物都滅絕了。",
            "key_sentences": [
                {
                    "sentence": "The meteorite crater is in Chicxulub, in the Yucatan in Mexico, and it's 180 kilometers across!",
                    "tag": "🔥 課本 p.43 T/C 配對必考題",
                    "note": "通古斯 (Tunguska, 1908 俄羅斯)：空中爆炸、燒毀 8000 萬棵樹；希克蘇魯伯 (Chicxulub, 6500 萬年前墨西哥)：隕石長 20 公里、坑寬 180 公里、塵埃遮日變冷、導致恐龍與 70% 動植物滅絕！"
                }
            ]
        }
    ],
    "rd6_5": [
        {
            "sequence": 1,
            "section_title": "📖 課本全文第 1 節 (p.20)：Chapter 5: Astronomy — Ancient Astronomers & Abu Simbel",
            "eng": "Astronomy is studying the planets and the stars, and people who study astronomy are called astronomers. Do you know what they have discovered?\n\nAncient Astronomers\nThousands of years ago, people in places like China, Iraq, and Greece used the Sun, the Moon, and the stars to calculate the time of year and the seasons. This is how they knew the dates of festivals and when to plant seeds. Many people, like the Ancient Egyptians or the Incas of South America, thought that the Sun was a god. They built beautiful temples for the Sun.\n\n[Discover! Box]\nSunlight falls on the statues in this Ancient Egyptian temple at sunrise on two days every year. These were important days in the Egyptian calendar.",
            "chi": "天文學（Astronomy）是研究行星與恆星的學科，而研究天文學的人被稱為天文學家（astronomers）。你知道他們發現了什麼嗎？\n\n古代天文學家（Ancient Astronomers）\n數千年前，在中國、伊拉克和希臘等地的人們利用太陽、月亮和星星來計算一年中的時間與季節。這就是他們得知節日日期與何時播種（plant seeds）的方法。許多民族，像是古埃及人或南美洲的印加人，認為太陽是神明。他們為太陽建造了美麗的神廟（temples）。\n\n【探索專欄 Discover!：阿布辛貝神廟】\n每年有兩天的日出時分，陽光會精準照射進這座古埃及神廟內部的雕像上。這兩天是古埃及曆法（calendar）中的重要日子。",
            "key_sentences": [
                {
                    "sentence": "Thousands of years ago, people in places like China, Iraq, and Greece used the Sun, the Moon, and the stars to calculate the time of year and the seasons.",
                    "tag": "⭐ 古代天文用途必考",
                    "note": "古人觀測日月星辰來計算季節、節日日期 (dates of festivals) 與何時播種 (when to plant seeds)。"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 課本全文第 2 節 (p.21)：Understanding the Solar System — Copernicus, Galileo & Newton",
            "eng": "Most ancient astronomers believed that Earth was at the center of our solar system. They thought that the Sun, the other stars, and all the planets orbited Earth.\nIn 1543, a Polish astronomer called Copernicus said that the Sun was at the center of our solar system, but people didn't believe him. Later, other astronomers like Galileo Galilei, from Pisa, now in Italy, believed him, but important people stopped them writing about their ideas. Almost 150 years later, a British astronomer called Isaac Newton proved that Earth orbits the Sun.\n\n[Discover! Box]\nIsaac Newton discovered the force of gravity. Gravity makes things fall to the ground on Earth. It also makes the planets orbit the Sun.",
            "chi": "大多數古代天文學家相信地球位於我們太陽系的中心。他們認為太陽、其他恆星以及所有行星都繞著地球運行。\n1543 年，一位名叫哥白尼（Copernicus）的波蘭天文學家提出太陽位於太陽系的中心，但當時人們並不相信他。後來，其他像來自比薩（位於今日義大利）的伽利略（Galileo Galilei）等天文學家相信了他，但權貴人士阻止他們把這些想法寫出來。將近 150 年後，一位名叫艾薩克·牛頓（Isaac Newton）的英國天文學家證明了地球是繞著太陽運行的。\n\n【探索專欄 Discover!】\n艾薩克·牛頓發現了重力（萬有引力，gravity）的力量。重力使地球上的物體掉落到地面，它同時也使行星繞著太陽運行。",
            "key_sentences": [
                {
                    "sentence": "In 1543, a Polish astronomer called Copernicus said that the Sun was at the center of our solar system, but people didn't believe him.",
                    "tag": "🔥 四大科學家貢獻配對（必考！）",
                    "note": "哥白尼 (Copernicus, 1543)：提出太陽中心說但沒人信；伽利略 (Galileo, 1609)：相信哥白尼並用望遠鏡觀測，但被權貴阻止寫作；牛頓 (Newton)：發現重力 (gravity) 並證明 (proved) 地球繞日！"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 課本全文第 3 節 (p.22)：Galileo's Telescope, The Milky Way & Edwin Hubble",
            "eng": "Galileo and the First Telescopes\nTelescopes help people to learn about our solar system. In 1609, Galileo used one of the first telescopes to look at the night sky. He saw mountains and craters on the Moon, and four moons around Jupiter. The first telescopes were very small. Later, people made bigger telescopes, and they discovered new planets and moons.\n\nOur Galaxy and the Universe\nWhen Galileo looked at a bright area in the night sky, he discovered that it was made of many stars. Later, people discovered that this is the center of our galaxy, the Milky Way. For a long time, astronomers thought that the Milky Way was the only galaxy in the universe. Then in 1930, an American astronomer called Edwin Hubble discovered another galaxy. Now we know that there are billions of galaxies in the universe.",
            "chi": "伽利略與第一批望遠鏡\n望遠鏡幫助人們了解我們的太陽系。1609 年，伽利略使用了最早的望遠鏡之一來觀察夜空。他看見了月球上的山脈和隕石坑，以及木星周圍的四顆衛星。最早的望遠鏡非常小。後來，人們製造了更大的望遠鏡，並發現了新的行星和衛星。\n\n我們的星系與宇宙\n當伽利略觀察夜空中一片明亮的區域時，他發現那是由許多恆星組成的。後來人們發現這就是我們星系——銀河系（the Milky Way）的中心。在很長一段時間裡，天文學家以為銀河系是宇宙中唯一的星系。直到 1930 年，一位名叫愛德溫·哈伯（Edwin Hubble）的美國天文學家發現了另一個星系。現在我們知道宇宙中有數十億個星系！",
            "key_sentences": [
                {
                    "sentence": "Then in 1930, an American astronomer called Edwin Hubble discovered another galaxy. Now we know that there are billions of galaxies in the universe.",
                    "tag": "🔥 課本是非題兩大陷阱",
                    "note": "陷阱 1：銀河系 (Milky Way) 是由無數恆星 (stars) 組成，不是 comets！陷阱 2：哈伯在 1930 年發現的是另一個『星系 (galaxy)』，不是另一個宇宙 (universe)！"
                }
            ]
        },
        {
            "sequence": 4,
            "section_title": "📖 課本全文第 4 節 (p.23)：Astronomy Today — Radio Waves, X-rays, Spacecraft & Hubble",
            "eng": "Astronomy Today\nToday, astronomers use huge telescopes to study the stars. They can see the light from galaxies billions of kilometers from Earth. Astronomers use different telescopes to look for other types of energy from stars, called radio waves and X-rays. Astronomers also use spacecraft to explore our solar system. Spacecraft orbit or fly past other planets and take photos. Some spacecraft have visited other planets and moons, too.\n\n[Discover! Box]\nThe Hubble Space Telescope has orbited Earth since 1990. It can take better photos than telescopes on Earth because it's outside Earth's atmosphere.",
            "chi": "今日天文學（Astronomy Today）\n今天，天文學家使用巨型望遠鏡來研究恆星。他們能看見來自距離地球數十億公里遠的星系光芒。天文學家使用不同的望遠鏡來尋找來自恆星的其他類型能量，稱為無線電波（radio waves）和 X 光（X-rays）。天文學家也使用太空船（spacecraft）來探索我們的太陽系。太空船繞行或飛越其他行星並拍攝照片。有些太空船甚至已經造訪了其他行星和衛星。\n\n【探索專欄 Discover!：哈伯太空望遠鏡】\n哈伯太空望遠鏡自 1990 年以來一直繞著地球運行。它能拍出比地球上的望遠鏡更清晰的照片，因為它位於地球大氣層之外。",
            "key_sentences": [
                {
                    "sentence": "The Hubble Space Telescope has orbited Earth since 1990. It can take better photos than telescopes on Earth because it's outside Earth's atmosphere.",
                    "tag": "🔥 哈伯望遠鏡高解析度原因",
                    "note": "哈伯自 1990 年升空，拍照更清晰是因為位於『地球大氣層之外 (outside Earth's atmosphere)』，不受大氣干擾！"
                }
            ]
        }
    ],
    "tea_midterm_1": [
        {
            "sequence": 1,
            "section_title": "📖 岱崙小考 Discover 3 U13 主題精讀：Simple Machines in Our Daily Lives (簡單機械與發明)",
            "eng": "Simple machines are inventions that make our work easier. A lever, a ramp, a wedge, a screw, and a wheel and axle are all simple machines! On the playground, a seesaw is a kind of lever, and a slide is a kind of ramp. A wheelchair uses a ramp to go up into a building easily, because a hill or staircase is too steep.\nIn the kitchen and workshop, we use wedges and screws every day. The blade of an axe or a sharp knife is a wedge that helps us cut wood or food. A jar lid is actually a giant screw that holds food tightly inside a jar, and a doorknob is a wheel and axle that helps us open doors! Modern machines like bicycles and cars use many simple machines together.",
            "chi": "簡單機械是能讓我們的工作變得更輕鬆的發明。槓桿（lever）、斜坡道（ramp）、楔子（wedge）、螺絲（screw）以及輪軸（wheel and axle）全都是簡單機械！在遊樂場裡，蹺蹺板（seesaw）是一種槓桿，而溜滑梯（slide）則是一種斜坡。輪椅（wheelchair）利用斜坡道輕鬆進入建築物，因為山丘（hill）或樓梯太陡峭（steep）了。\n在廚房和工作坊裡，我們每天都使用楔子和螺絲。斧頭（axe）或鋒利小刀（knife）的刀刃就是幫助我們劈木頭或切食物的楔子。果醬罐蓋（jar lid）其實是一個把食物緊緊鎖在罐子裡的大螺絲，而門把（doorknob）則是幫助我們開門的輪軸！像腳踏車（bicycle）和汽車這樣的現代機器（modern machines）結合運用了許多簡單機械。",
            "key_sentences": [
                {
                    "sentence": "A lever, a ramp, a wedge, a screw, and a wheel and axle are all simple machines!",
                    "tag": "🔥 岱崙 W2 聽寫 20 單字核心句",
                    "note": "特別注意 Rex 曾拼錯的 4 個字：wedge（❌wadge）、knife（❌Knif 漏 e）、mountain（❌mountion）、wheelchair（❌whillchair）。"
                }
            ]
        },
        {
            "sequence": 2,
            "section_title": "📖 岱崙小考 Discover 3 U14 主題精讀：The Glassblower's Workshop & Eyeglasses (吹玻璃與眼鏡鏡框)",
            "eng": "Inside a hot workshop, a glassblower melts sand and glass inside a giant furnace. When the glass is very hot and soft, the glassblower shapes it into beautiful glassware, such as a delicate flower vase or a water pitcher.\nGlass is also used to make lenses for eyeglasses! Opticians put the glass lenses into metal or plastic frames so people can wear eyeglasses on their faces and see clearly. In the workshop, workers also use tools like a heavy hammer and thin metal wire to fix frames and machines.",
            "chi": "在炎熱的工作坊（workshop）裡，吹玻璃工匠（glassblower）在巨大的熔爐（furnace）中融化沙子與玻璃。當玻璃變得非常高溫且柔軟時，工匠將它塑造成精美的玻璃器皿（glassware），像是精緻的花瓶（vase）或水壺（pitcher）。\n玻璃也被用來製作眼鏡（eyeglasses）的鏡片！驗光師把玻璃鏡片裝進金屬或塑膠鏡框（frames）裡，讓人們可以把眼鏡戴在臉上看清楚東西。在工作坊裡，工人們也會使用沉重的鐵鎚（hammer）和細金屬鐵絲（wire）等工具來修理鏡框與機器。",
            "key_sentences": [
                {
                    "sentence": "Inside a hot workshop, a glassblower melts glass inside a giant furnace.",
                    "tag": "🔥 岱崙 W4 聽寫失分字 furnace",
                    "note": "熔爐是 furnace（字尾 -ace 發 /ɪs/ 音，Rex 曾誤拼為 furnes ❌）。"
                },
                {
                    "sentence": "Opticians put the glass lenses into metal or plastic frames so people can wear eyeglasses",
                    "tag": "🔥 岱崙 W4 聽寫失分字 frames",
                    "note": "眼鏡鏡框是 frames /freɪmz/（Rex 曾誤寫成法國 France ❌）。"
                }
            ]
        },
        {
            "sequence": 3,
            "section_title": "📖 岱崙小考高分作文範本 (W2 & W5 實戰 15/16 分)：Michelle's Neighborhood & If I Had 6000 Dollars",
            "eng": "[Week 2 Writing: Michelle's Neighborhood]\nHave you ever been to my neighborhood? I have lived in my neighborhood for four years. It is very close to my school. I can get to school in under ten minutes on foot. The convenience store and the bus stop are very close, too. There are many stores in my neighborhood. Across the street from the coffee shop, there is a stationery store and a pharmacy. Best of all, my neighborhood has a park, and my friends and I often play and ride our bikes there. I really like living in my neighborhood!\n\n[Week 5 Writing: If I Had 6000 Dollars]\nIf I had 6000 dollars, I would do three things. First, I love fair rides, so I would go to an amusement park with my friends. Next, I would share some of the money with my sister. I think it is important to share money with your family. Finally, I would spend some money on myself. A new jacket would cost me about 750 dollars. With the rest of the money, I would treat my friends to a movie. Wouldn't it be great to have 6000 dollars?",
            "chi": "【Week 2 寫作真題：Michelle 的社區】\n你曾經來過我的社區嗎？我已經在我的社區住了四年了。它離我的學校非常近。我走路不到十分鐘就能到學校。便利商店和公車站也非常近。我的社區裡有許多商店。在咖啡店的對街，有一家文具店和一家藥局。最棒的是，我的社區有一座公園，我和朋友們常在那裡玩耍並騎腳踏車。我真的很喜歡住在我的社區裡！\n\n【Week 5 寫作真題：如果我有 6000 美元】\n如果我有 6000 美元，我會做三件事。首先，我熱愛遊樂設施，所以我會和朋友們一起去遊樂園。接下來，我會把一部分的錢分享給我妹妹。我認為與家人分享金錢是很重要的。最後，我會花一些錢在自己身上。一件新夾克大約會花費我 750 美元。用剩下的錢，我會請朋友們看一場電影。擁有 6000 美元難道不是很棒嗎？",
            "key_sentences": [
                {
                    "sentence": "The convenience store and the bus stop are very close, too.",
                    "tag": "⚠️ W2 作文唯一扣分點",
                    "note": "very 後面必接原級 close（不可寫 closer）！"
                },
                {
                    "sentence": "A new jacket would cost me about 750 dollars. With the rest of the money, I would treat my friends to a movie.",
                    "tag": "⭐ W5 作文滿分亮點句",
                    "note": "精準運用『物 + would cost + 人 + 金錢』與『With the rest of the money, I would treat + 人 + to + 物』！"
                }
            ]
        }
    ]
}


# ==============================================================================
# 2. 為缺少單字卡的 5 個期中考單元補齊「Tiger 7 大錨點記憶單字卡」
# ==============================================================================
def make_vocab(vid, book_id, unit_id, word, pos, chi, breakdown, trick, scene, collocation, img, context_eng, context_chi, chant, compare):
    return {
        "id": vid,
        "book_id": book_id,
        "unit_id": unit_id,
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
    }


NEW_MIDTERM_VOCAB = [
    # ---------------- RWW6 Unit 5: Lost and Found (rw6_5) ----------------
    make_vocab("voc_m501", "rw6", "rw6_5", "turned right", "動詞片語 (Phrase)｜原形 turn right", "右轉",
               "turn (轉動/轉彎) + right (右邊)。考卷聽寫常考過去式 turned right。",
               "諧音「吞ไร」。聯想：吞一口飯往「右轉」。注意過去式 turn 要加 -ed！",
               "走到森林步道岔路口，看著木牌箭頭往右手邊轉過去。",
               "搭配: turn right at the corner (在轉角右轉)｜反義: turn left (左轉)", "↪️",
               "There's a place we should have turned right, but we went straight.",
               "有一個地方我們本來應該右轉，但我們卻直走了。",
               "路口看清再轉彎，turned right 往右不迷路！",
               "turn right (右轉-動作) vs. on the right (在右邊-位置)。"),
    make_vocab("voc_m502", "rw6", "rw6_5", "went straight", "動詞片語 (Phrase)｜原形 go straight", "直走",
               "went (go 的過去式) + straight (筆直地，gh 不發音)。",
               "straight 諧音「死墜特」：筆直往下墜！gh 完全不發音但拼字絕不能漏！",
               "在迷霧森林中沒有轉彎，沿著步道一直往前直直走。",
               "搭配: go straight for two blocks (直走兩個街區)｜同義: walk straight ahead", "⬆️",
               "We should have turned right, but I think we went straight.",
               "我們本來應該右轉，但我想我們卻直走了。",
               "gh 隱形不發音，went straight 筆直往前行！",
               "straight (筆直地/直的) vs. strange (奇怪的)。"),
    make_vocab("voc_m503", "rw6", "rw6_5", "on the left", "介系詞片語 (Prep. Phrase)", "在左邊 / 在左側",
               "on (在...接觸面上) + the + left (左邊)。固定使用介系詞 on！",
               "口訣：「左邊右邊貼著路，介系詞用 on 記清楚！」(on the left / on the right)。",
               "步道左手邊草地上擺著一張長長的木頭長凳 (log bench)。",
               "完整片語: on the left side of the trail (在步道左側)｜反義: on the right", "⬅️",
               "She pointed to a log bench on the left side of the trail.",
               "她指著步道左側的一張原木長凳。",
               "左邊右邊用 on 牽，on the left 在左手邊！",
               "on the left (在左邊-靜態位置) vs. turn left (左轉-動態轉向，不加 the)。"),
    make_vocab("voc_m504", "rw6", "rw6_5", "next to", "介系詞片語 (Prep. Phrase)", "在...旁邊 / 緊鄰著",
               "next (下一個/緊接著) + to (指向) -> 緊挨在旁邊。",
               "注意 next 字尾有 t，後面再接 to，連音時不要漏掉 t！",
               "長凳上，弟弟緊挨著姊姊坐在一起休息。",
               "同義詞: beside, by｜搭配: sit next to my sister (坐在我姊姊旁邊)", "👯",
               "Jaya realized they were next to a different, smaller hill.",
               "佳雅意識到他們正位於另一座較小的山丘旁邊。",
               "Next 加 to 肩並肩，就在旁邊最親密！",
               "next to (緊鄰在旁) vs. near (在附近，不一定緊貼)。"),
    make_vocab("voc_m505", "rw6", "rw6_5", "go back", "動詞片語 (Phrase)", "折返 / 回去",
               "go (走) + back (後面/返回) -> 往回走、折返原路。",
               "發現走錯路時，先別急著 go back (回頭)，可以先爬上高處看地圖！",
               "在迷霧步道中停下腳步，討論要不要沿著原路回頭下山。",
               "搭配: go back down the trail (沿步道折返下山), go back home (回家)", "🔙",
               "Before we go back down the trail, we should hike up the hill!",
               "在我們沿著步道折返下山前，我們應該爬上山丘看看！",
               "迷路別急 go back，登高望遠找對策！",
               "go back (回去那裡) vs. come back (回來這裡)。"),
    make_vocab("voc_m506", "rw6", "rw6_5", "up the hill", "介系詞片語 (Prep. Phrase)", "往山丘上 / 上山",
               "up (往上) + the hill (山丘)。下山則是 down the hill。",
               "hike up the hill 爬上山丘，山頂就能高過濃霧 (above the fog)！",
               "一家人邁開步伐往小山丘頂端爬上去，頭頂露出燦爛陽光。",
               "搭配: hike up the hill (健行上山), walk up the hill｜反義: down the hill", "⛰️",
               "We should hike up the hill and take a look around!",
               "我們應該爬上山丘並四處看看！",
               "Up the hill 往上爬，衝破迷霧見太陽！",
               "hill (山丘/小山) vs. mountain (高大山脈)。"),
    make_vocab("voc_m507", "rw6", "rw6_5", "read a map", "動詞片語 (Phrase)", "看地圖 / 判讀地圖",
               "read (閱讀/判讀) + a map (一張地圖)。英文「看地圖」必用動詞 read，不用 look！",
               "地圖上有文字、符號與方位，需要像讀書一樣「判讀」，所以用 read a map！",
               "站在山頂上攤開摺疊地圖，手指著南方的燈塔標記。",
               "搭配: know how to read a map (懂得如何看地圖), use a compass with a map", "🗺️",
               "We know how to read a map, so let's look.",
               "我們懂得如何看地圖，所以我們來看看吧。",
               "看書看報看地圖，英文通通用 read！",
               "read a map (看懂/判讀地圖) vs. look at the map (視線看向地圖)。"),
    make_vocab("voc_m508", "rw6", "rw6_5", "between", "介系詞 (Prep.)", "在...（兩者）之間",
               "be- (by) + twain (古英語 two 兩個) -> 夾在「兩個」事物中間！",
               "看到字根裡的 tw- 就想到 two (二)！夾在 A 和 B 兩個中間必用 between A and B！",
               "媽媽坐在長凳正中間，左邊是我、右邊是姊姊。",
               "必考公式: between A and B (在 A 與 B 之間)｜例: between Mars and Jupiter", "↔️",
               "We're on a hill between the lighthouse and our usual picnic spot.",
               "我們所在的山丘介於燈塔與我們平常野餐地點之間。",
               "tw 代表兩個人，between 夾在兩者間！",
               "between (兩者之間) vs. among (三者以上之中)。"),
    make_vocab("voc_m509", "rw6", "rw6_5", "compass", "名詞 (Noun)", "指北針 / 羅盤",
               "com- (together 共同) + pass (步伐/範圍) -> 丈量四方步距的羅盤。",
               "諧音「看帕斯」。看一眼指北針就能 pass (通過) 迷霧森林！注意字尾雙 s (ss)！",
               "手掌心托著一個圓形銅製指北針，紅色磁針穩穩指著 N (北方)。",
               "搭配: use a compass to tell direction (用指北針辨別方向)", "🧭",
               "A compass is an instrument you use to tell direction.",
               "指北針是一種你用來辨別方向的儀器。",
               "看準北方再出發，compass 字尾兩個 s！",
               "compass (指北針/圓規) vs. camp (露營)。"),
    make_vocab("voc_m510", "rw6", "rw6_5", "foggy", "形容詞 (Adj.)", "有霧的 / 濃霧瀰漫的",
               "fog (名詞：霧) + 重複字尾 g + y (形容詞字尾) -> foggy。",
               "短母音 o + 單子音 g，變形容詞時必須「雙寫 g 再加 y」(fog -> foggy)，就像 sun -> sunny！",
               "清晨森林裡白茫茫一片，連十公尺外的大樹都看不清楚。",
               "詞族: fog (名詞：霧)｜搭配: one foggy morning (一個起霧的早晨)", "🌫️",
               "Jaya and her family went hiking one foggy morning.",
               "佳雅和她的家人於一個起霧的早晨去健行。",
               "f-o-g 霧茫茫，雙寫 g 加 y 變 foggy！",
               "foggy (形容詞：有霧的) vs. fog (名詞：霧)。"),
    make_vocab("voc_m511", "rw6", "rw6_5", "crooked", "形容詞 (Adj.)", "彎曲的 / 歪斜的",
               "crook (彎鉤) + -ed (形容詞化，發 /ɪd/ 音) -> 彎曲變形的。",
               "諧音「酷客的」。酷客種在山頂的樹長得「彎彎曲曲的 (crooked)」！",
               "山頂上佇立著一棵樹幹奇特彎曲的老樹，像在雲海中招手。",
               "反義詞: straight (筆直的)｜搭配: a tall, crooked tree (一棵高大彎曲的樹)", "🌳",
               "Their goal was a hill with a tall, crooked tree on top.",
               "他們的目標是一座山頂上有一棵高大彎曲樹木的山丘。",
               "crooked 樹幹彎又歪，straight 筆直站一排！",
               "crooked (彎曲的) vs. straight (筆直的)。"),
    make_vocab("voc_m512", "rw6", "rw6_5", "lighthouse", "名詞 (Noun)", "燈塔",
               "light (光/燈) + house (房子/塔樓) -> 發光指引船隻的高塔。",
               "複合字超好記：light (光) + house (屋) = 燈塔！",
               "海邊懸崖上紅白相間的高塔，在濃霧中射出耀眼光束並鳴響霧角。",
               "搭配: the lighthouse near town (城鎮附近的燈塔)", "🚨",
               "A lighthouse is a tall tower built on the coast.",
               "燈塔是建造在海岸邊的高塔。",
               "Light 加 house 不分家，海岸高聳大燈塔！",
               "lighthouse (燈塔) vs. greenhouse (溫室)。"),

    # ---------------- RWW6 Unit 6: The World of Orienteering (rw6_6) ----------------
    make_vocab("voc_m601", "rw6", "rw6_6", "orienteering", "名詞 (Noun)", "定向越野運動",
               "orient (東方/確定方向) + -eer (從事...的人/活動) + -ing -> 結合地圖與指北針的野外尋標運動。",
               "拆成 5 個音節記：o-ri-en-teer-ing！中間有 orient (方向)，後面有雙 e 的 teer + ing！",
               "選手拿著地圖與指北針在森林裡奔跑，尋找樹後的紅白三角旗打卡。",
               "搭配: the sport of orienteering (定向越野運動)｜岱崙 W5 聽寫必考大字！", "🏃",
               "In the sport of orienteering, racers use a map and compass to find stations.",
               "在定向越野運動中，參賽者使用地圖和指北針尋找站點。",
               "o-ri-en-teer-ing，森林尋寶我最行！",
               "orienteering (定向越野) vs. engineering (工程學)。"),
    make_vocab("voc_m602", "rw6", "rw6_6", "controls", "名詞 (Noun, 複數)", "（定向越野的）控制點 / 打卡站",
               "con- (共同) + trol (滾動/檢核卷軸) -> 比賽中用來檢核選手是否到訪的「控制站點」。",
               "平常 control 是「控制」，但在定向越野專指「必找的打卡控制點 (stations)」！",
               "大樹後方掛著紅白相間的三角旗，旁邊有打孔器讓選手在卡片上打卡。",
               "課本定義: stations, which are called controls｜搭配: find all the controls to win", "🚩",
               "Racers use a map and compass to find stations, which are called controls.",
               "參賽者使用地圖和指北針尋找稱為「控制點」的站點。",
               "紅白旗幟藏樹後，找到 controls 打卡走！",
               "control card (控制打卡計分卡) vs. control flag (控制點標誌旗)。"),
    make_vocab("voc_m603", "rw6", "rw6_6", "in front of", "介系詞片語 (Prep. Phrase)", "在...（外部）正前方",
               "in + front (正面/前部) + of -> 三個獨立單字組成的方位介系詞！",
               "⚠️ 岱崙 W4 小考真實失分王！Rex 曾寫成『infront off ❌』！切記：① in 與 front 中間要空格；② 最後是單 f 的 of！",
               "定向越野的控制旗藏在一塊巨大岩石的正前方。",
               "反義詞: behind (在...後面)｜搭配: in front of a big rock (在巨石前面)", "🪨",
               "They may be in front of a big rock or behind a tree.",
               "它們可能位於巨石前方或大樹後面。",
               "in、front、of 三個字，單 f 的 of 別寫錯！",
               "in front of (在物體外部前方) vs. in the front of (在車廂/教室內部前排)。"),
    make_vocab("voc_m604", "rw6", "rw6_6", "behind", "介系詞 (Prep.)", "在...後面",
               "be- (在) + hind (後方的) -> 藏在某物的背後。",
               "諧音「比害羞」。因為比別人害羞，所以躲在大樹「後面 (behind)」！",
               "紅白相間的控制點旗幟被巧妙地掛在大樹幹正後方，從正面看不到。",
               "反義詞: in front of (在...前面)｜搭配: behind a tree (在樹後面)", "🌲",
               "Controls may be in front of a big rock or behind a tree.",
               "控制點可能位於巨石前方或大樹後面。",
               "害羞躲在樹後面，behind 與 in front of 相對面！",
               "behind (在...後面-位置) vs. go back (往回走-動作)。"),
    make_vocab("voc_m605", "rw6", "rw6_6", "corner", "名詞 (Noun)", "街角 / 轉角 / 角落",
               "源自拉丁文 cornu (角/號角) + -er -> 兩條街道交會形成的角 (a place where two roads meet)。",
               "諧音「摳呢」。站在「街角 (corner)」摳著腦袋問路人商店怎麼走。",
               "站在十字路口的紅綠燈轉角處，向路人詢問書店方向。",
               "課本英英定義: a place where two roads meet｜搭配: standing on a corner (站在街角)", "📐",
               "Standing on a corner, you ask someone how to get to a store.",
               "站在街角，你向某人詢問如何前往一家商店。",
               "兩條馬路交會處，站在 corner 問問路！",
               "on a corner (在戶外街角) vs. around the corner (即將到來/在轉角處)。"),
    make_vocab("voc_m606", "rw6", "rw6_6", "go two blocks", "動詞片語 (Phrase)", "走兩個街區",
               "go (走) + two blocks (兩個街區，超過一個街區 block 必加 s)。",
               "課本英英定義題：『Go two blocks』means『move this far (移動這麼遠的距離)』！",
               "沿著城市棋盤狀街道，經過兩個路口街區再左轉。",
               "延伸搭配: go two blocks north (往北走兩個街區), two blocks from my house", "🏙️",
               "They tell you to \"go two blocks north, turn left.\"",
               "他們告訴你：「往北走兩個街區，然後左轉。」",
               "城市指路算街區，go two blocks 記心裡！",
               "block (名詞：街區/積木；動詞：阻擋)。"),
    make_vocab("voc_m607", "rw6", "rw6_6", "across from", "介系詞片語 (Prep. Phrase)", "在...對面 / 在...對街",
               "across (橫越到對面) + from (從...算起) -> 在馬路或空間的正對面。",
               "課本英英定義：『across the street from』means『on the other side (在另一側/對面)』！",
               "站在馬路這一側，正對面就是那家書店與公園。",
               "同義片語: across the street from｜搭配: live across from the park (住在公園對面)", "🛣️",
               "You'll be across the street from the bookstore.",
               "你就會在書店的對街（對面）。",
               "隔著馬路看對面，across from 最常見！",
               "across from (介系詞：在...對面) vs. cross the street (動詞：過馬路)。"),
    make_vocab("voc_m608", "rw6", "rw6_6", "cross the street", "動詞片語 (Phrase)", "過馬路 / 穿越街道",
               "cross (動詞：穿越/橫渡) + the street (街道)。",
               "課本英英定義：『cross the street』means『go to the other side (走到對面去)』！",
               "在城市賽跑中，選手邁開大步穿越斑馬線跑到馬路對面的終點線。",
               "注意詞性：cross 是動詞（過馬路），across 是介系詞（在對面）！", "🚶",
               "In a race in a city, you might only need to cross the street to get to the finish line.",
               "在城市裡的比賽，你計算也許只需要過馬路就能抵達終點線。",
               "動詞穿越用 cross，介系詞對面用 across！",
               "cross the street (= go across the street)。"),
    make_vocab("voc_m609", "rw6", "rw6_6", "along a river", "介系詞片語 (Prep. Phrase)", "沿著一條河",
               "along (順著長條形物體的邊緣往前) + a river (河流)。",
               "a + long (長長的) -> 順著「長長的」河岸或步道一路跑就是 along！",
               "定向越野選手順著蜿蜒的溪流岸邊一路往前奔跑。",
               "搭配: run along a river (沿著河邊跑), walk along the street (沿著街走)", "🏞️",
               "In orienteering, you will likely run along a river, climb over rocks, and go up and down hills.",
               "在定向越野中，你很可能會沿著河邊奔跑、爬過岩石，並在山丘間上下穿梭。",
               "順著長河岸邊跑，along a river 記得好！",
               "along (沿著邊緣線條) vs. across (橫越到對岸)。"),
    make_vocab("voc_m610", "rw6", "rw6_6", "visual", "名詞 / 形容詞 (N. / Adj.)", "視覺圖表（圖片、圖解、地圖） / 視覺的",
               "源自拉丁文 videre (to see 看見) + -ual -> 看得見的視覺輔助圖表。",
               "跟 video (影片)、vision (視力) 同字根！課本閱讀目標：Use visuals (善用視覺圖表獲取正文中沒寫出的資訊)！",
               "閱讀課文時，旁邊附上的「圖 1 控制旗照片」與「圖 2 18格打卡表」就是 visuals。",
               "包含: pictures (圖片), diagrams (圖解), maps (地圖)", "📊",
               "Visuals provide information that is not in a text.",
               "視覺圖表提供正文中沒有寫出的補充資訊。",
               "看文別忘看圖表，visuals 藏著得分寶！",
               "visual (視覺圖表) vs. text (純文字正文)。"),

    # ---------------- RWW6 Unit 7: Languages We Use (rw6_7) ----------------
    make_vocab("voc_m701", "rw6", "rw6_7", "native speaker", "名詞片語 (Noun Phrase)", "母語使用者",
               "native (天生的/本土的，源自拉丁文 nasci 出生) + speaker (說話者)。",
               "從一出生 (native) 在家裡跟爸媽學的第一種語言，你就是它的 native speaker！",
               "小嬰兒在家裡聽著爸媽說話，自然而然學會的第一種母語。",
               "課本定義: the first language you learned and speak at home", "🗣️",
               "Everyone is a native speaker of their first language.",
               "每個人都是自己第一語言的母語使用者。",
               "在家從小開口說，native speaker 就是我！",
               "native language (母語-在家學) vs. official language (官方語言-政府立法、學校學)。"),
    make_vocab("voc_m702", "rw6", "rw6_7", "official language", "名詞片語 (Noun Phrase)", "官方語言",
               "official (官方的/正式的，源自 office 公務機關) + language (語言)。",
               "有 office (政府辦公室) 在裡面！政府公務機關透過立法 (pass a law) 指定的語言就是 official language！",
               "國會大樓裡通過法律，正式宣布全國學校與政府機關使用的法定語言。",
               "課本定義: the language used by the government of a country", "🏛️",
               "An official language is the one used by the government of a country.",
               "官方語言是一國政府所使用的語言。",
               "政府立法學校教，official language 很重要！",
               "注意：墨西哥與美國雖然普遍說西語/英語，但因未立法，皆無 official language！"),
    make_vocab("voc_m703", "rw6", "rw6_7", "pass a law", "動詞片語 (Phrase)", "通過法律 / 立法",
               "pass (通過/表決通過) + a law (一項法律)。",
               "國家想要擁有官方語言，不能只靠大家常講，必須在國會「pass a law (通過法律)」才算數！",
               "法官與議員敲下木槌，正式通過一項國家語言法案。",
               "過去式: passed a law｜否定: never passed a law", "⚖️",
               "A country has to pass a law to make a language official.",
               "一個國家必須通過法律，才能使一種語言成為官方語言。",
               "若要語言變官方，pass a law 立法不能忘！",
               "law (法律) vs. low (低的)。"),
    make_vocab("voc_m704", "rw6", "rw6_7", "bar graph", "名詞片語 (Noun Phrase)", "長條圖",
               "bar (長條/橫木) + graph (圖表，字根寫/畫) -> 用長方形色條比較數量的統計圖。",
               "長得像一條一條巧克力棒 (bar) 的統計圖表，就是 bar graph！",
               "課本第 51 頁用藍、橘、黃、粉、紫五條橫向長條，比較全球 196 國的官方語言數量。",
               "課本定義: A bar graph uses rectangles to show how much or how many.", "📊",
               "A bar graph compares two or more things.",
               "長條圖用來比較兩個或更多的事物。",
               "長方色條比多少，bar graph 數據一目了然！",
               "bar graph (長條圖) vs. pie chart (圓餅圖) vs. line graph (折線圖)。"),
    make_vocab("voc_m705", "rw6", "rw6_7", "sign language", "名詞片語 (Noun Phrase)", "手語",
               "sign (手勢/符號/標誌) + language (語言)。注意 sign 的 g 不發音 /saɪn/！",
               "用手勢訊號 (signals) 與臉部表情來交談的語言，就是 sign language！",
               "把手放在下巴再往外移，在美國手語 (ASL) 中同時代表「謝謝」與「不客氣」。",
               "搭配: American Sign Language (美國手語), use hands to make signals", "🤟",
               "People who can't hear or speak use special languages called sign languages.",
               "聽不見或無法說話的人使用稱為手語的特殊語言。",
               "Sign 的 g 不發音，比出訊號傳真心！",
               "sign (手勢/標誌，g不發音) vs. signal (訊號，g要發音 /ˈsɪɡnəl/)。"),
    make_vocab("voc_m706", "rw6", "rw6_7", "Mandarin", "專有名詞 (Proper Noun)", "華語 / 普通話 / 國語",
               "源自梵語 mantrin (官員)，指中文裡全國通用的標準官方話（華語）。",
               "諧音「慢得林」。中國有超過百種方言，但大家彼此溝通都講 Mandarin！首字母必大寫！",
               "來自不同省份的人們聚在一起，用標準華語流利地交談。",
               "搭配: speak Mandarin (說華語)", "🇨🇳",
               "Most people just use one Chinese language to talk with each other. It's called Mandarin.",
               "大多數人只使用一種中文來彼此交談，稱為華語。",
               "中國方言上百種，通用 Mandarin 最暢通！",
               "Mandarin (大寫：華語) vs. mandarin (小寫：柑橘)。"),
    make_vocab("voc_m707", "rw6", "rw6_7", "Hindi", "專有名詞 (Proper Noun)", "印地語（印度主要母語與官方語言之一）",
               "源自波斯語 Hind (印度河流域) -> 印度北部屋與全國最廣泛的本土語言。",
               "看到 Hind- 就想到 India (印度)！印度的兩大官方語言就是 Hindi 和 English！",
               "在印度新德里的街道與學校裡，標示牌同時印著印地語與英語。",
               "必考事實: Hindi and English are the two official languages of India.", "🇮🇳",
               "Many people in India speak Hindi. But Hindi and English are the two official languages of India.",
               "許多印度人說印地語。而印地語和英語是印度的兩種官方語言。",
               "印度母語上千種，Hindi、English 官方用！",
               "India (國家：印度) vs. Indian (印度人/印度的) vs. Hindi (語言：印地語)。"),
    make_vocab("voc_m708", "rw6", "rw6_7", "government", "名詞 (Noun)", "政府",
               "govern (統治/管理) + -ment (名詞字尾) -> 治理國家的政府機構。",
               "注意中間有個 n (gover-n-ment)！千萬不要漏寫中間的 n！",
               "首都的國會與行政大樓，官員們使用官方語言處理國家大事。",
               "搭配: used by the government of a country (由一國政府所使用)", "🏢",
               "An official language is the one used by the government of a country.",
               "官方語言是一國政府所使用的語言。",
               "govern 加 ment 管國家，中間 n 字別漏啦！",
               "govern (動詞：治理) vs. government (名詞：政府)。"),

    # ---------------- RWW6 Unit 8: So Many Questions (rw6_8) ----------------
    make_vocab("voc_m801", "rw6", "rw6_8", "bilingual", "形容詞 / 名詞 (Adj. / N.)", "雙語的 / 通曉兩種語言的人",
               "字首 bi- (two 兩個，如 bicycle 兩輪腳踏車) + lingu (拉丁文 lingua 舌頭/語言) + -al -> 會說兩種語言的！",
               "課本 p.57 必考英英定義：『bilingual』means『speaking two languages (說兩種語言)』！",
               "Erico 的父母既會說葡萄牙語、又會說英語，在家雙語切換自如。",
               "字首延伸: bicycle (雙輪車), monolingual (單語的), trilingual (三語的)", "🗣️",
               "Do they speak Portuguese and English? Are they bilingual?",
               "他們說葡萄牙語和英語嗎？他們是雙語人士嗎？",
               "bi 代表數字二，bilingual 雙語頂呱呱！",
               "bilingual (雙語的) vs. native speaker (母語者)。"),
    make_vocab("voc_m802", "rw6", "rw6_8", "accent", "名詞 (Noun)", "腔調 / 口音",
               "ac- (to) + cent (拉丁文 cantus 唱歌/語調) -> 說話時獨特的發音腔調。",
               "課本 p.57 必考英英定義：『accent』means『a way to pronounce words (發音單字的方式)』！",
               "Erico 雖然有葡萄牙名字、家人來自澳洲，但開口講英文卻是標準的英國腔 (British accent)！",
               "搭配: have a British accent (有英國腔), Australian accent (澳洲腔)", "🎙️",
               "You sound like you have a British accent, but you have an Italian name.",
               "你聽起來有英國腔調，但你卻有個義大利名字。",
               "說話發音有腔調，accent 就是 pronounce 的味道！",
               "accent (口音/腔調) vs. accept (接受) vs. accident (意外)。"),
    make_vocab("voc_m803", "rw6", "rw6_8", "prediction", "名詞 (Noun)", "預測 / 推測",
               "字首 pre- (before 預先) + dict (say 說，如 dictionary 字典) + -ion -> 在事情發生前「預先說出」結果！",
               "動詞是 predict (預測)，名詞是 prediction！課本閱讀目標：Make predictions (利用故事線索與背景知識預測情節)！",
               "看到 Rosa 抱著畫紙、畫筆與色鉛筆，我們立刻預測她要去上美術課 (art class)！",
               "搭配: make a prediction (做出預測)｜動詞: predict", "🔮",
               "A prediction is what you think will happen.",
               "預測就是你認為未來將會發生的事。",
               "pre 是預先 dict 是說，prediction 預測未來不錯過！",
               "prediction (未來預測，常含 will) vs. fact (已發生的既成事實)。"),
    make_vocab("voc_m804", "rw6", "rw6_8", "Portuguese", "專有名詞 / 形容詞 (N. / Adj.)", "葡萄牙語 / 葡萄牙的 / 葡萄牙人的",
               "Portugal (葡萄牙) + -ese (表示國家語言或人民的字尾，如 Chinese, Japanese)。",
               "注意不只有葡萄牙 (Portugal) 講 Portuguese，巴西 (Brazil) 的母語也是 Portuguese！",
               "Erico 的爸爸來自巴西、媽媽來自葡萄牙，所以他先學會了葡萄牙語，也幫助他更快學會義大利語。",
               "課本考點: Knowing Portuguese helped Erico learn some Italian.", "🇵🇹",
               "Yes, Portuguese did help me learn some Italian.",
               "是的，葡萄牙語確實幫助我學會了一些義大利語。",
               "葡萄牙與巴西人，都講 Portuguese 一家人！",
               "Portugal (國家：葡萄牙) vs. Portuguese (語言：葡萄牙語)。"),
    make_vocab("voc_m805", "rw6", "rw6_8", "Italian", "專有名詞 / 形容詞 (N. / Adj.)", "義大利語 / 義大利的 / 義大利人",
               "Italy (義大利) 去 y + -ian (國家語言/人民字尾，如 Australian, Canadian, Brazilian)。",
               "Rosa 在家說義大利語 (Italian)，所以開門看到名字像義大利人的 Erico 時，第一句話就用 Italian 問他！",
               "Rosa 在走廊門口用義大利語問 Erico 能不能幫她扶門。",
               "搭配: speak Italian at home (在家說義大利語), an Italian name", "🇮🇹",
               "\"Can you hold the door?\" the girl asked Erico in Italian.",
               "「你可以幫我扶著門嗎？」女孩用義大利語問艾里柯。",
               "Italy 去 y 加 ian，Italian 義大利語記心間！",
               "Italy (國家：義大利) vs. Italian (語言/人：義大利語/義大利人)。"),
    make_vocab("voc_m806", "rw6", "rw6_8", "supplies", "名詞 (Noun, 複數)", "用品 / 補給品 / 教材文具",
               "supply (單數：供給/用品) 去 y 變 i + es -> 各式各樣的必備用品。",
               "Rosa 懷裡抱著 drawing paper, paint brushes, colored pencils，這些統稱為 art supplies (美術用品)！",
               "Rosa 邊走邊問問題，懷裡抱著的一大堆美術用品不小心掉滿地。",
               "搭配: art supplies (美術用品), school supplies (學用品，WR3 U4 也考！)", "🎨",
               "The girl walked through, carrying a big pile of drawing paper and other supplies.",
               "女孩走了過去，手裡抱著一大疊圖畫紙和其他用品。",
               "去 y 變 i 加 es，school supplies 學用品全帶齊！",
               "supply (單數/動詞) vs. supplies (複數名詞：日常/美術/學校用品)。"),
    make_vocab("voc_m807", "rw6", "rw6_8", "interrupt", "動詞 (Verb)", "插話 / 打斷（談話）",
               "字首 inter- (between 在...中間) + 字根 rupt (break 打破/斷裂，如 erupt 火山爆發) -> 從講話中間切斷別人！",
               "Erico 才剛講到媽媽來自葡萄牙，好奇寶寶 Rosa 就忍不住「插話 (interrupted)」連問六個問題！",
               "別人話還沒講完，突然舉手喊「Oh!」打斷對方接著問問題。",
               "三態: interrupt, interrupted, interrupted", "✋",
               "\"Oh!\" Rosa interrupted. \"Do they speak Portuguese and English?\"",
               "「噢！」蘿莎插話道。「他們說葡萄牙語和英語嗎？」",
               "inter 中間 rupt 斷，interrupt 插話把話斷！",
               "interrupt (打斷談話) vs. reply (回答)。"),
    make_vocab("voc_m808", "rw6", "rw6_8", "pronounce", "動詞 (Verb)", "發音",
               "pro- (forth 向前) + nounce (喊出/宣布) -> 把字音清楚念出來。",
               "課本 p.57 用來定義 accent：『a way to pronounce words (把單字發音出來的方式)』！",
               "看著音標，張開嘴巴把每個音節準確念出來。",
               "名詞: pronunciation (發音，注意拼寫去掉 o 變 nun)｜搭配: pronounce words", "👄",
               "An accent means a way to pronounce words.",
               "腔調是指將單字發音出來的一種方式。",
               "pro 向前 nounce 念，pronounce 發音最標準！",
               "pronounce (動詞：發音) vs. pronunciation (名詞：發音)。"),

    # ---------------- 岱崙 3C 考卷真題必背單字 (tea_midterm_1: OD3 U13~U14) ----------------
    make_vocab("voc_tea01", "tea_midterm", "tea_midterm_1", "wedge", "名詞 (Noun)", "楔子 / 三角木（簡單機械）",
               "古英語 wecg -> 一端厚、一端薄呈三角形，用來劈開木頭或卡住門的簡單機械。",
               "⚠️ 岱崙 W2 考卷真實失分字！Rex 曾拼成『wadge ❌』！口訣：跟 edge (邊緣)、bed (床) 一樣，中間是短母音 e，絕對不是 a！",
               "工人用鐵鎚把一塊三角形木楔子 (wedge) 敲進大木頭縫隙裡，把木頭劈開。",
               "搭配: a wooden wedge (木楔子)｜同類機械: lever, ramp, screw, wheel and axle", "📐",
               "He hammered a wooden wedge into the log.",
               "他把一塊木楔子敲進原木裡。",
               "W-E-D-G-E，中間是 e 不是 a，三角楔子頂呱呱！",
               "wedge (楔子 - 母音 e) vs. ❌wadge (錯誤拼法)。"),
    make_vocab("voc_tea02", "tea_midterm", "tea_midterm_1", "knife", "名詞 (Noun)｜複數 knives", "小刀 / 餐刀",
               "古諾斯語 knifr -> 切東西的刀刃本身就是一種 wedge (楔子)。",
               "⚠️ 岱崙 W2 考卷真實失分字！Rex 曾寫成『Knif ❌』（首字母誤大寫且漏掉字尾不發音 e）！口訣：K 隱形不發音，字尾 e 幫 i 發長音 /aɪ/！",
               "廚房砧板上放著一把閃亮鋒利的水果小刀。",
               "複數變化: knife -> knives (去 fe 改 ves)｜搭配: a sharp knife", "🔪",
               "The blade of a knife is a kind of wedge.",
               "小刀的刀刃是一種楔子。",
               "k-n-i-f-e，字頭 k 靜音、字尾 e 必寫！",
               "knife (單數：一把小刀) vs. knives (複數：多把小刀)。"),
    make_vocab("voc_tea03", "tea_midterm", "tea_midterm_1", "mountain", "名詞 (Noun)", "高山 / 山脈",
               "源自拉丁文 mons (山) -> 法語 montaigne -> 英語 mountain。",
               "⚠️ 岱崙 W2 考卷真實失分字！Rex 曾拼成『mountion ❌』！口訣：山上有下「雨 (rain)」，所以字尾是 -tain (a-i-n)，絕對不是 -tion！",
               "遠方白雪皚皚的雄偉高山直插雲霄。",
               "同尾詞族: fountain (噴泉), captain (隊長), curtain (窗簾) 全部都是 -tain！", "🏔️",
               "Climbing a steep mountain takes a lot of energy.",
               "攀登陡峭的高山需要消耗大量體力。",
               "高山淋雨 rain，字尾必寫 t-a-i-n！",
               "mountain (高山 - 字尾 -tain) vs. hill (小山丘)。"),
    make_vocab("voc_tea04", "tea_midterm", "tea_midterm_1", "wheelchair", "名詞 (Noun)", "輪椅",
               "wheel (輪子) + chair (椅子) -> 裝有輪子的行動輔助椅。",
               "⚠️ 岱崙 W2 考卷真實失分字！Rex 曾寫成『whillchair ❌』！口訣：輪子 wheel 中間是兩個圓圓的車輪『e-e』，不是 i-l-l！",
               "無障礙斜坡道 (ramp) 幫助坐輪椅的人輕鬆進入大樓。",
               "拆字記憶: wheel (w-h-e-e-l) + chair (c-h-a-i-r)", "♿",
               "A ramp helps a person in a wheelchair enter a building.",
               "斜坡道幫助坐輪椅的人進入建築物。",
               "wheel 雙 e 像雙輪，加上 chair 變輪椅！",
               "wheel (輪子 - ee) vs. will (將會 / 意志 - ill)。"),
    make_vocab("voc_tea05", "tea_midterm", "tea_midterm_1", "furnace", "名詞 (Noun)", "熔爐 / 火爐",
               "源自拉丁文 fornax (高溫烤爐) -> 用來高溫熔化玻璃或金屬的封閉巨爐。",
               "⚠️ 岱崙 W4 考卷真實失分字！Rex 曾拼成『furnes ❌』！口訣：熔爐裡面熱得像「王宮 (palace)」的「表面 (surface)」，字尾是 -ace (a-c-e)！",
               "吹玻璃工坊裡，熊熊烈火在巨大的磚造熔爐裡把玻璃燒得通紅。",
               "同尾詞族: furnace (熔爐), surface (表面), palace (宮殿), necklace (項鍊) 全是 -ace！", "🔥",
               "A glassblower melts glass inside a giant furnace.",
               "吹玻璃工匠在巨大的熔爐裡熔化玻璃。",
               "fur 加 nace (n-a-c-e)，高溫熔爐記清楚！",
               "furnace (熔爐 - 字尾 -ace) vs. ❌furnes (錯誤拼法)。"),
    make_vocab("voc_tea06", "tea_midterm", "tea_midterm_1", "frames", "名詞 (Noun, 複數)", "（眼鏡的）鏡框 / 框架",
               "frame (框/結構) + s (一副眼鏡有左右兩個鏡框，常以複數 frames 出現)。",
               "⚠️ 岱崙 W4 考卷真實失分字！Rex 曾寫成『france ❌（法國）』！口訣：f-r-a-m-e-s 閉嘴音 /m/，不是法國 France 的 /n/！",
               "一雙配有輕巧金屬鏡框的近視眼鏡。",
               "搭配: eyeglasses with metal frames (金屬鏡框的眼鏡), picture frame (相框)", "👓",
               "He bought a pair of eyeglasses with metal frames.",
               "他買了一副金屬鏡框的眼鏡。",
               "f-r-a-m-e-s 是鏡框，別把鏡框寫成法國 France！",
               "frames (鏡框 /freɪmz/) vs. France (法國 /fræns/)。"),
    make_vocab("voc_tea07", "tea_midterm", "tea_midterm_1", "lever", "名詞 (Noun)", "槓桿（簡單機械）",
               "源自法語 lever (抬起/舉起) -> 用支點撬動重物的桿子。",
               "諧音「拉吧」。用力「拉吧 (lever)」，槓桿就能把大石頭撬起來！",
               "遊樂場的蹺蹺板 (seesaw) 就是生活中最常見的槓桿。",
               "搭配: pull the lever (拉動槓桿)｜例: A seesaw is a lever.", "⚖️",
               "A seesaw on the playground is a kind of lever.",
               "遊樂場裡的蹺蹺板是一種槓桿。",
               "L-E-V-E-R，支點撬動大石頭！",
               "lever (槓桿) vs. clever (聰明的) vs. never (從不) — 拼寫超像三兄弟！"),
    make_vocab("voc_tea08", "tea_midterm", "tea_midterm_1", "ramp", "名詞 (Noun)", "斜坡道 / 坡道（簡單機械）",
               "源自古法語 ramper (爬升/傾斜) -> 連接高低兩處的斜面坡道。",
               "諧音「軟坡」。推輪椅或搬重物走「斜坡道 (ramp)」比爬樓梯輕鬆多了！",
               "大樓門口無障礙通道的緩斜坡，以及遊樂場的溜滑梯 (slide)。",
               "搭配: go up a ramp (走上斜坡道)｜例: A slide is a kind of ramp.", "📐",
               "Workers used a wooden ramp to push heavy boxes onto the truck.",
               "工人們利用木製斜坡道把沉重的箱子推上卡車。",
               "R-A-M-P 斜坡道，推車上樓最省力！",
               "ramp (斜坡道) vs. lamp (檯燈) vs. camp (露營)。"),
    make_vocab("voc_tea09", "tea_midterm", "tea_midterm_1", "wheel and axle", "名詞片語 (Noun Phrase)", "輪軸（簡單機械）",
               "wheel (大輪子) + and + axle (中間穿過的轉軸 a-x-l-e)。",
               "注意軸心是 a-x-l-e (先 l 再 e)，不要跟斧頭 axe 搞混！",
               "轉動房間的圓形門把 (doorknob) 或踩腳踏車車輪，都是靠輪軸運作。",
               "考卷必考拼寫: wheel and axle (三個字全小寫)", "⚙️",
               "A doorknob is an example of a wheel and axle.",
               "門把就是輪軸的一個例子。",
               "大輪 wheel 配中軸 axle，轉動門把真輕鬆！",
               "axle (輪軸的軸心 a-x-l-e) vs. axe (斧頭 a-x-e)。"),
    make_vocab("voc_tea10", "tea_midterm", "tea_midterm_1", "doorknob", "名詞 (Noun)", "門把 / 球形門柄",
               "door (門) + knob (球形把手，字首 k 不發音 /nɑːb/)。",
               "拆成 door + knob！記得 knob 跟 knife 一樣，開頭都有一個隱形保鑣『k』不發音！",
               "手握住門上的圓形銅製把手一轉，把門推開。",
               "同規則靜音 k: knob (把手), knife (刀), knee (膝蓋), know (知道)", "🚪",
               "Turn the doorknob to open the wooden door.",
               "轉動門把以打開木門。",
               "door 加 knob 變門把，knob 的 k 別漏掉！",
               "doorknob (球形門把) vs. jar lid (罐子蓋)。"),
    make_vocab("voc_tea11", "tea_midterm", "tea_midterm_1", "glassblower", "名詞 (Noun)", "吹玻璃工匠",
               "glass (玻璃) + blow (吹) + -er (從事...的人) -> 吹製玻璃藝術品的工匠。",
               "三個熟字合體：glass (玻璃) + blow (吹) + er (人) = glassblower（中間不空格）！",
               "工匠拿著長鐵管沾取熔爐裡的火紅玻璃膏，吹氣塑造成漂亮的花瓶。",
               "相關詞族: glassware (玻璃器皿), eyeglasses (眼鏡), vase (花瓶), pitcher (水壺)", "🏺",
               "The glassblower made a beautiful blue vase and a pitcher.",
               "吹玻璃工匠製作了一個美麗的藍色花瓶與一個水壺。",
               "glass 加 blow 再加 er，吹製玻璃藝術家！",
               "glassblower (吹玻璃工匠-人) vs. glassware (玻璃器皿-物品總稱)。"),
    make_vocab("voc_tea12", "tea_midterm", "tea_midterm_1", "glassware", "名詞 (Noun, 不可數)", "玻璃器皿（總稱）",
               "glass (玻璃) + ware (器皿/製品，如 hardware 五金、software 軟體、tableware 餐具)。",
               "只要字尾有 -ware 就是「某某製品/器皿總稱」（不可數名詞，不加 s）！",
               "架子上擺滿了晶瑩剔透的玻璃杯、玻璃花瓶 (vase) 與玻璃水壺 (pitcher)。",
               "同族字: tableware (餐具), silverware (銀器), hardware (硬體/五金)", "🥂",
               "The shop sells delicate glassware made in Italy.",
               "這家店販售義大利製造的精緻玻璃器皿。",
               "glass 加 ware 玻璃器皿，總稱不可數不加 s！",
               "glassware (玻璃器皿) vs. eyeglasses (眼鏡，必加 es)。")
]


# ==============================================================================
# 3. 為缺少文法的期中考單元補齊「文法焦點與岱崙考卷避坑卡」
# ==============================================================================
NEW_MIDTERM_GRAMMAR = [
    # RWW6 U5
    {
        "id": "gra_m501",
        "book_id": "rw6",
        "unit_id": "rw6_5",
        "rule_title": "Reading Strategy: Identify and Analyze the Setting (識別與分析故事時空背景) 🧭",
        "eng_exp": "The setting is WHERE (place) and WHEN (time & weather) a story happens. It affects the characters' actions and the plot! In 'Lost and Found', the thick fog (weather) caused the family to miss their turn (plot), and climbing above the fog (place) helped them read the map and find the crooked tree.",
        "chi_exp": "【閱讀核心策略】「時空背景 (Setting)」包含故事發生的「地點 (Where)」與「時間/天氣 (When & Weather)」。背景會直接影響角色行動與劇情發展！\n⚠️ 岱崙段考必考因果鏈：因為早晨起濃霧 (one foggy morning) ➔ 看不到地標，本來該右轉 (should have turned right) 卻誤直走 (went straight) ➔ 爬上小山丘頂端高過濃霧 (above the fog) ➔ 對照南方燈塔與東北方彎樹成功定位！",
        "examples": [
            "Time & Weather: Jaya and her family went hiking one foggy morning. And it's noon now. (時間與天氣：起霧的早晨到正午十二點。)",
            "Cause & Effect: Because of the thick fog, they missed their turn and went straight instead of turning right. (環境影響情節：因濃霧錯過轉彎處。)",
            "Elevation Key: The top of the smaller hill was ABOVE the fog, so the fog was at the bottom of the hill! (關鍵考題：山頂在霧之上，所以霧在山腳下！)",
            "Metaphor: The hill with the crooked tree looked like an island in a sea of clouds. (比喻：東北方目標山頭看起來像雲海中的島嶼。)"
        ]
    },
    {
        "id": "gra_m502",
        "book_id": "rw6",
        "unit_id": "rw6_5",
        "rule_title": "Spatial & Navigational Phrases (戶外健行與空間方位片語) 🗺️",
        "eng_exp": "Use precise prepositional and verb phrases to describe trail directions and relative positions: on the left side of, turn right / left, go straight, go back, hike up the hill, next to, between A and B, and read a map.",
        "chi_exp": "【方位片語避坑指南】\n1. 「在左/右邊」靜態位置必加 on the：`on the left` / `on the right`。\n2. 「左/右轉」動態動作不加 the：`turn left` / `turn right`（過去式 `turned right`）。\n3. 「直走」：`go straight`（過去式 `went straight`，注意 straight 的 gh 不發音）。\n4. 「看地圖」英文動詞固定用 `read a map`（不可寫 look a map）。\n5. 「在兩者之間」固定用 `between A and B`。",
        "examples": [
            "She pointed to a log bench on the left side of the trail. (她指著步道左側的原木長凳。)",
            "We usually turn right, but on this trip we decided to go straight. (我們通常右轉，但這次決定直走。)",
            "Before we go back, we should hike up the hill and read a map. (在折返前，我們應該爬上山丘看地圖。)",
            "I sat down next to my sister, and Mom sat down between us. (我坐在姊姊旁邊，媽媽坐在我們兩人之間。)"
        ]
    },
    # RWW6 U6
    {
        "id": "gra_m601",
        "book_id": "rw6",
        "unit_id": "rw6_6",
        "rule_title": "Reading Strategy: Use Visuals & Orienteering Rules (善用視覺圖表與定向越野致勝規則) 🚩",
        "eng_exp": "Pictures, diagrams, and maps are visuals. Visuals provide extra information that is NOT in the text! In 'The World of Orienteering', Figure 1 shows the red-and-white flag, and Figure 2 shows the control card has 18 controls. To win, a racer MUST find and mark ALL controls (a full card)!",
        "chi_exp": "【閱讀與是非題兩大魔王陷阱】\n⚠️ 陷阱 1：課本是非題問『A visual gives the same information that is in a text.』答案是 **FALSE (錯)**！因為視覺圖表提供的是「正文中沒寫出的額外補充資訊（例如從 Figure 2 才知道控制卡共有 18 格）」！\n⚠️ 陷阱 2：課本是非題問『You must finish first to win an orienteering event.』答案是 **FALSE (錯)**！因為如果漏掉任何一個控制點 (misses a control)，就算第一個衝過終點線也不算贏，必須是「打滿全卡所有控制點 (with a full card)」最快完成的人才會贏！",
        "examples": [
            "Visual Clue 1: Figure 1 shows a bright red-and-white control flag hanging behind a tree. (圖 1 顯示紅白相間的控制旗。)",
            "Visual Clue 2: Looking at Figure 2 (Orienteering Control Card), we can see there are 18 controls in total. (從圖 2 可讀出共有 18 個控制點。)",
            "Winning Rule: They might cross the finish line first, but the next person to finish with a full card will win the race! (打滿全卡者才獲勝！)",
            "Gear Rule: Racers must use BOTH a map and a compass (not only a compass) to find controls and the finish line. (必須同時使用地圖與指北針。)"
        ]
    },
    {
        "id": "gra_m602",
        "book_id": "rw6",
        "unit_id": "rw6_6",
        "rule_title": "Context Clues & Prepositions of Terrain (上下文詞義推論與地形方位介系詞) 🏞️",
        "eng_exp": "Master the difference between urban directions (standing on a corner, go two blocks north, across the street from, cross the street) and outdoor terrain navigation (in front of a rock, behind a tree, run along a river, climb over rocks, go up and down hills).",
        "chi_exp": "【岱崙 W4 考卷扣分陷阱與課本英英定義】\n1. ⚠️ `in front of`（在...正前方）：三個字必須分開寫，且是單 f 的 `of`（千萬別像小考寫成 `infront off` ❌）！\n2. 課本 p.43 必考 4 大英英同義配對：\n   • `corner` = a place where two roads meet（兩條路交會處）\n   • `go two blocks` = move this far（移動這麼遠的街區距離）\n   • `across the street from` = on the other side（在馬路對面）\n   • `cross the street` = go to the other side（穿越馬路走到對面去）",
        "examples": [
            "Go two blocks north, turn left, and you'll be across the street from the bookstore. (往北走兩個街區左轉，就在書店對街。)",
            "Controls may be in front of a big rock or behind a tree. (控制點可能在巨石前或大樹後。)",
            "You will likely run along a river, climb over rocks, and go up and down hills. (沿著河跑、爬過岩石、上下山丘。)"
        ]
    },
    # RWW6 U7
    {
        "id": "gra_m701",
        "book_id": "rw6",
        "unit_id": "rw6_7",
        "rule_title": "Reading Strategy: Understand a Bar Graph & 196 Countries Data (長條圖判讀與全球官方語言統計) 📊",
        "eng_exp": "A bar graph uses rectangles to compare how much or how many. In the graph 'Official Languages for 196 Countries': 0 official languages = 8 countries (e.g., Mexico, USA); 1 official language = 110 countries (e.g., France); 2 = 48 countries (e.g., India, Tanzania); 3 = 16 countries; 4+ = 14 countries (e.g., Zimbabwe with 16!).",
        "chi_exp": "【課本 p.51 長條圖與國家案例交叉比對（必考！）】\n• **0 種官方語言（藍條：8 國）**：**墨西哥 (Mexico)**（雖普遍說 Spanish）、**美國 (USA)**（雖普遍說 English），因為從未通過法律 (`never passed a law`)！\n• **1 種官方語言（橘條：110 國，佔最多）**：**法國 (France)**（母語與官方語言皆為 French）。\n• **2 種官方語言（黃綠條：48 國）**：**印度 (India)**（官方語言為 Hindi 與 English，全境有超過 1,000 種母語）、**坦尚尼亞 (Tanzania)**（English 與 Swahili）。\n• **4 種以上官方語言（紫條：14 國）**：**辛巴威 (Zimbabwe)**（擁有世界最多的 **16 種**官方語言，因被 4 個鄰國包圍！）。",
        "examples": [
            "A country has to pass a law to make a language official. (國家必須通過法律才能確立官方語言。)",
            "Mexico and the United States have NO official languages because neither country has passed a law to make one. (墨、美皆無官方語言。)",
            "Zimbabwe has the most official languages in the world—sixteen! It belongs to the purple bar (4+) in the bar graph. (辛巴威有 16 種官方語言。)",
            "In India, Hindi and English are the two official languages, while people speak over a thousand native languages. (印度有兩種官方語言。)"
        ]
    },
    # RWW6 U8
    {
        "id": "gra_m801",
        "book_id": "rw6",
        "unit_id": "rw6_8",
        "rule_title": "Reading Strategy: Make Predictions & Erico's Multicultural Profile (預測策略與 Erico 跨國背景總整理) 🔮",
        "eng_exp": "A prediction is what you think will happen in the future based on story clues and your own knowledge (usually using 'will'). In 'So Many Questions', clues like 'drawing paper, paint brushes, and colored pencils' let us predict Rosa is going to art class!",
        "chi_exp": "【閱讀理解必考雙核心】\n1. **什麼是 Prediction（預測）？** 針對「尚未發生的未來」進行合理推論（例如 `Darla will do well in school.` 是預測；`Darla fell asleep` 是過去已發生的事實，不是預測！）。\n2. **Erico 的跨國背景懶人包（課本 p.56 T/F 必考）**：\n   • 名字來源：**葡萄牙語名字 (Portuguese name)**（但 Rosa 一開始誤以為是義大利名字，先用 **Italian** 對他說話）。\n   • 出生與家庭：**澳洲 (Australia)**（爸爸從**巴西 Brazil** 搬去澳洲，媽媽來自**葡萄牙 Portugal**）。\n   • 居住經歷：曾在**義大利 (Italy)** 住過 3 個月，目前剛來**美國 (USA)** 第 2 個月。\n   • 說話口音：帶著**英國腔 (British accent)**（不是澳洲腔！至於為什麼有英國腔，是個 long story）。\n   • 語言優勢：會說葡萄牙語確實幫助他學會了一些義大利語（`Portuguese did help me learn some Italian`）。",
        "examples": [
            "Clue -> Prediction: Rosa is carrying drawing paper, paint brushes, and colored pencils ➔ She will go to an art class. (從美術用品預測去上美術課。)",
            "Word Definition 1: 'bilingual' means speaking two languages. (bilingual 意為通曉兩種語言。)",
            "Word Definition 2: 'accent' means a way to pronounce words. (accent 意為發音單字的方式/腔調。)",
            "Character Attitude: Erico realized that asking so many questions was Rosa's way of being friendly. (Erico 理解連珠發問是 Rosa 表示友善的方式。)"
        ]
    },
    # 岱崙 3C 考卷真題特訓 (tea_midterm_1)
    {
        "id": "gra_tea01",
        "book_id": "tea_midterm",
        "unit_id": "tea_midterm_1",
        "rule_title": "🔥 岱崙 3C 小考兩大魔王題型搶分公式（倒裝附和句 + 三級副詞長句合成）",
        "eng_exp": "Master the two highest-weight sentence writing tasks in Tiger English Academy 3C Quizzes: (1) Past Simple Agreement with so / too / either / neither; (2) Three-tier Adverb Comparison combining positive, comparative, and superlative adverbs in one long sentence.",
        "chi_exp": "【Rex 期中考必拿回的 23 分救命公式】\n① **Week 2 倒裝與附和句 (Grammar U13)**：\n   • 先看題幹有沒有動詞！若題幹只有 `[Olivia, Penny - 100% on quiz / so]`，前半句一定要自己補上過去式動詞 **`got`** 與所有格 **`her/his`** ➔ `Olivia got 100% on her quiz`\n   • 肯定句尾：`, and Michael did, too.`（或 `, and Michael got 95% on his quiz, too.`）\n   • 肯定倒裝：`, and so did Penny.`（萬萬不可寫 `are` 或 `100% did`！）\n   • 否定句尾：`Ray didn't pass the quiz, and Jim didn't, either.`（過去式否定必用 `didn't + 原形 V`，不可寫 `are not pass`！）\n   • 否定倒裝：`Ray didn't pass the quiz, and neither did Jim.`\n\n② **Week 4 & 5 三級副詞比較長句合成 (Grammar U14)**：\n   • 標準三段式結構：`[主詞1 + V + 原級副詞], [主詞2 + V + 比較級副詞 + than + 主詞1], but [主詞3 + V + the + 最高級副詞].`\n   • 單音節副詞 (`fast, hard, high, late, early`)：直接加 `-er / -est`（`fast ➔ faster than ➔ the fastest`，**嚴禁加 more**！）。\n   • 多音節 `-ly` 副詞 (`quickly,ゆっくり/slowly, clearly, horribly, beautifully`)：用 `more ... than / the most ...`（`quickly ➔ more quickly than ➔ the most quickly`）。\n   • 不規則副詞 (`far, well, badly`)：`far ➔ farther/further than ➔ the farthest/furthest`；`well ➔ better than ➔ the best`。\n   • **三大防扣分鐵律**：(A) 可數單數主詞前要加 `a / an`（`A person`, `An eight year old`）且第三人稱單數現在式動詞要加 `-s`（`runs`, `laughs`）；(B) `than` 後方必須是第一個主詞，不可重複寫第二個主詞；(C) 最高級前面一定要加 **`the`**！",
        "examples": [
            "【W2 倒裝滿分範本】Olivia got 100% on her quiz, and so did Penny. / Ray didn't pass the quiz, and neither did Jim.",
            "【W4 單音節副詞滿分範本】A person runs fast, a dog runs faster than a person, but a lion runs the fastest.",
            "【W4 多音節副詞滿分範本】A five year old can walk quickly, an eight year old can walk more quickly than a five year old, but an adult can walk the most quickly.",
            "【W5 不規則副詞滿分範本】A frog can jump far, a rabbit can jump farther than a frog, but a kangaroo can jump the farthest.",
            "【W5 單三動詞滿分範本】A clown laughs horribly, a ghost laughs more horribly than a clown, but a witch laughs the most horribly."
        ]
    }
]


# ==============================================================================
# 4. 為缺少測驗題的 5 個期中考單元補齊雙軌測驗題庫（每題皆含 4 選項，相容紙筆與 iPad 點選）
# ==============================================================================
def make_quiz(qid, book_id, unit_id, qtype, question, options, answer, diff, explanation):
    return {
        "id": qid,
        "book_id": book_id,
        "unit_id": unit_id,
        "type": qtype,
        "question": question,
        "options": options,
        "answer": answer,
        "difficulty": diff,
        "explanation": explanation
    }


NEW_MIDTERM_QUIZZES = [
    # ---------------- RWW6 Unit 5 (rw6_5) ----------------
    make_quiz("q_m501", "rw6", "rw6_5", "reading",
              "Where is the family in the story 'Lost and Found', and what is the weather like?",
              ["On a hiking trail; it is very foggy.", "At the beach; it is sunny and windy.", "In a big city; it is raining heavily.", "At a campsite; it is snowing."],
              "On a hiking trail; it is very foggy.", "★★☆☆☆",
              "🟢 正解：On a hiking trail; it is very foggy。\n📖 依據：故事開頭第一句『Jaya and her family went hiking one foggy morning.』明確交代時空背景 (Setting)。"),
    make_quiz("q_m502", "rw6", "rw6_5", "reading",
              "How did Jaya and her family get on the wrong trail?",
              ["They went straight instead of turning right.", "They turned left at the log bench.", "They forgot to bring their map.", "They walked back down the hill."],
              "They went straight instead of turning right.", "★★★☆☆",
              "🟢 正解：They went straight instead of turning right。\n📖 依據：弟弟 Manoj 說『There's a place we should have turned right, but I think we went straight.』課本 p.38 第 3 題原題！"),
    make_quiz("q_m503", "rw6", "rw6_5", "reading",
              "When the family climbed to the top of the smaller hill, where was the fog?",
              ["At the bottom of the hill (below them)", "High above the hill", "Inside the lighthouse", "Only on the east side"],
              "At the bottom of the hill (below them)", "★★★☆☆",
              "🟢 正解：At the bottom of the hill (below them)。\n📖 依據：課本 p.37 寫道『they discovered the top of the hill was above the fog』，山頂高過濃霧，因此濃霧在山腳下（課本 p.38 必考陷阱題）！"),
    make_quiz("q_m504", "rw6", "rw6_5", "reading",
              "What did the family do on top of the smaller hill to find their way?",
              ["They read a map and looked at landmarks.", "They had their picnic lunch.", "They called the lighthouse keeper.", "They slept on a log bench."],
              "They read a map and looked at landmarks.", "★★☆☆☆",
              "🟢 正解：They read a map and looked at landmarks。\n📖 依據：媽媽說『We know how to read a map, so let's look.』並對照南方的燈塔找出東北方的目標山丘。"),
    make_quiz("q_m505", "rw6", "rw6_5", "reading",
              "Where did Jaya and her family originally plan to hike to?",
              ["The hill with a tall, crooked tree on top", "The lighthouse near town", "The log bench on the left", "The beach in the south"],
              "The hill with a tall, crooked tree on top", "★★☆☆☆",
              "🟢 正解：The hill with a tall, crooked tree on top。\n📖 依據：課文第 2 行『Their goal was a hill with a tall, crooked tree on top. They liked to picnic there.』"),
    make_quiz("q_m506", "rw6", "rw6_5", "reading",
              "In the passage 'Warning! Warning!', why does someone turn on the light and horn in a lighthouse when fog forms?",
              ["To warn people in ships where the land is", "To help hikers find the crooked tree", "To tell fishermen that dinner is ready", "To make the fog disappear quickly"],
              "To warn people in ships where the land is", "★★☆☆☆",
              "🟢 正解：To warn people in ships where the land is。\n📖 依據：課本 p.39 副篇最後一句『This warns people in ships where the land is, telling them which direction not to go.』"),
    make_quiz("q_m507", "rw6", "rw6_5", "vocab",
              "She pointed to a log bench ______ the left side of the trail.",
              ["on", "in", "at", "by"],
              "on", "★★★☆☆",
              "🟢 正解：on。\n🔑 公式：『在左邊 / 在左側』固定搭配介系詞 on (on the left / on the left side of)。"),
    make_quiz("q_m508", "rw6", "rw6_5", "vocab",
              "We know the lighthouse is south, and we're on a hill ______ the lighthouse and our picnic spot.",
              ["between", "among", "across", "along"],
              "between", "★★☆☆☆",
              "🟢 正解：between。\n🔑 公式：between A and B 表示『介於 A 與 B 兩者之間』。"),
    make_quiz("q_m509", "rw6", "rw6_5", "vocab",
              "We knew where we were going, so we didn't need to ______ a map.",
              ["read", "look", "watch", "see"],
              "read", "★★★☆☆",
              "🟢 正解：read。\n🔑 公式：英文中『看地圖、判讀地圖』固定使用動詞 read (read a map)，不用 look 或 watch！"),
    make_quiz("q_m510", "rw6", "rw6_5", "vocab",
              "A ______ is an instrument with a small pointed magnet that always points north.",
              ["compass", "lighthouse", "telescope", "furnace"],
              "compass", "★☆☆☆☆",
              "🟢 正解：compass（指北針）。\n📖 依據：Topic 3 導讀定義『A compass is an instrument you use to tell direction.』"),

    # ---------------- RWW6 Unit 6 (rw6_6) ----------------
    make_quiz("q_m601", "rw6", "rw6_6", "reading",
              "True or False: 'A visual gives the exact same information that is already in a text.'",
              ["False — Visuals provide extra information that is NOT in a text.", "True — Visuals only repeat the words in the text.", "True — You don't need to look at visuals while reading.", "False — Visuals are only for decoration."],
              "False — Visuals provide extra information that is NOT in a text.", "★★★☆☆",
              "🟢 正解：False — Visuals provide extra information that is NOT in a text。\n📖 依據：課本 p.40 Reading Goal 明確定義『Visuals provide information that is not in a text.』"),
    make_quiz("q_m602", "rw6", "rw6_6", "reading",
              "In orienteering, what are the hidden stations that racers must find called?",
              ["Controls", "Corners", "Blocks", "Compasses"],
              "Controls", "★★☆☆☆",
              "🟢 正解：Controls（控制點）。\n📖 依據：課文第 11-12 行『racers use a map and compass to find stations, which are called controls.』"),
    make_quiz("q_m603", "rw6", "rw6_6", "reading",
              "Look at Figure 2 (Orienteering Control Card) in Unit 6. How many controls are there on the card?",
              ["18 controls", "10 controls", "12 controls", "25 controls"],
              "18 controls", "★★★☆☆",
              "🟢 正解：18 controls。\n📖 依據：課本 p.41 Figure 2 控制卡上的編號格子從 1 到 18，這是必須透過閱讀視覺圖表 (Use Visuals) 才能答出的經典考題！"),
    make_quiz("q_m604", "rw6", "rw6_6", "reading",
              "Who wins an orienteering race?",
              ["The fastest racer who finishes with a FULL card (all controls marked)", "Anyone who crosses the finish line first, even if they missed a control", "The racer who runs the furthest distance in the woods", "The person who draws the best map"],
              "The fastest racer who finishes with a FULL card (all controls marked)", "★★★★☆",
              "🟢 正解：The fastest racer who finishes with a FULL card。\n⚠️ 陷阱：課本 p.42 是非題第 8 題『You must finish first to win』為 False！若漏掉控制點，就算先過終點線也不算贏，必須打滿全卡 (with a full card)！"),
    make_quiz("q_m605", "rw6", "rw6_6", "vocab",
              "In the sentence 'Standing on a corner, you ask someone how to get to a store,' what does 'corner' mean?",
              ["A place where two roads meet", "A red and white flag in the woods", "A spot behind a big rock", "A card with 18 boxes"],
              "A place where two roads meet", "★★☆☆☆",
              "🟢 正解：A place where two roads meet（兩條道路交會的轉角處）。課本 p.43 Context Clues 第 1 題原題！"),
    make_quiz("q_m606", "rw6", "rw6_6", "vocab",
              "In the sentence 'You'll be across the street from the bookstore,' what does 'across the street from' mean?",
              ["On the other side of the street", "Behind the bookstore", "Two blocks north of the street", "Inside the bookstore"],
              "On the other side of the street", "★★☆☆☆",
              "🟢 正解：On the other side of the street（在馬路的另一側/對面）。課本 p.43 Context Clues 第 3 題原題！"),
    make_quiz("q_m607", "rw6", "rw6_6", "vocab",
              "Controls are hard to see. They may be ______ a big rock or behind a tree.",
              ["in front of", "infront off", "in front off", "infront of"],
              "in front of", "★★★★☆",
              "🟢 正解：in front of。\n⚠️ 考場真實失分：Rex 在 Week 4 小考寫成『infront off ❌』！切記是三個獨立單字 in + front + of（單 f）！"),
    make_quiz("q_m608", "rw6", "rw6_6", "reading",
              "In the short passage 'Treasure Hunt' (p.43), where is Bayani's house, and what treasure did the team find?",
              ["Across from the park; they found cookies (food they ate).", "Behind the school; they found gold coins.", "Next to the river; they found a new compass.", "North of the swings; they found a map."],
              "Across from the park; they found cookies (food they ate).", "★★★☆☆",
              "🟢 正解：Across from the park; they found cookies。\n📖 依據：第一句『He lives across the street from the park』，最後一句『We ate them』搭配插圖餅乾盒可知寶藏是 cookies！"),

    # ---------------- RWW6 Unit 7 (rw6_7) ----------------
    make_quiz("q_m701", "rw6", "rw6_7", "reading",
              "What must a country do if it wants to make a language an 'official language'?",
              ["It has to pass a law.", "It has to ask everyone to speak it at home.", "It has to draw a bar graph.", "It has to build a language school."],
              "It has to pass a law.", "★★☆☆☆",
              "🟢 正解：It has to pass a law（必須通過法律）。\n📖 依據：課本 p.50 第一段最後一句『A country has to pass a law to make a language official.』"),
    make_quiz("q_m702", "rw6", "rw6_7", "reading",
              "Why do Mexico and the United States have NO official language?",
              ["Because neither country has ever passed a law to make one.", "Because people there don't speak Spanish or English.", "Because they have more than a thousand languages.", "Because they only use sign language."],
              "Because neither country has ever passed a law to make one.", "★★★☆☆",
              "🟢 正解：Because neither country has ever passed a law to make one。\n📖 依據：墨西哥人雖普遍說 Spanish、美國人普遍說 English，但兩國從未通過法律指定官方語言！"),
    make_quiz("q_m703", "rw6", "rw6_7", "reading",
              "According to the bar graph 'Official Languages for 196 Countries' (p.51), how many countries have NO (0) official language, and how many have ONE (1) official language?",
              ["8 countries have 0; 110 countries have 1.", "14 countries have 0; 48 countries have 1.", "0 countries have 0; 196 countries have 1.", "16 countries have 0; 110 countries have 1."],
              "8 countries have 0; 110 countries have 1.", "★★★☆☆",
              "🟢 正解：8 countries have 0; 110 countries have 1。\n📖 依據：課本 p.51 長條圖：0 種 = 8 國（藍條）；1 種 = 110 國（橘條，佔全球大多數）；2 種 = 48 國；3 種 = 16 國；4+ 種 = 14 國。"),
    make_quiz("q_m704", "rw6", "rw6_7", "reading",
              "Which country has the MOST official languages in the world (sixteen!), and which bar in the graph includes it?",
              ["Zimbabwe — in the purple bar for '4+' (14 countries)", "India — in the yellow bar for '2' (48 countries)", "China — in the orange bar for '1' (110 countries)", "Mexico — in the blue bar for '0' (8 countries)"],
              "Zimbabwe — in the purple bar for '4+' (14 countries)", "★★★☆☆",
              "🟢 正解：Zimbabwe — in the purple bar for '4+'。\n📖 依據：辛巴威 (Zimbabwe) 有 16 種官方語言（世界第一），在長條圖中歸類於『4+ 種官方語言』的紫色長條！"),
    make_quiz("q_m705", "rw6", "rw6_7", "reading",
              "What are the two official languages of India?",
              ["Hindi and English", "Mandarin and English", "Spanish and French", "Shona and Swahili"],
              "Hindi and English", "★★☆☆☆",
              "🟢 正解：Hindi and English。\n📖 依據：課本 p.51 最後一段『But Hindi and English are the two official languages of India.』"),
    make_quiz("q_m706", "rw6", "rw6_7", "reading",
              "Where might you NOT use an official language according to Unit 7?",
              ["At home (where people usually speak their native language)", "In government offices", "At school", "In court and laws"],
              "At home (where people usually speak their native language)", "★★☆☆☆",
              "🟢 正解：At home。\n📖 依據：課本 p.52 選擇題第 4 題原題！在家裡人們通常說的是自己的母語 (native language)。"),

    # ---------------- RWW6 Unit 8 (rw6_8) ----------------
    make_quiz("q_m801", "rw6", "rw6_8", "reading",
              "Which of the following sentences is a 'prediction' (預測)?",
              ["Darla will do well in school.", "Darla fell asleep on the rug.", "Rosa dropped her art supplies on the floor.", "Erico lived in Italy for three months."],
              "Darla will do well in school.", "★★☆☆☆",
              "🟢 正解：Darla will do well in school。\n📖 依據：課本 p.54 Get Ready 第 1 題原題！Prediction 是對未來將會發生之事的推測（常含 will），其他三項都是過去已發生的事實。"),
    make_quiz("q_m802", "rw6", "rw6_8", "reading",
              "In 'So Many Questions', what language did Rosa FIRST use to speak to Erico, and what class can we predict she is going to?",
              ["She spoke in Italian; she is going to an art class.", "She spoke in Portuguese; she is going to a music class.", "She spoke in English; she is going to a gym class.", "She spoke in Spanish; she is going to a math class."],
              "She spoke in Italian; she is going to an art class.", "★★★☆☆",
              "🟢 正解：She spoke in Italian; she is going to an art class。\n📖 依據：第一句『\"Can you hold the door?\" the girl asked Erico in Italian.』，且她抱著 drawing paper, paint brushes, colored pencils，因此預測是去上美術課！"),
    make_quiz("q_m803", "rw6", "rw6_8", "reading",
              "Where is Erico's family from, and where were his parents born?",
              ["His family is from Australia; his dad is from Brazil and his mom is from Portugal.", "His family is from Italy; both parents were born in England.", "His family is from the USA; his dad is from Mexico and his mom is from Spain.", "His family is from Brazil; his dad is from Australia and his mom is from Italy."],
              "His family is from Australia; his dad is from Brazil and his mom is from Portugal.", "★★★☆☆",
              "🟢 正解：His family is from Australia; his dad is from Brazil and his mom is from Portugal。\n📖 依據：課文第 20-22 行『My name is Portuguese, but my family's from Australia. My dad moved there from Brazil, and my mom's from Portugal...』"),
    make_quiz("q_m804", "rw6", "rw6_8", "reading",
              "What kind of accent does Erico have when he speaks English, and how did he feel about Rosa's many questions?",
              ["He has a British accent; he realized asking questions was Rosa's way of being friendly.", "He has an Australian accent; he thought Rosa was very rude and unfriendly.", "He has an Italian accent; he walked away angrily.", "He has an American accent; he refused to answer her."],
              "He has a British accent; he realized asking questions was Rosa's way of being friendly.", "★★★☆☆",
              "🟢 正解：He has a British accent; he realized asking questions was Rosa's way of being friendly。\n📖 依據：課本 p.56 是非題第 5、7 題必考點！Erico 講話是英國腔 (British accent)，且他明白連珠發問是 Rosa 展現友善的方式。"),
    make_quiz("q_m805", "rw6", "rw6_8", "vocab",
              "In Unit 8, what do the words 'accent' and 'bilingual' mean?",
              ["accent = a way to pronounce words; bilingual = speaking two languages", "accent = asking many questions; bilingual = moving to two countries", "accent = drawing pictures; bilingual = being friendly to new students", "accent = an official law; bilingual = a native speaker"],
              "accent = a way to pronounce words; bilingual = speaking two languages", "★★☆☆☆",
              "🟢 正解：accent = a way to pronounce words（發音方式/腔調）；bilingual = speaking two languages（說兩種語言）。課本 p.57 詞義題原題！"),

    # ---------------- 岱崙 3C 考卷真題特訓 (tea_midterm_1) ----------------
    make_quiz("q_tea01", "tea_midterm", "tea_midterm_1", "grammar",
              "【岱崙 W2 考卷真題】請選出 [Olivia, Penny - 100% on quiz / so] 的滿分正確改寫句：",
              [
                  "Olivia got 100% on her quiz, and so did Penny.",
                  "Olivia 100% on her quiz, and 100% did Penny.",
                  "Olivia got 100% on her quiz, and so was Penny.",
                  "Olivia got 100% on her quiz, and Penny did so."
              ],
              "Olivia got 100% on her quiz, and so did Penny.", "★★★★☆",
              "🟢 正解：Olivia got 100% on her quiz, and so did Penny。\n⚠️ 考場失分剖析：Rex 當時寫成『Olivia 100% on her quiz, 100% did Penny ❌』，漏掉動詞 got，又把 100% 當成倒裝詞！一般動詞過去式 got 的肯定倒裝必用『so did + 主詞』！"),
    make_quiz("q_tea02", "tea_midterm", "tea_midterm_1", "grammar",
              "【岱崙 W2 考卷真題】請選出 [Ryan, Michael - 95% on quiz / too] 的滿分正確改寫句：",
              [
                  "Ryan got 95% on his quiz, and Michael did, too.",
                  "Ryan 95% on quiz, and Michael are too.",
                  "Ryan got 95% on his quiz, and Michael was, too.",
                  "Ryan got 95% on his quiz, and too did Michael."
              ],
              "Ryan got 95% on his quiz, and Michael did, too.", "★★★★☆",
              "🟢 正解：Ryan got 95% on his quiz, and Michael did, too.（或 Michael got 95% on his quiz, too.）\n⚠️ 考場失分剖析：Rex 當時寫成『Michael are too ❌』！前句是過去式一般動詞 got，附和句必須用助動詞 did，絕對不能用 are 或 was！"),
    make_quiz("q_tea03", "tea_midterm", "tea_midterm_1", "grammar",
              "【岱崙 W2 考卷真題】請選出 [Ray, Jim - not pass quiz / either] 的滿分正確改寫句：",
              [
                  "Ray didn't pass the quiz, and Jim didn't, either.",
                  "Ray are not pass quiz, and Jim are either.",
                  "Ray wasn't pass the quiz, and Jim wasn't, either.",
                  "Ray didn't pass the quiz, and either did Jim."
              ],
              "Ray didn't pass the quiz, and Jim didn't, either.", "★★★★☆",
              "🟢 正解：Ray didn't pass the quiz, and Jim didn't, either。\n⚠️ 考場失分剖析：Rex 在考場把『沒有通過』直譯寫成『Ray are not pass quiz ❌』被扣光 3 分！一般動詞 pass 的過去式否定必須借用助動詞 didn't + 原形動詞 pass！"),
    make_quiz("q_tea04", "tea_midterm", "tea_midterm_1", "grammar",
              "【岱崙 W4 考卷真題】How fast do they run? (person, dog & lion) 請選出完全正確的三級副詞比較長句：",
              [
                  "A person runs fast, a dog runs faster than a person, but a lion runs the fastest.",
                  "A person runs fast, a dog runs more faster than a dog, but a lion runs fastest.",
                  "Person run fast, dog run faster than person, but lion run the most fast.",
                  "A person runs fastly, a dog runs more fastly than a person, but a lion runs the most fastly."
              ],
              "A person runs fast, a dog runs faster than a person, but a lion runs the fastest.", "★★★★★",
              "🟢 正解：A person runs fast, a dog runs faster than a person, but a lion runs the fastest。\n⚠️ 考場三大扣分坑全解：① fast 是單音節副詞，比較級是 faster（不可寫 more faster ❌）；② than 後面是第一個主詞 a person（不可重複寫 a dog ❌）；③ 最高級必加定冠詞 the (the fastest)！"),
    make_quiz("q_tea05", "tea_midterm", "tea_midterm_1", "grammar",
              "【岱崙 W4 考卷真題】How quickly can they walk? (five year old, eight year old & adult) 請選出滿分長句：",
              [
                  "A five year old can walk quickly, an eight year old can walk more quickly than a five year old, but an adult can walk the most quickly.",
                  "A five year old can walk quickly, an eight year old can walk quicker than a five year old, but an adult can walk the quickest.",
                  "Five year old can walk quick, eight year old can walk more quickly, but adult can walk most quickly.",
                  "A five year old can walk quickly, an eight year old can walk more quickly than an eight year old, but an adult can walk the most quickly."
              ],
              "A five year old can walk quickly, an eight year old can walk more quickly than a five year old, but an adult can walk the most quickly.", "★★★★★",
              "🟢 正解：A five year old can walk quickly, an eight year old can walk more quickly than a five year old, but an adult can walk the most quickly。\n🔑 公式：多音節 -ly 副詞比較級必用 more quickly than，最高級必用 the most quickly；且 eight 母音開頭前用冠詞 an！"),
    make_quiz("q_tea06", "tea_midterm", "tea_midterm_1", "grammar",
              "【岱崙 W5 考卷真題】How horribly do they laugh? (clown, ghost & witch) 請選出滿分長句：",
              [
                  "A clown laughs horribly, a ghost laughs more horribly than a clown, but a witch laughs the most horribly.",
                  "A clown laugh horribly, a ghost laugh more horribly than a clown, but a witch laugh the most horribly.",
                  "A clown laughs horrible, a ghost laughs more horrible than a clown, but a witch laughs the most horrible.",
                  "A clown laughs horribly, a ghost laughs horriblier than a clown, but a witch laughs the horribliest."
              ],
              "A clown laughs horribly, a ghost laughs more horribly than a clown, but a witch laughs the most horribly.", "★★★★★",
              "🟢 正解：A clown laughs horribly, a ghost laughs more horribly than a clown, but a witch laughs the most horribly。\n⚠️ 考場真實失分：題幹問 How do they laugh? 當拆成單數主詞 A clown / A ghost / A witch 時，現在式動詞必須全部加上第三人稱單數 -s (laughs)！"),
    make_quiz("q_tea07", "tea_midterm", "tea_midterm_1", "vocab",
              "【岱崙 W2 & W4 聽寫易錯字總驗收】下列哪一組單字的拼寫「全部正確」？（請仔細檢查 Rex 曾錯過的 6 個字！）",
              [
                  "wedge / knife / mountain / wheelchair / furnace / frames",
                  "wadge / Knif / mountion / whillchair / furnes / france",
                  "wedge / knife / mountian / wheelchair / furnes / frames",
                  "wadge / knife / mountain / whillchair / furnace / France"
              ],
              "wedge / knife / mountain / wheelchair / furnace / frames", "★★★★☆",
              "🟢 正解：wedge (楔子) / knife (小刀) / mountain (山脈) / wheelchair (輪椅) / furnace (熔爐) / frames (鏡框)。\n⚠️ 避開考場鉛筆錯字：wadge ❌、Knif ❌、mountion ❌、whillchair ❌、furnes ❌、france ❌！")
]


# ==============================================================================
# 5. 六上期中考專屬 1★ ~ 10★ 晨間體操語感秒殺題庫 (50 題，每星級 5 題)
# ==============================================================================
def make_bg(idx, book_id, unit_id, star, question, options, answer, green_tip, red_trap):
    stars_str = "★" * min(5, (star + 1) // 2) + "☆" * (5 - min(5, (star + 1) // 2))
    return {
        "id": f"bg_mid_{idx:03d}",
        "book_id": book_id,
        "unit_id": unit_id,
        "type": "brain_gym",
        "is_midterm": True,
        "star": star,
        "question": question,
        "options": options,
        "answer": answer,
        "difficulty": f"Lv.{star} ({stars_str})",
        "explanation": f"🟢 正確語感直覺：{green_tip}\n🔴 誘答盲點排除：{red_trap}"
    }


MIDTERM_BRAIN_GYM = [
    # ⭐ Level 1: 肯定與否定句尾附和 (too vs. either)
    make_bg(1, "gra3", "gra3_13", 1,
            "Bell's invention was ready on February 14, and Gray's invention was ready, ______.",
            ["too", "either", "so", "neither"], "too",
            "前句是肯定句 (was ready)，且空格在『句尾逗號後』，無腦秒選 too！",
            "either 只能用在否定句尾；so 與 neither 必須放在句首倒裝。"),
    make_bg(2, "gra3", "gra3_13", 1,
            "In the 1870s, people didn't have telephones. They didn't have computers, ______.",
            ["either", "too", "neither", "so"], "either",
            "看到前句有否定詞 didn't，且空格在『句尾逗號後』，否定句尾必選 either！",
            "千萬不能選 too（too 只能配肯定句）；neither 已經包含 not，不能跟 didn't 同句並存。"),
    make_bg(3, "wr3", "wr3_4", 1,
            "I can get to my school in ten minutes ______ foot.",
            ["on", "by", "in", "with"], "on",
            "『走路、步行』是雙腳踩在地上，英文固定搭配 on foot！",
            "by 後面只能接交通工具（by bus, by subway, by car, by bike），嚴禁寫出中式英文 by foot！"),
    make_bg(4, "gra3", "gra3_15", 1,
            "______ apples are there in the bowl on the kitchen table?",
            ["How many", "How much", "How far", "How long"], "How many",
            "apples 有加 -s 是『可數複數名詞』，詢問數量必用 How many！",
            "How much 是用來問不可數名詞（如 water, milk, sugar, bread, flour）。"),
    make_bg(5, "gra3", "gra3_15", 1,
            "______ olive oil and butter do we need for the mini pizzas?",
            ["How much", "How many", "How often", "How fast"], "How much",
            "olive oil（橄欖油）與 butter（奶油）皆為液體/膏狀不可數名詞，必用 How much！",
            "不可數名詞沒有複數形，不能用 How many。"),

    # ⭐ Level 2: 句首倒裝附和 (So vs. Neither)
    make_bg(6, "gra3", "gra3_13", 2,
            "Antonio Meucci made a telephone machine in the 19th century. ______ did Elisha Gray.",
            ["So", "Too", "Neither", "Either"], "So",
            "前句 made 是『肯定過去式』，空格在句首且後面已經倒裝 (did Elisha Gray)，秒選 So！",
            "Too 絕對不能放句首（*Too did Gray 是大忌）；Neither 用於否定句。"),
    make_bg(7, "gra3", "gra3_13", 2,
            "Meucci didn't become rich and famous from his invention. ______ did Reis.",
            ["Neither", "Either", "So", "Too"], "Neither",
            "前句 didn't 是『否定句』，句首倒裝表示『雷斯也沒有』，必選 Neither！",
            "Either 不能放句首倒裝；So 只用於肯定附和。"),
    make_bg(8, "wr3", "wr3_4", 2,
            "Cynthia ______ lived in her neighborhood ______ three years.",
            ["has; for", "have; for", "has; ago", "lived; for"], "has; for",
            "Cynthia 是第三人稱單數配 has lived（現在完成式），持續『長達三年』搭配介系詞 for！",
            "ago 只能配過去簡單式（moved here three years ago），現在完成式嚴禁出現 ago！"),
    make_bg(9, "wr3", "wr3_5", 2,
            "With the first 100 dollars, I would buy a nice present ______ my mom.",
            ["for", "to", "with", "at"], "for",
            "課本 p.43 改錯原題：buy + 禮物 + for + 人（為媽媽買禮物）！",
            "give / send 才配 to（give a present to my mom）；buy 必配 for！"),
    make_bg(10, "rd6", "rd6_4", 2,
            "Where is the asteroid belt located in our solar system?",
            ["Between Mars and Jupiter", "Between Earth and Mars", "Further away than Neptune", "Between Venus and Earth"], "Between Mars and Jupiter",
            "小行星帶 (asteroid belt) 夾在『火星 (Mars) 與木星 (Jupiter) 之間』！",
            "海王星之外 (further away than Neptune) 的是古柏帶 (Kuiper belt)！"),

    # ⭐ Level 3: 倒裝助動詞辨析 (Be 動詞 vs. 一般動詞 did)
    make_bg(11, "gra3", "gra3_13", 3,
            "Alexander Graham Bell's mother was deaf. So ______ his wife.",
            ["was", "did", "were", "had"], "was",
            "先抓前句動詞！前句是 Be 動詞『was』，附和句必須鏡像對映使用 Be 動詞『was』！",
            "千萬別看到過去式就無腦填 did！只有前句是一般動作動詞（如 helped, invented）才用 did。"),
    make_bg(12, "gra3", "gra3_13", 3,
            "Swan's light bulb worked for a long time, and so ______ Edison's light bulb.",
            ["did", "was", "worked", "had"], "did",
            "前句動詞 worked 是『一般動詞過去式』，附和句必須請出過去式助動詞『did』！",
            "上一句『Swan's light bulb was a success』才用 So was；這句動詞是 worked，必用 So did！"),
    make_bg(13, "gra3", "gra3_13", 3,
            "Ryan got 95% on his English quiz, and Michael ______, too.",
            ["did", "are", "was", "got"], "did",
            "岱崙 W2 小考真題！前句動詞 got 是一般動詞過去式，句尾附和必用『Michael did, too.』！",
            "Rex 在考場誤寫成『Michael are too ❌』，既錯了時態（過去式），又錯用了 be 動詞！"),
    make_bg(14, "gra3", "gra3_13", 3,
            "Ray ______ pass the quiz yesterday, and Jim didn't, either.",
            ["didn't", "are not", "wasn't", "don't"], "didn't",
            "岱崙 W2 小考真題！pass 是一般動詞（通過），過去式否定必須借用助動詞『didn't + 原形 pass』！",
            "中文說『不是通過』，但英文絕不能寫『are not pass』或『wasn't pass』！"),
    make_bg(15, "gra3", "gra3_13", 3,
            "Antonio Meucci wasn't from the U.K. Neither ______ Johann Philipp Reis.",
            ["was", "wasn't", "did", "didn't"], "was",
            "雙重考點：① 前句 wasn't 是 Be 動詞，後句也用 Be 動詞；② Neither 已含否定，後面必接『肯定形 was』！",
            "選 wasn't 會造成雙重否定錯誤；選 did 則是搞錯動詞種類。"),

    # ⭐ Level 4: 形容詞 vs. 副詞基礎與不規則變化
    make_bg(16, "gra3", "gra3_14", 4,
            "The people on the ground were cheering ______ and waving at Orville ______.",
            ["loudly; excitedly", "loud; excited", "louder; exciting", "loudly; excited"], "loudly; excitedly",
            "修飾動作動詞 cheering（歡呼）與 waving（揮手），必須使用『-ly 副詞』loudly 與 excitedly！",
            "Rex 在小考曾寫出『Peter laughed loud ❌』，漏掉副詞字尾 -ly！"),
    make_bg(17, "gra3", "gra3_14", 4,
            "Orville and Wilbur Wright worked very ______ and built a plane that flew ______.",
            ["hard; fast", "hardly; fastly", "hard; fastly", "hardly; fast"], "hard; fast",
            "超級必背同形副詞：hard（努力地）與 fast（快速地）本身就是副詞，完全不加 -ly！",
            "英文裡根本沒有 *fastly 這個字！而 hardly 的意思是『幾乎不』，不是努力地！"),
    make_bg(18, "gra3", "gra3_14", 4,
            "Jane is a ______ singer. She sings very ______.",
            ["good; well", "well; good", "good; goodly", "better; good"], "good; well",
            "第一格修飾名詞 singer 用形容詞 good；第二格修飾動詞 sings 必須用不規則副詞 well！",
            "千萬不能寫『She sings good ❌』！good 的副詞是 well。"),
    make_bg(19, "wr3", "wr3_4", 4,
            "The convenience store and the bus stop are very ______ to my house, too.",
            ["close", "closer", "closest", "closely"], "close",
            "岱崙 W2 作文唯一扣分點！程度副詞『very（非常）』後面必須接『原級形容詞 close（近的）』！",
            "Rex 在考卷上誤寫成『very closer ❌』！沒有跟別人比較時，very 後面絕對不能加 -er。"),
    make_bg(20, "rd6", "rd6_4", 4,
            "Most ______ burn in the atmosphere, but pieces that hit a planet's surface are called ______.",
            ["meteors; meteorites", "meteorites; meteors", "asteroids; comets", "comets; craters"], "meteors; meteorites",
            "在空中大氣層燃燒的叫流星 (meteors)；沒燒完撞上地表的石頭叫隕石 (meteorites，字尾 -ite 表礦石)！",
            "這兩個字順序對調是 Space Ch.4 最常考的閱讀陷阱！"),

    # ⭐ Level 5: 副詞比較級與最高級核心公式
    make_bg(21, "gra3", "gra3_14", 5,
            "The Wright brothers' first plane flew ______ than the glider, and it flew ______ than the glider, too.",
            ["further; more quickly", "more far; quicker", "farther; more quicker", "furthest; most quickly"], "further; more quickly",
            "看到 than 用比較級：不規則副詞 far ➔ further/farther；多音節副詞 quickly ➔ more quickly！",
            "嚴禁寫出 *more quicker（雙重比較）或將 -ly 副詞直接去 y 加 er (*quicker)！"),
    make_bg(22, "gra3", "gra3_14", 5,
            "A person runs fast, a dog runs ______ than a person, but a lion runs ______.",
            ["faster; the fastest", "more faster; the fastest", "faster; fastest", "more fast; the most fast"], "faster; the fastest",
            "岱崙 W4 小考真題！單音節副詞 fast 的比較級是 faster，最高級是 the fastest（必加 the）！",
            "Rex 在考場同時踩了兩個坑：寫成『more faster ❌』又漏掉最高級的『the ❌』！"),
    make_bg(23, "gra3", "gra3_14", 5,
            "Ali uses the Internet ______ than his brother, but his sister uses it ______ of all.",
            ["more regularly; the most regularly", "regularlier; the regularliest", "more regular; the most regular", "most regularly; more regularly"], "more regularly; the most regularly",
            "regularly 是多音節 -ly 副詞，比較級加 more，最高級加 the most！",
            "不能用形容詞 regular 來修飾動詞 uses。"),
    make_bg(24, "gra3", "gra3_14", 5,
            "A duck flew farther ______ an eagle in the sky.",
            ["than", "then", "that", "from"], "than",
            "岱崙 W5 小考真題！比較級後面表示『比...』的連接詞拼寫是 t-h-a-n (than)！",
            "Rex 在考場把 than 誤拼成時間副詞『then (t-h-e-n 然後) ❌』被紅筆圈出扣分！"),
    make_bg(25, "gra3", "gra3_14", 5,
            "A clown laughs horribly, a ghost laughs more horribly than a clown, but a witch ______ the most horribly.",
            ["laughs", "laugh", "laughing", "is laugh"], "laughs",
            "岱崙 W5 小考真題！主詞 a witch 是第三人稱單數，一般現在式動詞必須加 -s (laughs)！",
            "題幹問『How horribly do they laugh?』是複數 they，但造句拆成單數 a clown / a ghost / a witch 時，漏加 s 就扣分！"),

    # ⭐ Level 6: 可數/不可數名詞與 14 大容器量詞
    make_bg(26, "gra3", "gra3_15", 6,
            "There are three ______ of ______ on the plate.",
            ["slices; bread", "slices; breads", "slice; bread", "pieces; breads"], "slices; bread",
            "bread（麵包）是不可數名詞，永遠不加 -s！複數『三片』必須加在前面的量詞 slices 上！",
            "*three slices of breads 是小六段考最愛考的雙重複數陷阱！"),
    make_bg(27, "gra3", "gra3_15", 6,
            "We need a ______ of flour, a ______ of honey, and a ______ of chocolate to make the cake.",
            ["bag; jar; bar", "bar; bottle; bag", "carton; can; slice", "jar; bag; cup"], "bag; jar; bar",
            "課本 p.78-79 黃金量詞配對：一袋麵粉 (a bag of flour)、一罐蜂蜜 (a jar of honey)、一塊長條巧克力 (a bar of chocolate)！",
            "玻璃廣口罐果醬/蜂蜜用 jar；盒裝牛奶/雞蛋用 carton；條塊狀巧克力/肥皂用 bar。"),
    make_bg(28, "gra3", "gra3_15", 6,
            "Put ______ oregano and ______ olives on each round of pizza dough.",
            ["a little; a few", "a few; a little", "many; much", "a slice of; a bar of"], "a little; a few",
            "課本 p.76 食譜原句！oregano（香草粉）不可數配 a little；olives（橄欖）可數複數配 a few！",
            "a little + 不可數名詞；a few + 可數複數名詞，兩者絕對不能顛倒！"),
    make_bg(29, "gra3", "gra3_15", 6,
            "Grandma always drinks a ______ of coffee when she eats a ______ of cake!",
            ["cup; piece", "carton; bar", "packet; jar", "bowl; can"], "cup; piece",
            "熱咖啡裝在有把手的杯子用 a cup of coffee；切塊蛋糕用 a piece of cake！",
            "carton 是紙盒（裝牛奶/雞蛋），bar 是長條塊（裝巧克力）。"),
    make_bg(30, "rd6", "rd6_5", 6,
            "In 1543, ______ said the Sun was at the center, and almost 150 years later, ______ proved it with gravity.",
            ["Copernicus; Isaac Newton", "Galileo; Edwin Hubble", "Isaac Newton; Copernicus", "Edwin Hubble; Galileo"], "Copernicus; Isaac Newton",
            "Space Ch.5 歷史時間軸：1543 年波蘭天文學家哥白尼 (Copernicus) 提出日心說；150 年後英國牛頓 (Newton) 發現重力並數學證明 (proved)！",
            "伽利略 (Galileo) 是 1609 年用望遠鏡觀測木星四衛星；哈伯 (Hubble) 是 1930 年發現銀河系外的其他星系。"),

    # ⭐ Level 7: 假設語氣與金錢花費句型 (Write Right 3 U5)
    make_bg(31, "wr3", "wr3_5", 7,
            "If I ______ 6,000 dollars, I ______ buy a nice present for my mom.",
            ["had; would", "have; will", "had; will", "would have; bought"], "had; would",
            "岱崙 W5 考卷真題！與現在事實相反的假設語氣：If + 過去式 (had)，主要子句必用『would + 原形動詞』！",
            "Rex 在考場曾誤寫『If I had..., I will... ❌』！只要 If 子句是過去式 had，後面絕對不能出現 will！"),
    make_bg(32, "wr3", "wr3_5", 7,
            "If I ______ a millionaire, I would donate money to a charity group.",
            ["were", "am", "will be", "would be"], "were",
            "在與現在事實相反的 If 虛擬子句中，不論主詞是第幾人稱，Be 動詞一律使用『were』！",
            "If 子句裡不能放 would be 或 will be，正式寫作也不用 am。"),
    make_bg(33, "wr3", "wr3_5", 7,
            "A baseball glove and some comic books would ______ me about 70 dollars.",
            ["cost", "spend", "pay", "take"], "cost",
            "先看主詞！主詞是『物品 (A baseball glove and some comic books)』，物花某人多少錢必用『cost + 人 + 錢』！",
            "spend 的主詞必須是『人』（I would spend 70 dollars on...），物品不能當 spend 的主詞！"),
    make_bg(34, "wr3", "wr3_5", 7,
            "With the ______ of the money, I would ______ my best friends to lunch.",
            ["rest; treat", "most; cost", "all; buy", "some; donate"], "rest; treat",
            "兩大高頻片語：With the rest of the money（用剩下的錢）；treat + 人 + to + 餐點/電影（請某人吃.../看...）！",
            "donate 要配 to a charity group；buy 要配 for my friends。"),
    make_bg(35, "wr3", "wr3_5", 7,
            "______ it ______ great to have 300 dollars?",
            ["Wouldn't; be", "Wouldn't; is", "Won't; Ø", "Didn't; be"], "Wouldn't; be",
            "課本 p.43 改錯第 4 題原題！結尾反問句『Wouldn't it be great to...?』，助動詞 Wouldn't 後面必須補上原形 be 動詞！",
            "課本特別警告學生常漏寫 be 變成『*Wouldn't it great to have 300 dollars? ❌』！"),

    # ⭐ Level 8: 科普天文與讀寫進階高頻陷阱 (Space Ch4~5 & RWW6 U5~8)
    make_bg(36, "rd6", "rd6_4", 8,
            "Which meteorite impact happened 65 million years ago in Mexico and caused the dinosaurs to die?",
            ["The Chicxulub meteorite (180 km crater)", "The Tunguska meteorite in Russia (1908)", "Halley's Comet in 1986", "The 21 comet pieces on Jupiter in 1994"], "The Chicxulub meteorite (180 km crater)",
            "希克蘇魯伯隕石 (Chicxulub) 在 6500 萬年前撞擊墨西哥尤卡坦半島，形成 180 公里寬巨坑，塵埃遮日導致恐龍滅絕！",
            "通古斯 (Tunguska) 是 1908 年在俄羅斯西伯利亞空中爆炸燒毀 8000 萬棵樹，沒有造成恐龍滅絕！"),
    make_bg(37, "rd6", "rd6_5", 8,
            "Why can the Hubble Space Telescope take better photos than telescopes on Earth?",
            ["Because it orbits outside Earth's atmosphere.", "Because it is much bigger than any telescope on Earth.", "Because it lands on the Moon to take photos.", "Because it was built by Galileo in 1990."], "Because it orbits outside Earth's atmosphere.",
            "課本 p.23 Discover 專欄原句：哈伯拍照更清晰是因為它位於『地球大氣層之外 (outside Earth's atmosphere)』，不受大氣干擾！",
            "並非因為它體積比地面望遠鏡大，也不是因為它降落在月球上。"),
    make_bg(38, "rd6", "rd6_5", 8,
            "True or False: 'In 1930, Edwin Hubble discovered another universe.'",
            ["False — He discovered another GALAXY (there is only one universe with billions of galaxies).", "True — He found a second universe beyond the Milky Way.", "False — He discovered the four moons of Jupiter.", "True — The Milky Way is the only galaxy."], "False — He discovered another GALAXY (there is only one universe with billions of galaxies).",
            "課本 p.45 是非題第 5 題經典陷阱！哈伯發現的是另一個『星系 (galaxy)』，宇宙 (universe) 只有一個，裡面有數十億個星系！",
            "千萬別把 galaxy（星系）和 universe（宇宙）搞混！"),
    make_bg(39, "rw6", "rw6_7", 8,
            "In Unit 7, which statement about languages is TRUE?",
            ["Zimbabwe has 16 official languages, while Mexico and the U.S. have 0 official languages.", "Spanish is the official language of Mexico because everyone speaks it.", "Most countries in the world (110 countries) have 4 or more official languages.", "India has over 1,000 official languages."], "Zimbabwe has 16 official languages, while Mexico and the U.S. have 0 official languages.",
            "辛巴威有 16 種官方語言（世界最多）；美、墨兩國因從未通過法律 (never passed a law)，官方語言數量為 0！",
            "印度是有超過 1000 種母語 (native languages)，但官方語言只有 2 種 (Hindi & English)；全球有 110 國只有 1 種官方語言。"),
    make_bg(40, "rw6", "rw6_8", 8,
            "In Unit 8 'So Many Questions', which statement about Erico is FALSE?",
            ["Erico speaks with an Australian accent.", "Erico was born in Australia, and his parents were born in Brazil and Portugal.", "Knowing Portuguese helped Erico learn some Italian.", "Rosa first spoke to Erico in Italian."], "Erico speaks with an Australian accent.",
            "課本 p.56 是非題第 7 題！Erico 雖然家人來自澳洲，但他說話帶著『英國腔 (British accent)』，不是澳洲腔！",
            "其他三項皆為課文真實細節（爸巴西、媽葡萄牙、葡語幫他學義語、Rosa 第一句講義語）。"),

    # ⭐ Level 9: 岱崙小考高難度綜合文法陷阱
    make_bg(41, "gra3", "gra3_13", 9,
            "A: 'I have never been to the U.S. Patent Office.' — B: '______'",
            ["Neither have I.", "Neither did I.", "So have I.", "I haven't, too."], "Neither have I.",
            "前句有否定詞 never（從未），且助動詞是現在完成式的『have』，否定倒裝必用『Neither have I.』！",
            "不能用 did（因為前句助動詞是 have），也不能用 So（因為 never 是語意否定）。"),
    make_bg(42, "gra3", "gra3_14", 9,
            "Of all the students in the computer class, Ali types ______, and he finishes his work ______.",
            ["the fastest; the most easily", "the most fast; the easiest", "faster; more easily", "the fastest; the most easy"], "the fastest; the most easily",
            "看到範圍『Of all the students（所有學生當中）』必用最高級副詞：fast ➔ the fastest；easily ➔ the most easily！",
            "fast 不可加 most；修飾動詞 finishes 必須用副詞 the most easily 而非形容詞 the easiest。"),
    make_bg(43, "gra3", "gra3_14", 9,
            "Galileo could see things ______ with his telescope than Lippershey could, and Newton could see ______ of all.",
            ["more clearly; the furthest", "clearlier; the farthest", "more clear; the most far", "most clearly; further"], "more clearly; the furthest",
            "第一格有 than 配多音節副詞比較級 more clearly；第二格有 of all 配不規則副詞最高級 the furthest！",
            "clearly 不能加 -er；far 的最高級是 the furthest / the farthest，不是 *the most far。"),
    make_bg(44, "wr3", "wr3_4", 9,
            "My father always has his suits ______ at the dry cleaner's ______ the street from our house.",
            ["cleaned; across", "clean; cross", "cleaning; across", "to clean; between"], "cleaned; across",
            "課本 p.35 高分句型：『have + 物品 (his suits) + 過去分詞 V-p.p. (cleaned)』表示把西裝送去給人洗；『在...對街』用 across the street from！",
            "西裝是『被洗』所以用過去分詞 cleaned；cross 是動詞，此處需介系詞 across。"),
    make_bg(45, "gra3", "gra3_15", 9,
            "Could you buy two ______ of ______ and three ______ of ______ at the grocery store?",
            ["loaves; bread; cartons; milk", "loafs; breads; carton; milks", "slices; breads; bottles; waters", "bags; flours; jars; honeys"], "loaves; bread; cartons; milk",
            "量詞轉複數（loaf ➔ loaves 兩條吐司、carton ➔ cartons 三盒牛奶），而 of 後方的不可數名詞 bread 與 milk 絕對不加 -s！",
            "breads, milks, waters, flours, honeys 全部都是不可數名詞誤加 s 的嚴重錯誤！"),

    # ⭐ Level 10: 滿分魔王終極秒殺挑戰
    make_bg(46, "tea_midterm", "tea_midterm_1", 10,
            "【魔王改錯】Which sentence has ZERO grammar or spelling mistakes?",
            [
                "A frog can jump far, a rabbit can jump farther than a frog, but a kangaroo can jump the farthest.",
                "A frog can jump far, a rabbit can jump more farther than a frog, but a kangaroo can jump farthest.",
                "A glassblower melts glass in a giant furnes to make metal france for eyeglasses.",
                "The control flag was hidden infront off the big rock."
            ],
            "A frog can jump far, a rabbit can jump farther than a frog, but a kangaroo can jump the farthest.",
            "完全符合三級副詞比較公式：far ➔ farther than a frog ➔ but ... the farthest，冠詞與拼字 100% 滿分！",
            "其他三句分別含有：*more farther / 漏 the、*furnes (應為 furnace) / *france (應為 frames)、*infront off (應為 in front of)！"),
    make_bg(47, "tea_midterm", "tea_midterm_1", 10,
            "【魔王改錯】Which agreement sentence pair is 100% grammatically CORRECT?",
            [
                "Houses didn't have telephones in the 1870s, and neither did offices.",
                "Bell was a famous scientist, and so did Meucci.",
                "Ray didn't pass the quiz, and neither didn't Jim.",
                "Edison invented a light bulb, and Swan did, either."
            ],
            "Houses didn't have telephones in the 1870s, and neither did offices.",
            "前句 didn't have 是過去式一般動詞否定，後句用『neither + 肯定助動詞 did + 主詞 offices』完全正確！",
            "B 選項 was 應配 so was；C 選項 neither 後嚴禁雙重否定 didn't；D 選項肯定句尾應配 too 而非 either。"),
    make_bg(48, "wr3", "wr3_5", 10,
            "【魔王改錯】Which conditional sentence is 100% grammatically CORRECT?",
            [
                "If I had 6,000 dollars, I would spend half of the money on a nice present for my mom.",
                "If I would have 6,000 dollars, I will buy a nice present to my mom.",
                "A new jacket and a comic book would spend me about 800 dollars.",
                "Wouldn't it great if I was have a lot of money?"
            ],
            "If I had 6,000 dollars, I would spend half of the money on a nice present for my mom.",
            "精準結合：If + had, I would spend... + on + present + for my mom，四大考點一次全對！",
            "B 錯在 If 子句放 would 且用 will、buy...to；C 錯在物品當主詞卻用 spend（應為 cost）；D 漏了原形 be 動詞 Wouldn't it be great。"),
    make_bg(49, "rd6", "rd6_4", 10,
            "【跨章節科普綜合】Which scientific fact from Read and Discover 6: Space (Ch.4 & Ch.5) is 100% TRUE?",
            [
                "Comets come from the Kuiper belt and form a long tail of ice and dust when they become hotter near the Sun.",
                "Comets come from the asteroid belt and become colder when they approach the Sun.",
                "The Milky Way is made of billions of comets, and Hubble discovered another universe in 1930.",
                "Galileo discovered the force of gravity in 1543 and proved that the Sun orbits Earth."
            ],
            "Comets come from the Kuiper belt and form a long tail of ice and dust when they become hotter near the Sun.",
            "彗星來自古柏帶 (Kuiper belt) 或深空，靠近太陽時變熱 (become hotter) 釋放冰與塵埃形成數百萬公里長的彗尾！",
            "B 錯在來源與 colder；C 錯在銀河系是恆星 (stars) 組成且哈伯發現的是 galaxy；D 發現重力並證明地球繞日的是牛頓 (Newton)。"),
    make_bg(50, "rw6", "rw6_6", 10,
            "【跨單元讀寫綜合】Which statement about Reading with Writing 6 (Units 5 ~ 8) is 100% TRUE?",
            [
                "In orienteering, a racer who crosses the finish line first without a full control card does NOT win the race.",
                "In 'Lost and Found', the fog was high above the top of the hill, so the family couldn't read their map.",
                "Spanish is the official language of Mexico because the government passed a law.",
                "In 'So Many Questions', Erico thought Rosa was rude and unfriendly because she interrupted him."
            ],
            "In orienteering, a racer who crosses the finish line first without a full control card does NOT win the race.",
            "定向越野必須集滿全卡所有控制點 (a full card with all 18 controls) 才能獲勝，漏打卡就算第一個衝線也會輸！",
            "B 山頂在霧之上 (above the fog)；C 墨西哥未立法無官方語言；D Erico 認為發問是 Rosa 表達友善 (friendly) 的方式。")
]


def main():
    data = load_existing_english_data()

    # 1. 重組 Books：將六上期中考 5 大書系置頂，並加入 `tea_midterm`
    midterm_books = [
        {
            "book_id": "gra3",
            "book_name": "📘 Oxford Discover Grammar 3 (六上期中考 U13~U15)",
            "is_midterm": True
        },
        {
            "book_id": "wr3",
            "book_name": "📝 Write Right Level 3 (六上期中考 U4~U5)",
            "is_midterm": True
        },
        {
            "book_id": "rw6",
            "book_name": "📖 Reading with Writing Level 6 (六上期中考 U5~U8)",
            "is_midterm": True
        },
        {
            "book_id": "rd6",
            "book_name": "🚀 Read and Discover 6: Space (六上期中考 Ch4~Ch5)",
            "is_midterm": True
        },
        {
            "book_id": "tea_midterm",
            "book_name": "🏆 岱崙 3C 考卷真題與 OD3 必考單字 (U13~U14)",
            "is_midterm": True
        }
    ]
    other_books = [
        {
            "book_id": "od3",
            "book_name": "📚 Oxford Discover 3 (延伸單元 U7~U8)",
            "is_midterm": False
        },
        {
            "book_id": "tiger_5b",
            "book_name": "📚 Tiger 五下歷史單字庫",
            "is_midterm": False
        }
    ]
    data["books"] = midterm_books + other_books

    # 2. 注入新增的 Vocabulary, Grammar, Quizzes 與 Brain Gym
    existing_vocab_ids = {v["id"] for v in data["vocabulary"]}
    for v in NEW_MIDTERM_VOCAB:
        if v["id"] in existing_vocab_ids:
            data["vocabulary"] = [x for x in data["vocabulary"] if x["id"] != v["id"]]
        data["vocabulary"].append(v)

    existing_gra_ids = {g["id"] for g in data["grammar"]}
    for g in NEW_MIDTERM_GRAMMAR:
        if g["id"] in existing_gra_ids:
            data["grammar"] = [x for x in data["grammar"] if x["id"] != g["id"]]
        data["grammar"].append(g)

    # 移除舊的 brain_gym 與我們即將覆寫的 q_m / q_tea / bg_mid 題目
    new_q_ids = {q["id"] for q in NEW_MIDTERM_QUIZZES} | {b["id"] for b in MIDTERM_BRAIN_GYM}
    data["quizzes"] = [
        q for q in data["quizzes"]
        if q.get("type") != "brain_gym" and q["id"] not in new_q_ids
    ]
    data["quizzes"].extend(NEW_MIDTERM_QUIZZES)
    data["quizzes"].extend(MIDTERM_BRAIN_GYM)

    # 3. 更新 12 個期中考單元的完整課文 (reading_content)
    midterm_unit_ids = set(MIDTERM_FULL_READINGS.keys())
    data["reading_content"] = [
        r for r in data["reading_content"]
        if r["unit_id"] not in midterm_unit_ids
    ]
    for uid, passages in MIDTERM_FULL_READINGS.items():
        if uid.startswith("gra3"):
            bid = "gra3"
        elif uid.startswith("wr3"):
            bid = "wr3"
        elif uid.startswith("rw6"):
            bid = "rw6"
        elif uid.startswith("rd6"):
            bid = "rd6"
        else:
            bid = "tea_midterm"
        for p in passages:
            data["reading_content"].append({
                "book_id": bid,
                "unit_id": uid,
                "sequence": p["sequence"],
                "section_title": p["section_title"],
                "eng": p["eng"],
                "chi": p["chi"],
                "key_sentences": p.get("key_sentences", []),
                "exp_eng": "",
                "exp_chi": ""
            })

    # 4. 重組與清理 Units：標註 12 個期中考單元，並移除完全空白的佔位單元
    MIDTERM_UNIT_META = {
        "gra3_13": ("gra3", "🔥 Unit 13: Making History (倒裝與附和句 So / Too / Either / Neither)", "ODG3_U13", "How do inventions change our lives? — So, Too, Either, Neither"),
        "gra3_14": ("gra3", "🔥 Unit 14: Success Stories (副詞形成與三級比較級/最高級)", "ODG3_U14", "What makes a success story? — Comparative & Superlative Adverbs"),
        "gra3_15": ("gra3", "🔥 Unit 15: Tasty Treats (可數/不可數名詞與 14 大計量片語)", "ODG3_U15", "Where does our food come from? — Count/Noncount & Measure Phrases"),
        "wr3_4": ("wr3", "🔥 Unit 4: Around My Neighborhood (社區空間描寫與現在完成式)", "WR3_U04", "Writing Task: Write about your neighborhood (have lived for / on foot)"),
        "wr3_5": ("wr3", "🔥 Unit 5: If I Had a Lot of Money (與現在事實相反的假設語氣)", "WR3_U05", "Writing Task: What would you do if you had 300 / 6000 dollars?"),
        "rw6_5": ("rw6", "🔥 Unit 5: Lost and Found (時空背景分析 Setting 與迷霧健行)", "RWW6_U05", "Reading Goal: Identify and Analyze the Setting (Time, Place & Weather)"),
        "rw6_6": ("rw6", "🔥 Unit 6: The World of Orienteering (定向越野與視覺圖表 Visuals)", "RWW6_U06", "Reading Goal: Use Visuals (Diagrams, Control Flags & 18-Box Card)"),
        "rw6_7": ("rw6", "🔥 Unit 7: Languages We Use (母語、官方語言與長條圖判讀)", "RWW6_U07", "Reading Goal: Understand a Bar Graph (Official Languages in 196 Countries)"),
        "rw6_8": ("rw6", "🔥 Unit 8: So Many Questions (跨文化雙語背景與預測情節)", "RWW6_U08", "Reading Goal: Make Predictions (Clues + Knowledge ➔ Future Events)"),
        "rd6_4": ("rd6", "🔥 Chapter 4: Rocks and Ice (小行星帶、古柏帶、彗星與隕石)", "SPACE_CH04", "CLIL Astronomy: Asteroids, Comets, Meteors, Meteorites & Chicxulub"),
        "rd6_5": ("rd6", "🔥 Chapter 5: Astronomy (天文學史：哥白尼、伽利略、牛頓與哈伯)", "SPACE_CH05", "CLIL Astronomy: Ancient Temples, Gravity, Milky Way & Hubble Telescope"),
        "tea_midterm_1": ("tea_midterm", "🔥 Week 2~5 考卷特訓：OD3 U13~14 簡單機械與吹玻璃單字 + 滿分範文", "TEA_QUIZ_REVIEW", "Tiger English Academy 3C Quiz 真題單字、三級比較長句與滿分作文")
    }

    # 確保 tea_midterm_1 存在於 units
    existing_u_map = {u["unit_id"]: u for u in data["units"]}
    for uid, (bid, title, mid_id, bq) in MIDTERM_UNIT_META.items():
        existing_u_map[uid] = {
            "book_id": bid,
            "unit_id": uid,
            "unit_title": title,
            "big_question": bq,
            "is_midterm": True,
            "midterm_unit_id": mid_id
        }

    # 篩選非空白單元，並讓期中考單元排在各書最前面
    active_unit_ids = (
        {v["unit_id"] for v in data["vocabulary"]}
        | {r["unit_id"] for r in data["reading_content"]}
        | {g["unit_id"] for g in data["grammar"]}
        | {q["unit_id"] for q in data["quizzes"] if q.get("type") != "brain_gym"}
    )

    cleaned_units = []
    # 先放 12 個期中考單元
    for uid in MIDTERM_UNIT_META.keys():
        cleaned_units.append(existing_u_map[uid])

    # 再放其他有內容的單元
    for u in data["units"]:
        uid = u["unit_id"]
        if uid in MIDTERM_UNIT_META:
            continue
        if uid in active_unit_ids:
            u["is_midterm"] = False
            cleaned_units.append(u)

    data["units"] = cleaned_units

    # 更新 metadata
    data["metadata"] = {
        "version": "2.0.0-midterm-unified",
        "generated_at": "2026-10-20",
        "total_books": len(data["books"]),
        "total_units": len(data["units"]),
        "total_vocab": len(data["vocabulary"]),
        "total_grammar": len(data["grammar"]),
        "total_reading": len(data["reading_content"]),
        "total_quizzes": len(data["quizzes"])
    }

    # 寫回 english_data.js
    js_content = (
        "/**\n"
        " * 六年級英語特訓系統 — 全域資料層 (v2.0 六上期中考 12 單元深度整合版)\n"
        " * 包含：7大記憶錨點單字卡、100% 課本完整原文與必考句標註、文法避坑卡、雙軌測驗與 50 題晨間體操秒殺題庫\n"
        " */\n"
        "const ENGLISH_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
        "window.ENGLISH_DATA = ENGLISH_DATA;\n\n"
        "if (typeof module !== 'undefined' && module.exports) {\n"
        "  module.exports = ENGLISH_DATA;\n"
        "}\n"
    )

    with open(ENGLISH_DATA_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("Successfully generated upgraded english_data.js!")
    print(json.dumps(data["metadata"], indent=2))


if __name__ == "__main__":
    main()
