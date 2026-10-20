# -*- coding: utf-8 -*-
"""
build_midterm_data.py
全面解析期中考 11 個單元的高保真內容，產出純靜態前端資料庫 midterm_data.js
特點：
1. 精簡單元名稱為小學生一眼看懂的 "Unit XX: 標題"
2. 課文分句精讀 (Sentence Shadowing) 採用純正課本課文，嚴格清洗任何註腳與括號雜質
3. 每一句英文均附帶地道繁體中文翻譯，支援前台一鍵展開
4. 零打字點詞抓錯 (Mistake Buster)：精準單詞索引定位、零重複、零中文雜質混入
5. 紙筆/語音雙軌測驗 (Dual Quiz)：支援聽寫、填空、選擇(含選項渲染)、改寫，並附帶針對性三段式詳解
"""

import os
import re
import json
import yaml

WORKSPACE = r"c:\@植善課業\AI\英語學習網頁"
TARGET_JS = os.path.join(WORKSPACE, "midterm_data.js")

FILES = [
    {
        "id": "ODG3_U13",
        "book": "Oxford Discover Grammar 3",
        "display_title": "Unit 13: Making History",
        "category": "文法專修",
        "category_icon": "📘",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\02_Oxford_Discover_Grammar_3\Unit_13_Making_History.md")
    },
    {
        "id": "ODG3_U14",
        "book": "Oxford Discover Grammar 3",
        "display_title": "Unit 14: Success Stories",
        "category": "文法專修",
        "category_icon": "📘",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\02_Oxford_Discover_Grammar_3\Unit_14_Success_Stories.md")
    },
    {
        "id": "ODG3_U15",
        "book": "Oxford Discover Grammar 3",
        "display_title": "Unit 15: Tasty Treats",
        "category": "文法專修",
        "category_icon": "📘",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\02_Oxford_Discover_Grammar_3\Unit_15_Tasty_Treats.md")
    },
    {
        "id": "WR3_U04",
        "book": "Write Right Level 3",
        "display_title": "Unit 4: Around My Neighborhood",
        "category": "寫作專攻",
        "category_icon": "📝",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\04_Write_Right_3\Unit_04_Around_My_Neighborhood.md")
    },
    {
        "id": "WR3_U05",
        "book": "Write Right Level 3",
        "display_title": "Unit 5: If I Had a Lot of Money",
        "category": "寫作專攻",
        "category_icon": "📝",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\04_Write_Right_3\Unit_05_If_I_Had_a_Lot_of_Money.md")
    },
    {
        "id": "SPACE_CH04",
        "book": "Oxford Read and Discover 6: Space",
        "display_title": "Chapter 4: Rocks and Ice",
        "category": "科普長篇",
        "category_icon": "🚀",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\05_Read_and_Discover_6_Space\Chapter_04_Rocks_and_Ice.md")
    },
    {
        "id": "SPACE_CH05",
        "book": "Oxford Read and Discover 6: Space",
        "display_title": "Chapter 5: Astronomy",
        "category": "科普長篇",
        "category_icon": "🚀",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\05_Read_and_Discover_6_Space\Chapter_05_Astronomy.md")
    },
    {
        "id": "RWW6_U05",
        "book": "Reading with Writing Level 6",
        "display_title": "Unit 5: Lost and Found",
        "category": "讀寫進階",
        "category_icon": "📖",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\03_Reading_with_Writing_6\Unit_05_Travel_and_Transport.md")
    },
    {
        "id": "RWW6_U06",
        "book": "Reading with Writing Level 6",
        "display_title": "Unit 6: The World of Orienteering",
        "category": "讀寫進階",
        "category_icon": "📖",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\03_Reading_with_Writing_6\Unit_06_Amazing_Journeys.md")
    },
    {
        "id": "RWW6_U07",
        "book": "Reading with Writing Level 6",
        "display_title": "Unit 7: Languages We Use",
        "category": "讀寫進階",
        "category_icon": "📖",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\03_Reading_with_Writing_6\Unit_07_A_World_of_Words.md")
    },
    {
        "id": "RWW6_U08",
        "book": "Reading with Writing Level 6",
        "display_title": "Unit 8: So Many Questions",
        "category": "讀寫進階",
        "category_icon": "📖",
        "file": os.path.join(WORKSPACE, r"六年級上\課本\03_Reading_with_Writing_6\Unit_08_Dictionaries_and_Search.md")
    }
]

# 1. 精準純淨課文與標準中文對照資料庫
CURATED_PASSAGES = {
    "ODG3_U13": [
        {
            "section_title": "電話發明史 (The History of the Telephone)",
            "sentences": [
                {"en": "In the 19th century, Alexander Graham Bell was working on a new invention.", "zh": "在 19 世紀，亞歷山大·格拉漢姆·貝爾正在研發一項新發明。"},
                {"en": "He was trying to invent a telephone.", "zh": "他當時正試圖發明電話。"},
                {"en": "Other scientists were trying to invent telephones, too.", "zh": "其他科學家當時也正試圖發明電話。"},
                {"en": "Antonio Meucci and Johann Philipp Reis made telephone machines.", "zh": "安東尼奧·梅烏奇與約翰·菲利普·雷斯製作了電話機器。"},
                {"en": "So did Elisha Gray.", "zh": "以利沙·格雷也是。"},
                {"en": "On February 14, 1876, Gray's invention was ready.", "zh": "1876 年 2 月 14 日，格雷的發明準備好了。"},
                {"en": "Bell's invention was ready, too.", "zh": "貝爾的發明也準備好了。"},
                {"en": "Gray hurried to the U.S. Patent Office to get a licence for his invention.", "zh": "格雷匆忙趕往美國專利局，為他的發明申請專利許可。"},
                {"en": "So did Bell.", "zh": "貝爾也是。"},
                {"en": "But Bell got there first.", "zh": "但貝爾搶先一步抵達。"},
                {"en": "Gray did not become rich and famous.", "zh": "格雷並未因此變得富有和出名。"},
                {"en": "Meucci didn't become rich and famous, either.", "zh": "梅烏奇也沒有變得富有和出名。"},
                {"en": "Neither did Reis.", "zh": "雷斯也是。"},
                {"en": "But we remember them today as important people in the history of the telephone.", "zh": "但今天我們將他們銘記為電話歷史上的重要人物。"}
            ]
        },
        {
            "section_title": "電燈泡發明歷程 (Inventing the Light Bulb)",
            "sentences": [
                {"en": "In 1878, Thomas Edison was trying to invent a light bulb.", "zh": "1878 年，湯瑪斯·愛迪生正試圖發明電燈泡。"},
                {"en": "Joseph Swan was trying to invent a light bulb, too.", "zh": "約瑟夫·斯旺當時也正試圖發明電燈泡。"},
                {"en": "Edison and Swan weren't the only scientists to experiment with light bulbs.", "zh": "愛迪生和斯旺並不是唯一實驗電燈泡的科學家。"},
                {"en": "Other scientists were experimenting with light bulbs, too.", "zh": "其他科學家當時也正在實驗電燈泡。"},
                {"en": "British inventor Humphry Davy invented a light bulb.", "zh": "英國發明家漢弗里·戴維發明了電燈泡。"},
                {"en": "So did Canadian inventor Henry Woodward.", "zh": "加拿大發明家亨利·伍德沃德也是。"},
                {"en": "Swan's light bulb was a success.", "zh": "斯旺的電燈泡獲得了成功。"},
                {"en": "So was Edison's light bulb.", "zh": "愛迪生的電燈泡也是。"},
                {"en": "Swan's light bulb worked for a long time.", "zh": "斯旺的電燈泡運作了很長時間。"},
                {"en": "So did Edison's light bulb.", "zh": "愛迪生的電燈泡也是。"},
                {"en": "Swan got a patent for his invention.", "zh": "斯旺為他的發明取得了專利。"},
                {"en": "Edison got a patent, too.", "zh": "愛迪生也取得了專利。"},
                {"en": "Swan and Edison weren't friends, but their inventions changed the world!", "zh": "斯旺和愛迪生並不是朋友，但他們的發明改變了世界！"}
            ]
        }
    ],
    "ODG3_U14": [
        {
            "section_title": "萊特兄弟的飛行夢想 (The Wright Brothers' Dream of Flight)",
            "sentences": [
                {"en": "Orville and Wilbur Wright wanted to fly when they were small boys.", "zh": "奧維爾和威爾伯·萊特小時候就想要飛行。"},
                {"en": "They liked to play with flying toys.", "zh": "他們喜歡玩飛行玩具。"},
                {"en": "When the boys were older, they decided to make a flying machine.", "zh": "當男孩子們長大後，他們決定製造一架飛行機器。"},
                {"en": "In 1900, they built a glider.", "zh": "1900 年，他們造了一架滑翔機。"},
                {"en": "It didn't fly very quickly, and it didn't fly very far.", "zh": "它飛得不是很快，也飛得不是很遠。"},
                {"en": "In 1903, Orville and Wilbur successfully made the world's first airplane flight.", "zh": "1903 年，奧維爾與威爾伯成功實現了世界上第一次飛機飛行。"},
                {"en": "Their plane flew further than the glider.", "zh": "他們的飛機比滑翔機飛得更遠。"},
                {"en": "It flew more quickly than the glider, too.", "zh": "它飛得也比滑翔機更快。"},
                {"en": "But it only stayed in the sky for one minute.", "zh": "但它只在空中停留了一分鐘。"},
                {"en": "The Wright brothers made another plane in 1908.", "zh": "萊特兄弟在 1908 年又製造了另一架飛機。"},
                {"en": "It was their best machine.", "zh": "那是他們最好的機器。"},
                {"en": "It flew the most quickly.", "zh": "它飛得最快。"},
                {"en": "It flew the furthest, too.", "zh": "它飛得也最遠。"},
                {"en": "People watched excitedly as the plane stayed in the air for thirty minutes.", "zh": "當飛機在空中停留三十分鐘時，人們興奮地注視著。"},
                {"en": "It was a wonderful sight!", "zh": "那是一幅美妙的景象！"}
            ]
        },
        {
            "section_title": "望遠鏡發明與太空探索 (The Invention of Telescopes)",
            "sentences": [
                {"en": "Hans Lippershey invented the first telescope in 1608.", "zh": "漢斯·利伯希在 1608 年發明了第一架望遠鏡。"},
                {"en": "He couldn't see very far with his telescope, but he could see things quite clearly.", "zh": "用他的望遠鏡看不太遠，但他能看得很清楚。"},
                {"en": "In 1609, Galileo made another telescope.", "zh": "1609 年，伽利略造了另一架望遠鏡。"},
                {"en": "Galileo could see things more clearly with his telescope than he could with Lippershey's telescope.", "zh": "伽利略用他的望遠鏡比用利伯希的望遠鏡能看得更清晰。"},
                {"en": "Galileo could see further with his telescope, too.", "zh": "伽利略用他的望遠鏡也能看得更遠。"},
                {"en": "He used his telescope to look into space and see the surface of the moon!", "zh": "他用望遠鏡觀測太空，並看見了月球表面！"},
                {"en": "Isaac Newton invented a new kind of telescope in 1670.", "zh": "艾薩克·牛頓在 1670 年發明了一種新型望遠鏡。"},
                {"en": "With his new telescope, he could see the furthest of all, and he could see things the most clearly.", "zh": "用他的新望遠鏡，他看得最遠，也看得最清晰。"},
                {"en": "Newton used his telescope to study the planets.", "zh": "牛頓用他的望遠鏡來研究行星。"}
            ]
        }
    ],
    "ODG3_U15": [
        {
            "section_title": "披薩的美食傳奇 (The Story of Pizza)",
            "sentences": [
                {"en": "Pizza is one of the most famous foods in the world.", "zh": "披薩是世界上最著名的食物之一。"},
                {"en": "Long ago, people in Greece and Rome ate flat bread with olive oil and herbs.", "zh": "很久以前，希臘和羅馬的人們吃塗有橄欖油和香草的扁麵包。"},
                {"en": "In the 18th century, people in Naples started to put tomatoes on their dough.", "zh": "在 18 世紀，拿坡里的人們開始在麵團上放番茄。"},
                {"en": "In 1889, a baker made a special pizza for Queen Margherita of Italy.", "zh": "1889 年，一位烘焙師為義大利瑪格麗特王后製作了一款特色披薩。"},
                {"en": "He used red tomatoes, white mozzarella cheese, and green basil.", "zh": "他使用了紅番茄、白莫扎瑞拉起司和綠羅勒。"},
                {"en": "These were the colors of the Italian flag.", "zh": "這些是義大利國旗的顏色。"},
                {"en": "Today, people bake pizzas in hot wood ovens all over the world.", "zh": "今天，世界各地的人們在炎熱的燃木烤爐中烘烤披薩。"}
            ]
        },
        {
            "section_title": "艾蜜莉的廚房準備 (Emily in the Kitchen)",
            "sentences": [
                {"en": "Emily is in the kitchen making lunch for her family.", "zh": "艾蜜莉在廚房裡為家人準備午餐。"},
                {"en": "There is a bowl of apples on the table and there is a bar of chocolate, too.", "zh": "桌上有一碗蘋果，還有一塊巧克力。"},
                {"en": "There are some slices of bread on a plate.", "zh": "盤子裡有一些切片麵包。"},
                {"en": "There is a bag of flour and a jar of honey in the cupboard.", "zh": "櫥櫃裡有一袋麵粉和一罐蜂蜜。"},
                {"en": "There is a bottle of water in the fridge and there is a carton of milk, too.", "zh": "冰箱裡有一瓶水，還有一盒牛奶。"},
                {"en": "Emily drinks a glass of milk before she starts cooking.", "zh": "艾蜜莉在開始做飯前喝了一杯牛奶。"}
            ]
        }
    ],
    "WR3_U04": [
        {
            "section_title": "我的溫馨便利社區 (Around My Neighborhood)",
            "sentences": [
                {"en": "Have you ever been to my neighborhood?", "zh": "你曾來過我的社區嗎？"},
                {"en": "I have lived in my neighborhood for three years, and I really like living here.", "zh": "我在我的社區住了三年，我真的很喜歡住在這裡。"},
                {"en": "The subway station and the bus stop are very close to my house.", "zh": "地鐵站和公車站離我家非常近。"},
                {"en": "I can get to my school in ten minutes on foot.", "zh": "我步行十分鐘就能到達我的學校。"},
                {"en": "There are many stores across the street from my house.", "zh": "我家對街有許多商店。"},
                {"en": "There is a bakery next to the convenience store.", "zh": "便利商店隔壁有一家麵包店。"},
                {"en": "Best of all, my neighborhood has a beautiful green park.", "zh": "最棒的是，我的社區有一座美麗的綠色公園。"},
                {"en": "I can play soccer with my friends there every weekend.", "zh": "我每週末都可以在那裡和朋友們踢足球。"}
            ]
        }
    ],
    "WR3_U05": [
        {
            "section_title": "如果我有三百美元 (What Would You Do with 300 Dollars?)",
            "sentences": [
                {"en": "If I had 300 dollars, I would spend the money wisely.", "zh": "如果我有三百美元，我會明智地花這筆錢。"},
                {"en": "First, I would buy a nice present for my mom.", "zh": "首先，我會為媽媽買一份精美的禮物。"},
                {"en": "She works hard every day, so I would get her a warm scarf.", "zh": "她每天工作很辛苦，所以我想給她買一條溫暖的圍巾。"},
                {"en": "With some of the money, I would buy a baseball glove and some comic books.", "zh": "用其中的一些錢，我會買一個棒球手套和幾本漫畫書。"},
                {"en": "They would cost me about 70 dollars.", "zh": "它們大約會花費我 70 美元。"},
                {"en": "Then, I would treat my best friends to lunch at a hamburger restaurant.", "zh": "然後，我會在漢堡店請我最好的朋友們吃午餐。"},
                {"en": "With the rest of the money, I would open up a bank account and save it.", "zh": "用剩下的錢，我會開一個銀行帳戶存起來。"}
            ]
        }
    ],
    "SPACE_CH04": [
        {
            "section_title": "太陽系中的岩石與冰塊 (Rocks and Ice in the Solar System)",
            "sentences": [
                {"en": "Between Mars and Jupiter, there are millions of rocks orbiting the Sun.", "zh": "在火星和木星之間，有數以百萬計的岩石圍繞著太陽運行。"},
                {"en": "This region is called the asteroid belt.", "zh": "這個區域被稱為小行星帶。"},
                {"en": "Some asteroids are as small as houses, while others are many kilometers across.", "zh": "有些小行星小如房屋，而有些則有幾公里寬。"},
                {"en": "Further away in space, beyond Neptune, there are huge pieces of ice called comets.", "zh": "在太空更遠處、海王星之外，有被稱為彗星的巨大冰塊。"},
                {"en": "When a comet approaches the Sun, heat releases dust and ice, forming a glowing tail millions of kilometers long.", "zh": "當彗星接近太陽時，熱量釋放出塵埃和冰，形成數百萬公里長的發光彗尾。"},
                {"en": "Halley's Comet orbits the Sun every seventy-five years.", "zh": "哈雷彗星每 75 年繞太陽一圈。"},
                {"en": "A meteor is a piece of rock or dust that burns brightly as it enters a planet's atmosphere.", "zh": "流星是當進入行星大氣層時劇烈燃燒的岩石或塵埃碎片。"},
                {"en": "If a piece of space rock survives and hits the ground, it is called a meteorite.", "zh": "如果太空岩石碎片存留並撞擊地面，它被稱為隕石。"}
            ]
        }
    ],
    "SPACE_CH05": [
        {
            "section_title": "觀測星空與現代天文學 (Watching the Skies and Modern Astronomy)",
            "sentences": [
                {"en": "For thousands of years, people have looked up at the stars and wondered about the universe.", "zh": "數千年來，人們仰望星空並對宇宙充滿好奇。"},
                {"en": "Early astronomers thought the Earth was at the center of the solar system.", "zh": "早期的天文學家認為地球處於太陽系的中心。"},
                {"en": "Nicolaus Copernicus discovered that the planets orbit the Sun.", "zh": "尼古拉·哥白尼發現行星是圍繞著太陽運行的。"},
                {"en": "Galileo built a telescope and discovered four moons orbiting Jupiter.", "zh": "伽利略建造了望遠鏡，發現了繞木星運行的四顆衛星。"},
                {"en": "Today, astronomers use giant telescopes to look deep into space.", "zh": "今天，天文學家使用巨型望遠鏡觀測深空。"},
                {"en": "The Hubble Space Telescope orbits high above Earth's atmosphere.", "zh": "哈伯太空望遠鏡在地球大氣層高處軌道運行。"},
                {"en": "It takes clear photos of distant stars, nebulae, and galaxies.", "zh": "它拍攝遙遠恆星、星雲和星系的清晰照片。"}
            ]
        }
    ],
    "RWW6_U05": [
        {
            "section_title": "迷霧中的山林探險 (Lost and Found on the Trail)",
            "sentences": [
                {"en": "One foggy morning, Jaya and her family went hiking.", "zh": "一個起霧的早晨，佳雅和她的家人去健行。"},
                {"en": "Their goal was a hill with a tall, crooked tree on top.", "zh": "他們的目標是一座山頂上有一棵高大彎曲樹木的山丘。"},
                {"en": "They walked past a log bench on the left side of the trail.", "zh": "他們走過了步道左側的一張原木長凳。"},
                {"en": "Manoj realized they should have turned right instead of going straight.", "zh": "馬諾傑意識到他們應該右轉而不是直走。"},
                {"en": "They climbed up a smaller hill and discovered the top was above the fog.", "zh": "他們爬上一座較小的山丘，發現山頂高於濃霧之上。"},
                {"en": "They looked at the map and saw the lighthouse to the south near town.", "zh": "他們看著地圖，看見城鎮附近南方的燈塔。"},
                {"en": "Then they saw the hill with the crooked tree to the northeast.", "zh": "接著他們看見東北方那座有著彎曲大樹的山丘。"},
                {"en": "It looked like an island in a sea of clouds.", "zh": "它看起來就像雲海中的一座島嶼。"}
            ]
        }
    ],
    "RWW6_U06": [
        {
            "section_title": "定向越野的冒險世界 (The World of Orienteering)",
            "sentences": [
                {"en": "In the sport of orienteering, racers use a map and compass to find stations called controls.", "zh": "在定向越野運動中，參賽者使用地圖和指南針尋找稱為「控制點」的站點。"},
                {"en": "A special red and white flag marks each control.", "zh": "每個控制點都標有特殊的紅白相間旗幟。"},
                {"en": "Controls may be in front of a big rock or behind a tree.", "zh": "控制點可能位在巨石前方或大樹後面。"},
                {"en": "At each control, racers mark a card they carry with them.", "zh": "在每個控制點，參賽者會在隨身攜帶的卡片上做記號。"},
                {"en": "The winner is not simply the fastest runner, but the next person to finish with a full card.", "zh": "獲勝者不僅僅是跑最快的人，而是打滿全卡所有控制點並率先抵達終點的人。"},
                {"en": "In orienteering, you will likely run along a river, climb over rocks, and go up and down hills.", "zh": "在定向越野中，你可能會沿著河邊奔跑、爬過岩石，並在山丘間上下穿梭。"}
            ]
        }
    ],
    "RWW6_U07": [
        {
            "section_title": "我們使用的語言世界 (Languages We Use)",
            "sentences": [
                {"en": "Everyone is a native speaker of their first language learned at home.", "zh": "每個人都是自己在家中學到的第一語言的母語使用者。"},
                {"en": "An official language is the one used by the government of a country.", "zh": "官方語言是一個國家政府所使用的語言。"},
                {"en": "A country has to pass a law to make a language official.", "zh": "一個國家必須通過法律才能使某種語言成為官方語言。"},
                {"en": "Mexico never passed a law, so it has no official language.", "zh": "墨西哥從未通過相關法律，因此沒有官方語言。"},
                {"en": "Zimbabwe has the most official languages in the world, with sixteen!", "zh": "辛巴威擁有世界上最多的官方語言，高達十六種！"},
                {"en": "Hindi and English are the two official languages of India.", "zh": "印地語和英語是印度的兩種官方語言。"},
                {"en": "People who cannot hear or speak use sign languages to communicate with their hands.", "zh": "聽不見或無法說話的人使用手語透過雙手來溝通。"}
            ]
        }
    ],
    "RWW6_U08": [
        {
            "section_title": "夏日校園的雙語對話 (So Many Questions)",
            "sentences": [
                {"en": "Rosa walked through the door, carrying a big pile of drawing paper and art supplies.", "zh": "羅莎走過門口，抱著一大疊圖畫紙和美術用品。"},
                {"en": "She spoke Italian at home and asked Erico a lot of questions.", "zh": "她在家說義大利語，並問了埃里科許多問題。"},
                {"en": "Erico's name is Portuguese, and his family is from Australia.", "zh": "埃里科的名字是葡萄牙文，而他的家人來自澳洲。"},
                {"en": "His dad moved there from Brazil, and his mom is from Portugal.", "zh": "他的爸爸從巴西搬到那裡，而他的媽媽來自葡萄牙。"},
                {"en": "Speaking Portuguese helped Erico learn some Italian.", "zh": "會說葡萄牙語幫助埃里科學會了一些義大利語。"},
                {"en": "Erico realized that asking so many questions was Rosa's way of being friendly.", "zh": "埃里科明白問這麼多問題是羅莎表達友善的方式。"},
                {"en": "He helped her pick up her paper, paint brushes, and colored pencils.", "zh": "他幫她撿起圖畫紙、畫筆和彩色鉛筆。"}
            ]
        }
    ]
}

# 2. 11 個單元 100% 純淨單字庫 (附音標、音節、詞性、中文、例句與拼寫提醒，完全杜絕文法公式或中文混入英文單字欄)
CURATED_VOCAB = {
    "ODG3_U13": [
        {"word": "invention", "phonetic": "/ɪnˈvɛnʃən/", "syllables": "in-ven-tion", "pos": "n.", "meaning": "發明；發明物", "example": "On February 14, 1876, Gray's invention was ready.", "note": "字尾為 -tion，動詞原形為 invent。"},
        {"word": "scientist", "phonetic": "/ˈsaɪəntɪst/", "syllables": "sci-en-tist", "pos": "n.", "meaning": "科學家", "example": "Other scientists were trying to invent telephones, too.", "note": "注意開頭 sci- 的 c 不發音，切勿漏寫 c。"},
        {"word": "patent", "phonetic": "/ˈpætənt/", "syllables": "pat-ent", "pos": "n.", "meaning": "專利；專利權", "example": "Swan got a patent for his invention.", "note": "搭配 get a patent for... (取得...的專利)。"},
        {"word": "licence", "phonetic": "/ˈlaɪsəns/", "syllables": "li-cence", "pos": "n.", "meaning": "許可證；執照", "example": "Gray hurried to get a licence for his invention.", "note": "英式拼法為 licence，美式常拼作 license。"},
        {"word": "experiment", "phonetic": "/ɪkˈspɛrɪmənt/", "syllables": "ex-per-i-ment", "pos": "v./n.", "meaning": "做實驗；實驗", "example": "Other scientists were experimenting with light bulbs, too.", "note": "搭配介系詞 experiment with (用...做實驗)。"},
        {"word": "light bulb", "phonetic": "/ˈlaɪt ˌbʌlb/", "syllables": "light bulb", "pos": "n.", "meaning": "電燈泡", "example": "Thomas Edison was trying to invent a light bulb.", "note": "light 中的 gh 不發音；bulb 尾音為 b。"},
        {"word": "famous", "phonetic": "/ˈfeɪməs/", "syllables": "fa-mous", "pos": "adj.", "meaning": "著名的；出名的", "example": "Gray did not become rich and famous.", "note": "字尾為 -ous，勿拼成 famus。"},
        {"word": "history", "phonetic": "/ˈhɪstəri/", "syllables": "his-to-ry", "pos": "n.", "meaning": "歷史", "example": "They are important people in the history of the telephone.", "note": "in the history of... (在...的歷史上)。"},
        {"word": "either", "phonetic": "/ˈiːðər/", "syllables": "ei-ther", "pos": "adv.", "meaning": "也不（用於否定句尾）", "example": "Meucci didn't become rich and famous, either.", "note": "用於否定句尾，前面通常加逗號。"},
        {"word": "neither", "phonetic": "/ˈniːðər/", "syllables": "nei-ther", "pos": "adv.", "meaning": "也不（用於否定倒裝句首）", "example": "Meucci didn't become rich. Neither did Reis.", "note": "n + either，放在句首時後面必須倒裝（Neither + 助動詞/be + 主詞）。"}
    ],
    "ODG3_U14": [
        {"word": "glider", "phonetic": "/ˈɡlaɪdər/", "syllables": "glid-er", "pos": "n.", "meaning": "滑翔機", "example": "In 1900, the Wright brothers built a glider.", "note": "源自動詞 glide (滑翔) + r。"},
        {"word": "telescope", "phonetic": "/ˈtɛlɪˌskoʊp/", "syllables": "tel-e-scope", "pos": "n.", "meaning": "望遠鏡", "example": "Hans Lippershey invented the first telescope in 1608.", "note": "tele- (遠距離) + scope (觀測鏡)。"},
        {"word": "surface", "phonetic": "/ˈsɜːrfɪs/", "syllables": "sur-face", "pos": "n.", "meaning": "表面", "example": "Galileo could see the surface of the moon!", "note": "sur- + face，指物體或星球的表面。"},
        {"word": "quickly", "phonetic": "/ˈkwɪkli/", "syllables": "quick-ly", "pos": "adv.", "meaning": "快速地", "example": "Their plane flew more quickly than the glider.", "note": "比較級 more quickly，最高級 the most quickly。"},
        {"word": "clearly", "phonetic": "/ˈklɪrli/", "syllables": "clear-ly", "pos": "adv.", "meaning": "清楚地；清晰地", "example": "Galileo could see things more clearly with his telescope.", "note": "clear + ly，比較級為 more clearly。"},
        {"word": "easily", "phonetic": "/ˈiːzəli/", "syllables": "eas-i-ly", "pos": "adv.", "meaning": "容易地；輕鬆地", "example": "Today we can communicate more easily than in the past.", "note": "easy 去 y 改 i 加 -ly，比較級為 more easily。"},
        {"word": "carefully", "phonetic": "/ˈkɛrfəli/", "syllables": "care-ful-ly", "pos": "adv.", "meaning": "仔細地；小心地", "example": "She painted the picture more carefully than her brother.", "note": "careful + ly（有兩個 l），比較級為 more carefully。"},
        {"word": "happily", "phonetic": "/ˈhæpɪli/", "syllables": "hap-pi-ly", "pos": "adv.", "meaning": "快樂地；開心地", "example": "The children played happily in the park.", "note": "happy 去 y 改 i 加 -ly。"},
        {"word": "further", "phonetic": "/ˈfɜːrðər/", "syllables": "fur-ther", "pos": "adv.", "meaning": "更遠地（far 的不規則比較級）", "example": "Their plane flew further than the glider.", "note": "far 的比較級可寫作 further 或 farther，不可加 more！"},
        {"word": "furthest", "phonetic": "/ˈfɜːrðɪst/", "syllables": "fur-thest", "pos": "adv.", "meaning": "最遠地（far 的不規則最高級）", "example": "With Newton's telescope, he could see the furthest of all.", "note": "far 的最高級為 the furthest 或 the farthest。"}
    ],
    "ODG3_U15": [
        {"word": "dough", "phonetic": "/doʊ/", "syllables": "dough", "pos": "n.", "meaning": "麵團（不可數名詞）", "example": "People in Naples started to put tomatoes on their dough.", "note": "結尾 gh 不發音，發 /doʊ/，屬於不可數名詞。"},
        {"word": "flour", "phonetic": "/ˈflaʊər/", "syllables": "flour", "pos": "n.", "meaning": "麵粉（不可數名詞）", "example": "There is a bag of flour in the cupboard.", "note": "發音與 flower 相同，通常搭配 a bag of flour。"},
        {"word": "olive oil", "phonetic": "/ˈɑːlɪv ˌɔɪl/", "syllables": "ol-ive oil", "pos": "n.", "meaning": "橄欖油（不可數名詞）", "example": "People ate flat bread with olive oil and herbs.", "note": "液體為不可數名詞，搭配 a bottle of olive oil。"},
        {"word": "a loaf of", "phonetic": "/ə ˈloʊf əv/", "syllables": "a loaf of", "pos": "phrase", "meaning": "一條（麵包）", "example": "My mom bought a loaf of bread at the bakery.", "note": "複數時 loaf 去 f 改 ves：two loaves of bread！"},
        {"word": "a slice of", "phonetic": "/ə ˈslaɪs əv/", "syllables": "a slice of", "pos": "phrase", "meaning": "一片（披薩、起司、麵包、肉）", "example": "There are some slices of bread on a plate.", "note": "專門搭配薄片狀食物：bread, pizza, cheese, meat。"},
        {"word": "a jar of", "phonetic": "/ə ˈdʒɑːr əv/", "syllables": "a jar of", "pos": "phrase", "meaning": "一罐（廣口玻璃罐：果醬、蜂蜜、橄欖）", "example": "There is a jar of honey in the cupboard.", "note": "搭配黏稠或醃漬物：jam, honey, olives, peanut butter。"},
        {"word": "a carton of", "phonetic": "/ə ˈkɑːrtən əv/", "syllables": "a car-ton of", "pos": "phrase", "meaning": "一紙盒（牛奶、果汁、雞蛋）", "example": "There is a carton of milk in the fridge.", "note": "指紙盒或塑膠盒裝：a carton of milk / juice / eggs。"},
        {"word": "a bar of", "phonetic": "/ə ˈbɑːr əv/", "syllables": "a bar of", "pos": "phrase", "meaning": "一塊／一條（巧克力、肥皂）", "example": "There is a bar of chocolate on the table.", "note": "專門搭配塊狀硬物：a bar of chocolate / soap。"},
        {"word": "a bowl of", "phonetic": "/ə ˈboʊl əv/", "syllables": "a bowl of", "pos": "phrase", "meaning": "一碗（湯、米飯、麥片、義大利麵、蘋果）", "example": "There is a bowl of apples on the table.", "note": "可搭配不可數飲食 (soup, rice) 或可數複數名詞 (apples, strawberries)。"},
        {"word": "a glass of", "phonetic": "/ə ˈɡlæs əv/", "syllables": "a glass of", "pos": "phrase", "meaning": "一玻璃杯（水、牛奶、果汁）", "example": "Emily drinks a glass of milk before she starts cooking.", "note": "複數加 es：two glasses of water / juice / milk。"}
    ],
    "WR3_U04": [
        {"word": "neighborhood", "phonetic": "/ˈneɪbərˌhʊd/", "syllables": "neigh-bor-hood", "pos": "n.", "meaning": "社區；街坊鄰里", "example": "I have lived in my neighborhood for three years.", "note": "neigh- 中 gh 不發音，字尾 -hood 表區域或狀態。"},
        {"word": "grocery store", "phonetic": "/ˈɡroʊsəri ˌstɔːr/", "syllables": "gro-cer-y store", "pos": "n.", "meaning": "食品雜貨店；超市", "example": "My mom buys fresh fruit at the grocery store.", "note": "gro-cer-y 拼寫注意中間是 c 不是 s。"},
        {"word": "stationery store", "phonetic": "/ˈsteɪʃəˌnɛri ˌstɔːr/", "syllables": "sta-tion-er-y store", "pos": "n.", "meaning": "文具店", "example": "I buy notebooks and pens at the stationery store.", "note": "必考拼寫：文具是 station-er-y (e 代表 pen)，勿拼成 stationary！"},
        {"word": "convenience store", "phonetic": "/kənˈviːnjəns ˌstɔːr/", "syllables": "con-ven-ience store", "pos": "n.", "meaning": "便利商店", "example": "There is a bakery next to the convenience store.", "note": "con-ven-i-ence 字尾為 -ence。"},
        {"word": "pharmacy", "phonetic": "/ˈfɑːrməsi/", "syllables": "phar-ma-cy", "pos": "n.", "meaning": "藥局；藥房", "example": "The pharmacy is across the street from the hospital.", "note": "開頭 ph 發 /f/ 音，字尾為 -cy。"},
        {"word": "hair salon", "phonetic": "/ˈhɛr səˌlɑːn/", "syllables": "hair sa-lon", "pos": "n.", "meaning": "美髮院；髮廊", "example": "The hair salon is around the corner from my house.", "note": "salon 只有一個 l，重音在第二音節。"},
        {"word": "dry cleaner's", "phonetic": "/ˌdraɪ ˈkliːnərz/", "syllables": "dry clean-er's", "pos": "n.", "meaning": "乾洗店", "example": "The dry cleaner's is between the bakery and the bank.", "note": "習慣加上所有格 's，省略了 shop/store。"},
        {"word": "bakery", "phonetic": "/ˈbeɪkəri/", "syllables": "bak-er-y", "pos": "n.", "meaning": "麵包店；烘焙坊", "example": "There is a bakery next to the convenience store.", "note": "bake 去 e 加 -ery。"},
        {"word": "subway station", "phonetic": "/ˈsʌbweɪ ˌsteɪʃən/", "syllables": "sub-way sta-tion", "pos": "n.", "meaning": "地鐵站；捷運站", "example": "The subway station is very close to my house.", "note": "Close to the subway station, there is a department store."},
        {"word": "across from", "phonetic": "/əˈkrɔːs frəm/", "syllables": "a-cross from", "pos": "prep.", "meaning": "在...的對面", "example": "The park is across the street from my house.", "note": "across 只有一個 c、兩個 s；不可寫成 cross from。"}
    ],
    "WR3_U05": [
        {"word": "allowance", "phonetic": "/əˈlaʊəns/", "syllables": "al-low-ance", "pos": "n.", "meaning": "零用錢", "example": "I save my weekly allowance in a piggy bank.", "note": "allow (允許) + ance，注意有兩個 l。"},
        {"word": "bank account", "phonetic": "/ˈbæŋk əˌkaʊnt/", "syllables": "bank ac-count", "pos": "n.", "meaning": "銀行帳戶", "example": "I would open up a bank account and save the money.", "note": "account 中間有兩個 c；搭配動詞 open up (開戶)。"},
        {"word": "expensive", "phonetic": "/ɪkˈspɛnsɪv/", "syllables": "ex-pen-sive", "pos": "adj.", "meaning": "昂貴的", "example": "If I had a lot of money, I would buy an expensive watch.", "note": "ex-pen-sive，反義詞為 cheap。"},
        {"word": "delicious", "phonetic": "/dɪˈlɪʃəs/", "syllables": "de-li-cious", "pos": "adj.", "meaning": "美味的；可口的", "example": "We ate a delicious meal at the restaurant.", "note": "字尾 -cious 發 /ʃəs/ 音。"},
        {"word": "necklace", "phonetic": "/ˈnɛkləs/", "syllables": "neck-lace", "pos": "n.", "meaning": "項鍊", "example": "I would buy a pretty necklace for my mom.", "note": "複合字：neck (脖子) + lace (蕾絲/帶子)。"},
        {"word": "bracelet", "phonetic": "/ˈbreɪslət/", "syllables": "brace-let", "pos": "n.", "meaning": "手鍊；手環", "example": "She wore a silver bracelet on her wrist.", "note": "中間 c 發 /s/ 音。"},
        {"word": "skateboard", "phonetic": "/ˈskeɪtˌbɔːrd/", "syllables": "skate-board", "pos": "n.", "meaning": "滑板", "example": "If I had 100 dollars, I would buy a new skateboard.", "note": "複合字：skate (溜冰/滑行) + board (板子)。"},
        {"word": "sunglasses", "phonetic": "/ˈsʌnˌɡlæsɪz/", "syllables": "sun-glass-es", "pos": "n.", "meaning": "太陽眼鏡（恆用複數）", "example": "He bought a cool pair of sunglasses.", "note": "鏡片有兩片，字尾永遠加 -es，量詞用 a pair of。"},
        {"word": "sneakers", "phonetic": "/ˈsniːkərz/", "syllables": "sneak-ers", "pos": "n.", "meaning": "運動鞋；球鞋（常用複數）", "example": "I need a new pair of sneakers for gym class.", "note": "雙腳穿的鞋子常加 -s，搭配 a pair of sneakers。"},
        {"word": "wisely", "phonetic": "/ˈwaɪzli/", "syllables": "wise-ly", "pos": "adv.", "meaning": "明智地；聰明地", "example": "If I had 300 dollars, I would spend the money wisely.", "note": "wise (聰明的) + ly，修飾動詞 spend。"}
    ],
    "SPACE_CH04": [
        {"word": "asteroid", "phonetic": "/ˈæstəˌrɔɪd/", "syllables": "as-ter-oid", "pos": "n.", "meaning": "小行星", "example": "The asteroid belt is between Mars and Jupiter.", "note": "位於火星與木星之間、環繞太陽運行的岩石天體。"},
        {"word": "comet", "phonetic": "/ˈkɑːmɪt/", "syllables": "com-et", "pos": "n.", "meaning": "彗星", "example": "Comets are huge pieces of ice and dust.", "note": "由冰與塵埃組成，靠近太陽時會受熱產生數百萬公里長的彗尾 (tail)。"},
        {"word": "meteor", "phonetic": "/ˈmiːtiər/", "syllables": "me-te-or", "pos": "n.", "meaning": "流星", "example": "Most meteors burn when they enter the atmosphere.", "note": "進入行星大氣層時摩擦燃燒發光的天體碎片（尚未撞擊地面）。"},
        {"word": "meteorite", "phonetic": "/ˈmiːtiəˌraɪt/", "syllables": "me-te-or-ite", "pos": "n.", "meaning": "隕石", "example": "Sometimes big meteorites hit Earth and make a crater.", "note": "meteor + -ite (礦石字尾)，指沒有燒光並實際撞擊星球表面的隕石！"},
        {"word": "crater", "phonetic": "/ˈkreɪtər/", "syllables": "cra-ter", "pos": "n.", "meaning": "隕石坑；撞擊坑", "example": "The Chicxulub meteorite crater is 180 kilometers across.", "note": "大型隕石撞擊地面所留下的巨大碗狀凹坑。"},
        {"word": "atmosphere", "phonetic": "/ˈætməˌsfɪr/", "syllables": "at-mos-phere", "pos": "n.", "meaning": "大氣層", "example": "Meteors are pieces of rock that enter a planet's atmosphere.", "note": "at-mos-phere，注意 ph 發 /f/ 音。"},
        {"word": "Kuiper belt", "phonetic": "/ˈkaɪpər ˌbɛlt/", "syllables": "Kui-per belt", "pos": "n.", "meaning": "古柏帶", "example": "The Kuiper belt is further away than Neptune.", "note": "位於海王星軌道外側、由無數冰塊組成的環狀區域，是許多彗星的故鄉。"},
        {"word": "explosion", "phonetic": "/ɪkˈsploʊʒən/", "syllables": "ex-plo-sion", "pos": "n.", "meaning": "爆炸", "example": "When the meteorite hit Earth, there was a huge explosion.", "note": "動詞 explode 去 de 加 -sion。"},
        {"word": "dinosaur", "phonetic": "/ˈdaɪnəˌsɔːr/", "syllables": "di-no-saur", "pos": "n.", "meaning": "恐龍", "example": "About 65 million years ago, the dinosaurs died.", "note": "di-no-saur，字尾是 -saur 而不是 -sour。"}
    ],
    "SPACE_CH05": [
        {"word": "astronomy", "phonetic": "/əˈstrɑːnəmi/", "syllables": "as-tron-o-my", "pos": "n.", "meaning": "天文學", "example": "Astronomy is studying the planets and the stars.", "note": "astro- (星體) + -nomy (學科)。"},
        {"word": "astronomer", "phonetic": "/əˈstrɑːnəmər/", "syllables": "as-tron-o-mer", "pos": "n.", "meaning": "天文學家", "example": "People who study astronomy are called astronomers.", "note": "字尾 -er 代表從事該學科研究的科學家。"},
        {"word": "telescope", "phonetic": "/ˈtɛlɪˌskoʊp/", "syllables": "tel-e-scope", "pos": "n.", "meaning": "望遠鏡", "example": "In 1609, Galileo used one of the first telescopes.", "note": "伽利略用望遠鏡發現月球坑洞與木星的四顆衛星。"},
        {"word": "gravity", "phonetic": "/ˈɡrævəti/", "syllables": "grav-i-ty", "pos": "n.", "meaning": "萬有引力；地心引力", "example": "Isaac Newton discovered the force of gravity.", "note": "重力讓物體掉落地面，也讓行星繞著太陽公轉。"},
        {"word": "galaxy", "phonetic": "/ˈɡæləksi/", "syllables": "gal-ax-y", "pos": "n.", "meaning": "星系", "example": "In 1930, Edwin Hubble discovered another galaxy.", "note": "複數為 galaxies（去 y 改 ies）；宇宙中有數十億個星系。"},
        {"word": "Milky Way", "phonetic": "/ˌmɪlki ˈweɪ/", "syllables": "Milk-y Way", "pos": "n.", "meaning": "銀河系", "example": "The Milky Way is the galaxy where our solar system lives.", "note": "專有名詞首字母需大寫，前面常加定冠詞 the。"},
        {"word": "spacecraft", "phonetic": "/ˈspeɪsˌkræft/", "syllables": "space-craft", "pos": "n.", "meaning": "太空船；太空探測器（單複數同形）", "example": "Astronomers use spacecraft to explore our solar system.", "note": "單複數同形，不可加 -s！"},
        {"word": "calculate", "phonetic": "/ˈkælkjəˌleɪt/", "syllables": "cal-cu-late", "pos": "v.", "meaning": "計算；推算", "example": "Ancient people used the stars to calculate the seasons.", "note": "use numbers to find out something (用數字推算某事)。"},
        {"word": "universe", "phonetic": "/ˈjuːnɪˌvɜːrs/", "syllables": "u-ni-verse", "pos": "n.", "meaning": "宇宙", "example": "There are billions of galaxies in the universe.", "note": "uni- (單一整體)，整個宇宙只有一個，包含數十億個星系 (galaxies)。"},
        {"word": "prove", "phonetic": "/pruːv/", "syllables": "prove", "pos": "v.", "meaning": "證明；證實", "example": "Isaac Newton proved that Earth orbits the Sun.", "note": "過去式為 proved，意為 show that something is correct。"}
    ],
    "RWW6_U05": [
        {"word": "compass", "phonetic": "/ˈkʌmpəs/", "syllables": "com-pass", "pos": "n.", "meaning": "指南針；指北針", "example": "A compass is an instrument you use to tell direction.", "note": "字尾有兩個 s；內有磁針永遠指向北方 (north)。"},
        {"word": "lighthouse", "phonetic": "/ˈlaɪtˌhaʊs/", "syllables": "light-house", "pos": "n.", "meaning": "燈塔", "example": "A lighthouse is a tall tower built on the coast.", "note": "複合字：light (燈光) + house (房屋)，頂端有巨型燈具與號角 (horn)。"},
        {"word": "foggy", "phonetic": "/ˈfɔːɡi/", "syllables": "fog-gy", "pos": "adj.", "meaning": "有霧的；濃霧瀰漫的", "example": "Jaya and her family went hiking one foggy morning.", "note": "名詞 fog (霧) 重複字尾 g 加 -y 變成形容詞 foggy。"},
        {"word": "crooked", "phonetic": "/ˈkrʊkɪd/", "syllables": "crook-ed", "pos": "adj.", "meaning": "彎曲的；歪斜的", "example": "Their goal was a hill with a tall, crooked tree on top.", "note": "-ed 發 /ɪd/ 音，讀作兩音節 crook-ed。"},
        {"word": "turn right", "phonetic": "/tɜːrn ˈraɪt/", "syllables": "turn right", "pos": "phrase", "meaning": "右轉", "example": "There is a place we should have turned right.", "note": "反義片語為 turn left (左轉)。"},
        {"word": "go straight", "phonetic": "/ɡoʊ ˈstreɪt/", "syllables": "go straight", "pos": "phrase", "meaning": "直走", "example": "We decided to go straight instead of turning.", "note": "straight 中的 gh 不發音，切勿漏寫 gh。"},
        {"word": "go back", "phonetic": "/ɡoʊ ˈbæk/", "syllables": "go back", "pos": "phrase", "meaning": "折返；回去", "example": "Before we go back down the trail, let's hike up the hill.", "note": "指沿原路返回或回到某地。"},
        {"word": "on the left", "phonetic": "/ɑːn ðə ˈlɛft/", "syllables": "on the left", "pos": "phrase", "meaning": "在左邊；在左側", "example": "She pointed to a log bench on the left side of the trail.", "note": "介系詞用 on：on the left / on the right。"},
        {"word": "up the hill", "phonetic": "/ʌp ðə ˈhɪl/", "syllables": "up the hill", "pos": "phrase", "meaning": "往山上；爬上山丘", "example": "We should hike up the hill and take a look around!", "note": "下山則為 down the hill。"},
        {"word": "read a map", "phonetic": "/riːd ə ˈmæp/", "syllables": "read a map", "pos": "phrase", "meaning": "看地圖；判讀地圖", "example": "We know how to read a map, so let's look.", "note": "「看地圖」英文動詞用 read，不用 look 或 watch！"}
    ],
    "RWW6_U06": [
        {"word": "orienteering", "phonetic": "/ˌɔːriɛnˈtɪrɪŋ/", "syllables": "o-ri-en-teer-ing", "pos": "n.", "meaning": "定向越野運動", "example": "In the sport of orienteering, racers use a map and compass.", "note": "結合地圖與指北針在野外尋找檢查點並打卡的計時運動。"},
        {"word": "control", "phonetic": "/kənˈtroʊl/", "syllables": "con-trol", "pos": "n.", "meaning": "（定向越野的）控制點、檢查站", "example": "Racers must find all the controls to win.", "note": "比賽中必須集滿卡片上全部 18 個 controls 的打孔記號才算有效完賽。"},
        {"word": "corner", "phonetic": "/ˈkɔːrnər/", "syllables": "cor-ner", "pos": "n.", "meaning": "街角；轉角（兩條道路交會處）", "example": "Standing on a corner, you ask someone how to get to a store.", "note": "課文定義：a place where two roads meet。"},
        {"word": "visual", "phonetic": "/ˈvɪʒuəl/", "syllables": "vis-u-al", "pos": "n./adj.", "meaning": "視覺圖表（圖片、圖解、地圖）；視覺的", "example": "Visuals provide information that is not in a text.", "note": "包含 pictures, diagrams, and maps，能補充文章未寫出的細節。"},
        {"word": "go two blocks", "phonetic": "/ɡoʊ ˈtuː ˈblɑːks/", "syllables": "go two blocks", "pos": "phrase", "meaning": "走兩個街區（表示移動距離）", "example": "Go two blocks north and turn left.", "note": "block 指兩條十字路口之間的「街區」，go two blocks 意為 move this far。"},
        {"word": "across the street", "phonetic": "/əˈkrɔːs ðə ˈstriːt/", "syllables": "a-cross the street", "pos": "phrase", "meaning": "在對街；在馬路對面", "example": "You will be across the street from the bookstore.", "note": "意為 on the other side (在另一側)；動詞片語「過馬路」則是 cross the street。"},
        {"word": "along a river", "phonetic": "/əˈlɔːŋ ə ˈrɪvər/", "syllables": "a-long a riv-er", "pos": "phrase", "meaning": "沿著河流", "example": "In orienteering, you will likely run along a river.", "note": "along 表示「順著、沿著（線狀地形）」。"},
        {"word": "climb over rocks", "phonetic": "/klaɪm ˈoʊvər ˈrɑːks/", "syllables": "climb o-ver rocks", "pos": "phrase", "meaning": "爬過岩石", "example": "Racers climb over rocks and go up and down hills.", "note": "climb 的 b 不發音！over 表「越過障礙物上方」。"},
        {"word": "up and down hills", "phonetic": "/ʌp ænd daʊn ˈhɪlz/", "syllables": "up and down hills", "pos": "phrase", "meaning": "在山丘間上下起伏穿梭", "example": "You will climb over rocks and go up and down hills.", "note": "描述野外高低起伏的地形挑戰。"}
    ],
    "RWW6_U07": [
        {"word": "native speaker", "phonetic": "/ˌneɪtɪv ˈspiːkər/", "syllables": "na-tive speak-er", "pos": "n.", "meaning": "母語使用者", "example": "Everyone is a native speaker of their first language.", "note": "native language 指從小在家中自然習得的母語。"},
        {"word": "official language", "phonetic": "/əˈfɪʃəl ˈlæŋɡwɪdʒ/", "syllables": "of-fi-cial lan-guage", "pos": "n.", "meaning": "官方語言", "example": "An official language is the one used by the government.", "note": "official 中間有兩個 f，ci 發 /ʃ/ 音。"},
        {"word": "pass a law", "phonetic": "/pæs ə ˈlɔː/", "syllables": "pass a law", "pos": "phrase", "meaning": "通過法律；立法", "example": "A country has to pass a law to make a language official.", "note": "若沒有 pass a law（如墨西哥、美國），該國就沒有法定官方語言。"},
        {"word": "bar graph", "phonetic": "/ˈbɑːr ˌɡræf/", "syllables": "bar graph", "pos": "n.", "meaning": "長條圖", "example": "A bar graph uses rectangles to show how much or how many.", "note": "graph 的 ph 發 /f/ 音；用長方形長度比較不同項目的數量。"},
        {"word": "Mandarin", "phonetic": "/ˈmændərɪn/", "syllables": "Man-da-rin", "pos": "n.", "meaning": "華語；普通話；國語", "example": "Most people in China use Mandarin to talk with each other.", "note": "專有名詞首字母 M 必須大寫。"},
        {"word": "sign language", "phonetic": "/ˈsaɪn ˌlæŋɡwɪdʒ/", "syllables": "sign lan-guage", "pos": "n.", "meaning": "手語", "example": "People who cannot hear or speak use sign languages.", "note": "sign 中的 g 不發音！利用手勢、臉部表情與肢體動作溝通。"},
        {"word": "government", "phonetic": "/ˈɡʌvərnmənt/", "syllables": "gov-ern-ment", "pos": "n.", "meaning": "政府", "example": "An official language is used by the government of a country.", "note": "gov-ern-ment，切勿漏寫中間的 n！"},
        {"word": "communicate", "phonetic": "/kəˈmjuːnɪˌkeɪt/", "syllables": "com-mu-ni-cate", "pos": "v.", "meaning": "溝通；交流", "example": "They communicate by making different faces and moving their bodies.", "note": "注意開頭 com-mu- 有兩個 m。"}
    ],
    "RWW6_U08": [
        {"word": "bilingual", "phonetic": "/baɪˈlɪŋɡwəl/", "syllables": "bi-lin-gual", "pos": "adj.", "meaning": "雙語的；能說兩種語言的", "example": "Do they speak Portuguese and English? Are they bilingual?", "note": "字首 bi- 代表「二」（如 bicycle 兩輪腳踏車），指 speaking two languages。"},
        {"word": "accent", "phonetic": "/ˈæksɛnt/", "syllables": "ac-cent", "pos": "n.", "meaning": "口音；腔調", "example": "You sound like you have a British accent.", "note": "課文定義：a way to pronounce words（發音吐字的方式）。"},
        {"word": "prediction", "phonetic": "/prɪˈdɪkʃən/", "syllables": "pre-dic-tion", "pos": "n.", "meaning": "預測；推測", "example": "A prediction is what you think will happen in the future.", "note": "pre- (預先) + dict (說) + -ion，預測未來可能發生的事。"},
        {"word": "Italian", "phonetic": "/ɪˈtæljən/", "syllables": "I-tal-ian", "pos": "n./adj.", "meaning": "義大利語；義大利的", "example": "Rosa speaks Italian at home.", "note": "Italy 去 y 加 -ian，語言與國籍字首 I 永遠大寫。"},
        {"word": "Portuguese", "phonetic": "/ˌpɔːrtʃəˈɡiːz/", "syllables": "Por-tu-guese", "pos": "n./adj.", "meaning": "葡萄牙語；葡萄牙的", "example": "Speaking Portuguese helped Erico learn some Italian.", "note": "葡萄牙 (Portugal) 與巴西 (Brazil) 都說 Portuguese；字尾為 -guese。"},
        {"word": "pronounce", "phonetic": "/prəˈnaʊns/", "syllables": "pro-nounce", "pos": "v.", "meaning": "發音", "example": "An accent is a special way to pronounce words.", "note": "動詞為 pro-nounce (中間是 o-u)，名詞發音則是 pronunciation。"},
        {"word": "interrupt", "phonetic": "/ˌɪntəˈrʌpt/", "syllables": "in-ter-rupt", "pos": "v.", "meaning": "打斷（談話）；插嘴", "example": "Rosa interrupted Erico and asked five questions quickly.", "note": "inter- + rupt，注意中間有兩個 r。"},
        {"word": "supplies", "phonetic": "/səˈplaɪz/", "syllables": "sup-plies", "pos": "n.", "meaning": "用品；物資（常指文具或美術用品）", "example": "Rosa dropped her art supplies while she was talking.", "note": "單數為 supply，去 y 改 ies 變成複數 supplies。"}
    ]
}

# 3. 11 個單元 100% 精準單詞定位改錯題 (Mistake Buster)
# 每一題確保只有單一明確錯誤詞 (wrong_index 精確對應 tokens[wrong_index])，讓 12 歲學生點擊體驗 100% 零挫折！
CURATED_MISTAKES = {
    "ODG3_U13": [
        {
            "trap_id": "ODG13_ERR_1",
            "sentence": "Antonio Meucci was an inventor, and so did Alexander Graham Bell.",
            "wrong_word": "did",
            "correct_word": "was",
            "fixed_sentence": "Antonio Meucci was an inventor, and so was Alexander Graham Bell.",
            "reason": "前句主要動詞是 be 動詞 was，後句肯定倒裝附和必須沿用 be 動詞『so was...』，絕對不可混用助動詞 did！"
        },
        {
            "trap_id": "ODG13_ERR_2",
            "sentence": "Thomas Edison invented a light bulb, and Joseph Swan was, too.",
            "wrong_word": "was,",
            "correct_word": "did,",
            "fixed_sentence": "Thomas Edison invented a light bulb, and Joseph Swan did, too.",
            "reason": "前句動詞 invented 是一般動詞過去式，後句附和必須請出助動詞『did, too』，不可用 be 動詞 was！"
        },
        {
            "trap_id": "ODG13_ERR_3",
            "sentence": "Elisha Gray did not become rich, and Meucci didn't, too.",
            "wrong_word": "too.",
            "correct_word": "either.",
            "fixed_sentence": "Elisha Gray did not become rich, and Meucci didn't, either.",
            "reason": "否定句尾（didn't 後方）表示「也不」必須用『either』；too 只能用在肯定句尾！"
        },
        {
            "trap_id": "ODG13_ERR_4",
            "sentence": "Meucci didn't get a telephone patent, and neither didn't Reis.",
            "wrong_word": "didn't",
            "correct_word": "did",
            "fixed_sentence": "Meucci didn't get a telephone patent, and neither did Reis.",
            "reason": "『Neither』本身已經包含否定（Not + either），後面的助動詞必須用肯定形『did』，寫成 neither didn't 會變成雙重否定錯誤！"
        },
        {
            "trap_id": "ODG13_ERR_5",
            "sentence": "Olivia got 100% on her quiz, and 100% did Penny.",
            "wrong_word": "100%",
            "correct_word": "so",
            "fixed_sentence": "Olivia got 100% on her quiz, and so did Penny.",
            "reason": "【岱崙 W2 真題陷阱】肯定倒裝附和句開頭必須用連接副詞『so (and so did Penny)』，不可把受詞 100% 搬到助動詞前面！"
        },
        {
            "trap_id": "ODG13_ERR_6",
            "sentence": "Ryan got 95% on his quiz, and Michael are, too.",
            "wrong_word": "are,",
            "correct_word": "did,",
            "fixed_sentence": "Ryan got 95% on his quiz, and Michael did, too.",
            "reason": "【岱崙 W2 真題陷阱】前句 got 是過去式一般動詞，後句附和必須用過去式助動詞『did, too』，不可用現在式 be 動詞 are！"
        },
        {
            "trap_id": "ODG13_ERR_7",
            "sentence": "Ray are not pass the quiz, and Jim didn't, either.",
            "wrong_word": "are not",
            "correct_word": "didn't",
            "fixed_sentence": "Ray didn't pass the quiz, and Jim didn't, either.",
            "reason": "【岱崙 W2 真題陷阱】一般動詞 pass 的過去式否定必須用助動詞『didn't pass』，絕對不可寫成 are not pass！"
        },
        {
            "trap_id": "ODG13_ERR_8",
            "sentence": "Bell's mother was deaf, and so did his wife.",
            "wrong_word": "did",
            "correct_word": "was",
            "fixed_sentence": "Bell's mother was deaf, and so was his wife.",
            "reason": "前句是『was deaf (be動詞 + 形容詞)』，後句倒裝附和必須對齊使用『so was his wife』，不可用 did！"
        },
        {
            "trap_id": "ODG13_ERR_9",
            "sentence": "Gray hurried to the Patent Office, and too did Bell.",
            "wrong_word": "too",
            "correct_word": "so",
            "fixed_sentence": "Gray hurried to the Patent Office, and so did Bell.",
            "reason": "放在倒裝句首（助動詞 did 前面）表示「也是」必須用『so』；too 只能放在句尾逗號後面！"
        },
        {
            "trap_id": "ODG13_ERR_10",
            "sentence": "Houses didn't have telephones then, and neither were offices.",
            "wrong_word": "were",
            "correct_word": "did",
            "fixed_sentence": "Houses didn't have telephones then, and neither did offices.",
            "reason": "前句是『didn't have (一般動詞過去式否定)』，後句 neither 倒裝必須對齊助動詞『neither did offices』，不可用 were！"
        },
        {
            "trap_id": "ODG13_ERR_11",
            "sentence": "Swan wasn't happy about the patent, and Edison wasn't, too.",
            "wrong_word": "too.",
            "correct_word": "either.",
            "fixed_sentence": "Swan wasn't happy about the patent, and Edison wasn't, either.",
            "reason": "前句與後句皆為否定（wasn't），句尾附和詞必須用『either』，不可用 too！"
        },
        {
            "trap_id": "ODG13_ERR_12",
            "sentence": "Meucci didn't become rich, and Reis did, either.",
            "wrong_word": "did,",
            "correct_word": "didn't,",
            "fixed_sentence": "Meucci didn't become rich, and Reis didn't, either.",
            "reason": "句尾有否定附和詞『either』時，前面的助動詞必須是否定形『didn't』！"
        }
    ],
    "ODG3_U14": [
        {
            "trap_id": "ODG14_ERR_1",
            "sentence": "The Wright brothers' plane flew more further than the glider.",
            "wrong_word": "more",
            "correct_word": "much",
            "fixed_sentence": "The Wright brothers' plane flew much further than the glider.",
            "reason": "『further』本身已經是 far 的不規則比較級，前面絕對不可再加 more（雙重比較級錯誤），若要加強語氣可用 much！"
        },
        {
            "trap_id": "ODG14_ERR_2",
            "sentence": "Galileo could see things clearlier with his new telescope.",
            "wrong_word": "clearlier",
            "correct_word": "more clearly",
            "fixed_sentence": "Galileo could see things more clearly with his new telescope.",
            "reason": "由形容詞加 -ly 構成的多音節副詞（clearly），比較級必須在前面加『more (more clearly)』，不可字尾加 -er！"
        },
        {
            "trap_id": "ODG14_ERR_3",
            "sentence": "In 1908, their best airplane flew the faster of all.",
            "wrong_word": "faster",
            "correct_word": "fastest",
            "fixed_sentence": "In 1908, their best airplane flew the fastest of all.",
            "reason": "句尾有『of all（在全部之中）』且前面有定冠詞 the，必須使用最高級『fastest』！"
        },
        {
            "trap_id": "ODG14_ERR_4",
            "sentence": "A witch laughs horribly, and a vampire laughs horribly than a witch.",
            "wrong_word": "horribly",
            "correct_word": "more horribly",
            "fixed_sentence": "A witch laughs horribly, and a vampire laughs more horribly than a witch.",
            "reason": "【岱崙 W4 真題陷阱】後面有比較連詞『than』，多音節副詞 horribly 前面必須加上『more (more horribly than)』，不可漏掉 more！"
        },
        {
            "trap_id": "ODG14_ERR_5",
            "sentence": "An eight year old can walk more than a five year old.",
            "wrong_word": "more",
            "correct_word": "more quickly",
            "fixed_sentence": "An eight year old can walk more quickly than a five year old.",
            "reason": "【岱崙 W5 真題陷阱】比較「走得多快 (How quickly)」時，不能只寫 walk more than，必須把副詞本體寫出來：『walk more quickly than』！"
        },
        {
            "trap_id": "ODG14_ERR_6",
            "sentence": "A dog runs faster than a person, but a lion runs fastest.",
            "wrong_word": "fastest.",
            "correct_word": "the fastest.",
            "fixed_sentence": "A dog runs faster than a person, but a lion runs the fastest.",
            "reason": "【岱崙 W5 真題陷阱】三級比較長句的最後一段最高級，前面務必加上定冠詞『the (the fastest)』！"
        },
        {
            "trap_id": "ODG14_ERR_7",
            "sentence": "A frog can jump far, but kangaroo can jump the farthest.",
            "wrong_word": "kangaroo",
            "correct_word": "a kangaroo",
            "fixed_sentence": "A frog can jump far, but a kangaroo can jump the farthest.",
            "reason": "【岱崙 W5 真題陷阱】可數單數動物名詞『kangaroo / lion / dog』當主詞時，前面絕對不可漏掉不定冠詞『a / an』！"
        },
        {
            "trap_id": "ODG14_ERR_8",
            "sentence": "Jerome did badly in the quiz, and Ivan did more badly than Jerome.",
            "wrong_word": "more badly",
            "correct_word": "worse",
            "fixed_sentence": "Jerome did badly in the quiz, and Ivan did worse than Jerome.",
            "reason": "【岱崙 W4 真題陷阱】『badly（糟糕地）』是不規則變化副詞：badly ➔ worse ➔ the worst，絕對不可寫成 more badly！"
        },
        {
            "trap_id": "ODG14_ERR_9",
            "sentence": "Eric did well in his quiz, and Penny did more well than Eric.",
            "wrong_word": "more well",
            "correct_word": "better",
            "fixed_sentence": "Eric did well in his quiz, and Penny did better than Eric.",
            "reason": "【岱崙 W4 真題陷阱】『well（表現好地）』是不規則變化副詞：well ➔ better ➔ the best，絕對不可寫成 more well！"
        },
        {
            "trap_id": "ODG14_ERR_10",
            "sentence": "Peter laughs loudly, Helen laughs more loud than Peter, but Jack laughs the most loudly.",
            "wrong_word": "more loud",
            "correct_word": "more loudly",
            "fixed_sentence": "Peter laughs loudly, Helen laughs more loudly than Peter, but Jack laughs the most loudly.",
            "reason": "【岱崙 W4 真題陷阱】修飾一般動詞 laughs 必須全程使用副詞『loudly (more loudly than)』，不可半路退回形容詞 loud！"
        },
        {
            "trap_id": "ODG14_ERR_11",
            "sentence": "A dog runs more faster than a person in the park.",
            "wrong_word": "more faster",
            "correct_word": "faster",
            "fixed_sentence": "A dog runs faster than a person in the park.",
            "reason": "【岱崙 W4 真題陷阱】『fast』是單音節同形副詞，比較級直接加 -er 變成『faster』，前面不可重複加 more！"
        },
        {
            "trap_id": "ODG14_ERR_12",
            "sentence": "A duck flew farther then an eagle in the sky.",
            "wrong_word": "then",
            "correct_word": "than",
            "fixed_sentence": "A duck flew farther than an eagle in the sky.",
            "reason": "【岱崙 W4 真題陷阱】比較級後面連接比較對象的介系詞是『than（比）』，切勿拼成副詞 then（然後）！"
        }
    ],
    "ODG3_U15": [
        {
            "trap_id": "ODG15_ERR_1",
            "sentence": "We need to buy two loafs of bread at the bakery.",
            "wrong_word": "loafs",
            "correct_word": "loaves",
            "fixed_sentence": "We need to buy two loaves of bread at the bakery.",
            "reason": "量詞『loaf（一條）』字尾是 f，變成複數時必須去 f 改 ves 成為『loaves』！"
        },
        {
            "trap_id": "ODG15_ERR_2",
            "sentence": "How many olive oil did the baker put on the dough?",
            "wrong_word": "many",
            "correct_word": "much",
            "fixed_sentence": "How much olive oil did the baker put on the dough?",
            "reason": "『olive oil（橄欖油）』是液體不可數名詞，詢問數量必須用『How much』，不可用 How many！"
        },
        {
            "trap_id": "ODG15_ERR_3",
            "sentence": "There are three bottles of milks in the refrigerator.",
            "wrong_word": "milks",
            "correct_word": "milk",
            "fixed_sentence": "There are three bottles of milk in the refrigerator.",
            "reason": "『milk（牛奶）』是不可數名詞，複數標記已經加在容器『bottles』上，後面的 milk 永遠不可加 s！"
        },
        {
            "trap_id": "ODG15_ERR_4",
            "sentence": "Emily ate two slices of pizzas for lunch yesterday.",
            "wrong_word": "pizzas",
            "correct_word": "pizza",
            "fixed_sentence": "Emily ate two slices of pizza for lunch yesterday.",
            "reason": "在量詞片語『two slices of...』後方，當物質看待的 pizza 不加 s，複數已經體現在 slices 上！"
        },
        {
            "trap_id": "ODG15_ERR_5",
            "sentence": "Is there any flours left in the kitchen cupboard?",
            "wrong_word": "flours",
            "correct_word": "flour",
            "fixed_sentence": "Is there any flour left in the kitchen cupboard?",
            "reason": "『flour（麵粉）』屬於粉末狀不可數名詞，沒有複數形，不可加 s！"
        },
        {
            "trap_id": "ODG15_ERR_6",
            "sentence": "My mom bought a jar of chocolates for my birthday.",
            "wrong_word": "jar",
            "correct_word": "bar",
            "fixed_sentence": "My mom bought a bar of chocolate for my birthday.",
            "reason": "塊狀巧克力標準容器量詞為『a bar of chocolate』；a jar of 是用來裝果醬 (jam) 或蜂蜜 (honey) 的玻璃罐！"
        }
    ],
    "WR3_U04": [
        {
            "trap_id": "WR04_ERR_1",
            "sentence": "I have lived in this neighborhood since three years.",
            "wrong_word": "since",
            "correct_word": "for",
            "fixed_sentence": "I have lived in this neighborhood for three years.",
            "reason": "『three years（三年）』是一段持續的時間長度，現在完成式必須搭配介系詞『for』；since 後面只能接過去時間起點（如 since 2021）！"
        },
        {
            "trap_id": "WR04_ERR_2",
            "sentence": "My family has lived in this house for five years ago.",
            "wrong_word": "ago.",
            "correct_word": "now.",
            "fixed_sentence": "My family has lived in this house for five years now.",
            "reason": "『ago（...以前）』專屬於過去簡單式（如 I moved here five years ago），絕對不可與現在完成式『have/has lived + for...』連用！"
        },
        {
            "trap_id": "WR04_ERR_3",
            "sentence": "The grocery store is cross the street from my house.",
            "wrong_word": "cross",
            "correct_word": "across",
            "fixed_sentence": "The grocery store is across the street from my house.",
            "reason": "『cross』是動詞（穿越馬路）；前面已經有 be 動詞 is，必須用介系詞『across (在...對面)』！"
        },
        {
            "trap_id": "WR04_ERR_4",
            "sentence": "Close the subway station, there is a big department store.",
            "wrong_word": "Close",
            "correct_word": "Close to",
            "fixed_sentence": "Close to the subway station, there is a big department store.",
            "reason": "表示「離...很近」必須加上介系詞 to，寫成『Close to + 地點』；單寫 Close 會變成動詞「關門」！"
        },
        {
            "trap_id": "WR04_ERR_5",
            "sentence": "There are a bakery and a pharmacy around the corner.",
            "wrong_word": "are",
            "correct_word": "is",
            "fixed_sentence": "There is a bakery and a pharmacy around the corner.",
            "reason": "『There is / There are』採「就近原則」，緊鄰的第一個名詞『a bakery』是單數，因此必須用『There is』！"
        },
        {
            "trap_id": "WR04_ERR_6",
            "sentence": "The dry cleaner's is between the bank or the hair salon.",
            "wrong_word": "or",
            "correct_word": "and",
            "fixed_sentence": "The dry cleaner's is between the bank and the hair salon.",
            "reason": "表示「在 A 與 B 兩者之間」固定搭配為『between A and B』，連接詞必須用 and！"
        }
    ],
    "WR3_U05": [
        {
            "trap_id": "WR05_ERR_1",
            "sentence": "If I have a lot of money, I would buy a big house.",
            "wrong_word": "have",
            "correct_word": "had",
            "fixed_sentence": "If I had a lot of money, I would buy a big house.",
            "reason": "「與現在事實相反」的第二條件句（假設語氣），If 子句動詞必須退一位改用過去式『had』！"
        },
        {
            "trap_id": "WR05_ERR_2",
            "sentence": "If I had 300 dollars, I will save it in a bank account.",
            "wrong_word": "will",
            "correct_word": "would",
            "fixed_sentence": "If I had 300 dollars, I would save it in a bank account.",
            "reason": "前面 If 子句為過去式『had』（虛擬假設），主要子句的助動詞必須對應使用過去式型態『would』，不可用 will！"
        },
        {
            "trap_id": "WR05_ERR_3",
            "sentence": "If I was a millionaire, I would travel around the world.",
            "wrong_word": "was",
            "correct_word": "were",
            "fixed_sentence": "If I were a millionaire, I would travel around the world.",
            "reason": "在正式英文寫作的與現在事實相反假設語氣中，無論主詞是 I / he / she，be 動詞一律使用『were (If I were...)』！"
        },
        {
            "trap_id": "WR05_ERR_4",
            "sentence": "With some of the money, I would bought a baseball glove.",
            "wrong_word": "bought",
            "correct_word": "buy",
            "fixed_sentence": "With some of the money, I would buy a baseball glove.",
            "reason": "情態助動詞『would』後面必須接「原形動詞 buy」，不可接過去式 bought！"
        },
        {
            "trap_id": "WR05_ERR_5",
            "sentence": "The skateboard and sneakers would cost I about 80 dollars.",
            "wrong_word": "I",
            "correct_word": "me",
            "fixed_sentence": "The skateboard and sneakers would cost me about 80 dollars.",
            "reason": "動詞『cost』後面必須接「受格代名詞 me（cost + 人 + 金錢）」，不可接主格 I！"
        },
        {
            "trap_id": "WR05_ERR_6",
            "sentence": "I would treat my best friends for lunch at a restaurant.",
            "wrong_word": "for",
            "correct_word": "to",
            "fixed_sentence": "I would treat my best friends to lunch at a restaurant.",
            "reason": "「請某人吃某物」固定片語為『treat + 人 + to + 食物/餐點』，介系詞必須用 to！"
        }
    ],
    "SPACE_CH04": [
        {
            "trap_id": "SP04_ERR_1",
            "sentence": "The asteroid belt is located between Earth and Jupiter.",
            "wrong_word": "Earth",
            "correct_word": "Mars",
            "fixed_sentence": "The asteroid belt is located between Mars and Jupiter.",
            "reason": "根據課文第 16 頁，小行星帶（asteroid belt）精確位置介於『火星 (Mars) 與木星 (Jupiter)』之間！"
        },
        {
            "trap_id": "SP04_ERR_2",
            "sentence": "A lot of icy comets come from the asteroid belt.",
            "wrong_word": "asteroid",
            "correct_word": "Kuiper",
            "fixed_sentence": "A lot of icy comets come from the Kuiper belt.",
            "reason": "由冰與塵埃組成的彗星（comets）主要來自海王星外側的『古柏帶 (Kuiper belt)』，而非岩石組成的小行星帶！"
        },
        {
            "trap_id": "SP04_ERR_3",
            "sentence": "Comets become colder when they travel near the Sun.",
            "wrong_word": "colder",
            "correct_word": "hotter",
            "fixed_sentence": "Comets become hotter when they travel near the Sun.",
            "reason": "當彗星靠近太陽時會變得『更熱 (hotter)』，使冰與塵埃散逸形成數百萬公里長的彗尾！"
        },
        {
            "trap_id": "SP04_ERR_4",
            "sentence": "A meteorite burns up in the sky before hitting the ground.",
            "wrong_word": "meteorite",
            "correct_word": "meteor",
            "fixed_sentence": "A meteor burns up in the sky before hitting the ground.",
            "reason": "進入大氣層燃燒發光的是『流星 (meteor)』；沒有燒完並成功撞擊星球地面的石塊才叫『隕石 (meteorite)』！"
        },
        {
            "trap_id": "SP04_ERR_5",
            "sentence": "In 1994, twenty-one pieces of a comet hit the Moon.",
            "wrong_word": "the Moon.",
            "correct_word": "Jupiter.",
            "fixed_sentence": "In 1994, twenty-one pieces of a comet hit Jupiter.",
            "reason": "1994 年 21 塊彗星碎片撞擊的是氣體巨行星『木星 (Jupiter)』，部分爆炸規模甚至比地球還大！"
        },
        {
            "trap_id": "SP04_ERR_6",
            "sentence": "The Tunguska meteorite impact caused the dinosaurs to die.",
            "wrong_word": "Tunguska",
            "correct_word": "Chicxulub",
            "fixed_sentence": "The Chicxulub meteorite impact caused the dinosaurs to die.",
            "reason": "造成 6500 萬年前恐龍滅絕的是墨西哥尤卡坦半島的『希克蘇魯伯 (Chicxulub)』隕石；通古斯事件發生於 1908 年俄羅斯！"
        }
    ],
    "SPACE_CH05": [
        {
            "trap_id": "SP05_ERR_1",
            "sentence": "In 1543, Copernicus said that Earth was at the center.",
            "wrong_word": "Earth",
            "correct_word": "the Sun",
            "fixed_sentence": "In 1543, Copernicus said that the Sun was at the center.",
            "reason": "波蘭天文學家哥白尼（Copernicus）於 1543 年提出的是『太陽中心說 (the Sun was at the center)』，打破古人地心說！"
        },
        {
            "trap_id": "SP05_ERR_2",
            "sentence": "Galileo discovered the force of gravity and proved Copernicus right.",
            "wrong_word": "Galileo",
            "correct_word": "Newton",
            "fixed_sentence": "Newton discovered the force of gravity and proved Copernicus right.",
            "reason": "發現萬有引力（gravity）並證明地球繞太陽公轉的是英國科學家『牛頓 (Isaac Newton)』！"
        },
        {
            "trap_id": "SP05_ERR_3",
            "sentence": "In 1930, Edwin Hubble discovered another universe in space.",
            "wrong_word": "universe",
            "correct_word": "galaxy",
            "fixed_sentence": "In 1930, Edwin Hubble discovered another galaxy in space.",
            "reason": "哈伯（Edwin Hubble）在 1930 年發現的是銀河系以外的另一個『星系 (galaxy)』，宇宙（universe）只有一個！"
        },
        {
            "trap_id": "SP05_ERR_4",
            "sentence": "The Milky Way galaxy is made of billions of icy comets.",
            "wrong_word": "comets.",
            "correct_word": "stars.",
            "fixed_sentence": "The Milky Way galaxy is made of billions of icy stars.",
            "reason": "伽利略透過望遠鏡發現銀河系（Milky Way）明亮的光帶是由無數顆『恆星 (stars)』所組成，而非彗星！"
        },
        {
            "trap_id": "SP05_ERR_5",
            "sentence": "Hubble takes better photos because it is inside Earth's atmosphere.",
            "wrong_word": "inside",
            "correct_word": "outside",
            "fixed_sentence": "Hubble takes better photos because it is outside Earth's atmosphere.",
            "reason": "哈伯太空望遠鏡能拍出更清晰的照片，是因為它運行於地球大氣層『之外 (outside Earth's atmosphere)』，不受大氣干擾！"
        }
    ],
    "RWW6_U05": [
        {
            "trap_id": "RWW05_ERR_1",
            "sentence": "Jaya and her family got lost because they turned right.",
            "wrong_word": "turned right.",
            "correct_word": "went straight.",
            "fixed_sentence": "Jaya and her family got lost because they went straight.",
            "reason": "根據故事第 7-8 行，他們在應該右轉的地方誤『直走 (went straight)』，才走到沒見過的原木長凳！"
        },
        {
            "trap_id": "RWW05_ERR_2",
            "sentence": "When they climbed the small hill, the fog was above them.",
            "wrong_word": "above",
            "correct_word": "below",
            "fixed_sentence": "When they climbed the small hill, the fog was below them.",
            "reason": "根據故事第 18 行，小山丘的山頂高於濃霧（above the fog），所以濃霧是在他們『下方 (below them / at the bottom of the hill)』！"
        },
        {
            "trap_id": "RWW05_ERR_3",
            "sentence": "We knew the trail well, so we needed to watch a map.",
            "wrong_word": "watch",
            "correct_word": "read",
            "fixed_sentence": "We knew the trail well, so we needed to read a map.",
            "reason": "英文中「看地圖、判讀地圖」固定動詞搭配為『read a map』，不可使用 watch 或 look！"
        },
        {
            "trap_id": "RWW05_ERR_4",
            "sentence": "The tall lighthouse with a loud horn was to the north.",
            "wrong_word": "north.",
            "correct_word": "south.",
            "fixed_sentence": "The tall lighthouse with a loud horn was to the south.",
            "reason": "媽媽看地圖定位時指出：城鎮附近的燈塔位於『南方 (south)』，而彎曲大樹的野餐山頭在東北方（northeast）！"
        }
    ],
    "RWW6_U06": [
        {
            "trap_id": "RWW06_ERR_1",
            "sentence": "In orienteering, racers only use a compass to find controls.",
            "wrong_word": "only",
            "correct_word": "both a map and",
            "fixed_sentence": "In orienteering, racers use both a map and a compass to find controls.",
            "reason": "定向越野選手必須『同時使用地圖與指北針 (a map and a compass)』，單靠指北針無法得知控制點位置！"
        },
        {
            "trap_id": "RWW06_ERR_2",
            "sentence": "The racer who crosses the finish line first always wins.",
            "wrong_word": "always",
            "correct_word": "with a full card",
            "fixed_sentence": "The racer who crosses the finish line with a full card wins.",
            "reason": "定向越野規定必須找齊所有控制點並打滿整張控制卡（with a full card）；若漏打一個點，就算第一個衝線也不算贏！"
        },
        {
            "trap_id": "RWW06_ERR_3",
            "sentence": "Control flags are placed so racers can see them easily.",
            "wrong_word": "easily.",
            "correct_word": "hardly.",
            "fixed_sentence": "Control flags are placed so racers cannot see them easily.",
            "reason": "課文第 14-21 行指出控制旗刻意藏在大石頭前或樹後，從各方向都『不容易直接看見 (can't see them easily)』！"
        },
        {
            "trap_id": "RWW06_ERR_4",
            "sentence": "According to Figure 2, there are twelve controls on the card.",
            "wrong_word": "twelve",
            "correct_word": "eighteen",
            "fixed_sentence": "According to Figure 2, there are eighteen controls on the card.",
            "reason": "檢視課本 Figure 2 的定向越野打卡表（Control Card），上面共有編號 1 到『18 (eighteen)』個打卡格！"
        }
    ],
    "RWW6_U07": [
        {
            "trap_id": "RWW07_ERR_1",
            "sentence": "Spanish is the official language of Mexico by government law.",
            "wrong_word": "official",
            "correct_word": "most spoken",
            "fixed_sentence": "Spanish is the most spoken language of Mexico by government law.",
            "reason": "墨西哥從未通過法律（never passed a law）指定官方語言，因此墨西哥有『0 個官方語言』，西班牙語只是最普遍使用的語言！"
        },
        {
            "trap_id": "RWW07_ERR_2",
            "sentence": "According to the bar graph, eight countries have one official language.",
            "wrong_word": "one",
            "correct_word": "no",
            "fixed_sentence": "According to the bar graph, eight countries have no official language.",
            "reason": "根據第 51 頁長條圖，有 8 個國家是『0 個官方語言 (no official language)』；擁有 1 個官方語言的國家高達 110 國！"
        },
        {
            "trap_id": "RWW07_ERR_3",
            "sentence": "China has the most official languages in the world with sixteen.",
            "wrong_word": "China",
            "correct_word": "Zimbabwe",
            "fixed_sentence": "Zimbabwe has the most official languages in the world with sixteen.",
            "reason": "擁有全世界最多官方語言（16 種）的國家是非洲的『辛巴威 (Zimbabwe)』！"
        },
        {
            "trap_id": "RWW07_ERR_4",
            "sentence": "An official language is the first language you learn at home.",
            "wrong_word": "An official",
            "correct_word": "A native",
            "fixed_sentence": "A native language is the first language you learn at home.",
            "reason": "在家中從小習得的第ㄧ語言稱為『母語 (native language)』；政府立法在學校與公務使用的才叫官方語言 (official language)！"
        }
    ],
    "RWW6_U08": [
        {
            "trap_id": "RWW08_ERR_1",
            "sentence": "When Rosa met Erico, she first spoke to him in Portuguese.",
            "wrong_word": "Portuguese.",
            "correct_word": "Italian.",
            "fixed_sentence": "When Rosa met Erico, she first spoke to him in Italian.",
            "reason": "故事第 1-2 行明確寫道：Rosa 因為看到 Erico 的名字像義大利文，開口第一句話是用『義大利語 (Italian)』請他幫忙扶門！"
        },
        {
            "trap_id": "RWW08_ERR_2",
            "sentence": "Erico grew up in Australia, so he speaks with an Australian accent.",
            "wrong_word": "an Australian",
            "correct_word": "a British",
            "fixed_sentence": "Erico grew up in Australia, so he speaks with a British accent.",
            "reason": "Rosa 驚訝地發現 Erico 雖然來自澳洲家庭，但說話卻帶著『英國腔 (British accent)』，這也是結尾長故事的伏筆！"
        },
        {
            "trap_id": "RWW08_ERR_3",
            "sentence": "Being bilingual means a person can speak three languages fluently.",
            "wrong_word": "three",
            "correct_word": "two",
            "fixed_sentence": "Being bilingual means a person can speak two languages fluently.",
            "reason": "字首『bi-』代表數字 2，因此『bilingual（雙語的）』是指能流利使用『兩種 (two)』語言！"
        },
        {
            "trap_id": "RWW08_ERR_4",
            "sentence": "Erico thought Rosa was rude because she asked many questions.",
            "wrong_word": "rude",
            "correct_word": "friendly",
            "fixed_sentence": "Erico thought Rosa was friendly because she asked many questions.",
            "reason": "故事第 31-32 行指出 Erico 明白問這麼多問題是 Rosa 表達『友善 (friendly)』的方式，並親切幫她撿畫具！"
        }
    ]
}

def build_mistake_tokens(item):
    """精準定位 wrong_word 在 sentence.split() 中的 index，杜絕錯位"""
    sentence = item["sentence"]
    wrong_word = item["wrong_word"]
    correct_word = item["correct_word"]
    tokens = sentence.split()
    wrong_idx = -1

    # 1. 若 wrong_word 含有空格（多詞片語），將其在 tokens 中合併為單一 token，方便小學生一鍵點擊
    if " " in wrong_word and wrong_word in sentence:
        sub_parts = wrong_word.split()
        n = len(sub_parts)
        for i in range(len(tokens) - n + 1):
            if " ".join(tokens[i:i+n]) == wrong_word:
                merged_tokens = tokens[:i] + [wrong_word] + tokens[i+n:]
                return merged_tokens, i, wrong_word, correct_word

    # 2. 精確匹配含標點或去標點之單一 token（由後往前或精確比對，避免誤中句首常見字）
    w_clean = re.sub(r'[.,!?;:"]', '', wrong_word).lower()
    for idx, t in enumerate(tokens):
        if t == wrong_word:
            wrong_idx = idx
            break
    if wrong_idx == -1:
        for idx, t in enumerate(tokens):
            t_clean = re.sub(r'[.,!?;:"]', '', t).lower()
            if t_clean == w_clean:
                wrong_idx = idx
                wrong_word = t
                break

    if wrong_idx == -1:
        wrong_idx = 0

    return tokens, wrong_idx, wrong_word, correct_word


# 4. 針對各單元選擇題、克漏字、填空題與改寫題之精準題庫補充與詳解生成
UNIT_GRAMMAR_META = {
    "ODG3_U13": {
        "concept": "Unit 13 附和句核心文法（Too / Either / So / Neither 助動詞與 Be 動詞對齊）",
        "trap": "必考陷阱：① 前句是 be 動詞 (was/were)，附和句必用 was/were，禁用 did；② 否定句尾必用 either，禁用 too；③ Neither 本身已否定，後面助動詞必用肯定形 (Neither did Reis)！"
    },
    "ODG3_U14": {
        "concept": "Unit 14 副詞比較級與最高級（Comparative & Superlative Adverbs）",
        "trap": "必考陷阱：① 字尾 -ly 多音節副詞比較級加 more / the most (more clearly)；② 單音節 fast/hard 直接加 -er/-est；③ far 的不規則變化為 further / the furthest，絕不可加 more！"
    },
    "ODG3_U15": {
        "concept": "Unit 15 可數與不可數名詞及容器計量片語（Measure Words & How much/many）",
        "trap": "必考陷阱：① 液體/粉末/麵團 (milk, water, flour, dough, olive oil) 為不可數，訊問用 How much；② 複數加在容器上 (two loaves of bread)，不可數名詞本身絕不可加 -s！"
    },
    "WR3_U04": {
        "concept": "Unit 4 社區導覽寫作：現在完成式 (have lived... for) 與方位介系詞",
        "trap": "必考陷阱：① have lived + for + 一段時間，句尾絕對不可加 ago；② 在對面是 is across from（不可寫 cross）；③ 靠近某地是 Close to + 地點（不可漏寫 to）！"
    },
    "WR3_U05": {
        "concept": "Unit 5 與現在事實相反之第二條件句（If + 過去式, S + would + 原形動詞）",
        "trap": "必考陷阱：① If 子句動詞必須用過去式 (If I had / If I were)；② 主句必須用 would + 原形動詞 (would buy / would save)，不可用 will 或 would bought！"
    },
    "SPACE_CH04": {
        "concept": "Space Ch.4 小行星帶、古柏帶、彗星、流星與隕石撞擊史",
        "trap": "科學定義辨析：asteroid (火星與木星間的岩石)、comet (古柏帶的冰與塵埃，靠近太陽有長尾巴)、meteor (大氣層中燃燒的流星) vs. meteorite (撞擊地面的隕石)！"
    },
    "SPACE_CH05": {
        "concept": "Space Ch.5 天文學發展史：哥白尼日心說、伽利略望遠鏡、牛頓重力與哈伯星系",
        "trap": "科學史辨析：Copernicus (1543 提出太陽中心說)、Galileo (1609 用望遠鏡看月球坑洞與木星四衛星)、Newton (發現萬有引力證明公轉)、Hubble (1930 發現另一個星系 galaxy 而非 universe)！"
    },
    "RWW6_U05": {
        "concept": "Unit 5 閱讀策略：分析故事時空背景 (Identify Setting) 與戶外方位指引",
        "trap": "細節注意：濃霧 (foggy morning) 導致他們在該右轉處誤直走 (went straight)；爬上小山頂後位於濃霧之上 (above the fog)；看地圖英文必用 read a map！"
    },
    "RWW6_U06": {
        "concept": "Unit 6 閱讀策略：運用圖表視覺資訊 (Use Visuals) 與定向越野規則",
        "trap": "規則與圖表細節：Figure 2 控制卡共有 18 個控制點 (controls)；獲勝條件是「打滿全卡所有控制點 (finish with a full card)」而非單純跑最快！"
    },
    "RWW6_U07": {
        "concept": "Unit 7 閱讀策略：長條圖判讀 (Bar Graph) 與母語 vs. 官方語言定義",
        "trap": "數據與定義辨析：國家必須通過法律 (pass a law) 才有官方語言（墨西哥與美國為 0 官方語言，共 8 國）；110 國有 1 種官方語言；辛巴威有 16 種居冠！"
    },
    "RWW6_U08": {
        "concept": "Unit 8 閱讀策略：根據文本線索進行預測 (Make Predictions) 與多國語言文化",
        "trap": "人物與字彙細節：Rosa 抱著畫紙畫筆代表要去上美術課 (art class)；Rosa 第一句話講 Italian；Erico 雖來自澳洲家庭但講話是英國腔 (British accent)；bilingual 指雙語！"
    }
}

# 補足各單元缺少之題型與高強度岱崙考卷變式專項題（讓每單元 4 大分類篩選器 100% 都有題目可練）
CURATED_EXTRA_QUIZZES = {
    "ODG3_U13": [
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙考券題型】[Olivia, Penny - 100% on quiz / so]（提示：使用過去簡單式，切勿漏寫動詞 got！）",
            "answer": "Olivia got 100% on her quiz, and so did Penny.",
            "hint": "公式：主詞 A + got 100% on her quiz, and so did + 主詞 B.",
            "explanation": {
                "concept": "Unit 13 肯定倒裝附和長句合成（so + did + 主詞）",
                "formula": "Olivia got 100% on her quiz, and so did Penny.",
                "trap": "考場真實失分：① 看到 100% on quiz 忘了補動詞 got；② 誤寫成 100% did Penny 或 Penny was so did ❌！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙考券題型】[Ryan, Michael - 95% on quiz / too]（提示：使用過去簡單式，注意後句助動詞！）",
            "answer": "Ryan got 95% on his quiz, and Michael did, too.",
            "hint": "公式：主詞 A + got 95% on his quiz, and + 主詞 B + did, too.",
            "explanation": {
                "concept": "Unit 13 肯定句尾附和長句合成（主詞 + did, too）",
                "formula": "Ryan got 95% on his quiz, and Michael did, too.",
                "trap": "考場真實失分：前句動詞是過去式一般動詞 got，後句必須用『Michael did, too』，絕對不可寫 Michael are too ❌！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙考券題型】[Brad, Lisa - did not play baseball / either]（提示：否定句尾附和）",
            "answer": "Brad did not play baseball, and Lisa didn't, either.",
            "hint": "公式：主詞 A + did not V..., and + 主詞 B + didn't, either.",
            "explanation": {
                "concept": "Unit 13 否定句尾附和長句合成（主詞 + didn't, either）",
                "formula": "Brad did not play baseball, and Lisa didn't, either.",
                "trap": "否定句尾必須搭配『didn't, either』，不可用 too 或 did, either！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙考券題型】[Ray, Jim - not pass quiz / either]（提示：過去式否定必用 didn't pass！）",
            "answer": "Ray didn't pass the quiz, and Jim didn't, either.",
            "hint": "過去式一般動詞否定：Ray didn't pass the quiz（不可寫 Ray are not pass）",
            "explanation": {
                "concept": "Unit 13 過去簡單式否定與 either 附和",
                "formula": "Ray didn't pass the quiz, and Jim didn't, either.",
                "trap": "考場真實失分：看到題幹給 not pass quiz，誤寫成 Ray are not pass quiz ❌！一般動詞過去式否定必須請出 didn't！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙變式題型】[Ray, Jim - not pass quiz / neither]（提示：改用 neither 倒裝附和！）",
            "answer": "Ray didn't pass the quiz, and neither did Jim.",
            "hint": "公式：Ray didn't pass the quiz, and neither did Jim.（neither 後接肯定助動詞 did）",
            "explanation": {
                "concept": "Unit 13 否定倒裝附和長句合成（neither + did + 主詞）",
                "formula": "Ray didn't pass the quiz, and neither did Jim.",
                "trap": "neither 本身已含 not，後面助動詞必須用肯定形『did』，嚴禁寫成 neither didn't Jim ❌！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙變式題型】[Edison, Swan - a famous inventor / so]（提示：名詞身分無動作動詞，需用 be 動詞 was！）",
            "answer": "Edison was a famous inventor, and so was Swan.",
            "hint": "「是...發明家」用過去式 be 動詞 was，後句倒裝也必須用 so was Swan！",
            "explanation": {
                "concept": "Unit 13 Be 動詞過去式肯定倒裝（so + was/were + 主詞）",
                "formula": "Edison was a famous inventor, and so was Swan.",
                "trap": "前句是『was a famous inventor』，後句必須對齊 be 動詞寫『so was Swan』，不可慣性寫成 so did Swan ❌！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙變式題型】[Meucci, Reis - not rich and famous / neither]（提示：形容詞狀態需用 wasn't，後句用 neither was！）",
            "answer": "Meucci wasn't rich and famous, and neither was Reis.",
            "hint": "rich and famous 是形容詞，前面動詞用 wasn't，倒裝用 neither was Reis",
            "explanation": {
                "concept": "Unit 13 Be 動詞過去式否定倒裝（neither + was/were + 主詞）",
                "formula": "Meucci wasn't rich and famous, and neither was Reis.",
                "trap": "形容詞 rich 前面沒有一般動詞，必須用 be 動詞 wasn't，後句倒裝對應寫 neither was Reis！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙變式題型】[Swan, Edison - got a patent for his invention / too]（提示：一般動詞過去式 got，句尾用 did, too）",
            "answer": "Swan got a patent for his invention, and Edison did, too.",
            "hint": "前句動詞為 got，後句精簡附和為 and Edison did, too.",
            "explanation": {
                "concept": "Unit 13 一般動詞過去式肯定句尾附和",
                "formula": "Swan got a patent for his invention, and Edison did, too.",
                "trap": "切勿把 got 當成 be 動詞，後句必須用 Edison did, too。"
            }
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "Olivia got 100% on her quiz, and ( ______ ).",
            "options": ["so did Penny", "Penny was, too", "100% did Penny", "so was Penny"],
            "answer": "so did Penny",
            "hint": "前句動詞是過去式一般動詞 got，肯定倒裝用 so did + 主詞",
            "explanation": {
                "concept": "Unit 13 倒裝附和助動詞判斷",
                "formula": "got (一般動詞過去式) ➔ so did Penny / Penny did, too。",
                "trap": "不可選 so was Penny 或 100% did Penny。"
            }
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "Bell's mother was deaf, and ( ______ ).",
            "options": ["so was his wife", "so did his wife", "his wife did, too", "neither was his wife"],
            "answer": "so was his wife",
            "hint": "前句是肯定的 was deaf (be動詞)，附和必須沿用 was",
            "explanation": {
                "concept": "Unit 13 Be 動詞與一般動詞附和辨析",
                "formula": "was deaf ➔ so was his wife / his wife was, too。",
                "trap": "看到前句是 was，後句絕對不能選 did！"
            }
        }
    ],
    "ODG3_U14": [
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙 W4 真題】How did they do in their quiz? Anne: 100%, Penny: 95% & Eric: 90%（用 well 寫出三級比較長句，注意從 90% 的 Eric 寫起！）",
            "answer": "Eric did well in his quiz, Penny did better than Eric, but Anne did the best.",
            "hint": "三段式公式：<原級子句>, <比較級子句>, but <最高級子句>. (well ➔ better ➔ the best)",
            "explanation": {
                "concept": "Unit 14 不規則副詞三級比較長句合成（well ➔ better ➔ the best）",
                "formula": "Eric did well in his quiz, Penny did better than Eric, but Anne did the best.",
                "trap": "考場 0 分慘痛陷阱：① 絕對不能漏掉第一句原級（Eric did well in his quiz,）；② 因為比較 well（好 ➔ 更好 ➔ 最好），順序必須從 90% (Eric) ➔ 95% (Penny) ➔ 100% (Anne)！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙 W4 真題】How did they do in their quiz? Jerome: 65%, Ivan: 55% & Nate: 45%（用 badly 寫出三級比較長句，注意 badly ➔ worse ➔ the worst！）",
            "answer": "Jerome did badly in his quiz, Ivan did worse than Jerome, but Nate did the worst.",
            "hint": "因為比較 badly（差 ➔ 更差 ➔ 最差），從 65% (Jerome) ➔ 55% (Ivan) ➔ 45% (Nate)！",
            "explanation": {
                "concept": "Unit 14 不規則副詞三級比較長句合成（badly ➔ worse ➔ the worst）",
                "formula": "Jerome did badly in his quiz, Ivan did worse than Jerome, but Nate did the worst.",
                "trap": "考場真實失分：第一句原級『Jerome did badly in his quiz,』不可漏寫；Ivan did worse 後方不可漏寫『than Jerome』！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙 W4 真題】The distance they flew: eagle: 41km, duck: 91km & pigeon: 282km（用過去式 flew 與 far 寫出三級比較長句）",
            "answer": "An eagle flew far, a duck flew farther than an eagle, but a pigeon flew the farthest.",
            "hint": "注意 eagle 母音開頭用 An eagle；far ➔ farther (或 further) than ➔ the farthest (或 the furthest)",
            "explanation": {
                "concept": "Unit 14 距離副詞三級比較長句合成（far ➔ farther/further ➔ the farthest/furthest）",
                "formula": "An eagle flew far, a duck flew farther than an eagle, but a pigeon flew the farthest.",
                "trap": "考場真實失分：① 切勿漏寫第一句『An eagle flew far,』；② eagle 前冠詞必須用 an；③ flew 拼寫是 f-l-e-w 不是 frew！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙 W4 真題】How do they laugh? witch, vampire & zombie（用 horribly 寫出三級比較長句，注意現在式 do ➔ laughs！）",
            "answer": "A witch laughs horribly, a vampire laughs more horribly than a witch, but a zombie laughs the most horribly.",
            "hint": "問句是 How do they laugh (現在式)！三單主詞動詞必加 -s (laughs)，比較級必加 more！",
            "explanation": {
                "concept": "Unit 14 多音節副詞三級比較 + 現在簡單式第三人稱單數動詞 (-s)",
                "formula": "A witch laughs horribly, a vampire laughs more horribly than a witch, but a zombie laughs the most horribly.",
                "trap": "考場 4 重陷阱：① 必寫第一句 A witch laughs horribly；② 現在式必加 -s (laughs，不可寫 laughed)；③ 比較級必加 more (more horribly than)；④ zombie 勿拼成 zoobie！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙 W4 真題】How did they move? snail, tortoise & the old man（用過去式 moved 與 slowly 寫出三級比較長句，從 the old man 寫起！）",
            "answer": "The old man moved slowly, a tortoise moved more slowly than the old man, but a snail moved the most slowly.",
            "hint": "比誰移動得「更慢 (more slowly)」，順序：the old man (慢) ➔ a tortoise (更慢) ➔ a snail (最慢)",
            "explanation": {
                "concept": "Unit 14 多音節副詞三級比較 + 常識邏輯排序（slowly ➔ more slowly ➔ the most slowly）",
                "formula": "The old man moved slowly, a tortoise moved more slowly than the old man, but a snail moved the most slowly.",
                "trap": "注意題目雖然把 snail 寫在第一個，但因為要比「誰更慢、誰最慢」，必須把最慢的 a snail 放在最後壓軸（the most slowly）！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙 W5 真題】How fast do they run? person, dog & lion（注意題幹是現在式 do they run，單數名詞記得加 a，最高級加 the！）",
            "answer": "A person runs fast, a dog runs faster than a person, but a lion runs the fastest.",
            "hint": "現在式三單動詞 runs；fast ➔ faster than ➔ the fastest",
            "explanation": {
                "concept": "Unit 14 單音節副詞三級比較（fast ➔ faster ➔ the fastest）",
                "formula": "A person runs fast, a dog runs faster than a person, but a lion runs the fastest.",
                "trap": "考場真實失分：① 漏寫第一句 A person runs fast；② lion 前面漏寫 a；③ fastest 前面漏寫 the；④ 題幹問 do they run，不要自己亂加 can！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙 W5 真題】How quickly can they walk? five year old, eight year old & adult（注意 eight 與 adult 前面冠詞用 an！）",
            "answer": "A five year old can walk quickly, an eight year old can walk more quickly than a five year old, but an adult can walk the most quickly.",
            "hint": "比較級必須寫完整：can walk more quickly than（不可漏掉 quickly！）",
            "explanation": {
                "concept": "Unit 14 助動詞 can + 多音節副詞三級比較（quickly ➔ more quickly ➔ the most quickly）",
                "formula": "A five year old can walk quickly, an eight year old can walk more quickly than a five year old, but an adult can walk the most quickly.",
                "trap": "考場真實失分：中間句誤寫成 can walk more than ❌（漏了 quickly）；且 eight 與 adult 為母音開頭，冠詞必須用 an！"
            }
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "【岱崙 W5 真題】How far can they jump? frog, rabbit & kangaroo（注意 a kangaroo 冠詞與 the farthest 最高級！）",
            "answer": "A frog can jump far, a rabbit can jump farther than a frog, but a kangaroo can jump the farthest.",
            "hint": "far ➔ farther (或 further) than ➔ the farthest (或 the furthest)",
            "explanation": {
                "concept": "Unit 14 助動詞 can + 不規則副詞三級比較",
                "formula": "A frog can jump far, a rabbit can jump farther than a frog, but a kangaroo can jump the farthest.",
                "trap": "考場真實失分：but 後面的單數名詞『a kangaroo』千萬別漏掉冠詞 a，最高級別漏掉 the！"
            }
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "A witch laughs horribly, a vampire laughs ( ______ ) than a witch, but a zombie laughs the most horribly.",
            "options": ["more horribly", "horribly", "horriblier", "most horribly"],
            "answer": "more horribly",
            "hint": "後面有 than，多音節副詞 horribly 比較級前面必須加 more",
            "explanation": {
                "concept": "Unit 14 多音節副詞比較級",
                "formula": "more + 多音節副詞 (horribly) + than。",
                "trap": "考場真實失分：漏寫 more 直接寫 horribly than ❌。"
            }
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "Jerome did badly in his quiz, Ivan did ( ______ ) than Jerome, but Nate did the worst.",
            "options": ["worse", "more badly", "badlier", "worst"],
            "answer": "worse",
            "hint": "badly 的不規則比較級是 worse",
            "explanation": {
                "concept": "Unit 14 不規則副詞比較級（badly ➔ worse ➔ the worst）",
                "formula": "did badly ➔ did worse than ➔ did the worst。",
                "trap": "badly 是不規則變化，不可選 more badly 或 badlier！"
            }
        }
    ],
    "ODG3_U15": [
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "句型造句：用 How much 與 olive oil 造出詢問數量的疑問句（need / for the pizza）",
            "answer": "How much olive oil do we need for the pizza?",
            "hint": "olive oil 為不可數名詞，疑問詞用 How much"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "句型改寫：There is one loaf of bread on the table.（將 one 改為 three 並改寫全句）",
            "answer": "There are three loaves of bread on the table.",
            "hint": "注意 is 改為 are，loaf 複數去 f 改 ves (loaves)，bread 不可加 s！"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "看圖造句：用 Emily / drink / a glass of milk / before cooking 造出完整現在簡單式句子",
            "answer": "Emily drinks a glass of milk before cooking.",
            "hint": "主詞 Emily 為第三人稱單數，動詞 drink 記得加 -s"
        }
    ],
    "WR3_U04": [
        {
            "type": "choice", "category_tag": "choice",
            "question": "I have lived in my neighborhood ( ______ ) three years.",
            "options": ["for", "since", "ago", "in"],
            "answer": "for",
            "hint": "現在完成式搭配「一段時間長度 (three years)」必用介系詞 for"
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "I can get to my school ( ______ ) ten minutes on foot.",
            "options": ["in", "for", "at", "by"],
            "answer": "in",
            "hint": "表示「在...時間之內可以抵達」使用介系詞 in + 時間"
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "There are many stores ( ______ ) the street from my house.",
            "options": ["across", "cross", "between", "next"],
            "answer": "across",
            "hint": "across the street from...（在...的對街）"
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "The bakery is ( ______ ) the bank and the pharmacy.",
            "options": ["between", "across", "around", "next"],
            "answer": "between",
            "hint": "between A and B（在 A 與 B 兩者之間）"
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "Where do you buy notebooks, pens, and school supplies?",
            "options": ["At the stationery store.", "At the grocery store.", "At the dry cleaner's.", "At the hair salon."],
            "answer": "At the stationery store.",
            "hint": "購買文具與學用品的商店是 stationery store（文具店）"
        }
    ],
    "WR3_U05": [
        {
            "type": "fill", "category_tag": "fill",
            "question": "If I ( ______ ) 300 dollars, I would spend the money wisely. (填入 have 的正確假設語氣時態)",
            "answer": "had",
            "hint": "與現在事實相反的 If 條件句，動詞需用過去式 had"
        },
        {
            "type": "fill", "category_tag": "fill",
            "question": "With the rest of the money, I ( ______ ) open up a bank account and save it.",
            "answer": "would",
            "hint": "假設語氣主要子句助動詞用 would + 原形動詞"
        },
        {
            "type": "fill", "category_tag": "fill",
            "question": "A baseball glove and some comic books would cost ( ______ ) about 70 dollars. (填入 I 的正確代名詞格)",
            "answer": "me",
            "hint": "動詞 cost 後方接人時須用受格 me"
        },
        {
            "type": "fill", "category_tag": "fill",
            "question": "I would treat my best friends ( ______ ) lunch at a hamburger restaurant. (填入正確介系詞)",
            "answer": "to",
            "hint": "treat + 人 + to + 餐點（請某人吃...）"
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "If I ( ______ ) a millionaire, I would donate money to a charity group.",
            "options": ["were", "am", "will be", "be"],
            "answer": "were",
            "hint": "與現在事實相反的假設語氣，be 動詞一律用 were"
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "I would buy a nice warm scarf ( ______ ) my mom.",
            "options": ["for", "to", "with", "at"],
            "answer": "for",
            "hint": "buy + 禮物 + for + 人（買某物給某人，介系詞用 for）"
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "Wouldn't it ( ______ ) great to have 300 dollars?",
            "options": ["be", "is", "was", "been"],
            "answer": "be",
            "hint": "助動詞 Wouldn't 後面必須接原形 be 動詞"
        },
        {
            "type": "choice", "category_tag": "choice",
            "question": "With ( ______ ) of the money, I would open up a bank account.",
            "options": ["the rest", "rest", "many", "a few"],
            "answer": "the rest",
            "hint": "with the rest of the money（用剩下的錢）"
        }
    ],
    "SPACE_CH04": [
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "科學事實改錯重寫：The asteroid belt is between Earth and the Sun.",
            "answer": "The asteroid belt is between Mars and Jupiter.",
            "hint": "小行星帶位於火星 (Mars) 與木星 (Jupiter) 之間"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "科學事實改錯重寫：Comets become colder when they are near the Sun.",
            "answer": "Comets become hotter when they are near the Sun.",
            "hint": "彗星靠近太陽時會變得更熱 (hotter) 並產生彗尾"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "科學事實改錯重寫：Some meteorites hit the Moon in 1994.",
            "answer": "Twenty-one pieces of a comet hit Jupiter in 1994.",
            "hint": "1994 年是 21 塊彗星碎片撞擊木星 (Jupiter)"
        }
    ],
    "SPACE_CH05": [
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "科學史重寫：用 Isaac Newton / prove / Earth orbits the Sun 造出過去式完整句",
            "answer": "Isaac Newton proved that Earth orbits the Sun.",
            "hint": "牛頓發現萬有引力並證明了地球繞太陽公轉"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "科學事實改錯重寫：In 1930, Edwin Hubble discovered another universe.",
            "answer": "In 1930, Edwin Hubble discovered another galaxy.",
            "hint": "哈伯發現的是另一個星系 (galaxy)，而非另一個宇宙"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "科學問答造句：Why can the Hubble Space Telescope take better photos than telescopes on Earth?",
            "answer": "Because it is outside Earth's atmosphere.",
            "hint": "因為哈伯太空望遠鏡位於地球大氣層之外 (outside Earth's atmosphere)"
        }
    ],
    "RWW6_U05": [
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "閱讀理解造句：Where is the family in the story, and what is the weather like?",
            "answer": "They are on a hiking trail in the hills, and it is very foggy.",
            "hint": "描述時空背景 (Setting)：在山間健行步道上，且天氣濃霧瀰漫 (foggy)"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "方位片語造句：用 turn right / instead of / go straight 完成句子（We should...）",
            "answer": "We should turn right instead of going straight.",
            "hint": "instead of 後面動詞要加 -ing (going straight)"
        }
    ],
    "RWW6_U06": [
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "閱讀理解造句：What two tools do racers use to find controls in orienteering?",
            "answer": "Racers use a map and a compass to find controls.",
            "hint": "定向越野必備兩大導航工具：a map and a compass"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "規則造句：How does a racer win an orienteering race? (用 find all the controls / full card 回答)",
            "answer": "A racer must find all the controls and finish with a full card to win.",
            "hint": "必須找齊所有控制點並打滿整張控制卡才能獲勝"
        }
    ],
    "RWW6_U07": [
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "定義造句：What does a country have to do to make a language official? (用 pass a law 回答)",
            "answer": "A country has to pass a law to make a language official.",
            "hint": "國家必須通過法律 (pass a law) 才能將語言定為官方語言"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "圖表數據造句：According to the bar graph, how many countries have no official language?",
            "answer": "Eight countries have no official language.",
            "hint": "長條圖中 0 official languages 對應的國家數量是 8 國"
        }
    ],
    "RWW6_U08": [
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "情境預測造句：What class do you predict Rosa is going to, and why?",
            "answer": "She is going to an art class because she is carrying drawing paper and paint brushes.",
            "hint": "從她攜帶圖畫紙、水彩筆與色鉛筆預測她要去上美術課 (art class)"
        },
        {
            "type": "paper_rewrite", "category_tag": "rewrite",
            "question": "字彙定義造句：What does the word 'bilingual' mean? (用 speak two languages 造句)",
            "answer": "Bilingual means being able to speak two languages.",
            "hint": "bilingual 指能夠說兩種語言"
        }
    ]
}

def parse_markdown(meta):
    file_path = meta["file"]
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    # 1. Frontmatter
    fm = {}
    fm_m = re.match(r'^---\s*([\s\S]*?)\s*---', raw_content)
    if fm_m:
        try:
            fm = yaml.safe_load(fm_m.group(1)) or {}
        except:
            pass

    unit_id = meta["id"]
    g_meta = UNIT_GRAMMAR_META.get(unit_id, {
        "concept": f"{meta['display_title']} 核心考點",
        "trap": "注意主詞動詞時態一致性與單字拼寫細節。"
    })

    # 2. 提取精選課文與中文翻譯 (Curated Passages)
    passages = CURATED_PASSAGES.get(unit_id, [])

    # 3. 提取 100% 純淨單字庫 (Curated Vocab)
    vocab = CURATED_VOCAB.get(unit_id, [])

    # 4. 提取 100% 精準單詞索引改錯題 (Curated Mistake Buster)
    mistake_buster = []
    for m_item in CURATED_MISTAKES.get(unit_id, []):
        tokens, w_idx, w_word, c_word = build_mistake_tokens(m_item)
        mistake_buster.append({
            "trap_id": m_item["trap_id"],
            "sentence": m_item["sentence"],
            "tokens": tokens,
            "wrong_index": w_idx,
            "wrong_word": w_word,
            "correct_word": c_word,
            "fixed_sentence": m_item["fixed_sentence"],
            "reason": m_item["reason"]
        })

    # 5. 提取紙筆測驗題庫 (Quizzes)
    quizzes = []

    # A. 🔤 單字盲聽題型 (Spelling Listen)：僅使用純淨英文單字/片語，附音標、音節與專屬拼寫提示
    for v_idx, v in enumerate(vocab):
        w = v["word"].strip()
        meaning = v.get("meaning", "")
        note = v.get("note", "")
        example = v.get("example", "")
        phonetic = v.get("phonetic", "")
        syllables = v.get("syllables", w)
        pos = v.get("pos", "")
        quizzes.append({
            "id": f"{unit_id}_LIST_{v_idx+1}",
            "type": "spelling_listen",
            "category_tag": "listening",
            "question": "請聽電腦發音，在紙上拼寫出這個核心單字或片語：",
            "hint": f"詞性與中文：{pos} {meaning}",
            "audio_word": w,
            "phonetic": phonetic,
            "syllables": syllables,
            "answer": w,
            "explanation": {
                "concept": f"【{meta['display_title']}】核心字彙：{w} {phonetic} ({pos} {meaning})",
                "formula": f"課文例句：{example}",
                "trap": f"拼寫與用法關鍵：{note}"
            }
        })

    # B. 二選一括號選擇 (轉為填空題)
    circle_qs = re.findall(r'(\d+)\.\s+([^\[\]\n]+?)\s*(?:\[([^\[\]\n]+)\]\s*/\s*([^\n\s]+)|([^\n\s]+)\s*/\s*\[([^\[\]\n]+)\])', raw_content)
    for q_num, stem, opt_correct_1, opt_wrong_1, opt_wrong_2, opt_correct_2 in circle_qs:
        ans = (opt_correct_1 or opt_correct_2).strip()
        wrong_opt = (opt_wrong_1 or opt_wrong_2).strip().rstrip('.')
        stem_clean = stem.strip()
        quizzes.append({
            "id": f"{unit_id}_FILL_{len(quizzes)+1}",
            "type": "fill",
            "category_tag": "fill",
            "question": f"{stem_clean} ( {ans} / {wrong_opt} )",
            "answer": ans,
            "hint": f"二選一填空：請判斷應填入 {ans} 還是 {wrong_opt}",
            "explanation": {
                "concept": g_meta["concept"],
                "formula": f"正確完整句：{stem_clean} {ans}. （正解：{ans}，淘汰干擾項：{wrong_opt}）",
                "trap": g_meta["trap"]
            }
        })

    # B2. 課文對話與段落編號填空 (例如 ODG3_U13 Part C `**¹ [too]**` 與 ODG3_U14 Part B `**¹ [nervously]** *(nervous)*`)
    numbered_blanks = re.findall(r'([^.!?\n>]*\*\*[¹²³⁴⁵⁶⁷⁸⁹⁰]+\s*\[([^\]]+)\]\*\*(?:\s*\*\(([^)]+)\)\*)?[^.!?\n]*[.!?])', raw_content)
    for full_sent, ans_raw, paren_hint in numbered_blanks:
        ans_clean = ans_raw.strip()
        # 跳過已經在 C2 收錄的 [a. ...] 選擇式克漏字或句子配對
        if re.match(r'^[a-g]\.\s', ans_clean):
            continue
        q_sent = re.sub(r'\*\*[¹²³⁴⁵⁶⁷⁸⁹⁰]+\s*\[' + re.escape(ans_raw) + r'\]\*\*', '______', full_sent)
        q_sent = re.sub(r'\*\*[¹²³⁴⁵⁶⁷⁸⁹⁰]+\s*\[([^\]]+)\]\*\*', r'\1', q_sent)
        q_sent = q_sent.replace('*', '').strip()
        hint_str = f"提示詞：({paren_hint})" if paren_hint else "請填入正確的連接副詞或語法詞彙"
        quizzes.append({
            "id": f"{unit_id}_NB_{len(quizzes)+1}",
            "type": "fill",
            "category_tag": "fill",
            "question": q_sent,
            "answer": ans_clean,
            "hint": hint_str,
            "explanation": {
                "concept": g_meta["concept"],
                "formula": f"空格應填入『{ans_clean}』。",
                "trap": g_meta["trap"]
            }
        })

    # C1. 三選一多行選擇題 (ODG3_U13 Part B 等)
    mc_3_pattern = re.compile(
        r'(\d+)\.\s+([^\n]+)\n'
        r'\s*-\s*a\)\s*([^\n]+)\n'
        r'\s*-\s*b\)\s*([^\n]+)\n'
        r'\s*-\s*c\)\s*([^\n]+)'
    )
    for m in mc_3_pattern.finditer(raw_content):
        q_num, stem, raw_a, raw_b, raw_c = m.groups()
        raw_opts = [raw_a, raw_b, raw_c]
        clean_opts = []
        ans = ""
        for idx, ro in enumerate(raw_opts):
            # 檢查是否標記為正解
            is_correct = ("**" in ro) or re.search(r'\*\(正解[：:]\s*' + 'abc'[idx] + r'\)\*', ro)
            co = re.sub(r'\*\(正解[：:][^*]+\)\*', '', ro)
            co = co.replace('*', '').strip()
            clean_opts.append(co)
            if is_correct:
                ans = co
        if not ans and clean_opts:
            ans = clean_opts[0]
        quizzes.append({
            "id": f"{unit_id}_MC_{len(quizzes)+1}",
            "type": "choice",
            "category_tag": "choice",
            "question": stem.strip(),
            "options": clean_opts,
            "answer": ans,
            "hint": "三選一選擇題：請看選項在紙上寫下正確答案或代號",
            "explanation": {
                "concept": g_meta["concept"],
                "formula": f"題幹語境對應正解為『{ans}』（選項：{' / '.join(clean_opts)}）。",
                "trap": g_meta["trap"]
            }
        })

    # C2. 單行斜線三選一克漏字選擇題 (ODG3_U14 Part C & ODG3_U15 Part F)
    # 例如: 1. a most easier / b more than easily / **c more easily** *(正解：c)*
    inline_mc_pattern = re.compile(r'(\d+)\.\s+(?:a|\*\*a)\s+([^/\n]+?)\s*/\s*(?:b|\*\*b)\s+([^/\n]+?)\s*/\s*(?:c|\*\*c)\s+([^\n]+)')
    # 先抓取克漏字短文中的題號前後文，讓題幹完整呈現句子！
    cloze_context_map = {}
    for s_match in re.finditer(r'([^.!?\n]*\[(\d+)\][^.!?\n]*[.!?])', raw_content):
        full_sent, c_num = s_match.groups()
        sent_blank = re.sub(r'\*\*\[' + c_num + r'\]\s*[^*]+\*\*', '______', full_sent)
        sent_blank = re.sub(r'\[' + c_num + r'\]', '______', sent_blank)
        sent_blank = re.sub(r'\*\*\[\d+\]\s*([^*]+)\*\*', r'\1', sent_blank)
        cloze_context_map[c_num] = sent_blank.strip()

    for m in inline_mc_pattern.finditer(raw_content):
        q_num = m.group(1)
        full_line = m.group(0)
        parts = [p.strip() for p in full_line.split('/')]
        clean_opts = []
        ans = ""
        for idx, p in enumerate(parts):
            # 移除題號與 a/b/c 前綴
            p_no_num = re.sub(r'^\d+\.\s*', '', p)
            is_correct = ("**" in p_no_num) or re.search(r'\*\(正解[：:]\s*' + 'abc'[idx] + r'\)\*', p_no_num)
            co = re.sub(r'\*\(正解[：:][^*]+\)\*', '', p_no_num)
            co = co.replace('*', '').strip()
            co = re.sub(r'^[abc]\s+', '', co).strip()
            clean_opts.append(co)
            if is_correct:
                ans = co
        if not ans and clean_opts:
            ans = clean_opts[0]
        q_stem = cloze_context_map.get(q_num, f"克漏字第 {q_num} 題：請選出正確的語法形式填入空格")
        quizzes.append({
            "id": f"{unit_id}_CLOZE_{len(quizzes)+1}",
            "type": "choice",
            "category_tag": "choice",
            "question": q_stem,
            "options": clean_opts,
            "answer": ans,
            "hint": "克漏字三選一：比較各選項的詞性、比較級/最高級或量詞搭配",
            "explanation": {
                "concept": g_meta["concept"],
                "formula": f"空格填入『{ans}』使全句結構完整：{q_stem.replace('______', ans)}",
                "trap": g_meta["trap"]
            }
        })

    # C3. Markdown 勾選式選擇題 ([ ] a. ... / [x] **b. ...**，涵蓋 RWW6_U05 ~ U08 所有閱讀理解與字義選擇題)
    checkbox_mc_pattern = re.compile(
        r'(\d+)\.\s+([^\n]+)\n'
        r'((?:\s*-\s*\[[xX ]\]\s*[^\n]+\n?){2,4})'
    )
    for m in checkbox_mc_pattern.finditer(raw_content):
        q_num, stem, opts_block = m.groups()
        stem_clean = stem.replace('*', '').strip()
        opt_lines = re.findall(r'-\s*\[([xX ])\]\s*([^\n]+)', opts_block)
        clean_opts = []
        ans = ""
        note_extra = ""
        for mark, o_text in opt_lines:
            # 提取斜體補充說明 *(...)*
            note_m = re.search(r'\*\(([^)]+)\)\*', o_text)
            if note_m and mark.lower() == 'x':
                note_extra = note_m.group(1).strip()
            co = re.sub(r'\*\([^)]+\)\*', '', o_text)
            co = co.replace('*', '').strip()
            co = re.sub(r'^[a-d]\.\s*', '', co).strip()
            clean_opts.append(co)
            if mark.lower() == 'x':
                ans = co
        if not ans and clean_opts:
            ans = clean_opts[0]
        quizzes.append({
            "id": f"{unit_id}_RMC_{len(quizzes)+1}",
            "type": "choice",
            "category_tag": "choice",
            "question": stem_clean,
            "options": clean_opts,
            "answer": ans,
            "hint": "閱讀與字義選擇題：請從選項中選出最符合課文內容的答案",
            "explanation": {
                "concept": g_meta["concept"],
                "formula": f"正解：『{ans}』。{('課文依據：' + note_extra) if note_extra else '根據課文上下文線索與字義推論得出。'}",
                "trap": g_meta["trap"]
            }
        })

    # D. 可數不可數判斷 (ODG3_U15 Part A)
    cn_matches = re.findall(r'(\d+)\.\s+([A-Za-z\s]+?)\s*➔\s*\*\*\[([CN])\]\*\*(?:\s*\*\(?([^)\n]*)\)?\*)?', raw_content)
    for q_num, item, ans, note in cn_matches:
        ans_full = "C (可數名詞)" if ans.strip() == "C" else "N (不可數名詞)"
        quizzes.append({
            "id": f"{unit_id}_CN_{len(quizzes)+1}",
            "type": "choice",
            "category_tag": "choice",
            "question": f"判斷可數 (C: Count) 或不可數 (N: Noncount)：【 {item.strip()} 】",
            "options": ["C (可數名詞)", "N (不可數名詞)"],
            "answer": ans_full,
            "hint": f"提示：{note.strip()}" if note else "在紙上寫下 C 或 N",
            "explanation": {
                "concept": "名詞可數性辨析：Count (可數名詞) vs. Noncount (不可數名詞)",
                "formula": f"名詞『{item.strip()}』屬於【{ans_full}】（{note.strip() if note else '依物質形態判定'}）。",
                "trap": "液體 (water, milk, olive oil, juice)、粉末 (flour)、麵團 (dough) 與肉類起司麵包 (meat, cheese, bread) 皆為不可數名詞！"
            }
        })

    # E. How much / How many 填空 (ODG3_U15 Part D)
    how_matches = re.findall(r'(\d+)\.\s+\*\*\[(How much|How many)\]\*\*\s+([^\n?]+\?)', raw_content)
    for q_num, ans, stem in how_matches:
        quizzes.append({
            "id": f"{unit_id}_HOW_{len(quizzes)+1}",
            "type": "fill",
            "category_tag": "fill",
            "question": f"_______ {stem.strip()} (請填入 How much 或 How many)",
            "answer": ans.strip(),
            "hint": "觀察後面緊接的名詞是「可數複數名詞 (-s)」還是「不可數名詞」",
            "explanation": {
                "concept": "數量疑問詞：How many + 可數複數名詞 vs. How much + 不可數名詞",
                "formula": f"完整問句：{ans.strip()} {stem.strip()}",
                "trap": "即使詢問不可數名詞，若加上複數容器（如 How many loaves of bread），則要改用 How many！"
            }
        })

    # F. SPACE_CH04 專屬：Chicxulub (C) vs Tunguska (T) 隕石撞擊事件分類題
    if unit_id == "SPACE_CH04":
        ct_matches = re.findall(r'(\d+)\.\s+([^\n➔]+?)➔\s*\*\*([CT])\*\*\s*(?:\*\(([^)]+)\)\*)?', raw_content)
        for q_num, stem, ans_code, note in ct_matches:
            opt_c = "C (Chicxulub 希克蘇魯伯隕石)"
            opt_t = "T (Tunguska 通古斯隕石)"
            ans_full = opt_c if ans_code == "C" else opt_t
            quizzes.append({
                "id": f"{unit_id}_CT_{len(quizzes)+1}",
                "type": "choice",
                "category_tag": "choice",
                "question": f"判斷下列特徵屬於哪一場歷史隕石事件：This meteorite {stem.strip()}",
                "options": [opt_c, opt_t],
                "answer": ans_full,
                "hint": "選 C (6500萬年前墨西哥恐龍滅絕隕石) 或 T (1908年俄羅斯西伯利亞空中爆炸隕石)",
                "explanation": {
                    "concept": "Space Ch.4 兩大歷史隕石撞擊事件對比（Chicxulub vs. Tunguska）",
                    "formula": f"正解：{ans_full} — {note.strip() if note else ''}",
                    "trap": "希克蘇魯伯 (Chicxulub) 發生於 6500 萬年前墨西哥、長 20 公里、造成 180 公里隕石坑與恐龍滅絕；通古斯 (Tunguska) 發生於 1908 年俄羅斯空中爆炸、燒毀 8000 萬棵樹。"
                }
            })

    # G. 是非題 (True / False，僅匹配明確的 true/false 或 RWW6 的 T/F，排除 SPACE_CH04 的 C/T)
    if unit_id != "SPACE_CH04":
        tf_matches = re.findall(r'(\d+)\.\s+([^\n➔]+?)➔\s*\*\*(true|false|T|F)\*\*(?:\s*\*\(([^)]+)\)\*)?', raw_content, re.IGNORECASE)
        for q_num, question, ans, exp in tf_matches:
            ans_clean = ans.upper()
            ans_text = "True (正確)" if ans_clean in ['T', 'TRUE'] else "False (錯誤)"
            quizzes.append({
                "id": f"{unit_id}_TF_{len(quizzes)+1}",
                "type": "choice",
                "category_tag": "choice",
                "question": question.strip(),
                "options": ["True (正確)", "False (錯誤)"],
                "answer": ans_text,
                "hint": "是非題：請根據課文事實判斷 True (正確) 或 False (錯誤)",
                "explanation": {
                    "concept": g_meta["concept"],
                    "formula": f"本題為【{ans_text}】。課文依據：{exp.strip() if exp else '根據課文原文細節核對。'}",
                    "trap": g_meta["trap"]
                }
            })

    # H. 課文詞彙定義與克漏字填空題 (SPACE_CH04 Activity 1&2, SPACE_CH05 Activity 2&3, RWW6_U05 Part D&E, RWW6_U07 Part D&E)
    # H1: 定義配對 `1. This is made of ice and dust. ➔ **comet**` (單字答案，非完整句子，歸入 fill 而非 paper_rewrite)
    single_word_arrow = re.findall(r'(\d+)\s*\.?\s+([^\n➔]+?)\s*➔\s*\*\*([a-zA-Z\s]+)\*\*(?:\s*\*\(([^)]+)\)\*)?', raw_content)
    for q_num, clue, ans, note in single_word_arrow:
        ans_s = ans.strip()
        clue_s = clue.strip()
        if ans_s.upper() in ["T", "F", "C", "TRUE", "FALSE"] or "圖片" in clue_s:
            continue
        if len(ans_s.split()) <= 2:
            quizzes.append({
                "id": f"{unit_id}_DEF_{len(quizzes)+1}",
                "type": "fill",
                "category_tag": "fill",
                "question": f"根據英文定義拼寫出核心字彙：{clue_s}",
                "answer": ans_s,
                "hint": f"提示：{note.strip()}" if note else "請根據定義在紙上拼寫出正確單字",
                "explanation": {
                    "concept": f"{meta['display_title']} 英英定義與字彙配對",
                    "formula": f"『{clue_s}』對應的精確單字為：{ans_s}",
                    "trap": g_meta["trap"]
                }
            })

    # H2: 句子中粗體挖空填空 (例如 `1. There are two **rings** around the Sun.`)
    bold_fill_lines = re.findall(r'^\s*(\d+)\.\s+([^\n➔`]+\*\*[^*\n]+\*\*[^\n➔`]*)$', raw_content, re.MULTILINE)
    for q_num, line_text in bold_fill_lines:
        if "[How" in line_text or "[C]" in line_text or "[N]" in line_text:
            continue
        bold_words = re.findall(r'\*\*([^*]+)\*\*', line_text)
        if not bold_words:
            continue
        ans_str = " / ".join(bw.strip() for bw in bold_words)
        q_blank = re.sub(r'\*\*([^*]+)\*\*', '______', line_text).strip()
        quizzes.append({
            "id": f"{unit_id}_BFILL_{len(quizzes)+1}",
            "type": "fill",
            "category_tag": "fill",
            "question": q_blank,
            "answer": ans_str,
            "hint": "課文重點句填空：請在紙上寫出空格處的單字",
            "explanation": {
                "concept": g_meta["concept"],
                "formula": f"完整原句：{line_text.replace('**', '')}",
                "trap": g_meta["trap"]
            }
        })

    # I. 閱讀理解簡答題 (歸類為填空題型)
    qa_matches = re.findall(r'(\d+)\.\s*\*\*([^\n*?]+?\?)\*\*\s*\n\s*-\s*\*Answer\*:\s*`([^`]+)`', raw_content)
    for q_num, q_text, ans in qa_matches:
        quizzes.append({
            "id": f"{unit_id}_QA_{len(quizzes)+1}",
            "type": "fill",
            "category_tag": "fill",
            "question": q_text.strip(),
            "answer": ans.strip(),
            "hint": "閱讀理解簡答：在紙上寫下關鍵答案或完整句子",
            "explanation": {
                "concept": g_meta["concept"],
                "formula": f"標準解答：{ans.strip()}",
                "trap": g_meta["trap"]
            }
        })

    # J. 紙筆句型改寫題 (支援單行與跨行 `➔ **...**` 或 `➔ \`...\``，僅收錄完整句子改寫與造句，徹底排除單字或 T/F/C)
    rewrite_qs = re.findall(
        r'(\d+)\.\s*([^\n➔]+?)\s*(?:\n\s*)?➔\s*(?:`([^`]+)`|\*\*([^*\n]+)\*\*)(?:\s*\*\(([^)]+)\)\*)?',
        raw_content
    )
    rw_count = 0
    for q_num, prompt, ans_tick, ans_bold, note in rewrite_qs:
        ans_clean = (ans_tick or ans_bold).strip()
        p_clean = prompt.strip().replace('*', '')
        if "範例" in (note or "") or "範例" in p_clean:
            continue
        if ans_clean.upper() in ["T", "F", "C", "TRUE", "FALSE", "[C]", "[N]"]:
            continue
        # 排除太基礎的 There is a [單字] 機械造句或半句配對 (at the park.)
        if ans_clean.startswith("There is a ") or ans_clean.startswith("There is an ") or not ans_clean[0].isupper():
            continue
        if len(ans_clean.split()) < 4:
            continue
        if rw_count >= 12:
            break
        rw_count += 1
        quizzes.append({
            "id": f"{unit_id}_RW_{len(quizzes)+1}",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": f"句型改寫與造句：{p_clean}",
            "answer": ans_clean,
            "hint": f"提示：{note.strip()}" if note else "請在紙上寫出完整英文句子，再按「翻牌核對答案」",
            "explanation": {
                "concept": g_meta["concept"],
                "formula": f"標準改寫句：{ans_clean}",
                "trap": f"{note.strip() + '；' if note else ''}{g_meta['trap']}"
            }
        })

    # K. 補足各單元四大題型 (確保每一課的 🔤單字盲聽 / ✏️克漏填空 / 🎯觀念選擇 / 📝手寫造句 皆有充足題目，零空窗)
    extra_list = CURATED_EXTRA_QUIZZES.get(unit_id, [])
    for eq in extra_list:
        quizzes.append({
            "id": f"{unit_id}_EX_{len(quizzes)+1}",
            "type": eq["type"],
            "category_tag": eq["category_tag"],
            "question": eq["question"],
            "options": eq.get("options", []),
            "answer": eq["answer"],
            "hint": eq.get("hint", "請作答後翻牌核對詳解"),
            "explanation": eq.get("explanation", {
                "concept": g_meta["concept"],
                "formula": f"標準解答：{eq['answer']}",
                "trap": g_meta["trap"]
            })
        })

    return {
        "id": unit_id,
        "book": meta["book"],
        "display_title": meta["display_title"],
        "category": meta["category"],
        "category_icon": meta["category_icon"],
        "cefr": fm.get("cefr_target", "A2+"),
        "pages": str(fm.get("pages", "")).split("(")[0].strip(),
        "passages": passages,
        "vocab": vocab,
        "mistake_buster": mistake_buster,
        "quizzes": quizzes
    }

def main():
    print("Parsing all 11 midterm units with 100% clean vocab, mistake_buster, and quizzes...")
    units = []
    for m in FILES:
        u = parse_markdown(m)
        if u:
            units.append(u)
            sent_total = sum(len(p["sentences"]) for p in u["passages"])
            q_counts = {}
            for q in u["quizzes"]:
                t = q.get("category_tag", q.get("type"))
                q_counts[t] = q_counts.get(t, 0) + 1
            print(f"[{u['category']}] {u['display_title']}: {len(u['passages'])} 篇課文 ({sent_total} 句), {len(u['vocab'])} 單字, {len(u['mistake_buster'])} 改錯題, {len(u['quizzes'])} 題測驗 {q_counts}")

    # 注入岱崙美語 3C Quiz 歷史考卷專屬特訓單元
    try:
        from exam_review_data import EXAM_REVIEW_UNIT
        units.append(EXAM_REVIEW_UNIT)
        sent_total = sum(len(p["sentences"]) for p in EXAM_REVIEW_UNIT["passages"])
        print(f"[{EXAM_REVIEW_UNIT['category']}] {EXAM_REVIEW_UNIT['display_title']}: {len(EXAM_REVIEW_UNIT['passages'])} 篇課文 ({sent_total} 句), {len(EXAM_REVIEW_UNIT['vocab'])} 單字, {len(EXAM_REVIEW_UNIT['mistake_buster'])} 改錯題, {len(EXAM_REVIEW_UNIT['quizzes'])} 題測驗")
    except Exception as e:
        print(f"Error injecting EXAM_REVIEW_UNIT: {e}")

    js_code = f"""// ============================================================================
// 六年級上學期英語期中考特訓資料庫 (midterm_data.js)
// 包含 4 套教材、11 個單元 + 岱崙 3C 考卷真題特訓：
// 1. 句子級 (Sentence-by-Sentence) 點擊朗讀庫 (含地道繁體中文翻譯)
// 2. 零打字點詞抓錯 (Mistake Buster) — 100% 精準單詞索引定位
// 3. 紙筆手寫對答案 / 語音作答測驗題庫 (聽寫、填空、選擇、改寫)
// 4. 核心單字與容器計量片語庫 (附音標、音節、例句與拼寫防呆提醒)
// 更新日期: 2026-10-20
// ============================================================================

window.MIDTERM_DATABASE = {json.dumps(units, ensure_ascii=False, indent=2)};
"""
    with open(TARGET_JS, "w", encoding="utf-8") as f:
        f.write(js_code)
    print(f"\nSaved to {TARGET_JS} successfully!")

if __name__ == "__main__":
    main()
