/**
 * 六年級英語特訓系統 — 核心前端控制器 (app.js)
 * 職責：全域狀態機、視圖路由、Web Speech TTS 雙速語音、雙軌測驗、A4 列印引擎、錯題本與 AI 匯出
 */

(function () {
  'use strict';

  // ==========================================================================
  // 1. 全域狀態機 (AppState)
  // ==========================================================================
  const AppState = {
    currentView: 'midterm',        // 預設期中考衝刺專區 ('midterm' | 'study' | 'quiz' | 'braingym' | 'errorbook' | 'print')
    midtermSubtab: 'shadowing',    // 'shadowing' | 'mistake' | 'quiz' | 'exam'
    selectedMidtermUnitId: 'ODG3_U13',
    midtermAutoAdvance: false,
    activeSentenceIdx: null,
    selectedTokenIdx: null,
    currentMistakeIdx: 0,
    currentMidtermQuizIdx: 0,
    midtermQuizFilter: 'all',      // 'all' | 'listening' | 'fill' | 'choice' | 'rewrite'
    midtermDualMode: 'paper',      // 'paper' | 'voice'
    studySubtab: 'vocab',          // 'vocab' | 'reading' | 'grammar'
    selectedBookId: 'od3',         // 預設 Oxford Discover 3
    selectedUnitId: 'od3_1',       // 預設 Unit 1
    ttsSpeed: 1.0,                 // 1.0x 或 0.8x
    quizMode: 'paper',             // 'paper' (紙筆對答) | 'interactive' (iPad 點選)
    quizQuestions: [],             // 當前測驗題庫
    quizIndex: 0,                  // 當前題號 (0-indexed)
    quizResults: {},               // { [qId]: { status: 'correct'|'hesitant'|'wrong', selectedOption, timestamp } }
    brainGymQuestions: [],         // 晨間體操題目
    brainGymIndex: 0,
    errors: []                     // 終身錯題本清單
  };

  // LocalStorage 鍵名
  const STORAGE_KEY_ERRORS = 'tiger_english_errors_v1';
  const STORAGE_KEY_SETTINGS = 'tiger_english_settings_v1';

  // ==========================================================================
  // 2. 初始化與事件綁定
  // ==========================================================================
  document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    loadErrorBook();
    initSelectors();
    initNavigation();
    initSpeechSynthesis();
    initMidtermSprint();
    initStudyRoom();
    initQuizArena();
    initBrainGym();
    initErrorBook();
    initPrintEngine();
    initAiModal();

    // 初始渲染期中考專區與課本單元
    renderMidtermSprint();
    renderCurrentUnit();
  });

  // ==========================================================================
  // 3. 本地儲存與設定載入
  // ==========================================================================
  function loadSettings() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY_SETTINGS);
      if (saved) {
        const parsed = jsonParseSafe(saved);
        if (parsed.ttsSpeed) AppState.ttsSpeed = parsed.ttsSpeed;
        if (parsed.bookId) AppState.selectedBookId = parsed.bookId;
        if (parsed.unitId) AppState.selectedUnitId = parsed.unitId;
      }
    } catch (e) {
      console.warn('載入設定失敗:', e);
    }
    updateTtsSpeedButtonUI();
  }

  function saveSettings() {
    try {
      localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify({
        ttsSpeed: AppState.ttsSpeed,
        bookId: AppState.selectedBookId,
        unitId: AppState.selectedUnitId
      }));
    } catch (e) {
      console.warn('儲存設定失敗:', e);
    }
  }

  function loadErrorBook() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY_ERRORS);
      if (saved) {
        AppState.errors = jsonParseSafe(saved) || [];
      }
    } catch (e) {
      console.warn('載入錯題本失敗:', e);
      AppState.errors = [];
    }
    updateErrorCountBadge();
  }

  function saveErrorBook() {
    try {
      localStorage.setItem(STORAGE_KEY_ERRORS, JSON.stringify(AppState.errors));
    } catch (e) {
      console.warn('儲存錯題本失敗:', e);
    }
    updateErrorCountBadge();
  }

  function updateErrorCountBadge() {
    const badge = document.getElementById('errorCountBadge');
    if (badge) {
      badge.textContent = AppState.errors.length;
      badge.style.display = AppState.errors.length > 0 ? 'inline-block' : 'none';
    }
  }

  // ==========================================================================
  // 4. 下拉選單與視圖導覽
  // ==========================================================================
  function initSelectors() {
    const bookSelect = document.getElementById('bookSelect');
    const unitSelect = document.getElementById('unitSelect');
    if (!bookSelect || !unitSelect || !window.ENGLISH_DATA) return;

    // 填充課本選單
    bookSelect.innerHTML = '';
    ENGLISH_DATA.books.forEach(b => {
      const opt = document.createElement('option');
      opt.value = b.book_id;
      opt.textContent = b.book_name;
      if (b.book_id === AppState.selectedBookId) opt.selected = true;
      bookSelect.appendChild(opt);
    });

    // 課本切換事件
    bookSelect.addEventListener('change', (e) => {
      AppState.selectedBookId = e.target.value;
      populateUnitsForSelectedBook();
      saveSettings();
      renderCurrentUnit();
    });

    // 填充並切換單元
    populateUnitsForSelectedBook();

    unitSelect.addEventListener('change', (e) => {
      AppState.selectedUnitId = e.target.value;
      saveSettings();
      renderCurrentUnit();
    });
  }

  function populateUnitsForSelectedBook() {
    const unitSelect = document.getElementById('unitSelect');
    if (!unitSelect || !window.ENGLISH_DATA) return;

    unitSelect.innerHTML = '';
    const bookUnits = ENGLISH_DATA.units.filter(u => u.book_id === AppState.selectedBookId);

    if (bookUnits.length === 0) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = '無可用單元';
      unitSelect.appendChild(opt);
      AppState.selectedUnitId = '';
      return;
    }

    // 確保選中存在的單元
    let matchFound = false;
    bookUnits.forEach(u => {
      const opt = document.createElement('option');
      opt.value = u.unit_id;
      opt.textContent = u.unit_title || u.unit_id;
      if (u.unit_id === AppState.selectedUnitId) {
        opt.selected = true;
        matchFound = true;
      }
      unitSelect.appendChild(opt);
    });

    if (!matchFound) {
      AppState.selectedUnitId = bookUnits[0].unit_id;
      unitSelect.value = AppState.selectedUnitId;
    }
  }

  function initNavigation() {
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const viewId = tab.dataset.view;
        switchView(viewId);
      });
    });
  }

  function switchView(viewId) {
    AppState.currentView = viewId;

    // 更新導覽 Tab 高亮
    document.querySelectorAll('.nav-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.view === viewId);
    });

    // 切換面板
    document.querySelectorAll('.view-panel').forEach(p => {
      p.classList.toggle('active', p.id === `view-${viewId}`);
    });

    // 特殊視圖切換動作
    if (viewId === 'midterm') {
      renderMidtermSprint();
    } else if (viewId === 'quiz') {
      loadQuizForCurrentUnit();
    } else if (viewId === 'braingym') {
      loadBrainGym();
    } else if (viewId === 'errorbook') {
      renderErrorBook();
    } else if (viewId === 'print') {
      renderA4PrintPreview();
    }
  }

  // ==========================================================================
  // 5. 原生 Web Speech API 雙速發音引擎 (TTS)
  // ==========================================================================
  let bestEnVoice = null;

  function initSpeechSynthesis() {
    if (!('speechSynthesis' in window)) {
      console.warn('此瀏覽器不支援 Web Speech API');
      return;
    }

    function pickVoice() {
      const voices = window.speechSynthesis.getVoices();
      // 優先挑選自然美式/英式語音
      bestEnVoice = voices.find(v => (v.name.includes('Natural') || v.name.includes('Online')) && v.lang.startsWith('en'))
        || voices.find(v => v.lang === 'en-US')
        || voices.find(v => v.lang.startsWith('en'))
        || null;
    }

    pickVoice();
    if (speechSynthesis.onvoiceschanged !== undefined) {
      speechSynthesis.onvoiceschanged = pickVoice;
    }

    // 語速切換按鈕事件
    const ttsBtn = document.getElementById('ttsSpeedBtn');
    if (ttsBtn) {
      ttsBtn.addEventListener('click', () => {
        AppState.ttsSpeed = AppState.ttsSpeed === 1.0 ? 0.8 : 1.0;
        updateTtsSpeedButtonUI();
        saveSettings();
        speakWord(AppState.ttsSpeed === 0.8 ? 'Slow speed' : 'Normal speed');
      });
    }
  }

  function updateTtsSpeedButtonUI() {
    const label = document.getElementById('ttsSpeedLabel');
    if (label) {
      label.textContent = `${AppState.ttsSpeed.toFixed(1)}x`;
    }
  }

  function speakWord(text, onEndCallback) {
    if (!('speechSynthesis' in window) || !text) return;
    window.speechSynthesis.cancel(); // 防抖，中斷前一個發音

    const cleanText = text.replace(/[*_#`]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = AppState.ttsSpeed;
    utterance.pitch = 1.0;
    if (bestEnVoice) utterance.voice = bestEnVoice;
    utterance.lang = 'en-US';

    if (onEndCallback) {
      utterance.onend = onEndCallback;
    }

    window.speechSynthesis.speak(utterance);
  }

  // ==========================================================================
  // 6. 學習專區模組 (Study Room)
  // ==========================================================================
  function initStudyRoom() {
    const subtabs = document.querySelectorAll('.subtab-btn');
    subtabs.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.dataset.subtab;
        AppState.studySubtab = target;
        subtabs.forEach(b => b.classList.toggle('active', b.dataset.subtab === target));
        document.querySelectorAll('.subtab-content').forEach(c => {
          c.classList.toggle('active', c.id === `subtab-${target}-panel`);
        });
      });
    });

    // 單字搜尋
    const searchInput = document.getElementById('vocabSearchInput');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        filterVocabCards(query);
      });
    }

    // 連續朗讀單字
    const playAllBtn = document.getElementById('playAllVocabBtn');
    if (playAllBtn) {
      playAllBtn.addEventListener('click', playAllVocabSequentially);
    }

    // 展開/收合所有錨點
    const toggleBreakdownBtn = document.getElementById('toggleAllBreakdownBtn');
    if (toggleBreakdownBtn) {
      toggleBreakdownBtn.addEventListener('click', () => {
        const drawers = document.querySelectorAll('.anchor-section');
        const anyClosed = Array.from(drawers).some(d => d.style.display === 'none');
        drawers.forEach(d => d.style.display = anyClosed ? 'flex' : 'none');
        toggleBreakdownBtn.querySelector('span').textContent = anyClosed ? '📦 收合記憶錨點' : '💡 展開所有字根/記憶錨點';
      });
    }

    // 朗讀整篇課文
    const playReadingBtn = document.getElementById('playEntireReadingBtn');
    if (playReadingBtn) {
      playReadingBtn.addEventListener('click', playEntireReading);
    }

    // 切換課文中英對照
    const toggleChinese = document.getElementById('toggleChineseTranslation');
    if (toggleChinese) {
      toggleChinese.addEventListener('change', (e) => {
        document.querySelectorAll('.reading-chi').forEach(el => {
          el.style.display = e.target.checked ? 'block' : 'none';
        });
      });
    }
  }

  function renderCurrentUnit() {
    if (!window.ENGLISH_DATA) return;

    const book = ENGLISH_DATA.books.find(b => b.book_id === AppState.selectedBookId);
    const unit = ENGLISH_DATA.units.find(u => u.book_id === AppState.selectedBookId && u.unit_id === AppState.selectedUnitId);

    // 頂部橫幅更新
    const bannerBook = document.getElementById('studyBookName');
    const bannerTitle = document.getElementById('studyUnitTitle');
    const bannerBq = document.getElementById('studyBigQuestion');

    if (bannerBook) bannerBook.textContent = book ? book.book_name : AppState.selectedBookId;
    if (bannerTitle) bannerTitle.textContent = unit ? (unit.unit_title || unit.unit_id) : '單元學習';
    if (bannerBq) {
      if (unit && unit.big_question) {
        bannerBq.textContent = unit.big_question;
        bannerBq.style.display = 'block';
      } else {
        bannerBq.style.display = 'none';
      }
    }

    renderVocabSection();
    renderReadingSection();
    renderGrammarSection();
  }

  function renderVocabSection() {
    const grid = document.getElementById('vocabCardsGrid');
    const countTag = document.getElementById('vocabCountTag');
    if (!grid || !window.ENGLISH_DATA) return;

    grid.innerHTML = '';
    const vocabs = ENGLISH_DATA.vocabulary.filter(v => v.book_id === AppState.selectedBookId && v.unit_id === AppState.selectedUnitId);
    if (countTag) countTag.textContent = vocabs.length;

    if (vocabs.length === 0) {
      grid.innerHTML = '<div class="no-data-msg">本單元尚無收錄獨立單字卡，請切換至「課文閱聽」或「雙軌測驗」。</div>';
      return;
    }

    vocabs.forEach(item => {
      const card = document.createElement('div');
      card.className = 'vocab-card';
      card.dataset.word = (item.word || '').toLowerCase();
      card.dataset.chi = (item.chi || '').toLowerCase();

      card.innerHTML = `
        <div class="card-top-row">
          <div class="card-word-title">
            <span>${escapeHtml(item.word)}</span>
            ${item.pos ? `<span class="card-pos-tag">${escapeHtml(item.pos)}</span>` : ''}
          </div>
          <button class="btn-pronounce" title="發音" data-word="${escapeHtml(item.word)}">
            <span>🔊</span>
          </button>
        </div>
        <div class="card-meaning">${escapeHtml(item.chi)}</div>
        
        <div class="anchor-section">
          ${item.breakdown ? `<div class="anchor-item"><span class="anchor-badge badge-break">字根拆解</span><span class="anchor-text">${escapeHtml(item.breakdown)}</span></div>` : ''}
          ${item.trick ? `<div class="anchor-item"><span class="anchor-badge badge-trick">諧音聯想</span><span class="anchor-text">${escapeHtml(item.trick)}</span></div>` : ''}
          ${item.scene ? `<div class="anchor-item"><span class="anchor-badge badge-scene">情境畫面</span><span class="anchor-text">${escapeHtml(item.scene)}</span></div>` : ''}
          ${item.collocation ? `<div class="anchor-item"><span class="anchor-badge badge-colloc">搭配用法</span><span class="anchor-text">${escapeHtml(item.collocation)}</span></div>` : ''}
          ${item.chant ? `<div class="anchor-item"><span class="anchor-badge badge-chant">記憶口訣</span><span class="anchor-text">${escapeHtml(item.chant)}</span></div>` : ''}
          ${item.compare ? `<div class="anchor-item"><span class="anchor-badge badge-compare">易混比較</span><span class="anchor-text">${escapeHtml(item.compare)}</span></div>` : ''}
        </div>

        ${item.context_eng ? `
          <div class="card-example">
            <div class="example-eng">${escapeHtml(item.context_eng)}</div>
            ${item.context_chi ? `<div class="example-chi">${escapeHtml(item.context_chi)}</div>` : ''}
          </div>
        ` : ''}
      `;

      // 點擊發音按鈕
      card.querySelector('.btn-pronounce').addEventListener('click', (e) => {
        e.stopPropagation();
        speakWord(item.word);
      });

      // 點擊整張卡片發音
      card.addEventListener('click', () => {
        speakWord(item.word);
      });

      grid.appendChild(card);
    });
  }

  function filterVocabCards(query) {
    const cards = document.querySelectorAll('.vocab-card');
    cards.forEach(c => {
      const w = c.dataset.word || '';
      const chi = c.dataset.chi || '';
      const match = !query || w.includes(query) || chi.includes(query);
      c.style.display = match ? 'flex' : 'none';
    });
  }

  function playAllVocabSequentially() {
    const vocabs = ENGLISH_DATA.vocabulary.filter(v => v.book_id === AppState.selectedBookId && v.unit_id === AppState.selectedUnitId);
    if (vocabs.length === 0) return;

    let idx = 0;
    function speakNext() {
      if (idx >= vocabs.length) return;
      const v = vocabs[idx];
      // 高亮卡片
      document.querySelectorAll('.vocab-card').forEach((c, i) => {
        c.style.borderColor = (i === idx) ? 'var(--accent-primary)' : 'var(--border-light)';
      });
      speakWord(v.word, () => {
        idx++;
        setTimeout(speakNext, 600);
      });
    }
    speakNext();
  }

  function renderReadingSection() {
    const list = document.getElementById('readingPassagesList');
    const countTag = document.getElementById('readingCountTag');
    if (!list || !window.ENGLISH_DATA) return;

    list.innerHTML = '';
    const passages = ENGLISH_DATA.reading_content.filter(r => r.book_id === AppState.selectedBookId && r.unit_id === AppState.selectedUnitId);
    if (countTag) countTag.textContent = passages.length;

    if (passages.length === 0) {
      list.innerHTML = '<div class="no-data-msg">本單元尚無課文段落資料。</div>';
      return;
    }

    passages.forEach((p, idx) => {
      const card = document.createElement('div');
      card.className = 'reading-card';
      card.innerHTML = `
        <div class="reading-card-top">
          <span class="reading-seq">Paragraph ${p.sequence || (idx + 1)}</span>
          <button class="btn-pronounce" title="朗讀此段落">
            <span>🔊</span>
          </button>
        </div>
        <div class="reading-eng">${escapeHtml(p.eng)}</div>
        ${p.chi ? `<div class="reading-chi">${escapeHtml(p.chi)}</div>` : ''}
      `;

      card.querySelector('.btn-pronounce').addEventListener('click', () => {
        speakWord(p.eng);
      });

      list.appendChild(card);
    });
  }

  function playEntireReading() {
    const passages = ENGLISH_DATA.reading_content.filter(r => r.book_id === AppState.selectedBookId && r.unit_id === AppState.selectedUnitId);
    if (passages.length === 0) return;

    const fullText = passages.map(p => p.eng).join(' ');
    speakWord(fullText);
  }

  function renderGrammarSection() {
    const list = document.getElementById('grammarRulesList');
    const countTag = document.getElementById('grammarCountTag');
    if (!list || !window.ENGLISH_DATA) return;

    list.innerHTML = '';
    const rules = ENGLISH_DATA.grammar.filter(g => g.book_id === AppState.selectedBookId && g.unit_id === AppState.selectedUnitId);
    if (countTag) countTag.textContent = rules.length;

    if (rules.length === 0) {
      list.innerHTML = '<div class="no-data-msg">本單元尚無專屬文法規則卡。</div>';
      return;
    }

    rules.forEach(rule => {
      const card = document.createElement('div');
      card.className = 'grammar-card';
      
      let examplesHtml = '';
      if (rule.examples && rule.examples.length > 0) {
        examplesHtml = `
          <div class="grammar-examples-box">
            ${rule.examples.map(ex => `<div class="grammar-example-item">${escapeHtml(ex)}</div>`).join('')}
          </div>
        `;
      }

      card.innerHTML = `
        <div class="grammar-title">
          <span>🔍</span>
          <span>${escapeHtml(rule.rule_title)}</span>
        </div>
        ${rule.eng_exp ? `<div class="grammar-exp-eng">${escapeHtml(rule.eng_exp)}</div>` : ''}
        ${rule.chi_exp ? `<div class="grammar-exp-chi">${escapeHtml(rule.chi_exp)}</div>` : ''}
        ${examplesHtml}
      `;

      list.appendChild(card);
    });
  }

  // ==========================================================================
  // 7. 雙軌測驗系統 (Quiz Arena)
  // ==========================================================================
  function initQuizArena() {
    // 測驗模式切換 (紙筆對答軌 vs iPad 互動軌)
    const modeRadios = document.querySelectorAll('input[name="quizModeRadio"]');
    modeRadios.forEach(radio => {
      radio.addEventListener('change', (e) => {
        AppState.quizMode = e.target.value;
        document.querySelectorAll('.mode-btn').forEach(b => {
          b.classList.toggle('active', b.dataset.mode === AppState.quizMode);
        });
        updateQuizCardModeUI();
      });
    });

    // 紙筆軌：看答案與詳解
    const showAnswerBtn = document.getElementById('showAnswerBtn');
    if (showAnswerBtn) {
      showAnswerBtn.addEventListener('click', () => {
        const expBox = document.getElementById('explanationBox');
        if (expBox) expBox.classList.add('active');
      });
    }

    // 紙筆軌三態評估按鈕 (👍 / ⏳ / ❌)
    document.querySelectorAll('.btn-check').forEach(btn => {
      btn.addEventListener('click', () => {
        const resultType = btn.dataset.ans;
        handlePaperAnswerCheck(resultType);
      });
    });

    // 導航：上一題 / 下一題
    const prevBtn = document.getElementById('prevQuestionBtn');
    const nextBtn = document.getElementById('nextQuestionBtn');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (AppState.quizIndex > 0) {
          AppState.quizIndex--;
          renderQuizCard();
        }
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (AppState.quizIndex < AppState.quizQuestions.length - 1) {
          AppState.quizIndex++;
          renderQuizCard();
        }
      });
    }
  }

  function loadQuizForCurrentUnit() {
    if (!window.ENGLISH_DATA) return;
    const questions = ENGLISH_DATA.quizzes.filter(q => q.book_id === AppState.selectedBookId && q.unit_id === AppState.selectedUnitId && q.type !== 'brain_gym');
    
    AppState.quizQuestions = questions;
    AppState.quizIndex = 0;
    AppState.quizResults = {};

    renderQuizCard();
    renderQuizDotsNav();
  }

  function renderQuizCard() {
    const card = document.getElementById('quizCard');
    const progressText = document.getElementById('quizProgressText');
    const qTypeBadge = document.getElementById('quizTypeBadge');
    const expBox = document.getElementById('explanationBox');
    if (!card) return;

    if (expBox) expBox.classList.remove('active');

    if (AppState.quizQuestions.length === 0) {
      card.innerHTML = '<div class="no-data-msg" style="padding: 2rem;">本單元目前暫無測驗題目，請切換至其他單元或開啟「晨間體操」。</div>';
      if (progressText) progressText.textContent = '0 / 0 題';
      return;
    }

    const q = AppState.quizQuestions[AppState.quizIndex];
    if (progressText) progressText.textContent = `第 ${AppState.quizIndex + 1} / ${AppState.quizQuestions.length} 題`;
    if (qTypeBadge) qTypeBadge.textContent = `${q.type.toUpperCase()} QUIZ`;

    const qDifficulty = document.getElementById('qDifficulty');
    const qStem = document.getElementById('qStem');
    if (qDifficulty) qDifficulty.textContent = q.difficulty || '★★★☆☆';
    if (qStem) qStem.textContent = q.question;

    // 渲染 iPad 互動選項
    const optionsContainer = document.getElementById('interactiveOptions');
    if (optionsContainer) {
      optionsContainer.innerHTML = '';
      if (q.options && q.options.length > 0) {
        q.options.forEach(opt => {
          const btn = document.createElement('button');
          btn.className = 'option-btn';
          btn.textContent = opt;
          btn.addEventListener('click', () => handleInteractiveOptionClick(opt, q, btn));
          optionsContainer.appendChild(btn);
        });
      }
    }

    // 渲染詳解內容
    const expCorrectAns = document.getElementById('expCorrectAns');
    const expContent = document.getElementById('expContent');
    if (expCorrectAns) expCorrectAns.textContent = `正解：${q.answer}`;
    if (expContent) expContent.textContent = q.explanation || '暫無詳解說明。';

    updateQuizCardModeUI();
    updateCheckButtonsHighlight();
    updateQuizDotsActive();
  }

  function updateQuizCardModeUI() {
    const paperActions = document.getElementById('paperActions');
    const interactiveOptions = document.getElementById('interactiveOptions');
    const isPaper = AppState.quizMode === 'paper';

    if (paperActions) paperActions.style.display = isPaper ? 'flex' : 'none';
    if (interactiveOptions) interactiveOptions.style.display = isPaper ? 'none' : 'flex';
  }

  function handlePaperAnswerCheck(status) {
    const q = AppState.quizQuestions[AppState.quizIndex];
    if (!q) return;

    AppState.quizResults[q.id] = {
      status: status,
      timestamp: Date.now()
    };

    // 自動展開詳解
    const expBox = document.getElementById('explanationBox');
    if (expBox) expBox.classList.add('active');

    // 若答錯或猶豫，歸檔至錯題本
    if (status === 'wrong' || status === 'hesitant') {
      logErrorQuestion(q, status);
    } else if (status === 'correct') {
      removeErrorQuestion(q.id);
    }

    updateCheckButtonsHighlight();
    renderQuizDotsNav();
  }

  function handleInteractiveOptionClick(selectedOpt, question, btnElement) {
    const isCorrect = (selectedOpt.trim().toLowerCase() === question.answer.trim().toLowerCase());
    
    // 選項視覺反饋
    document.querySelectorAll('.option-btn').forEach(btn => {
      btn.classList.remove('selected-correct', 'selected-wrong');
      if (btn.textContent.trim().toLowerCase() === question.answer.trim().toLowerCase()) {
        btn.classList.add('selected-correct');
      }
    });

    if (!isCorrect) {
      btnElement.classList.add('selected-wrong');
    }

    // 展開詳解
    const expBox = document.getElementById('explanationBox');
    if (expBox) expBox.classList.add('active');

    // 記錄結果
    const status = isCorrect ? 'correct' : 'wrong';
    AppState.quizResults[question.id] = {
      status: status,
      selectedOption: selectedOpt,
      timestamp: Date.now()
    };

    if (isCorrect) {
      removeErrorQuestion(question.id);
    } else {
      logErrorQuestion(question, 'wrong');
    }

    renderQuizDotsNav();
  }

  function updateCheckButtonsHighlight() {
    const q = AppState.quizQuestions[AppState.quizIndex];
    const record = q ? AppState.quizResults[q.id] : null;

    document.querySelectorAll('.btn-check').forEach(btn => {
      const type = btn.dataset.ans;
      btn.classList.toggle('active', record && record.status === type);
    });
  }

  function renderQuizDotsNav() {
    const container = document.getElementById('quizDotsNav');
    if (!container) return;

    container.innerHTML = '';
    AppState.quizQuestions.forEach((q, idx) => {
      const dot = document.createElement('div');
      dot.className = 'dot-item';
      if (idx === AppState.quizIndex) dot.classList.add('current');

      const record = AppState.quizResults[q.id];
      if (record) {
        dot.classList.add(record.status);
      }

      dot.addEventListener('click', () => {
        AppState.quizIndex = idx;
        renderQuizCard();
      });

      container.appendChild(dot);
    });
  }

  function updateQuizDotsActive() {
    const dots = document.querySelectorAll('.dot-item');
    dots.forEach((dot, idx) => {
      dot.classList.toggle('current', idx === AppState.quizIndex);
    });
  }

  // ==========================================================================
  // 8. 晨間純腦力體操 (Morning Brain Gym 1★~10★)
  // ==========================================================================
  function initBrainGym() {
    // 晨間體操切換到此視圖時自動載入
  }

  function loadBrainGym() {
    const card = document.getElementById('braingymCard');
    if (!card || !window.ENGLISH_DATA) return;

    const bgList = ENGLISH_DATA.quizzes.filter(q => q.type === 'brain_gym');
    if (bgList.length === 0) {
      card.innerHTML = '<div class="no-data-msg">目前尚無晨間體操題目。</div>';
      return;
    }

    const currentQ = bgList[AppState.brainGymIndex % bgList.length];

    card.innerHTML = `
      <div class="card-question-box">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-weight:700; color:var(--accent-amber);">⭐ Level ${currentQ.star || 1} 晨間挑戰</span>
          <span class="q-difficulty">${currentQ.difficulty || '★★★☆☆'}</span>
        </div>
        <div class="q-stem" style="font-size:1.4rem;">${escapeHtml(currentQ.question)}</div>
      </div>

      <div class="interactive-options" id="bgOptionsContainer">
        ${currentQ.options.map(opt => `
          <button class="option-btn bg-opt-btn" data-opt="${escapeHtml(opt)}">
            <span>${escapeHtml(opt)}</span>
          </button>
        `).join('')}
      </div>

      <div class="explanation-box" id="bgExpBox" style="margin-top: 1rem;">
        <div class="exp-header">
          <span class="exp-badge">🧠 晨間雙色直覺解析</span>
          <span class="exp-correct-ans">正解：${escapeHtml(currentQ.answer)}</span>
        </div>
        <div class="exp-content">${escapeHtml(currentQ.explanation)}</div>
        <div style="margin-top: 1.25rem; display:flex; justify-content:flex-end;">
          <button id="nextBgBtn" class="btn-primary">
            <span>挑戰下一題 ⚡</span>
          </button>
        </div>
      </div>
    `;

    // 選項點選
    card.querySelectorAll('.bg-opt-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const opt = btn.dataset.opt;
        const isCorrect = (opt.trim().toLowerCase() === currentQ.answer.trim().toLowerCase());
        
        card.querySelectorAll('.bg-opt-btn').forEach(b => {
          if (b.dataset.opt.trim().toLowerCase() === currentQ.answer.trim().toLowerCase()) {
            b.classList.add('selected-correct');
          }
        });

        if (!isCorrect) {
          btn.classList.add('selected-wrong');
        }

        const expBox = document.getElementById('bgExpBox');
        if (expBox) expBox.classList.add('active');
      });
    });

    const nextBtn = document.getElementById('nextBgBtn');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        AppState.brainGymIndex++;
        loadBrainGym();
      });
    }
  }

  // ==========================================================================
  // 9. 終身錯題本 (Error Book)
  // ==========================================================================
  function initErrorBook() {
    const filterBook = document.getElementById('errorBookFilter');
    const filterStatus = document.getElementById('errorStatusFilter');

    if (filterBook) filterBook.addEventListener('change', renderErrorBook);
    if (filterStatus) filterStatus.addEventListener('change', renderErrorBook);

    // 啟動錯題消滅戰
    const retryBtn = document.getElementById('retryErrorsBtn');
    if (retryBtn) {
      retryBtn.addEventListener('click', () => {
        if (AppState.errors.length === 0) {
          alert('太棒了！目前錯題本空空如也，沒有需要消滅的錯題！');
          return;
        }
        AppState.quizQuestions = AppState.errors.map(e => e.questionData);
        AppState.quizIndex = 0;
        AppState.quizResults = {};
        switchView('quiz');
      });
    }
  }

  function logErrorQuestion(question, status) {
    const existingIdx = AppState.errors.findIndex(e => e.id === question.id);
    const record = {
      id: question.id,
      book_id: question.book_id,
      unit_id: question.unit_id,
      status: status, // 'wrong' or 'hesitant'
      lastAttempt: Date.now(),
      questionData: question
    };

    if (existingIdx >= 0) {
      AppState.errors[existingIdx] = record;
    } else {
      AppState.errors.push(record);
    }
    saveErrorBook();
  }

  function removeErrorQuestion(questionId) {
    const initialLen = AppState.errors.length;
    AppState.errors = AppState.errors.filter(e => e.id !== questionId);
    if (AppState.errors.length !== initialLen) {
      saveErrorBook();
    }
  }

  function renderErrorBook() {
    const list = document.getElementById('errorCardsList');
    const filterBook = document.getElementById('errorBookFilter');
    const filterStatus = document.getElementById('errorStatusFilter');
    if (!list) return;

    // 填充錯題課本篩選選單
    if (filterBook && filterBook.options.length <= 1 && window.ENGLISH_DATA) {
      ENGLISH_DATA.books.forEach(b => {
        const opt = document.createElement('option');
        opt.value = b.book_id;
        opt.textContent = b.book_name;
        filterBook.appendChild(opt);
      });
    }

    const selectedBook = filterBook ? filterBook.value : 'all';
    const selectedStatus = filterStatus ? filterStatus.value : 'all';

    let filtered = AppState.errors;
    if (selectedBook !== 'all') {
      filtered = filtered.filter(e => e.book_id === selectedBook);
    }
    if (selectedStatus !== 'all') {
      filtered = filtered.filter(e => e.status === selectedStatus);
    }

    list.innerHTML = '';
    if (filtered.length === 0) {
      list.innerHTML = '<div class="no-data-msg" style="padding: 2.5rem; text-align: center;">🎉 目前沒有符合篩選條件的錯題！觀念完全通透！</div>';
      return;
    }

    filtered.forEach(item => {
      const q = item.questionData;
      const card = document.createElement('div');
      card.className = 'error-item-card';
      card.innerHTML = `
        <div class="error-left-col">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <span class="error-status-tag ${item.status === 'wrong' ? 'status-wrong' : 'status-hesitant'}">
              ${item.status === 'wrong' ? '❌ 算錯 / 答錯' : '⏳ 猶豫 / 想很久'}
            </span>
            <span style="font-size:0.8rem; color:var(--text-muted);">${q.book_id.toUpperCase()} ｜ ${q.unit_id}</span>
          </div>
          <div class="error-q-stem">${escapeHtml(q.question)}</div>
          <div class="error-ans-row">正確答案：${escapeHtml(q.answer)}</div>
          <div style="font-size:0.88rem; color:var(--text-secondary); line-height:1.5;">${escapeHtml(q.explanation || '')}</div>
        </div>
        <div>
          <button class="btn-secondary btn-remove-err" data-id="${item.id}" title="已掌握，移出錯題本">
            <span>✅ 克服</span>
          </button>
        </div>
      `;

      card.querySelector('.btn-remove-err').addEventListener('click', () => {
        removeErrorQuestion(item.id);
        renderErrorBook();
      });

      list.appendChild(card);
    });
  }

  // ==========================================================================
  // 10. A4 考卷排版列印引擎 (Print Engine)
  // ==========================================================================
  function initPrintEngine() {
    const genBtn = document.getElementById('generatePrintPreviewBtn');
    const printBtn = document.getElementById('triggerPrintBtn');

    if (genBtn) genBtn.addEventListener('click', renderA4PrintPreview);
    if (printBtn) {
      printBtn.addEventListener('click', () => {
        window.print();
      });
    }

    // 監聽選項變更即時重新排版
    document.querySelectorAll('input[name="printType"]').forEach(r => {
      r.addEventListener('change', renderA4PrintPreview);
    });
    const countSelect = document.getElementById('printCountSelect');
    const modeSelect = document.getElementById('printAnswerMode');
    if (countSelect) countSelect.addEventListener('change', renderA4PrintPreview);
    if (modeSelect) modeSelect.addEventListener('change', renderA4PrintPreview);
  }

  function renderA4PrintPreview() {
    const sheet = document.getElementById('a4ExamSheet');
    if (!sheet || !window.ENGLISH_DATA) return;

    const printTypeRadio = document.querySelector('input[name="printType"]:checked');
    const printType = printTypeRadio ? printTypeRadio.value : 'spelling';
    const count = parseInt(document.getElementById('printCountSelect').value, 10) || 15;
    const isTeacher = (document.getElementById('printAnswerMode').value === 'teacher');

    const book = ENGLISH_DATA.books.find(b => b.book_id === AppState.selectedBookId);
    const unit = ENGLISH_DATA.units.find(u => u.book_id === AppState.selectedBookId && u.unit_id === AppState.selectedUnitId);

    const bookName = book ? book.book_name : '英語教材';
    const unitTitle = unit ? (unit.unit_title || unit.unit_id) : '單元評量';

    // 生成 QR Code (指向當前單元練習)
    let qrSvg = '';
    try {
      if (typeof qrcode !== 'undefined') {
        const qr = qrcode(0, 'M');
        qr.addData(window.location.href);
        qr.make();
        qrSvg = qr.createSvgTag({ scalable: true });
      }
    } catch (e) {
      console.warn('QR Code 生成失敗:', e);
    }

    let questionsHtml = '';

    if (printType === 'spelling') {
      // Spelling Bee 單字聽寫卷
      const vocabs = ENGLISH_DATA.vocabulary.filter(v => v.book_id === AppState.selectedBookId && v.unit_id === AppState.selectedUnitId).slice(0, count);
      
      questionsHtml = `
        <div class="sheet-questions-grid sheet-two-col">
          ${vocabs.map((v, i) => `
            <div class="sheet-q-item">
              <div class="sheet-q-stem">
                <strong>${i + 1}.</strong> 【${escapeHtml(v.chi)}】
                ${v.pos ? `<span style="font-size:9pt; color:#6B7280;">(${escapeHtml(v.pos)})</span>` : ''}
              </div>
              ${isTeacher 
                ? `<div class="sheet-teacher-ans">正解：${escapeHtml(v.word)}</div>` 
                : `<div class="sheet-spelling-line"></div>`
              }
            </div>
          `).join('')}
        </div>
      `;
    } else {
      // 文法或綜合評量卷
      const qList = ENGLISH_DATA.quizzes.filter(q => q.book_id === AppState.selectedBookId && q.unit_id === AppState.selectedUnitId && q.type !== 'brain_gym').slice(0, count);

      questionsHtml = `
        <div class="sheet-questions-grid">
          ${qList.map((q, i) => `
            <div class="sheet-q-item">
              <div class="sheet-q-stem">
                <strong>${i + 1}.</strong> ${escapeHtml(q.question)}
              </div>
              ${q.options && q.options.length > 0 ? `
                <div class="sheet-options-row">
                  ${q.options.map((opt, oi) => `<span>(${String.fromCharCode(65 + oi)}) ${escapeHtml(opt)}</span>`).join('')}
                </div>
              ` : ''}
              ${isTeacher 
                ? `<div class="sheet-teacher-ans">正解：${escapeHtml(q.answer)} ｜ ${escapeHtml(q.explanation || '')}</div>`
                : `<div style="height: 18px; border-bottom: 1px dotted #D1D5DB; margin-top: 4px;"></div>`
              }
            </div>
          `).join('')}
        </div>
      `;
    }

    sheet.innerHTML = `
      <div class="sheet-header">
        <div class="sheet-title-zone">
          <h1>${escapeHtml(bookName)} — ${escapeHtml(unitTitle)}</h1>
          <p>${printType === 'spelling' ? 'Spelling Bee 實體單字聽寫卷' : 'Grammar & Usage 文法診斷卷'} ｜ 總題數：${count} 題 ${isTeacher ? '（教師 / 家長解答版）' : ''}</p>
          <div class="sheet-meta-bar">
            <span>學校/班級：____________</span>
            <span>姓名：____________</span>
            <span>座號：______</span>
            <span>得分：______ / 100</span>
          </div>
        </div>
        <div class="sheet-qr-box">
          <div class="sheet-qr-code">${qrSvg}</div>
          <div class="sheet-qr-tip">掃描即時核對正解</div>
        </div>
      </div>

      ${questionsHtml}
    `;
  }

  // ==========================================================================
  // 11. AI Prompt Exporter 模組
  // ==========================================================================
  function initAiModal() {
    const modal = document.getElementById('aiPromptModal');
    const openBtn = document.getElementById('exportAiPromptBtn');
    const closeBtn = document.getElementById('closeModalBtn');
    const copyBtn = document.getElementById('copyPromptBtn');
    const textarea = document.getElementById('aiPromptTextarea');

    if (openBtn) {
      openBtn.addEventListener('click', () => {
        if (AppState.errors.length === 0) {
          alert('目前錯題本無任何錯題，不需要匯出！');
          return;
        }

        const promptText = generateAiPrompt();
        if (textarea) textarea.value = promptText;
        if (modal) modal.classList.add('active');
      });
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        if (modal) modal.classList.remove('active');
      });
    }

    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('active');
      });
    }

    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        if (textarea) {
          textarea.select();
          navigator.clipboard.writeText(textarea.value).then(() => {
            copyBtn.querySelector('span').textContent = '✅ 已成功複製！';
            setTimeout(() => {
              copyBtn.querySelector('span').textContent = '📋 一鍵複製 Prompt';
            }, 2000);
          });
        }
      });
    }
  }

  function generateAiPrompt() {
    const errorSample = AppState.errors.slice(0, 5).map((e, i) => {
      const q = e.questionData;
      return `【錯題 ${i + 1}】(${e.book_id.toUpperCase()} ${e.unit_id})\n題目：${q.question}\n正解：${q.answer}\n學生狀態：${e.status === 'wrong' ? '算錯/選錯' : '猶豫想很久'}\n詳解筆記：${q.explanation || '無'}`;
    }).join('\n\n');

    return `你是一位頂尖的小學六年級英語教研出題專家。
以下是一位 12 歲國小六年級學生在做英語測驗時遇到的錯題與盲點紀錄：

${errorSample}

請為這位學生執行「精準錯題消滅與自適應補強出題」：
1. 深入剖析學生在以上題目中的核心文法盲點（如 -ed/-ing 形容詞混淆、動詞三態變化、時態一致性、介系詞搭配失誤）。
2. 針對上述每個錯題觀念，量身生成 2~3 題「相同語法觀念、不同日常生活情境」的深度變式題（4 個選項，並附上標註正解與詳細防坑破題思路）。
3. 難度對標校內名校段考滿分與全民英檢（GEPT 初級）水準，請用繁體中文輸出。`;
  }

  // ==========================================================================
  // 六上期中考特訓專區 (Midterm Sprint Engine)
  // ==========================================================================
  let speechRecInstance = null;
  let autoAdvanceTimer = null;
  let autoAdvanceBarTimer = null;

  function initMidtermSprint() {
    if (!window.MIDTERM_DATABASE || !Array.isArray(window.MIDTERM_DATABASE)) {
      console.warn('未偵測到 MIDTERM_DATABASE 資料庫');
      return;
    }

    const unitSelect = document.getElementById('midtermUnitSelect');
    if (unitSelect) {
      unitSelect.innerHTML = '';
      
      // 按分類分組（置頂真實小考考券）
      const categories = [
        { name: '⭐ 歷史考券錯題特訓 (TEA 3C Quiz 真題)', cat: '歷史考券' },
        { name: '📘 文法專修 (Oxford Discover Grammar 3)', cat: '文法專修' },
        { name: '📝 寫作專攻 (Write Right Level 3)', cat: '寫作專攻' },
        { name: '🚀 科普長篇 (Oxford Read and Discover 6)', cat: '科普長篇' },
        { name: '📖 讀寫進階 (Reading with Writing Level 6)', cat: '讀寫進階' }
      ];

      categories.forEach(group => {
        const optgroup = document.createElement('optgroup');
        optgroup.label = group.name;
        const groupUnits = window.MIDTERM_DATABASE.filter(u => u.category === group.cat);
        groupUnits.forEach(u => {
          const opt = document.createElement('option');
          opt.value = u.id;
          opt.textContent = u.display_title || u.unit_title;
          if (u.id === AppState.selectedMidtermUnitId) opt.selected = true;
          optgroup.appendChild(opt);
        });
        unitSelect.appendChild(optgroup);
      });

      unitSelect.addEventListener('change', (e) => {
        AppState.selectedMidtermUnitId = e.target.value;
        AppState.activeSentenceIdx = null;
        AppState.currentMistakeIdx = 0;
        AppState.selectedTokenIdx = null;
        AppState.currentMidtermQuizIdx = 0;
        cancelOngoingSpeech();
        renderMidtermSprint();
      });
    }

    // 期中考 4 大 Subtabs 點擊
    const subtabs = document.querySelectorAll('.midterm-subtab-btn');
    subtabs.forEach(btn => {
      btn.addEventListener('click', () => {
        const subtab = btn.dataset.subtab;
        AppState.midtermSubtab = subtab;
        
        subtabs.forEach(b => b.classList.toggle('active', b.dataset.subtab === subtab));
        document.querySelectorAll('.midterm-subtab-content').forEach(c => {
          c.classList.toggle('active', c.id === `midterm-subtab-${subtab}`);
        });

        cancelOngoingSpeech();
        renderMidtermCurrentSubtab();
      });
    });

    // 逐句自動跟讀模式開關
    const autoAdvanceToggle = document.getElementById('autoAdvanceToggle');
    if (autoAdvanceToggle) {
      autoAdvanceToggle.addEventListener('change', (e) => {
        AppState.midtermAutoAdvance = e.target.checked;
      });
    }

    // 語速切換
    const midtermTtsBtn = document.getElementById('midtermTtsSpeedBtn');
    if (midtermTtsBtn) {
      midtermTtsBtn.addEventListener('click', () => {
        AppState.ttsSpeed = AppState.ttsSpeed === 1.0 ? 0.8 : 1.0;
        updateTtsSpeedButtonUI();
        const lbl = document.getElementById('midtermTtsSpeedLabel');
        if (lbl) lbl.textContent = `${AppState.ttsSpeed.toFixed(1)}x`;
      });
    }

    // 停止所有語音
    const stopSpeechBtn = document.getElementById('stopAllSpeechBtn');
    if (stopSpeechBtn) {
      stopSpeechBtn.addEventListener('click', () => {
        cancelOngoingSpeech();
      });
    }

    // 全篇中文翻譯開關
    let allZhVisible = false;
    const toggleAllZhBtn = document.getElementById('toggleAllZhBtn');
    if (toggleAllZhBtn) {
      toggleAllZhBtn.addEventListener('click', () => {
        allZhVisible = !allZhVisible;
        document.querySelectorAll('.sentence-zh-text').forEach(el => {
          el.style.display = allZhVisible ? 'block' : 'none';
        });
        document.querySelectorAll('.btn-sentence-zh').forEach(btn => {
          btn.classList.toggle('active', allZhVisible);
        });
        const label = toggleAllZhBtn.querySelector('span');
        if (label) {
          label.textContent = allZhVisible ? '🌐 隱藏全篇翻譯' : '🌐 顯示全篇翻譯';
        }
      });
    }

    // 篇章下拉切換
    const passageSelect = document.getElementById('passagePickerSelect');
    if (passageSelect) {
      passageSelect.addEventListener('change', () => {
        renderSentenceCardsForSelectedPassage();
      });
    }

    // 改錯題 (Mistake Buster) 事件
    initMistakeBusterEvents();

    // 雙軌測驗 (Dual Quiz) 事件
    initDualQuizEvents();

    // A4 模考列印事件
    initMidtermPrintEvents();
  }

  function getSelectedMidtermUnit() {
    if (!window.MIDTERM_DATABASE) return null;
    return window.MIDTERM_DATABASE.find(u => u.id === AppState.selectedMidtermUnitId) || window.MIDTERM_DATABASE[0];
  }

  function renderMidtermSprint() {
    const unit = getSelectedMidtermUnit();
    if (!unit) return;

    // 更新 Meta 標籤
    const metaBox = document.getElementById('midtermUnitMeta');
    if (metaBox) {
      const sentenceCount = (unit.passages || []).reduce((acc, p) => acc + (p.sentences || []).length, 0);
      metaBox.innerHTML = `
        <span class="meta-tag">教材：${escapeHtml(unit.book)}</span>
        <span class="meta-tag">難度：${escapeHtml(unit.cefr)}</span>
        <span class="meta-tag">頁碼：${escapeHtml(unit.pages)}</span>
        <span class="meta-tag">句庫：${sentenceCount} 句</span>
        <span class="meta-tag">改錯：${(unit.mistake_buster || []).length} 題</span>
        <span class="meta-tag">測驗：${(unit.quizzes || []).length} 題</span>
      `;
    }

    // 更新各 Subtab 上的計數徽章
    const sentenceCount = (unit.passages || []).reduce((acc, p) => acc + (p.sentences || []).length, 0);
    const sTag = document.getElementById('shadowingCountTag');
    if (sTag) sTag.textContent = `${sentenceCount} 句`;

    const mTag = document.getElementById('mistakeCountTag');
    if (mTag) mTag.textContent = `${(unit.mistake_buster || []).length} 題`;

    const qTag = document.getElementById('midtermQuizCountTag');
    if (qTag) qTag.textContent = `${(unit.quizzes || []).length} 題`;

    renderMidtermCurrentSubtab();
  }

  function renderMidtermCurrentSubtab() {
    if (AppState.midtermSubtab === 'shadowing') {
      renderSentenceShadowing();
    } else if (AppState.midtermSubtab === 'mistake') {
      renderMistakeBuster();
    } else if (AppState.midtermSubtab === 'quiz') {
      renderMidtermDualQuiz();
    } else if (AppState.midtermSubtab === 'exam') {
      renderMidtermA4Exam();
    }
  }

  function cancelOngoingSpeech() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    if (autoAdvanceTimer) {
      clearTimeout(autoAdvanceTimer);
      autoAdvanceTimer = null;
    }
    if (autoAdvanceBarTimer) {
      clearTimeout(autoAdvanceBarTimer);
      autoAdvanceBarTimer = null;
    }
    document.querySelectorAll('.sentence-card').forEach(c => {
      c.classList.remove('active-sentence');
      const b = c.querySelector('.shadowing-countdown-bar');
      if (b) b.remove();
    });
    if (speechRecInstance) {
      try { speechRecInstance.stop(); } catch (e) {}
    }
  }

  // ==========================================================================
  // 子模組 1: 句子精聽跟讀 (Sentence Shadowing)
  // ==========================================================================
  function renderSentenceShadowing() {
    const unit = getSelectedMidtermUnit();
    if (!unit || !unit.passages || unit.passages.length === 0) {
      const container = document.getElementById('sentenceCardsContainer');
      if (container) container.innerHTML = `<div class="empty-state">此單元暫無分句課文</div>`;
      return;
    }

    const pickerRow = document.getElementById('passagePickerRow');
    const pickerSelect = document.getElementById('passagePickerSelect');
    if (unit.passages.length > 1) {
      pickerRow.style.display = 'flex';
      pickerSelect.innerHTML = '';
      unit.passages.forEach((p, idx) => {
        const opt = document.createElement('option');
        opt.value = idx;
        opt.textContent = `篇章 ${idx + 1}：${p.section_title} (${(p.sentences || []).length} 句)`;
        pickerSelect.appendChild(opt);
      });
    } else {
      pickerRow.style.display = 'none';
    }

    renderSentenceCardsForSelectedPassage();
  }

  function renderSentenceCardsForSelectedPassage() {
    const unit = getSelectedMidtermUnit();
    if (!unit || !unit.passages) return;

    const pickerSelect = document.getElementById('passagePickerSelect');
    const pIdx = (pickerSelect && pickerSelect.value !== '') ? parseInt(pickerSelect.value, 10) : 0;
    const passage = unit.passages[pIdx] || unit.passages[0];
    const sentences = passage.sentences || [];

    const currentPassageTag = document.getElementById('currentPassageTag');
    if (currentPassageTag) {
      currentPassageTag.textContent = passage.section_title || '閱讀篇章';
    }

    const container = document.getElementById('sentenceCardsContainer');
    if (!container) return;
    container.innerHTML = '';

    sentences.forEach((sent, idx) => {
      const card = document.createElement('div');
      card.className = 'sentence-card';
      card.dataset.idx = idx;

      const enText = (typeof sent === 'object' && sent !== null) ? sent.en : String(sent);
      const zhText = (typeof sent === 'object' && sent !== null) ? (sent.zh || '') : '';

      card.innerHTML = `
        <div class="sentence-main">
          <div class="sentence-num-badge">#${String(idx + 1).padStart(2, '0')}</div>
          <div class="sentence-content-wrap">
            <div class="sentence-text">${escapeHtml(enText)}</div>
            ${zhText ? `<div class="sentence-zh-text" style="display: none;">${escapeHtml(zhText)}</div>` : ''}
          </div>
        </div>
        <div class="sentence-card-actions">
          ${zhText ? `<button class="btn-sentence-zh" title="查看中文翻譯">🌐 中文</button>` : ''}
          <button class="btn-sentence-speak" title="朗讀此句">🔊</button>
        </div>
      `;

      // 點擊中文按鈕切換翻譯
      const zhBtn = card.querySelector('.btn-sentence-zh');
      const zhBox = card.querySelector('.sentence-zh-text');
      if (zhBtn && zhBox) {
        zhBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          const isHidden = zhBox.style.display === 'none';
          zhBox.style.display = isHidden ? 'block' : 'none';
          zhBtn.classList.toggle('active', isHidden);
        });
      }

      // 點擊發音按鈕
      const speakBtn = card.querySelector('.btn-sentence-speak');
      if (speakBtn) {
        speakBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          playSentenceWithHighlight(enText, card, idx, sentences);
        });
      }

      // 點擊整張卡片發音高亮
      card.addEventListener('click', () => {
        playSentenceWithHighlight(enText, card, idx, sentences);
      });

      container.appendChild(card);
    });
  }

  function playSentenceWithHighlight(sentenceInput, cardEl, idx, allSentences) {
    cancelOngoingSpeech();
    cardEl.classList.add('active-sentence');

    if (!('speechSynthesis' in window)) {
      alert('您的瀏覽器不支援 Web Speech API 發音功能');
      return;
    }

    const rawText = (typeof sentenceInput === 'object' && sentenceInput !== null) ? (sentenceInput.en || '') : String(sentenceInput);
    const cleanText = rawText.replace(/[¹²³⁴⁵⁶⁷⁸⁹⁰\[\]*#_`]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'en-US';
    utterance.rate = AppState.ttsSpeed || 1.0;
    if (bestEnVoice) utterance.voice = bestEnVoice;

    utterance.onend = () => {
      // 若開啟了逐句自動跟讀模式且還有下一句
      if (AppState.midtermAutoAdvance && idx + 1 < allSentences.length) {
        // 插入 3 秒跟讀倒數進度條
        const bar = document.createElement('div');
        bar.className = 'shadowing-countdown-bar';
        cardEl.appendChild(bar);
        
        // 啟動動畫
        setTimeout(() => { bar.style.width = '100%'; }, 20);

        autoAdvanceTimer = setTimeout(() => {
          const nextCard = document.querySelector(`.sentence-card[data-idx="${idx + 1}"]`);
          if (nextCard) {
            playSentenceWithHighlight(allSentences[idx + 1], nextCard, idx + 1, allSentences);
            nextCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }, 3000);
      }
    };

    utterance.onerror = (err) => {
      console.warn('發音中斷或錯誤:', err);
    };

    window.speechSynthesis.speak(utterance);
  }

  // ==========================================================================
  // 子模組 2: 神探點詞抓錯 (Mistake Buster)
  // ==========================================================================
  function initMistakeBusterEvents() {
    const checkBtn = document.getElementById('checkMistakeBtn');
    if (checkBtn) {
      checkBtn.addEventListener('click', handleCheckMistake);
    }

    const resetBtn = document.getElementById('resetTokensBtn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        AppState.selectedTokenIdx = null;
        document.querySelectorAll('.token-chip').forEach(c => c.classList.remove('token-selected'));
        const drawer = document.getElementById('mistakeFeedbackDrawer');
        if (drawer) drawer.style.display = 'none';
      });
    }

    const playFixedBtn = document.getElementById('playCorrectedSentenceBtn');
    if (playFixedBtn) {
      playFixedBtn.addEventListener('click', () => {
        const text = document.getElementById('correctedText')?.textContent || '';
        speakSentenceText(text);
      });
    }

    const selfCorrectBtn = document.getElementById('mistakeSelfCorrectBtn');
    if (selfCorrectBtn) {
      selfCorrectBtn.addEventListener('click', () => {
        alert('🎉 太棒了！紙筆作答正確！記下一勝！');
      });
    }

    const selfWrongBtn = document.getElementById('mistakeSelfWrongBtn');
    if (selfWrongBtn) {
      selfWrongBtn.addEventListener('click', () => {
        saveCurrentMistakeToErrors();
        alert('📕 已將此改錯題收入【終身錯題本】，隨時複習！');
      });
    }

    const prevBtn = document.getElementById('prevMistakeBtn');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        const unit = getSelectedMidtermUnit();
        if (!unit || !unit.mistake_buster) return;
        if (AppState.currentMistakeIdx > 0) {
          AppState.currentMistakeIdx--;
          renderMistakeBuster();
        }
      });
    }

    const nextBtn = document.getElementById('nextMistakeBtn');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        const unit = getSelectedMidtermUnit();
        if (!unit || !unit.mistake_buster) return;
        if (AppState.currentMistakeIdx < unit.mistake_buster.length - 1) {
          AppState.currentMistakeIdx++;
          renderMistakeBuster();
        }
      });
    }
  }

  function renderMistakeBuster() {
    const unit = getSelectedMidtermUnit();
    const tokensBox = document.getElementById('sentenceTokensBox');
    const drawer = document.getElementById('mistakeFeedbackDrawer');
    if (drawer) drawer.style.display = 'none';

    if (!unit || !unit.mistake_buster || unit.mistake_buster.length === 0) {
      if (tokensBox) tokensBox.innerHTML = `<div class="empty-state">此單元未收錄獨立改錯題</div>`;
      return;
    }

    const total = unit.mistake_buster.length;
    if (AppState.currentMistakeIdx >= total) AppState.currentMistakeIdx = 0;
    const item = unit.mistake_buster[AppState.currentMistakeIdx];

    // 更新進度與標籤
    const pBadge = document.getElementById('mistakeProgressBadge');
    if (pBadge) pBadge.textContent = `關卡 ${AppState.currentMistakeIdx + 1} / ${total}`;

    const trapTag = document.getElementById('mistakeTrapTag');
    if (trapTag) trapTag.textContent = item.trap_id || '考卷必考改錯陷阱';

    AppState.selectedTokenIdx = null;
    tokensBox.innerHTML = '';

    const tokens = item.tokens || item.sentence.split(/\s+/);
    tokens.forEach((token, idx) => {
      const chip = document.createElement('span');
      chip.className = 'token-chip';
      chip.dataset.idx = idx;
      chip.textContent = token;

      chip.addEventListener('click', () => {
        // 點擊選取或取消選取
        if (AppState.selectedTokenIdx === idx) {
          AppState.selectedTokenIdx = null;
          chip.classList.remove('token-selected');
        } else {
          document.querySelectorAll('.token-chip').forEach(c => c.classList.remove('token-selected'));
          AppState.selectedTokenIdx = idx;
          chip.classList.add('token-selected');
        }
      });

      tokensBox.appendChild(chip);
    });

    // 渲染小圓點
    const dotsBox = document.getElementById('mistakeDots');
    if (dotsBox) {
      dotsBox.innerHTML = '';
      for (let i = 0; i < total; i++) {
        const dot = document.createElement('div');
        dot.className = `mistake-dot ${i === AppState.currentMistakeIdx ? 'active' : ''}`;
        dot.addEventListener('click', () => {
          AppState.currentMistakeIdx = i;
          renderMistakeBuster();
        });
        dotsBox.appendChild(dot);
      }
    }
  }

  function handleCheckMistake() {
    const unit = getSelectedMidtermUnit();
    if (!unit || !unit.mistake_buster) return;
    const item = unit.mistake_buster[AppState.currentMistakeIdx];
    const drawer = document.getElementById('mistakeFeedbackDrawer');
    const banner = document.getElementById('feedbackStatusBanner');
    const correctedText = document.getElementById('correctedText');
    const rationaleContent = document.getElementById('mistakeRationaleContent');

    if (!drawer) return;
    drawer.style.display = 'block';

    const isMatch = (AppState.selectedTokenIdx === item.wrong_index);
    if (isMatch) {
      banner.className = 'feedback-status-banner success';
      banner.innerHTML = `<span>🎯 神探級眼力！成功抓出錯誤單字「<strong>${escapeHtml(item.wrong_word)}</strong>」！</span>`;
      
      const selChip = document.querySelector(`.token-chip[data-idx="${AppState.selectedTokenIdx}"]`);
      if (selChip) {
        selChip.classList.add('token-correct-wrong');
        selChip.innerHTML = `${escapeHtml(item.wrong_word)}<div class="token-floating-badge">${escapeHtml(item.wrong_word)} ➔ ${escapeHtml(item.correct_word)}</div>`;
      }
    } else {
      banner.className = 'feedback-status-banner miss';
      banner.innerHTML = `<span>💡 差一點點！真正的陷阱是「<strong>${escapeHtml(item.wrong_word)}</strong>」！</span>`;
      
      const trueChip = document.querySelector(`.token-chip[data-idx="${item.wrong_index}"]`);
      if (trueChip) {
        trueChip.classList.add('token-correct-wrong');
        trueChip.innerHTML = `${escapeHtml(item.wrong_word)}<div class="token-floating-badge">${escapeHtml(item.wrong_word)} ➔ ${escapeHtml(item.correct_word)}</div>`;
      }
    }

    if (correctedText) correctedText.textContent = item.fixed_sentence;
    if (rationaleContent) rationaleContent.textContent = item.reason || '請注意前後時態與介系詞的一致性。';
  }

  function saveCurrentMistakeToErrors() {
    const unit = getSelectedMidtermUnit();
    if (!unit || !unit.mistake_buster) return;
    const item = unit.mistake_buster[AppState.currentMistakeIdx];

    const errObj = {
      id: `MISTAKE_${unit.id}_${AppState.currentMistakeIdx + 1}`,
      book_id: unit.book,
      unit_id: unit.unit_title,
      status: 'wrong',
      timestamp: Date.now(),
      questionData: {
        question: `【點詞抓錯】${item.sentence}`,
        answer: `${item.wrong_word} ➔ ${item.correct_word}（完整句：${item.fixed_sentence}）`,
        explanation: item.reason
      }
    };

    if (!AppState.errors.some(e => e.id === errObj.id)) {
      AppState.errors.push(errObj);
      saveErrorBook();
    }
  }

  // ==========================================================================
  // 子模組 3: 紙筆/語音雙軌測驗 (Dual Quiz Arena)
  // ==========================================================================
  function initDualQuizEvents() {
    const paperModeBtn = document.getElementById('dualModePaperBtn');
    const voiceModeBtn = document.getElementById('dualModeVoiceBtn');
    const panelPaper = document.getElementById('panelPaperQuiz');
    const panelVoice = document.getElementById('panelVoiceQuiz');

    if (paperModeBtn && voiceModeBtn) {
      paperModeBtn.addEventListener('click', () => {
        AppState.midtermDualMode = 'paper';
        paperModeBtn.classList.add('active');
        voiceModeBtn.classList.remove('active');
        if (panelPaper) panelPaper.classList.add('active');
        if (panelVoice) panelVoice.classList.remove('active');
      });

      voiceModeBtn.addEventListener('click', () => {
        AppState.midtermDualMode = 'voice';
        voiceModeBtn.classList.add('active');
        paperModeBtn.classList.remove('active');
        if (panelVoice) panelVoice.classList.add('active');
        if (panelPaper) panelPaper.classList.remove('active');
      });
    }

    // 題型分類篩選膠囊按鈕
    const filterPills = document.querySelectorAll('.quiz-pill-btn');
    filterPills.forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;
        AppState.midtermQuizFilter = filter;
        AppState.currentMidtermQuizIdx = 0;
        filterPills.forEach(b => b.classList.toggle('active', b.dataset.filter === filter));
        renderMidtermDualQuiz();
      });
    });

    // 單字盲聽重聽按鈕
    const playWordBtn = document.getElementById('btnPlayWordAudio');
    if (playWordBtn) {
      playWordBtn.addEventListener('click', () => {
        const quizzes = getFilteredMidtermQuizzes();
        const q = quizzes[AppState.currentMidtermQuizIdx];
        if (q && q.audio_word) {
          speakWordAudio(q.audio_word, 1.0);
        }
      });
    }

    const playWordSlowBtn = document.getElementById('btnPlayWordSlowAudio');
    if (playWordSlowBtn) {
      playWordSlowBtn.addEventListener('click', () => {
        const quizzes = getFilteredMidtermQuizzes();
        const q = quizzes[AppState.currentMidtermQuizIdx];
        if (q && q.audio_word) {
          speakWordAudio(q.audio_word, 0.8);
        }
      });
    }

    // 翻牌看解答
    const showAnsBtn = document.getElementById('midtermShowAnswerBtn');
    if (showAnsBtn) {
      showAnsBtn.addEventListener('click', () => {
        const drawer = document.getElementById('midtermAnswerDrawer');
        if (drawer) drawer.style.display = 'block';
      });
    }

    // 朗讀標準正解
    const playAnsBtn = document.getElementById('playMidtermAnsSpeechBtn');
    if (playAnsBtn) {
      playAnsBtn.addEventListener('click', () => {
        const ans = document.getElementById('midtermCorrectAns')?.textContent || '';
        speakSentenceText(ans);
      });
    }

    // 語音錄製作答按鈕
    const voiceMicBtn = document.getElementById('midtermVoiceMicBtn');
    if (voiceMicBtn) {
      voiceMicBtn.addEventListener('click', handleVoiceRecognition);
    }

    // 答對 / 答錯自評
    const correctBtn = document.getElementById('midtermAnsCorrectBtn');
    if (correctBtn) {
      correctBtn.addEventListener('click', () => {
        alert('👍 恭喜作答正確！記下一分！');
      });
    }

    const wrongBtn = document.getElementById('midtermAnsWrongBtn');
    if (wrongBtn) {
      wrongBtn.addEventListener('click', () => {
        saveCurrentQuizToErrors();
        alert('❌ 已將此測驗題歸檔至【終身錯題本】！');
      });
    }

    // 上一題 / 下一題
    const prevQBtn = document.getElementById('midtermPrevQBtn');
    if (prevQBtn) {
      prevQBtn.addEventListener('click', () => {
        const quizzes = getFilteredMidtermQuizzes();
        if (quizzes.length === 0) return;
        if (AppState.currentMidtermQuizIdx > 0) {
          AppState.currentMidtermQuizIdx--;
          renderMidtermDualQuiz();
        }
      });
    }

    const nextQBtn = document.getElementById('midtermNextQBtn');
    if (nextQBtn) {
      nextQBtn.addEventListener('click', () => {
        const quizzes = getFilteredMidtermQuizzes();
        if (quizzes.length === 0) return;
        if (AppState.currentMidtermQuizIdx < quizzes.length - 1) {
          AppState.currentMidtermQuizIdx++;
          renderMidtermDualQuiz();
        }
      });
    }
  }

  function getFilteredMidtermQuizzes() {
    const unit = getSelectedMidtermUnit();
    if (!unit || !unit.quizzes) return [];
    if (!AppState.midtermQuizFilter || AppState.midtermQuizFilter === 'all') {
      return unit.quizzes;
    }
    return unit.quizzes.filter(q => q.category_tag === AppState.midtermQuizFilter);
  }

  function updateQuizFilterPillsCounts() {
    const unit = getSelectedMidtermUnit();
    if (!unit || !unit.quizzes) return;
    const allCount = unit.quizzes.length;
    const listenCount = unit.quizzes.filter(q => q.category_tag === 'listening').length;
    const fillCount = unit.quizzes.filter(q => q.category_tag === 'fill').length;
    const choiceCount = unit.quizzes.filter(q => q.category_tag === 'choice').length;
    const rewriteCount = unit.quizzes.filter(q => q.category_tag === 'rewrite').length;

    const elAll = document.getElementById('countPillAll');
    if (elAll) elAll.textContent = allCount;
    const elListen = document.getElementById('countPillListening');
    if (elListen) elListen.textContent = listenCount;
    const elFill = document.getElementById('countPillFill');
    if (elFill) elFill.textContent = fillCount;
    const elChoice = document.getElementById('countPillChoice');
    if (elChoice) elChoice.textContent = choiceCount;
    const elRewrite = document.getElementById('countPillRewrite');
    if (elRewrite) elRewrite.textContent = rewriteCount;
  }

  function speakWordAudio(word, rate = 1.0) {
    if (!('speechSynthesis' in window) || !word) return;
    window.speechSynthesis.cancel();
    const cleanWord = word.replace(/[¹²³⁴⁵⁶⁷⁸⁹⁰\[\]*#_`]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(cleanWord);
    utterance.lang = 'en-US';
    utterance.rate = rate;
    if (bestEnVoice) utterance.voice = bestEnVoice;
    window.speechSynthesis.speak(utterance);
  }

  function renderMidtermDualQuiz() {
    const unit = getSelectedMidtermUnit();
    const drawer = document.getElementById('midtermAnswerDrawer');
    if (drawer) drawer.style.display = 'none';

    const transcriptBox = document.getElementById('voiceTranscriptBox');
    if (transcriptBox) transcriptBox.style.display = 'none';

    updateQuizFilterPillsCounts();

    const quizzes = getFilteredMidtermQuizzes();
    const total = quizzes.length;

    if (total === 0) {
      const stem = document.getElementById('midtermQuizStem');
      if (stem) stem.textContent = '此分類下暫無題目，請點選上方其他題型標籤練習。';
      const hint = document.getElementById('midtermQuizHint');
      if (hint) hint.textContent = '';
      const listenPlayer = document.getElementById('spellingListenPlayer');
      if (listenPlayer) listenPlayer.style.display = 'none';
      const progText = document.getElementById('midtermQuizProgressText');
      if (progText) progText.textContent = '第 0 / 0 題';
      const dotsBox = document.getElementById('midtermQuizDots');
      if (dotsBox) dotsBox.innerHTML = '';
      return;
    }

    if (AppState.currentMidtermQuizIdx >= total) AppState.currentMidtermQuizIdx = 0;
    const q = quizzes[AppState.currentMidtermQuizIdx];

    // 更新進度與類型標籤
    const progText = document.getElementById('midtermQuizProgressText');
    if (progText) progText.textContent = `第 ${AppState.currentMidtermQuizIdx + 1} / ${total} 題`;

    const badge = document.getElementById('midtermQuizTypeBadge');
    if (badge) {
      const typeMap = {
        spelling_listen: '🎧 單字盲聽測驗 (聽寫)',
        fill: '✏️ 課文與文法填空',
        choice: '🔘 文法選擇題',
        paper_rewrite: '✍️ 句子改寫與造句',
        true_false: '是非判斷題 (True / False)',
        qa_comprehension: '閱讀理解簡答題',
        ladder_challenge: '教研段考天梯題'
      };
      badge.textContent = typeMap[q.type] || '英語綜合測驗';
    }

    // 更新題幹與提示
    const stem = document.getElementById('midtermQuizStem');
    if (stem) stem.textContent = q.question;

    const hint = document.getElementById('midtermQuizHint');
    if (hint) hint.textContent = q.hint || '在實體紙筆寫下你的答案後核對';

    // 單字盲聽專屬播放器
    const listenPlayer = document.getElementById('spellingListenPlayer');
    if (q.type === 'spelling_listen') {
      if (listenPlayer) {
        listenPlayer.style.display = 'flex';
        const pBadge = document.getElementById('listenPhoneticBadge');
        if (pBadge) pBadge.textContent = q.phonetic || '/English/';
        const sBadge = document.getElementById('listenSyllableBadge');
        if (sBadge) sBadge.textContent = q.syllables ? `音節拆解：${q.syllables}` : '';
      }
      // 自動朗讀單字一次
      speakWordAudio(q.audio_word, 1.0);
    } else {
      if (listenPlayer) listenPlayer.style.display = 'none';
    }

    // 更新解答抽屜標準正解
    const correctAnsEl = document.getElementById('midtermCorrectAns');
    if (correctAnsEl) correctAnsEl.textContent = q.answer;

    // 結構化三色硬核教研詳解 (考點 + 公式 + 考場盲點)
    const expConcept = document.getElementById('expConceptText');
    const expFormula = document.getElementById('expFormulaText');
    const expTrap = document.getElementById('expTrapText');

    if (typeof q.explanation === 'object' && q.explanation !== null) {
      if (expConcept) expConcept.textContent = q.explanation.concept || `${unit.display_title || unit.book} 核心考點`;
      if (expFormula) expFormula.textContent = q.explanation.formula || '破題關鍵與文法搭配規則';
      if (expTrap) expTrap.textContent = q.explanation.trap || '注意前後時態、名詞單複數與介系詞的一致性。';
    } else {
      if (expConcept) expConcept.textContent = `${unit.display_title || unit.book} 核心考點`;
      if (expFormula) expFormula.textContent = q.explanation || q.hint || '請參考題幹指定之文法結構作答。';
      if (expTrap) expTrap.textContent = '小學生常犯錯誤：切記動詞時態一致性與名詞單複數。';
    }

    // 渲染小圓點導航
    const dotsBox = document.getElementById('midtermQuizDots');
    if (dotsBox) {
      dotsBox.innerHTML = '';
      const maxDots = Math.min(total, 20);
      for (let i = 0; i < maxDots; i++) {
        const dot = document.createElement('div');
        dot.className = `mistake-dot ${i === AppState.currentMidtermQuizIdx ? 'active' : ''}`;
        dot.addEventListener('click', () => {
          AppState.currentMidtermQuizIdx = i;
          renderMidtermDualQuiz();
        });
        dotsBox.appendChild(dot);
      }
    }
  }

  function handleVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const micBtn = document.getElementById('midtermVoiceMicBtn');
    const micLabel = document.getElementById('midtermVoiceMicLabel');
    const transcriptBox = document.getElementById('voiceTranscriptBox');
    const transcriptText = document.getElementById('voiceTranscriptText');
    const matchBadge = document.getElementById('voiceMatchBadge');

    if (!SpeechRecognition) {
      alert('您的瀏覽器不支援 Web Speech 語音辨識（建議使用 Chrome / Edge），請切換為【📝 紙筆模式】！');
      return;
    }

    if (speechRecInstance) {
      try { speechRecInstance.stop(); } catch (e) {}
      speechRecInstance = null;
      micBtn.classList.remove('recording');
      micLabel.textContent = '點擊麥克風口說唸出答案';
      return;
    }

    speechRecInstance = new SpeechRecognition();
    speechRecInstance.lang = 'en-US';
    speechRecInstance.interimResults = false;
    speechRecInstance.maxAlternatives = 1;

    micBtn.classList.add('recording');
    micLabel.textContent = '🎙️ 正在聆聽中... 請念出答案...';

    speechRecInstance.onresult = (event) => {
      const spoken = event.results[0][0].transcript || '';
      micBtn.classList.remove('recording');
      micLabel.textContent = '點擊麥克風重新作答';
      speechRecInstance = null;

      if (transcriptBox && transcriptText) {
        transcriptBox.style.display = 'block';
        transcriptText.textContent = `"${spoken}"`;
      }

      // 計算相似度
      const quizzes = getFilteredMidtermQuizzes();
      const q = quizzes[AppState.currentMidtermQuizIdx];
      const similarity = calculateStringSimilarity(spoken, q.answer);

      if (matchBadge) {
        if (similarity >= 0.65) {
          matchBadge.className = 'voice-match-badge matched';
          matchBadge.textContent = `🎉 匹配度 ${Math.round(similarity * 100)}%！發音與答案非常標準！`;
        } else {
          matchBadge.className = 'voice-match-badge unmatched';
          matchBadge.textContent = `💡 匹配度 ${Math.round(similarity * 100)}%，請參考下方標準解答`;
        }
      }

      // 自動展開解答抽屜
      const drawer = document.getElementById('midtermAnswerDrawer');
      if (drawer) drawer.style.display = 'block';
    };

    speechRecInstance.onerror = (err) => {
      console.warn('語音辨識錯誤:', err);
      micBtn.classList.remove('recording');
      micLabel.textContent = '點擊麥克風重新作答';
      speechRecInstance = null;
      alert('未偵測到清晰語音或麥克風權限受阻，請再次點擊麥克風嘗試。');
    };

    speechRecInstance.onend = () => {
      micBtn.classList.remove('recording');
      micLabel.textContent = '點擊麥克風口說唸出答案';
      speechRecInstance = null;
    };

    try {
      speechRecInstance.start();
    } catch (e) {
      console.warn('無法啟動語音辨識:', e);
    }
  }

  function saveCurrentQuizToErrors() {
    const unit = getSelectedMidtermUnit();
    const quizzes = getFilteredMidtermQuizzes();
    if (!unit || quizzes.length === 0) return;
    const q = quizzes[AppState.currentMidtermQuizIdx];

    const expText = typeof q.explanation === 'object' && q.explanation !== null
      ? `【考點】${q.explanation.concept}\n【破題】${q.explanation.formula}\n【陷阱】${q.explanation.trap}`
      : (q.explanation || q.hint);

    const errObj = {
      id: q.id || `QUIZ_${unit.id}_${AppState.currentMidtermQuizIdx + 1}`,
      book_id: unit.book,
      unit_id: unit.unit_title,
      status: 'wrong',
      timestamp: Date.now(),
      questionData: {
        question: q.question,
        answer: q.answer,
        explanation: expText
      }
    };

    if (!AppState.errors.some(e => e.id === errObj.id)) {
      AppState.errors.push(errObj);
      saveErrorBook();
    }
  }

  function speakSentenceText(text) {
    if (!('speechSynthesis' in window) || !text) return;
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[¹²³⁴⁵⁶⁷⁸⁹⁰\[\]*#_`]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'en-US';
    utterance.rate = AppState.ttsSpeed || 1.0;
    if (bestEnVoice) utterance.voice = bestEnVoice;
    window.speechSynthesis.speak(utterance);
  }

  function calculateStringSimilarity(s1, s2) {
    if (!s1 || !s2) return 0;
    const clean1 = s1.toLowerCase().replace(/[^a-z0-9\s]/g, '').trim();
    const clean2 = s2.toLowerCase().replace(/[^a-z0-9\s]/g, '').trim();
    if (clean1 === clean2) return 1.0;
    if (clean1.includes(clean2) || clean2.includes(clean1)) return 0.85;

    const tokens1 = clean1.split(/\s+/);
    const tokens2 = clean2.split(/\s+/);
    let matches = 0;
    tokens1.forEach(t => {
      if (tokens2.includes(t)) matches++;
    });
    return matches / Math.max(tokens1.length, tokens2.length);
  }

  // ==========================================================================
  // 子模組 4: A4 期中模擬卷列印
  // ==========================================================================
  function initMidtermPrintEvents() {
    const genBtn = document.getElementById('generateMidtermExamBtn');
    if (genBtn) {
      genBtn.addEventListener('click', renderMidtermA4Exam);
    }

    const printBtn = document.getElementById('triggerMidtermPrintBtn');
    if (printBtn) {
      printBtn.addEventListener('click', () => {
        window.print();
      });
    }
  }

  function renderMidtermA4Exam() {
    const sheet = document.getElementById('midtermA4Sheet');
    if (!sheet) return;

    const scopeSelect = document.getElementById('midtermPrintScope');
    const modeSelect = document.getElementById('midtermPrintMode');
    const scopeVal = scopeSelect ? scopeSelect.value : 'current';
    const modeVal = modeSelect ? modeSelect.value : 'student';

    const isTeacher = (modeVal === 'teacher');
    const isContrast = (modeVal === 'contrast');
    const today = new Date().toISOString().split('T')[0];

    // 分支 1: 岱崙美語歷史考券 1:1 復原重測卷 (Week 2 / Week 4 / Week 5 真題)
    if (scopeVal === 'quiz_original') {
      renderQuizOriginalExam(sheet, isTeacher, isContrast, today);
      return;
    }

    // 分支 2: AI 變式狙擊模擬卷 (動態抽換詞彙題)
    if (scopeVal === 'quiz_variant') {
      renderQuizVariantExam(sheet, isTeacher, isContrast, today);
      return;
    }

    // 分支 3: 既有常規範圍 (current 或 all)
    const isAll = (scopeVal === 'all');
    const currentUnit = getSelectedMidtermUnit();
    const targetUnits = isAll ? (window.MIDTERM_DATABASE || []) : (currentUnit ? [currentUnit] : []);

    // 匯整題目
    let allVocab = [];
    let allMistakes = [];
    let allRewrites = [];
    let allQuizzes = [];

    targetUnits.forEach(u => {
      (u.vocab || []).forEach(v => allVocab.push({ ...v, unit_title: u.unit_title }));
      (u.mistake_buster || []).forEach(m => allMistakes.push({ ...m, unit_title: u.unit_title }));
      (u.quizzes || []).forEach(q => {
        if (q.type === 'paper_rewrite') allRewrites.push({ ...q, unit_title: u.unit_title });
        else allQuizzes.push({ ...q, unit_title: u.unit_title });
      });
    });

    const examTitle = isAll ? '國小六年級上學期 英語期中考全真大模擬測驗卷' : `國小六年級上學期 英語期中評量特訓卷 — ${currentUnit ? (currentUnit.display_title || currentUnit.unit_title) : ''}`;

    let html = `
      <div class="exam-header">
        <div class="exam-header-left">
          <div class="exam-grade-badge">國小六年級英語 ｜ 114 學年度第一學期期中評量</div>
          <h1 class="exam-title">${escapeHtml(examTitle)}</h1>
          <div class="exam-meta-row">
            <span>評量範圍：${isAll ? '四大模組 11 單元總複習' : escapeHtml(currentUnit ? currentUnit.book : '')}</span>
            <span>滿分：100 分</span>
            <span>命題日期：${today}</span>
            ${isTeacher ? '<span style="color:#DC2626; font-weight:800;">【教師/家長解答檢閱卷】</span>' : ''}
            ${isContrast ? '<span style="color:#DC2626; font-weight:800;">【考券紅黑批改對照卷】</span>' : ''}
          </div>
        </div>
        <div class="exam-header-right">
          <div class="score-box">
            <span class="score-title">得分 / Score</span>
            <div class="score-line"></div>
          </div>
        </div>
      </div>

      <div class="student-info-row">
        <div class="info-item">班級：__________</div>
        <div class="info-item">座號：______</div>
        <div class="info-item">姓名：________________</div>
      </div>
    `;

    // Part I: 單字片語填空
    if (allVocab.length > 0) {
      const vocabSlice = allVocab.slice(0, 5);
      html += `
        <div class="exam-section">
          <div class="section-title-print">I. 核心單字與片語計量測驗 (每題 4 分，共 20 分)</div>
          <div class="exam-questions-grid">
      `;
      vocabSlice.forEach((v, idx) => {
        const promptWord = v.meaning || v.translation || '';
        const promptSub = v.example ? `(${v.example})` : (v.note ? `[${v.note}]` : '');
        let ansText = '____________________';
        if (isTeacher) {
          ansText = `<strong style="color:#DC2626; margin-left:10px;">${escapeHtml(v.word)}</strong>`;
        } else if (isContrast) {
          ansText = `<span class="contrast-redpen">${escapeHtml(v.word)}</span>`;
        }
        html += `
          <div class="print-q-item">
            <span class="q-num">${idx + 1}.</span>
            <span class="q-text">${escapeHtml(promptWord)} ${escapeHtml(promptSub)} ➔ ${ansText}</span>
          </div>
        `;
      });
      html += `</div></div>`;
    }

    // Part II: 神探改錯題 (Mistake Buster)
    if (allMistakes.length > 0) {
      const mistakeSlice = allMistakes.slice(0, 4);
      html += `
        <div class="exam-section">
          <div class="section-title-print">II. 語法偵錯與改錯題 (找出錯誤單字並在下方格子訂正整句，每題 7.5 分，共 30 分)</div>
          <div class="exam-questions-grid">
      `;
      mistakeSlice.forEach((m, idx) => {
        let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:24px; margin-top:6px;"></div>`;
        if (isTeacher) {
          ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：錯字「${escapeHtml(m.wrong_word)}」➔「${escapeHtml(m.correct_word)}」\n完整句：${escapeHtml(m.fixed_sentence)} (${escapeHtml(m.reason || '')})</div>`;
        } else if (isContrast) {
          ansLine = `
            <div class="contrast-box">
              <div>考場學生筆跡：<span class="contrast-pencil">${escapeHtml(m.wrong_word)}</span> ❌</div>
              <div>老師紅筆訂正：<span class="contrast-redpen">${escapeHtml(m.correct_word)}</span> ✓（完整句：<strong>${escapeHtml(m.fixed_sentence)}</strong>）</div>
              <span class="contrast-explanation">💡 教研防坑思路：${escapeHtml(m.reason || '')}</span>
            </div>
          `;
        }
        html += `
          <div class="print-q-item" style="margin-bottom:12px;">
            <span class="q-num">${idx + 1}.</span>
            <span class="q-text">原句：<code>${escapeHtml(m.sentence)}</code></span>
            ${ansLine}
          </div>
        `;
      });
      html += `</div></div>`;
    }

    // Part III: 句子改寫與重組
    if (allRewrites.length > 0) {
      const rwSlice = allRewrites.slice(0, 4);
      html += `
        <div class="exam-section">
          <div class="section-title-print">III. 句型轉換與倒裝附和句改寫 (每題 6 分，共 24 分)</div>
          <div class="exam-questions-grid">
      `;
      rwSlice.forEach((r, idx) => {
        let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:24px; margin-top:6px;"></div>`;
        if (isTeacher || isContrast) {
          ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：${escapeHtml(r.answer)}</div>`;
        }
        html += `
          <div class="print-q-item" style="margin-bottom:12px;">
            <span class="q-num">${idx + 1}.</span>
            <span class="q-text">${escapeHtml(r.question)}</span>
            ${ansLine}
          </div>
        `;
      });
      html += `</div></div>`;
    }

    // Part IV: 閱讀素養與綜合選擇
    if (allQuizzes.length > 0) {
      const qSlice = allQuizzes.slice(0, 5);
      html += `
        <div class="exam-section">
          <div class="section-title-print">IV. 閱讀理解與文法選擇 (每題 5.2 分，共 26 分)</div>
          <div class="exam-questions-grid">
      `;
      qSlice.forEach((q, idx) => {
        let ansLine = `( ______ )`;
        if (isTeacher || isContrast) {
          ansLine = `<strong style="color:#DC2626; margin-left:8px;">(正解：${escapeHtml(q.answer)})</strong>`;
        }
        html += `
          <div class="print-q-item" style="margin-bottom:10px;">
            <span class="q-num">${idx + 1}.</span>
            <span class="q-text">${escapeHtml(q.question)} ${ansLine}</span>
          </div>
        `;
      });
      html += `</div></div>`;
    }

    sheet.innerHTML = html;
  }

  function renderQuizOriginalExam(sheet, isTeacher, isContrast, today) {
    const title = '國小六年級 岱崙美語 3C Quiz 歷史真題 1:1 復原評量卷 (Week 2 / 4 / 5)';
    
    let html = `
      <div class="exam-header">
        <div class="exam-header-left">
          <div class="exam-grade-badge">岱崙美語 3C Quiz ｜ 歷史真實小考 1:1 復原重測</div>
          <h1 class="exam-title">${escapeHtml(title)}</h1>
          <div class="exam-meta-row">
            <span>出卷來源：Week 2, Week 4, Week 5 歷史真卷</span>
            <span>滿分：100 分</span>
            <span>命題日期：${today}</span>
            ${isTeacher ? '<span style="color:#DC2626; font-weight:800;">【標準解答卷】</span>' : ''}
            ${isContrast ? '<span style="color:#DC2626; font-weight:800;">【考場紅黑批改對照卷 (學生原答 vs 老師批改)】</span>' : ''}
          </div>
        </div>
        <div class="exam-header-right">
          <div class="score-box">
            <span class="score-title">得分 / Score</span>
            <div class="score-line"></div>
          </div>
        </div>
      </div>

      <div class="student-info-row">
        <div class="info-item">班級：__________</div>
        <div class="info-item">座號：______</div>
        <div class="info-item">姓名：________________</div>
      </div>
    `;

    // 考券 Part I: Spelling 單字聽寫 (Week 2, 4 真題)
    const spellingItems = [
      { num: 1, zh: "槓桿", ans: "lever", student: "lever", correct: true, note: "" },
      { num: 2, zh: "斜坡道", ans: "ramp", student: "ramp", correct: true, note: "" },
      { num: 3, zh: "楔子 (三角木)", ans: "wedge", student: "wadge", correct: false, note: "學生曾誤寫為 wadge，加強 /e/ 母音" },
      { num: 4, zh: "小刀", ans: "knife", student: "Knif", correct: false, note: "學生曾漏寫字尾 e" },
      { num: 5, zh: "山脈", ans: "mountain", student: "mountion", correct: false, note: "學生曾誤寫為 mountion" },
      { num: 6, zh: "輪椅", ans: "wheelchair", student: "whillchair", correct: false, note: "學生曾誤寫為 whillchair" },
      { num: 7, zh: "熔爐", ans: "furnace", student: "furnes", correct: false, note: "學生曾誤拼為 furnes，字尾為 -ace" },
      { num: 8, zh: "眼鏡鏡框", ans: "frames", student: "France", correct: false, note: "學生誤寫成法國 France" },
      { num: 9, zh: "在...前面", ans: "in front of", student: "infront off", correct: false, note: "三字需空格且介系詞為 of" },
      { num: 10, zh: "在...對面", ans: "across from", student: "across from", correct: true, note: "" }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">Part I. Spelling Bee 考場聽寫單字 (每題 2 分，共 20 分)</div>
        <div class="exam-questions-grid" style="grid-template-columns: 1fr 1fr; display: grid; gap: 8px 24px;">
    `;
    spellingItems.forEach(sp => {
      let ansDisplay = '____________________';
      if (isTeacher) {
        ansDisplay = `<strong style="color:#DC2626; margin-left:8px;">${sp.ans}</strong>`;
      } else if (isContrast) {
        if (sp.correct) {
          ansDisplay = `<span class="contrast-pencil">${sp.student}</span> <span style="color:#059669; font-weight:bold;">✓</span>`;
        } else {
          ansDisplay = `<span class="contrast-pencil">${sp.student}</span> ❌ ➔ <span class="contrast-redpen">${sp.ans}</span> <small style="color:#6B7280;">(${sp.note})</small>`;
        }
      }
      html += `
        <div class="print-q-item" style="font-size:10.5pt; margin-bottom:4px;">
          <span class="q-num">${sp.num}.</span>
          <span class="q-text">${sp.zh} ➔ ${ansDisplay}</span>
        </div>
      `;
    });
    html += `</div></div>`;

    // 考券 Part II: Grammar 3 (Unit 13) 倒裝附和句改寫 (Week 2 真題，學生得 5/12 分)
    const grammar13Items = [
      {
        q: "Ryan, Michael - 95% on quiz / too",
        ans: "Ryan got 95% on his quiz, and Michael did, too.",
        student: "Ryan 95% on quiz, Michael are too",
        redNote: "補動詞 got，刪 are too 改 did, too",
        reason: "肯定附和句：前面有一般動詞 got，後面用助動詞 did + too"
      },
      {
        q: "Brad, Lisa - did not play baseball / either",
        ans: "Brad did not play baseball, and Lisa didn't either.",
        student: "Brad did not play baseball, and Lisa didn't either.",
        redNote: "滿分作答 ✓",
        reason: "否定附和句：S + didn't + either 公式完全正確"
      },
      {
        q: "Olivia, Penny - 100% on quiz / so",
        ans: "Olivia got 100% on her quiz, and so did Penny.",
        student: "Olivia 100% on quiz, Penny was so did",
        redNote: "補動詞 got，改為 and so did Penny",
        reason: "倒裝附和句公式：so + 助動詞 (did) + 主詞 (Penny)"
      },
      {
        q: "Ray, Jim - not pass quiz / either",
        ans: "Ray didn't pass the quiz, and Jim didn't either.",
        student: "Ray are not pass quiz, and Jim didn't either.",
        redNote: "劃掉 are not pass，改為 didn't pass the quiz",
        reason: "過去式否定句必須使用助動詞 didn't + 原形動詞 pass"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">Part II. Grammar 3 (U13) 倒裝附和句長句改寫 (每題 6 分，共 24 分)</div>
        <div class="exam-questions-grid">
    `;
    grammar13Items.forEach((g, idx) => {
      let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:24px; margin-top:6px;"></div>`;
      if (isTeacher) {
        ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：${escapeHtml(g.ans)}</div>`;
      } else if (isContrast) {
        ansLine = `
          <div class="contrast-box">
            <div>學生考場手寫：<span class="contrast-pencil">${escapeHtml(g.student)}</span> ${g.student === g.ans ? '<span style="color:#059669; font-weight:bold;">✓</span>' : '❌'}</div>
            <div>老師紅筆批註：<span class="contrast-redpen">${escapeHtml(g.ans)}</span> <small>(${escapeHtml(g.redNote)})</small></div>
            <span class="contrast-explanation">💡 語法盲點剖析：${escapeHtml(g.reason)}</span>
          </div>
        `;
      }
      html += `
        <div class="print-q-item" style="margin-bottom:10px;">
          <span class="q-num">${idx + 1}.</span>
          <span class="q-text">Prompt: <strong>[${escapeHtml(g.q)}]</strong></span>
          ${ansLine}
        </div>
      `;
    });
    html += `</div></div>`;

    // 考券 Part III: Grammar 3 (Unit 14) 副詞三級比較長句合成 (Week 4 / 5 真題，重大失分點 4/20 分)
    const grammar14Items = [
      {
        q: "How fast can they run? person, dog & lion",
        ans: "A person runs fast, a dog runs faster than a person, but a lion runs the fastest.",
        student: "A person can run fast, a dog can run more fast than a dog, and a lion can run the faster",
        redNote: "劃掉 more fast 改 faster than a person；劃掉 the faster 改 the fastest；and 改 but",
        reason: "fast 是單音節副詞（faster, the fastest）；前後兩物比較對象需不同；最後一項為轉折 but"
      },
      {
        q: "How quickly can they walk? five year old, eight year old & adult",
        ans: "A five year old can walk quickly, an eight year old can walk more quickly than a five year old, but an adult can walk the most quickly.",
        student: "five year old walk quick, eight year old walk quicker than five year old, adult walk fastest",
        redNote: "補冠詞 A/an；quick 改副詞 quickly；比較級用 more quickly than；最高級用 the most quickly",
        reason: "修飾動詞 walk 必須用副詞形式 quickly；多音節副詞比較級與最高級為 more quickly / the most quickly"
      },
      {
        q: "How far can they jump? frog, rabbit & kangaroo",
        ans: "A frog can jump far, a rabbit can jump farther than a frog, but a kangaroo can jump the farthest.",
        student: "A frog can jump far, a rabbit can jump farther than a frog, but a kangaroo can jump farthest.",
        redNote: "farthest 前面補冠詞 the",
        reason: "最高級副詞前面務必加上 the（the farthest）"
      },
      {
        q: "How loudly can they laugh? Peter, Helen & Jack",
        ans: "Peter laughs loudly, Helen laughs more loudly than Peter, but Jack laughs the most loudly.",
        student: "Peter laugh loud, Helen laugh more loud than Peter, but Jack laugh the most loud.",
        redNote: "第三人稱單數動詞加 s (laughs)；loud 改為副詞 loudly / more loudly / the most loudly",
        reason: "一般動詞修飾副詞 -ly 與主詞第三人稱單數動詞加 -s"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">Part III. Grammar 3 (U14) 副詞三級長句合成 (每題 8 分，共 32 分)</div>
        <div class="exam-questions-grid">
    `;
    grammar14Items.forEach((g, idx) => {
      let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:24px; margin-top:6px;"></div>`;
      if (isTeacher) {
        ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：${escapeHtml(g.ans)}</div>`;
      } else if (isContrast) {
        ansLine = `
          <div class="contrast-box">
            <div>學生考場手寫：<span class="contrast-pencil">${escapeHtml(g.student)}</span> ❌</div>
            <div>老師紅筆批註：<span class="contrast-redpen">${escapeHtml(g.ans)}</span></div>
            <span class="contrast-explanation">💡 批改詳情：${escapeHtml(g.redNote)} ｜ 盲點：${escapeHtml(g.reason)}</span>
          </div>
        `;
      }
      html += `
        <div class="print-q-item" style="margin-bottom:12px;">
          <span class="q-num">${idx + 1}.</span>
          <span class="q-text">Prompt: <strong>[${escapeHtml(g.q)}]</strong></span>
          ${ansLine}
        </div>
      `;
    });
    html += `</div></div>`;

    // 考券 Part IV: RWW6 Unit 6 定向越野課文長篇聽寫 (Week 5 真題 25/25 滿分)
    html += `
      <div class="exam-section">
        <div class="section-title-print">Part IV. RWW6 (U6) 課文精準聽寫填空 (Orienteering 長篇，共 24 分)</div>
        <div class="print-q-item" style="line-height:1.8; font-size:10.5pt; background:#F8FAFC; border:1px solid #E2E8F0; padding:12px; border-radius:6px;">
    `;
    const dictationText = isTeacher ? 
      `In the sport of orienteering, racers use a <strong style="color:#DC2626;">map</strong> and <strong style="color:#DC2626;">compass</strong> to find stations, which are called <strong style="color:#DC2626;">controls</strong>. A special <strong style="color:#DC2626;">flag</strong> marks each control. Controls are placed in tricky locations to challenge racers' <strong style="color:#DC2626;">navigation</strong> skills. Racers must punch their cards at every station to prove they visited it. The person who finishes the course in the <strong style="color:#DC2626;">fastest</strong> time wins the race.` :
      (isContrast ?
      `In the sport of orienteering, racers use a <span class="contrast-redpen">map ✓</span> and <span class="contrast-redpen">compass ✓</span> to find stations, which are called <span class="contrast-redpen">controls ✓</span>. A special <span class="contrast-redpen">flag ✓</span> marks each control. Controls are placed in tricky locations to challenge racers' <span class="contrast-redpen">navigation ✓</span> skills. Racers must punch their cards at every station to prove they visited it. The person who finishes the course in the <span class="contrast-redpen">fastest ✓</span> time wins the race. <span style="display:block; color:#059669; font-weight:bold; margin-top:6px;">🎉 學生考場表現：25/25 滿分！生字拼寫與首字母大小寫零失誤！</span>` :
      `In the sport of orienteering, racers use a <strong>(1) ________</strong> and <strong>(2) ________</strong> to find stations, which are called <strong>(3) ________</strong>. A special <strong>(4) ________</strong> marks each control. Controls are placed in tricky locations to challenge racers' <strong>(5) ________</strong> skills. Racers must punch their cards at every station to prove they visited it. The person who finishes the course in the <strong>(6) ________</strong> time wins the race.`);

    html += `${dictationText}</div></div>`;

    sheet.innerHTML = html;
  }

  function renderQuizVariantExam(sheet, isTeacher, isContrast, today) {
    const title = '國小六年級英語 ｜ AI 變式狙擊模擬卷 (考券同構全新題型)';

    let html = `
      <div class="exam-header">
        <div class="exam-header-left">
          <div class="exam-grade-badge">AI 智慧自適應出題 ｜ 歷史考券 AI_SPEC 同構變式</div>
          <h1 class="exam-title">${escapeHtml(title)}</h1>
          <div class="exam-meta-row">
            <span>出題邏輯：抽換情境與人物，100% 相同文法考核內核</span>
            <span>滿分：100 分</span>
            <span>命題日期：${today}</span>
            ${(isTeacher || isContrast) ? '<span style="color:#DC2626; font-weight:800;">【標準解答卷】</span>' : ''}
          </div>
        </div>
        <div class="exam-header-right">
          <div class="score-box">
            <span class="score-title">得分 / Score</span>
            <div class="score-line"></div>
          </div>
        </div>
      </div>

      <div class="student-info-row">
        <div class="info-item">班級：__________</div>
        <div class="info-item">座號：______</div>
        <div class="info-item">姓名：________________</div>
      </div>
    `;

    // Part I: AI 變式倒裝附和句改寫 (4 題，每題 6 分 = 24 分)
    const variantG13 = [
      {
        prompt: "Emma, Lucas - finished the race / so",
        ans: "Emma finished the race, and so did Lucas.",
        hint: "肯定倒裝附和句：so + 過去助動詞 did + 主詞 Lucas"
      },
      {
        prompt: "Noah, Liam - did not watch TV / either",
        ans: "Noah did not watch TV, and Liam didn't either.",
        hint: "否定一般附和句：主詞 Liam + didn't + either"
      },
      {
        prompt: "Sophia, Ava - won the spelling contest / too",
        ans: "Sophia won the spelling contest, and Ava did, too.",
        hint: "肯定一般附和句：助動詞 did + 逗號 + too"
      },
      {
        prompt: "Ethan, Mason - was not late for school / neither",
        ans: "Ethan was not late for school, and neither was Mason.",
        hint: "否定倒裝附和句：neither + be動詞過去式 was + 主詞 Mason"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">I. AI 變式倒裝附和句改寫 (依指定連接詞合成句子，每題 6 分，共 24 分)</div>
        <div class="exam-questions-grid">
    `;
    variantG13.forEach((g, idx) => {
      let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:24px; margin-top:6px;"></div>`;
      if (isTeacher || isContrast) {
        ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：${escapeHtml(g.ans)} <small style="color:#4B5563;">(${escapeHtml(g.hint)})</small></div>`;
      }
      html += `
        <div class="print-q-item" style="margin-bottom:12px;">
          <span class="q-num">${idx + 1}.</span>
          <span class="q-text">Prompt: <strong>[${escapeHtml(g.prompt)}]</strong></span>
          ${ansLine}
        </div>
      `;
    });
    html += `</div></div>`;

    // Part II: AI 變式副詞三級長句合成 (4 題，每題 8 分 = 32 分)
    const variantG14 = [
      {
        prompt: "How loudly can they roar? cub, wolf & tiger",
        ans: "A cub can roar loudly, a wolf can roar more loudly than a cub, but a tiger can roar the most loudly.",
        hint: "多音節副詞 loudly ➔ more loudly than ➔ the most loudly"
      },
      {
        prompt: "How skillfully can they paint? beginner, student & artist",
        ans: "A beginner can paint skillfully, a student can paint more skillfully than a beginner, but an artist can paint the most skillfully.",
        hint: "注意 an artist 冠詞為 an；paint 需加或不加 s 視時態/助動詞而定"
      },
      {
        prompt: "How beautifully can they dance? Bella, Chloe & Mia",
        ans: "Bella dances beautifully, Chloe dances more beautifully than Bella, but Mia dances the most beautifully.",
        hint: "第三人稱單數動詞加 s (dances)；more beautifully / the most beautifully"
      },
      {
        prompt: "How high can they jump? cat, deer & horse",
        ans: "A cat can jump high, a deer can jump higher than a cat, but a horse can jump the highest.",
        hint: "單音節副詞 high ➔ higher than ➔ the highest"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">II. AI 變式副詞三級長句合成 (每題 8 分，共 32 分)</div>
        <div class="exam-questions-grid">
    `;
    variantG14.forEach((g, idx) => {
      let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:24px; margin-top:6px;"></div>`;
      if (isTeacher || isContrast) {
        ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：${escapeHtml(g.ans)} <small style="color:#4B5563;">(${escapeHtml(g.hint)})</small></div>`;
      }
      html += `
        <div class="print-q-item" style="margin-bottom:12px;">
          <span class="q-num">${idx + 1}.</span>
          <span class="q-text">Prompt: <strong>[${escapeHtml(g.prompt)}]</strong></span>
          ${ansLine}
        </div>
      `;
    });
    html += `</div></div>`;

    // Part III: 易混淆生詞與介系詞改錯 (4 題，每題 6 分 = 24 分)
    const variantMistakes = [
      {
        sent: "The new library is right infront off the city hall.",
        wrong: "infront off",
        correct: "in front of",
        fixed: "The new library is right in front of the city hall.",
        reason: "介系詞片語為 in front of（三字分開，介系詞是 of 不是 off）"
      },
      {
        sent: "The blacksmith heated the iron bar in the hot furnes.",
        wrong: "furnes",
        correct: "furnace",
        fixed: "The blacksmith heated the iron bar in the hot furnace.",
        reason: "熔爐拼寫為 furnace (-ace 字尾)"
      },
      {
        sent: "She broke the France of her glasses yesterday.",
        wrong: "France",
        correct: "frames",
        fixed: "She broke the frames of her glasses yesterday.",
        reason: "鏡框為 frames，不是國家法國 France"
      },
      {
        sent: "Workers used a sharp wadge to split the big log.",
        wrong: "wadge",
        correct: "wedge",
        fixed: "Workers used a sharp wedge to split the big log.",
        reason: "三角楔子拼寫為 wedge，母音為 e"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">III. 易混淆生字與介系詞改錯 (每題 6 分，共 24 分)</div>
        <div class="exam-questions-grid">
    `;
    variantMistakes.forEach((m, idx) => {
      let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:24px; margin-top:6px;"></div>`;
      if (isTeacher || isContrast) {
        ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：錯字「${escapeHtml(m.wrong)}」➔「${escapeHtml(m.correct)}」\n完整句：${escapeHtml(m.fixed)} (${escapeHtml(m.reason)})</div>`;
      }
      html += `
        <div class="print-q-item" style="margin-bottom:12px;">
          <span class="q-num">${idx + 1}.</span>
          <span class="q-text">原句：<code>${escapeHtml(m.sent)}</code></span>
          ${ansLine}
        </div>
      `;
    });
    html += `</div></div>`;

    // Part IV: 寫作句型造句 (2 題，每題 10 分 = 20 分)
    html += `
      <div class="exam-section">
        <div class="section-title-print">IV. 寫作核心句型造句 (每題 10 分，共 20 分)</div>
        <div class="exam-questions-grid">
          <div class="print-q-item" style="margin-bottom:14px;">
            <span class="q-num">1.</span>
            <span class="q-text">使用 <strong>If I had... I would...</strong> 寫出一個假設語氣句子（假如你有 5000 元，你會做什麼？）：</span>
            ${(isTeacher || isContrast) ? '<div style="color:#DC2626; font-weight:600; margin-top:4px;">範例正解：If I had 5000 dollars, I would buy a new bicycle for my brother.</div>' : '<div class="write-line" style="border-bottom:1px solid #000; height:28px; margin-top:8px;"></div>'}
          </div>
          <div class="print-q-item" style="margin-bottom:14px;">
            <span class="q-num">2.</span>
            <span class="q-text">使用 <strong>I have lived in... for...</strong> 寫出一個現在完成式居住年限句子：</span>
            ${(isTeacher || isContrast) ? '<div style="color:#DC2626; font-weight:600; margin-top:4px;">範例正解：I have lived in my neighborhood for five years.</div>' : '<div class="write-line" style="border-bottom:1px solid #000; height:28px; margin-top:8px;"></div>'}
          </div>
        </div>
      </div>
    `;

    sheet.innerHTML = html;
  }

  // ==========================================================================
  // 工具函式
  // ==========================================================================
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function jsonParseSafe(str) {
    try {
      return JSON.parse(str);
    } catch (e) {
      return null;
    }
  }

})();
