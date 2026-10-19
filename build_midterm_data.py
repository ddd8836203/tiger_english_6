# -*- coding: utf-8 -*-
"""
build_midterm_data.py
全面解析期中考 11 個單元的高保真內容，產出純靜態前端資料庫 midterm_data.js
特點：
1. 精簡單元名稱為小學生一眼看懂的 "Unit XX: 標題"
2. 課文分句精讀 (Sentence Shadowing) 採用純正課本課文，嚴格清洗任何註腳與括號雜質
3. 每一句英文均附帶地道繁體中文翻譯，支援前台一鍵展開
4. 零打字點詞抓錯 (Mistake Buster) 與紙筆/語音雙軌測驗 (Dual Quiz)
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

# 精準純淨課文與標準中文對照資料庫
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
                {"en": "One foggy morning, Sarah and her brother decided to hike up the hill.", "zh": "一個起霧的早晨，莎拉和她的哥哥決定徒步上山。"},
                {"en": "The thick fog covered the path, making it hard to see.", "zh": "濃霧籠罩著小徑，讓人很難看清。"},
                {"en": "They walked past a log bench on the left side of the trail.", "zh": "他們走過了步道左側的一張原木長凳。"},
                {"en": "Suddenly, they realized they could not find the crooked pine tree.", "zh": "突然間，他們意識到找不到那棵彎曲的松樹了。"},
                {"en": "Listen carefully! Do you hear the lighthouse horn?", "zh": "仔細聽！你聽見燈塔的號角聲了嗎？"},
                {"en": "The sound came from the south, guiding them toward the town.", "zh": "聲音從南方傳來，指引他們走向城鎮。"},
                {"en": "They climbed up a smaller hill above the fog line and saw the clear blue sky.", "zh": "他們爬上一座高於霧線的小山丘，看見了晴朗的藍天。"},
                {"en": "Soon, they safely reached their picnic spot with their family.", "zh": "不久，他們和家人安全抵達了野餐地點。"}
            ]
        }
    ],
    "RWW6_U06": [
        {
            "section_title": "定向越野的冒險世界 (The World of Orienteering)",
            "sentences": [
                {"en": "Orienteering is an exciting outdoor sport that began in Sweden.", "zh": "定向越野是一項起源於瑞典的令人興奮的戶外運動。"},
                {"en": "Racers use a topographical map and a magnetic compass to navigate through unfamiliar terrain.", "zh": "參賽者使用地形圖和磁指南針在陌生的地形中導航。"},
                {"en": "Along the course, there are checkpoints called controls.", "zh": "沿途設有被稱為「檢查點」的控制點。"},
                {"en": "Each control is marked with a distinctive red and white triangular flag.", "zh": "每個控制點都標有獨特的紅白三角旗。"},
                {"en": "Racers carry a punch card and mark it at every station to prove they visited it.", "zh": "參賽者攜帶打孔卡並在每個站點打卡，以證明他們曾經到訪。"},
                {"en": "The winner is not simply the fastest runner, but the one who accurately finds all the controls!", "zh": "獲勝者不僅僅是跑得最快的人，而是準確找到所有控制點的人！"}
            ]
        }
    ],
    "RWW6_U07": [
        {
            "section_title": "我們使用的語言世界 (Languages Around the Globe)",
            "sentences": [
                {"en": "There are about seven thousand languages spoken in the world today.", "zh": "今天世界上大約有七千種被使用的語言。"},
                {"en": "Chinese has the most native speakers of any language.", "zh": "中文是所有語言中擁有最多母語人口的語言。"},
                {"en": "English and Spanish are also spoken by hundreds of millions of people.", "zh": "英語和西班牙語也由數以億計的人使用。"},
                {"en": "In many countries, children grow up learning two or more languages.", "zh": "在許多國家，孩子們在成長過程中學習兩種或更多種語言。"},
                {"en": "People who can speak two languages fluently are called bilingual.", "zh": "能流利地說兩種語言的人被稱為雙語者。"},
                {"en": "Sign language uses hand movements and facial expressions to communicate without speaking.", "zh": "手語利用手部動作和麵部表情進行交流，無需開口說話。"},
                {"en": "Learning languages helps us understand different cultures and make friends around the world.", "zh": "學習語言能幫助我們理解不同文化並結交世界各地的朋友。"}
            ]
        }
    ],
    "RWW6_U08": [
        {
            "section_title": "夏日校園的雙語對話 (So Many Questions at Summer School)",
            "sentences": [
                {"en": "Rosa was carrying art supplies to her summer school classroom.", "zh": "羅莎正帶著美術用品前往她的夏令營教室。"},
                {"en": "She met a new boy named Erico in the hallway.", "zh": "她在走廊遇見了一位名叫埃里科的新男孩。"},
                {"en": "Erico had lived in Australia, Italy, and Brazil before moving here.", "zh": "埃里科在搬到這裡之前曾住在澳大利亞、義大利和巴西。"},
                {"en": "He spoke English with a British accent and could also speak Portuguese.", "zh": "他操著英國口音說英語，並且還會說葡萄牙語。"},
                {"en": "Rosa asked him many questions because she was curious about his journeys.", "zh": "羅莎問了他很多問題，因為她對他的旅程充滿好奇。"},
                {"en": "When you read a story, you can make predictions using clues and what you already know.", "zh": "當你閱讀故事時，你可以利用線索和已有知識來進行推測。"},
                {"en": "Erico smiled and predicted they would become great friends in art class.", "zh": "埃里科微笑著預測他們會在美術課上成為好朋友。"}
            ]
        }
    ]
}

def clean_sentence_token(token):
    # 徹底清除任何註腳符號、中括號、題目括號
    t = re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]', '', token)
    t = re.sub(r'\[[a-z]\.\s*([^\]]+)\]', r'\1', t)
    t = re.sub(r'\[([^\]]+)\]', r'\1', t)
    t = re.sub(r'[*_#>`]', '', t)
    return t.strip()

def find_wrong_token(err_s, fix_s):
    err_tokens = err_s.split()
    fix_tokens = fix_s.split()
    wrong_idx = -1
    wrong_w = ""
    correct_w = ""
    for idx, token in enumerate(err_tokens):
        c_err = re.sub(r'[.,!?;:"]', '', token)
        if idx < len(fix_tokens):
            c_fix = re.sub(r'[.,!?;:"]', '', fix_tokens[idx])
            if c_err.lower() != c_fix.lower():
                wrong_idx = idx
                wrong_w = token
                correct_w = fix_tokens[idx]
                break
    if wrong_idx == -1 and len(err_tokens) > 0:
        wrong_idx = 0
        wrong_w = err_tokens[0]
        correct_w = fix_tokens[0] if fix_tokens else ""
    return err_tokens, wrong_idx, wrong_w, correct_w

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

    # 2. 提取 AI_SPEC
    ai_spec = {}
    json_m = re.search(r'```json\s*(\{[\s\S]*?\})\s*```', raw_content)
    if json_m:
        try:
            ai_spec = json.loads(json_m.group(1))
        except:
            pass
    if not ai_spec:
        yaml_m = re.search(r'```yaml\s*([\s\S]*?)\s*```', raw_content)
        if yaml_m:
            try:
                ai_spec = yaml.safe_load(yaml_m.group(1)) or {}
                if "ai_spec" in ai_spec:
                    ai_spec = ai_spec["ai_spec"]
            except:
                pass

    # 3. 提取精選課文與中文翻譯 (Curated Passages)
    passages = CURATED_PASSAGES.get(meta["id"], [])

    # 4. 提取單字庫 (Vocab)
    vocab = []
    for key in ["vocabulary_lexicon", "scientific_lexicon", "vocabulary", "direction_and_spatial_lexicon", "navigational_vocabulary", "linguistic_lexicon"]:
        if key in ai_spec and isinstance(ai_spec[key], list):
            for v in ai_spec[key]:
                word = v.get("word") or v.get("term") or v.get("phrase")
                meaning = v.get("meaning_zh") or v.get("def_zh") or ""
                pos = v.get("pos", "phrase")
                ex = v.get("collocations") or v.get("collocation") or v.get("def_en") or v.get("context") or ""
                if word and not any(item["word"] == word for item in vocab):
                    vocab.append({"word": word, "pos": pos, "meaning": meaning, "example": ex})

    if meta["id"] == "ODG3_U13" and not vocab:
        u13_phrases = [
            {"word": "Me too.", "pos": "phrase", "meaning": "我也是 (日常口語肯定附和)", "example": "A: I like ice cream. B: Me too!"},
            {"word": "So do I.", "pos": "formula", "meaning": "我也是 (一般動詞肯定倒裝附和)", "example": "A: I play tennis. B: So do I."},
            {"word": "So did he / she.", "pos": "formula", "meaning": "他/她也是 (過去式一般動詞倒裝附和)", "example": "Bell invented a telephone. So did Gray."},
            {"word": "So was / were...", "pos": "formula", "meaning": "也是 (be動詞過去式肯定倒裝)", "example": "Bell's mother was deaf. So was his wife."},
            {"word": "Neither do I.", "pos": "formula", "meaning": "我也不 (現在式否定倒裝附和)", "example": "A: I don't like spiders. B: Neither do I."},
            {"word": "Neither did...", "pos": "formula", "meaning": "也不 (過去式否定倒裝附和)", "example": "Meucci didn't become rich. Neither did Reis."},
            {"word": "...didn't, either.", "pos": "formula", "meaning": "也不 (句尾逗號後否定附和)", "example": "They didn't have computers, either."}
        ]
        vocab.extend(u13_phrases)

    # 提取量詞/副詞表
    tables_2 = re.findall(r'\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|\n]+)\s*\|', raw_content)
    for col1, col2 in tables_2:
        c1, c2 = col1.strip(), col2.strip()
        if "---" in c1 or "容器" in c1 or "Adverb" in c1:
            continue
        if len(c1) > 1 and not any(v["word"] == c1 for v in vocab):
            vocab.append({"word": c1, "pos": "measure", "meaning": f"搭配: {c2}", "example": f"{c1} {c2.split('/')[0].strip()}"})

    tables_3 = re.findall(r'\|\s*\*\*([^*]+)\*\*\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*\*\*([^*]+)\*\*\s*\|', raw_content)
    for col1, col2, col3 in tables_3:
        c1, c2, c3 = col1.strip(), col2.strip(), col3.strip()
        if "---" in c1 or "Adverb" in c1:
            continue
        if len(c1) > 1 and not any(v["word"] == c1 for v in vocab):
            vocab.append({"word": c1, "pos": "adverb", "meaning": f"比較級: {c2} / 最高級: {c3}", "example": f"{c1} -> {c2} -> {c3}"})

    # 5. 提取改錯題 (Mistake Buster)
    mistake_buster = []
    traps = ai_spec.get("common_mistake_traps") or ai_spec.get("misconceptions_and_error_traps") or {}
    if isinstance(traps, dict):
        for trap_id, t in traps.items():
            err_s = t.get("error", "").replace('*', '').strip()
            fix_s = t.get("fix", "").replace('*', '').strip()
            reason = t.get("reason", "").strip()
            if err_s and fix_s:
                tokens, w_idx, w_word, c_word = find_wrong_token(err_s, fix_s)
                mistake_buster.append({
                    "trap_id": trap_id,
                    "sentence": err_s,
                    "tokens": tokens,
                    "wrong_index": w_idx,
                    "wrong_word": w_word,
                    "correct_word": c_word,
                    "fixed_sentence": fix_s,
                    "reason": reason
                })
    elif isinstance(traps, list):
        for t in traps:
            err_raw = t.get("error_pattern") or t.get("error", "")
            err_s = err_raw.replace('*', '').strip()
            fix_raw = t.get("correction") or t.get("fix", "")
            fix_s = fix_raw.replace('*', '').strip()
            reason = t.get("explanation") or t.get("reason", "")
            if "/" in err_s: err_s = err_s.split("/")[0].strip()
            if "/" in fix_s: fix_s = fix_s.split("/")[0].strip()
            if err_s and fix_s:
                tokens, w_idx, w_word, c_word = find_wrong_token(err_s, fix_s)
                mistake_buster.append({
                    "trap_id": t.get("trap_id", "TRAP"),
                    "sentence": err_s,
                    "tokens": tokens,
                    "wrong_index": w_idx,
                    "wrong_word": w_word,
                    "correct_word": c_word,
                    "fixed_sentence": fix_s,
                    "reason": reason
                })

    raw_corrections = re.findall(r'(\d+)\.\s*`([^`]+)`\s*\n\s*-\s*\*\*Correction\*\*:\s*`([^`]+)`(?:\s*\*(.*?)\*)?', raw_content)
    for num, wrong_s, fixed_s, reason in raw_corrections:
        tokens, w_idx, w_word, c_word = find_wrong_token(wrong_s, fixed_s)
        mistake_buster.append({
            "trap_id": f"PRACTICE_ERR_{num}",
            "sentence": wrong_s,
            "tokens": tokens,
            "wrong_index": w_idx,
            "wrong_word": w_word,
            "correct_word": c_word,
            "fixed_sentence": fixed_s,
            "reason": reason.strip() if reason else "請比對修正後的正確時態、詞性或介系詞"
        })

    # 6. 提取紙筆測驗題庫 (Quizzes)
    quizzes = []

    # A. 🔤 單字盲聽題型 (Spelling Listen)：自動將該單元所有核心單字轉為電腦發音聽寫題
    for v_idx, v in enumerate(vocab):
        w = v.get("word", "").strip()
        meaning = v.get("meaning") or v.get("translation") or "單元核心單字"
        note = v.get("note", "")
        example = v.get("example", "")
        phonetic = v.get("phonetic", "")
        if w:
            quizzes.append({
                "id": f"{meta['id']}_LIST_{v_idx+1}",
                "type": "spelling_listen",
                "category_tag": "listening",
                "question": "請聽電腦發音，在紙上拼寫出這個核心單字：",
                "hint": f"中文釋義：{meaning}",
                "audio_word": w,
                "phonetic": phonetic,
                "syllables": w,
                "answer": w,
                "explanation": {
                    "concept": f"{meta['display_title']} 核心字彙：{w}",
                    "formula": f"詞性與例句搭配：{example if example else meaning}",
                    "trap": f"注意拼寫盲點：{note if note else '切記母音與子音字母對應，勿漏寫尾音或不發音字母。'}"
                }
            })

    # B. 二選一括號選擇 (轉為克漏填空題)
    circle_qs = re.findall(r'(\d+)\.\s+([^\[\]\n]+?)\s*(?:\[([^\[\]\n]+)\]\s*/\s*([^\n\s]+)|([^\n\s]+)\s*/\s*\[([^\[\]\n]+)\])', raw_content)
    for q_num, stem, opt_correct_1, opt_wrong_1, opt_wrong_2, opt_correct_2 in circle_qs:
        ans = opt_correct_1 or opt_correct_2
        stem_clean = stem.strip()
        quizzes.append({
            "id": f"{meta['id']}_FILL_{len(quizzes)+1}",
            "type": "fill",
            "category_tag": "fill",
            "question": f"{stem_clean} ( ______ )",
            "answer": ans,
            "hint": "二選一紙筆填答，在紙上寫出正確單字",
            "explanation": {
                "concept": f"{meta['display_title']} 語法搭配與詞性辨析",
                "formula": f"破題關鍵：正確搭配為『{stem_clean} {ans}』。",
                "trap": "干擾項排除：其餘選項在詞性或語法時態上不符前後語境。"
            }
        })

    # C. 三選一選擇題 (文法選擇)
    mc_blocks = re.findall(r'(\d+)\.\s+([^\n]+?)\s*\n\s+-\s*a\)\s*([^\n]+?)\s*\n\s+-\s*b\)\s*([^\n]+?)\s*\n\s+-\s*c\)\s*([^\n]+?)(?:\s*\*\(正解[：:]\s*([abc])\*\))?', raw_content)
    for q_num, stem, opt_a, opt_b, opt_c, correct_key in mc_blocks:
        opts = [opt_a.replace('*', '').strip(), opt_b.replace('*', '').strip(), opt_c.replace('*', '').strip()]
        ans = ""
        if "**" in opt_a or correct_key == 'a': ans = opts[0]
        elif "**" in opt_b or correct_key == 'b': ans = opts[1]
        elif "**" in opt_c or correct_key == 'c': ans = opts[2]
        else: ans = opts[0]
        quizzes.append({
            "id": f"{meta['id']}_MC_{len(quizzes)+1}",
            "type": "choice",
            "category_tag": "choice",
            "question": stem.strip(),
            "options": opts,
            "answer": ans,
            "hint": "三選一紙筆填答",
            "explanation": {
                "concept": f"{meta['display_title']} 文法選擇考點",
                "formula": f"破題關鍵：題幹線索指定正確答案為『{ans}』。",
                "trap": "誘答陷阱：其餘選項在主詞單複數、時態或介系詞上有語法漏洞。"
            }
        })

    # D. 可數不可數判斷 (選擇題)
    cn_matches = re.findall(r'(\d+)\.\s+([A-Za-z\s]+?)\s*➔\s*\*\*\[([^\]]+)\]\*\*(?:\s*\*\(?([^)\n]*)\)?\*)?', raw_content)
    for q_num, item, ans, note in cn_matches:
        quizzes.append({
            "id": f"{meta['id']}_CN_{len(quizzes)+1}",
            "type": "choice",
            "category_tag": "choice",
            "question": f"判斷可數 (C: Count) 或不可數 (N: Noncount)：【 {item.strip()} 】",
            "options": ["C (可數名詞)", "N (不可數名詞)"],
            "answer": ans.strip(),
            "hint": f"中文意思：{note.strip()}" if note else "在紙上寫 C 或是 N",
            "explanation": {
                "concept": f"名詞分類：可數 (C) vs 不可數 (N)",
                "formula": f"名詞『{item.strip()}』特性：{ans.strip()}。不可數名詞計量需搭配容器（如 a slice of, a cup of）。",
                "trap": "注意固體、液體與抽象概念通常為不可數名詞，不可加 -s 或直接接 a/an。"
            }
        })

    # E. How much / How many 填空
    how_matches = re.findall(r'(\d+)\.\s+\*\*\[(How much|How many)\]\*\*\s+([^\n?]+\?)', raw_content)
    for q_num, ans, stem in how_matches:
        quizzes.append({
            "id": f"{meta['id']}_HOW_{len(quizzes)+1}",
            "type": "fill",
            "category_tag": "fill",
            "question": f"_______ {stem.strip()} (填入 How much 或 How many)",
            "answer": ans.strip(),
            "hint": "注意受詞是可數名詞複數還是不可數名詞",
            "explanation": {
                "concept": "疑問詞片語：How much vs How many",
                "formula": f"『How many + 可數複數名詞』；『How much + 不可數名詞』。本題受詞判定正解為『{ans.strip()}』。",
                "trap": "切勿僅看有沒有加 s，需注意不規則複數或不可數名詞。"
            }
        })

    # F. 改寫與造句題 (句子改寫)
    rewrite_qs = re.findall(r'(\d+)\.\s*([^\n➔]+?)\s*➔\s*(?:\`([^\`]+)\`|\*\*([^*]+)\*\*)', raw_content)
    for q_num, prompt, ans1, ans2 in rewrite_qs:
        ans = (ans1 or ans2).strip()
        p_clean = prompt.strip().replace('*', '')
        if "範例" in ans or "[N]" in ans or "[C]" in ans or "true" in ans.lower() or "false" in ans.lower():
            continue
        quizzes.append({
            "id": f"{meta['id']}_RW_{len(quizzes)+1}",
            "type": "paper_rewrite",
            "category_tag": "rewrite",
            "question": f"題目提示：{p_clean}",
            "answer": ans,
            "hint": "在紙上寫出完整句子後按「翻牌核對答案」",
            "explanation": {
                "concept": f"{meta['display_title']} 核心句型結構改寫",
                "formula": f"標準句型：{ans}",
                "trap": "小學生常犯錯誤：切記首字母大寫、標點符號與主詞動詞時態一致性。"
            }
        })

    # G. 是非題 (True / False，歸類為選擇題型)
    tf_matches = re.findall(r'(\d+)\.\s+([^\n➔]+?)➔\s*\*\*(true|false|T|F|C)\*\*(?:\s*\*(.*?)\*)?', raw_content, re.IGNORECASE)
    for q_num, question, ans, exp in tf_matches:
        ans_clean = ans.upper()
        if ans_clean in ['T', 'TRUE']: ans_text = "True (正確)"
        elif ans_clean in ['F', 'FALSE']: ans_text = "False (錯誤)"
        else: ans_text = ans_clean
        quizzes.append({
            "id": f"{meta['id']}_TF_{len(quizzes)+1}",
            "type": "choice",
            "category_tag": "choice",
            "question": question.strip(),
            "options": ["True (正確)", "False (錯誤)"],
            "answer": ans_text,
            "explanation": {
                "concept": f"{meta['display_title']} 課文事實與文法判斷",
                "formula": f"正解分析：{exp.strip() if exp else '根據課文事實與語法規則判定。'}",
                "trap": "審題注意細節數字、專有名詞與時態限定詞。"
            },
            "hint": "判斷 True 還是 False"
        })

    # H. 閱讀理解簡答題 (歸類為填空題型)
    qa_matches = re.findall(r'(\d+)\.\s*\*\*([^\n*?]+?\?)\*\*\s*\n\s*-\s*\*Answer\*:\s*`([^`]+)`', raw_content)
    for q_num, q_text, ans in qa_matches:
        quizzes.append({
            "id": f"{meta['id']}_QA_{len(quizzes)+1}",
            "type": "fill",
            "category_tag": "fill",
            "question": q_text.strip(),
            "answer": ans.strip(),
            "hint": "在紙上寫下答案關鍵字或完整句子",
            "explanation": {
                "concept": f"{meta['display_title']} 閱讀理解與細節檢索",
                "formula": f"課文原句定位正解：{ans.strip()}",
                "trap": "注意問句疑問詞（What, Why, Where, How）對應之作答時態與主詞人稱。"
            }
        })

    return {
        "id": meta["id"],
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
    print("Parsing all 11 midterm units with clean titles and curated passages...")
    units = []
    for m in FILES:
        u = parse_markdown(m)
        if u:
            units.append(u)
            sent_total = sum(len(p["sentences"]) for p in u["passages"])
            print(f"[{u['category']}] {u['display_title']}: {len(u['passages'])} 篇課文 ({sent_total} 句), {len(u['vocab'])} 單字/片語, {len(u['mistake_buster'])} 改錯題, {len(u['quizzes'])} 題測驗")

    # 注入岱崙美語 3C Quiz 歷史考券專屬特訓單元
    try:
        from exam_review_data import EXAM_REVIEW_UNIT
        units.append(EXAM_REVIEW_UNIT)
        sent_total = sum(len(p["sentences"]) for p in EXAM_REVIEW_UNIT["passages"])
        print(f"[{EXAM_REVIEW_UNIT['category']}] {EXAM_REVIEW_UNIT['display_title']}: {len(EXAM_REVIEW_UNIT['passages'])} 篇課文 ({sent_total} 句), {len(EXAM_REVIEW_UNIT['vocab'])} 單字/片語, {len(EXAM_REVIEW_UNIT['mistake_buster'])} 改錯題, {len(EXAM_REVIEW_UNIT['quizzes'])} 題測驗")
    except Exception as e:
        print(f"Error injecting EXAM_REVIEW_UNIT: {e}")

    js_code = f"""// ============================================================================
// 六年級上學期英語期中考特訓資料庫 (midterm_data.js)
// 包含 4 套教材、11 個單元完整結構：
// 1. 句子級 (Sentence-by-Sentence) 點擊朗讀庫 (含地道繁體中文翻譯)
// 2. 零打字點詞抓錯 (Mistake Buster)
// 3. 紙筆手寫對答案 / 語音作答測驗題庫
// 4. 核心單字與容器計量片語庫
// 更新日期: 2026-10-19
// ============================================================================

window.MIDTERM_DATABASE = {json.dumps(units, ensure_ascii=False, indent=2)};
"""
    with open(TARGET_JS, "w", encoding="utf-8") as f:
        f.write(js_code)
    print(f"\nSaved to {TARGET_JS} successfully!")

if __name__ == "__main__":
    main()
