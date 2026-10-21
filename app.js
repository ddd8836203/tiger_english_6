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
    midtermQuizStatus: {},         // { [qId]: 'correct' | 'wrong' }
    midtermMistakeStatus: {},      // { [trapId]: 'correct' | 'wrong' }
    studySubtab: 'vocab',          // 'vocab' | 'reading' | 'grammar'
    selectedBookId: 'gra3',        // 預設六上期中考 Grammar 3
    selectedUnitId: 'gra3_13',     // 預設 Unit 13
    ttsSpeed: 1.0,                 // 1.0x 或 0.8x
    quizMode: 'paper',             // 'paper' (紙筆對答) | 'interactive' (iPad 點選)
    quizCategory: 'all',           // 'all' | 'grammar' | 'reading' | 'vocab'
    isErrorBookRetry: false,       // 是否為錯題本消滅戰模式
    quizQuestions: [],             // 當前測驗題庫
    quizIndex: 0,                  // 當前題號 (0-indexed)
    quizResults: {},               // { [qId]: { status: 'correct'|'hesitant'|'wrong', selectedOption, timestamp } }
    brainGymQuestions: [],         // 晨間體操題目
    brainGymIndex: 0,
    brainGymTier: 'all',           // 'all' | '1-3' | '4-7' | '8-10'
    brainGymCombo: 0,
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
    switchView(AppState.currentView);
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
        if (parsed && parsed.ttsSpeed) AppState.ttsSpeed = parsed.ttsSpeed;
        if (parsed && parsed.bookId && window.ENGLISH_DATA) {
          const validUnit = ENGLISH_DATA.units.find(u => u.book_id === parsed.bookId && u.unit_id === parsed.unitId);
          if (validUnit && parsed.bookId !== 'od3') {
            AppState.selectedBookId = parsed.bookId;
            AppState.selectedUnitId = parsed.unitId;
            if (validUnit.midterm_unit_id) {
              AppState.selectedMidtermUnitId = validUnit.midterm_unit_id;
            }
          }
        }
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

  // 雙向同步期中考單元與頂部課本/單元選單
  function syncTopbarFromMidtermId(midtermUnitId) {
    if (!window.ENGLISH_DATA) return;
    const matchedUnit = ENGLISH_DATA.units.find(u => u.midterm_unit_id === midtermUnitId);
    if (matchedUnit) {
      AppState.selectedBookId = matchedUnit.book_id;
      AppState.selectedUnitId = matchedUnit.unit_id;
      const bookSelect = document.getElementById('bookSelect');
      if (bookSelect) bookSelect.value = AppState.selectedBookId;
      populateUnitsForSelectedBook();
      saveSettings();
      renderCurrentUnit();
    }
  }

  function syncMidtermFromTopbarUnit() {
    if (!window.ENGLISH_DATA) return;
    const matchedUnit = ENGLISH_DATA.units.find(u => u.book_id === AppState.selectedBookId && u.unit_id === AppState.selectedUnitId);
    if (matchedUnit && matchedUnit.midterm_unit_id) {
      AppState.selectedMidtermUnitId = matchedUnit.midterm_unit_id;
      const midtermSelect = document.getElementById('midtermUnitSelect');
      if (midtermSelect) midtermSelect.value = AppState.selectedMidtermUnitId;
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

    // 填充課本選單（分組：🔥 六上期中考核心教材 vs 📚 其他延伸教材）
    bookSelect.innerHTML = '';
    const midtermBooks = ENGLISH_DATA.books.filter(b => b.is_midterm);
    const otherBooks = ENGLISH_DATA.books.filter(b => !b.is_midterm);

    if (midtermBooks.length > 0) {
      const grpMid = document.createElement('optgroup');
      grpMid.label = '🔥 六上期中考核心範圍 (5 大教材)';
      midtermBooks.forEach(b => {
        const opt = document.createElement('option');
        opt.value = b.book_id;
        opt.textContent = b.book_name;
        if (b.book_id === AppState.selectedBookId) opt.selected = true;
        grpMid.appendChild(opt);
      });
      bookSelect.appendChild(grpMid);
    }

    if (otherBooks.length > 0) {
      const grpOther = document.createElement('optgroup');
      grpOther.label = '📚 課外與歷屆延伸教材';
      otherBooks.forEach(b => {
        const opt = document.createElement('option');
        opt.value = b.book_id;
        opt.textContent = b.book_name;
        if (b.book_id === AppState.selectedBookId) opt.selected = true;
        grpOther.appendChild(opt);
      });
      bookSelect.appendChild(grpOther);
    }

    // 課本切換事件
    bookSelect.addEventListener('change', (e) => {
      AppState.selectedBookId = e.target.value;
      AppState.isErrorBookRetry = false;
      populateUnitsForSelectedBook();
      syncMidtermFromTopbarUnit();
      saveSettings();
      renderCurrentUnit();
      if (AppState.currentView === 'quiz') loadQuizForCurrentUnit();
      if (AppState.currentView === 'print') renderA4PrintPreview();
    });

    // 填充並切換單元
    populateUnitsForSelectedBook();

    unitSelect.addEventListener('change', (e) => {
      AppState.selectedUnitId = e.target.value;
      AppState.isErrorBookRetry = false;
      syncMidtermFromTopbarUnit();
      saveSettings();
      renderCurrentUnit();
      if (AppState.currentView === 'quiz') loadQuizForCurrentUnit();
      if (AppState.currentView === 'print') renderA4PrintPreview();
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

    // 區分期中考單元與一般單元
    const midUnits = bookUnits.filter(u => u.is_midterm);
    const extUnits = bookUnits.filter(u => !u.is_midterm);
    let matchFound = false;

    const appendUnitOptions = (container, unitsList) => {
      unitsList.forEach(u => {
        const opt = document.createElement('option');
        opt.value = u.unit_id;
        opt.textContent = u.unit_title || u.unit_id;
        if (u.unit_id === AppState.selectedUnitId) {
          opt.selected = true;
          matchFound = true;
        }
        container.appendChild(opt);
      });
    };

    if (midUnits.length > 0 && extUnits.length > 0) {
      const grpMid = document.createElement('optgroup');
      grpMid.label = '🔥 本次期中考必考單元';
      appendUnitOptions(grpMid, midUnits);
      unitSelect.appendChild(grpMid);

      const grpExt = document.createElement('optgroup');
      grpExt.label = '📖 其他延伸單元';
      appendUnitOptions(grpExt, extUnits);
      unitSelect.appendChild(grpExt);
    } else {
      appendUnitOptions(unitSelect, bookUnits);
    }

    if (!matchFound) {
      const defaultUnit = midUnits.length > 0 ? midUnits[0] : bookUnits[0];
      AppState.selectedUnitId = defaultUnit.unit_id;
      unitSelect.value = AppState.selectedUnitId;
    }
  }

  function initNavigation() {
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const viewId = tab.dataset.view;
        if (viewId !== 'quiz') {
          AppState.isErrorBookRetry = false;
        }
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

    // 避免頂部舊版教材選單與「期中考衝刺專區 / 晨間體操 / 錯題本」的專屬選單打架
    const topSelectorZone = document.querySelector('.selector-zone');
    if (topSelectorZone) {
      const needsBookSelector = (viewId === 'study' || viewId === 'quiz' || viewId === 'print');
      topSelectorZone.style.display = needsBookSelector ? 'flex' : 'none';
    }

    // 特殊視圖切換動作
    if (viewId === 'midterm') {
      renderMidtermSprint();
    } else if (viewId === 'study') {
      renderCurrentUnit();
    } else if (viewId === 'quiz') {
      if (!AppState.isErrorBookRetry) {
        loadQuizForCurrentUnit();
      } else {
        renderQuizCard();
        renderQuizDotsNav();
      }
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

    // 切換必考長句與考點標註
    const toggleKeyAnnotations = document.getElementById('toggleKeyAnnotations');
    if (toggleKeyAnnotations) {
      toggleKeyAnnotations.addEventListener('change', () => {
        renderReadingSection();
      });
    }

    // 課文單字 7 大錨點彈出小卡 Modal 關閉事件
    const vocabModal = document.getElementById('vocabPopoverModal');
    const closeVocabModalBtn = document.getElementById('closeVocabPopoverBtn');
    if (closeVocabModalBtn && vocabModal) {
      closeVocabModalBtn.addEventListener('click', () => {
        vocabModal.classList.remove('active');
      });
    }
    if (vocabModal) {
      vocabModal.addEventListener('click', (e) => {
        if (e.target === vocabModal) vocabModal.classList.remove('active');
      });
    }
  }

  function openVocabPopoverModal(item) {
    const modal = document.getElementById('vocabPopoverModal');
    const content = document.getElementById('vocabPopoverContent');
    if (!modal || !content || !item) return;

    content.innerHTML = `
      <div class="vocab-popover-header">
        <div>
          <span class="vocab-popover-word">${escapeHtml(item.word)}</span>
          ${item.pos ? `<span class="card-pos-tag" style="margin-left:0.5rem;">${escapeHtml(item.pos)}</span>` : ''}
        </div>
        <button type="button" class="btn-pronounce" id="popoverSpeakWordBtn" title="發音">
          <span>🔊</span>
        </button>
      </div>
      <div class="vocab-popover-meaning">${escapeHtml(item.chi)}</div>
      <div class="anchor-section" style="display:flex;">
        ${item.breakdown ? `<div class="anchor-item"><span class="anchor-badge badge-break">字根拆解</span><span class="anchor-text">${escapeHtml(item.breakdown)}</span></div>` : ''}
        ${item.trick ? `<div class="anchor-item"><span class="anchor-badge badge-trick">諧音聯想</span><span class="anchor-text">${escapeHtml(item.trick)}</span></div>` : ''}
        ${item.scene ? `<div class="anchor-item"><span class="anchor-badge badge-scene">情境畫面</span><span class="anchor-text">${escapeHtml(item.scene)}</span></div>` : ''}
        ${item.collocation ? `<div class="anchor-item"><span class="anchor-badge badge-colloc">搭配用法</span><span class="anchor-text">${escapeHtml(item.collocation)}</span></div>` : ''}
        ${item.chant ? `<div class="anchor-item"><span class="anchor-badge badge-chant">記憶口訣</span><span class="anchor-text">${escapeHtml(item.chant)}</span></div>` : ''}
        ${item.compare ? `<div class="anchor-item"><span class="anchor-badge badge-compare">易混比較</span><span class="anchor-text">${escapeHtml(item.compare)}</span></div>` : ''}
      </div>
      ${item.context_eng ? `
        <div class="card-example" style="margin-top:0.85rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem;">
            <div class="example-eng">${escapeHtml(item.context_eng)}</div>
            <button type="button" class="btn-secondary" id="popoverSpeakSentenceBtn" style="padding:0.25rem 0.6rem; font-size:0.78rem; flex-shrink:0;">🔊 讀例句</button>
          </div>
          ${item.context_chi ? `<div class="example-chi">${escapeHtml(item.context_chi)}</div>` : ''}
        </div>
      ` : ''}
    `;

    const speakBtn = document.getElementById('popoverSpeakWordBtn');
    if (speakBtn) {
      speakBtn.addEventListener('click', () => speakWord(item.word));
    }
    const speakSentBtn = document.getElementById('popoverSpeakSentenceBtn');
    if (speakSentBtn) {
      speakSentBtn.addEventListener('click', () => speakWord(item.context_eng));
    }

    modal.classList.add('active');
    speakWord(item.word);
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

  function buildInteractiveReadingHtml(engText, keySentences, unitVocabs, showKeyAnnotations) {
    if (!engText) return '';

    // 準備單字匹配字典 (依字長由長到短排序，避免短字搶先匹配)
    const vocabMatchers = [];
    unitVocabs.forEach((v, vIdx) => {
      const base = (v.word || '').trim();
      if (!base || base.length < 3) return;
      const cleanBase = base.replace(/\s*\(.*?\)\s*/g, '').trim();
      if (!cleanBase) return;
      const escaped = cleanBase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      // 支援常見字尾變化 (-s, -es, -ed, -d, -ing, -er, -est, y->ies/ied)
      let patternStr = `\\b(${escaped}(?:s|es|ed|d|ing|er|est)?)\\b`;
      if (cleanBase.endsWith('y') && cleanBase.length > 3) {
        const stemY = cleanBase.slice(0, -1).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        patternStr = `\\b(${escaped}(?:s|ed|ing)?|${stemY}(?:ies|ied|ier|iest))\\b`;
      } else if (cleanBase.endsWith('e') && cleanBase.length > 3) {
        const stemE = cleanBase.slice(0, -1).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        patternStr = `\\b(${escaped}(?:s|d|r|st)?|${stemE}(?:ing|ed))\\b`;
      }
      vocabMatchers.push({
        vIdx,
        wordLen: cleanBase.length,
        regex: new RegExp(patternStr, 'gi')
      });
    });
    vocabMatchers.sort((a, b) => b.wordLen - a.wordLen);

    // 將一段純文字加上單字互動標記 (安全處理 HTML 跳脫與佔位符)
    function highlightVocabTokensInPlainSegment(segmentText) {
      if (!segmentText) return '';
      const placeholders = [];
      let workText = segmentText;

      vocabMatchers.forEach(matcher => {
        workText = workText.replace(matcher.regex, (match) => {
          // 避免替換到已經成為佔位符的內容
          if (match.includes('@@VOCAB_')) return match;
          const tokenIdx = placeholders.length;
          placeholders.push({ matchedText: match, vIdx: matcher.vIdx });
          return `@@VOCAB_${tokenIdx}@@`;
        });
      });

      let escapedHtml = escapeHtml(workText);
      escapedHtml = escapedHtml.replace(/@@VOCAB_(\d+)@@/g, (_, idxStr) => {
        const info = placeholders[parseInt(idxStr, 10)];
        if (!info) return '';
        return `<span class="reading-vocab-token" data-vidx="${info.vIdx}" title="點擊發音並查看 7 大記憶錨點小卡">${escapeHtml(info.matchedText)}</span>`;
      });
      return escapedHtml;
    }

    // 如果開啟必考長句高亮且該段有 key_sentences
    if (showKeyAnnotations && Array.isArray(keySentences) && keySentences.length > 0) {
      let remaining = engText;
      let resultHtml = '';
      // 依句子在段落中出現的位置排序切分
      const validKeys = keySentences
        .filter(ks => ks && ks.text && remaining.includes(ks.text))
        .sort((a, b) => remaining.indexOf(a.text) - remaining.indexOf(b.text));

      if (validKeys.length > 0) {
        let cursor = 0;
        validKeys.forEach(ks => {
          const pos = engText.indexOf(ks.text, cursor);
          if (pos === -1) return;
          const beforeText = engText.slice(cursor, pos);
          resultHtml += highlightVocabTokensInPlainSegment(beforeText);
          const innerHighlighted = highlightVocabTokensInPlainSegment(ks.text);
          resultHtml += `<span class="reading-key-sentence" title="${escapeHtml(ks.note || '必考重點句')}"><span class="key-star-badge">⭐ 必考句</span>${innerHighlighted}</span>`;
          cursor = pos + ks.text.length;
        });
        resultHtml += highlightVocabTokensInPlainSegment(engText.slice(cursor));
        return resultHtml;
      }
    }

    return highlightVocabTokensInPlainSegment(engText);
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

    // 取得本單元單字庫（若本單元為綜合考卷則合併期中考單字供點選）
    let unitVocabs = ENGLISH_DATA.vocabulary.filter(v => v.book_id === AppState.selectedBookId && v.unit_id === AppState.selectedUnitId);
    if (unitVocabs.length < 5) {
      unitVocabs = ENGLISH_DATA.vocabulary.filter(v => v.is_midterm);
    }

    const showChinese = document.getElementById('toggleChineseTranslation') ? document.getElementById('toggleChineseTranslation').checked : true;
    const showKeyAnnotations = document.getElementById('toggleKeyAnnotations') ? document.getElementById('toggleKeyAnnotations').checked : true;

    passages.forEach((p, idx) => {
      const card = document.createElement('div');
      card.className = 'reading-card';

      const interactiveEngHtml = buildInteractiveReadingHtml(p.eng, p.key_sentences, unitVocabs, showKeyAnnotations);

      let keyNotesHtml = '';
      if (showKeyAnnotations && Array.isArray(p.key_sentences) && p.key_sentences.length > 0) {
        keyNotesHtml = `
          <div class="reading-key-notes-box">
            ${p.key_sentences.map(ks => `
              <div class="reading-key-note-item">
                <span class="note-tag">🎯 段考考點解析</span>
                <span>${escapeHtml(ks.note)}</span>
              </div>
            `).join('')}
          </div>
        `;
      }

      card.innerHTML = `
        <div class="reading-card-top">
          <div style="display:flex; align-items:center; gap:0.65rem; flex-wrap:wrap;">
            <span class="reading-seq">Paragraph ${p.sequence || (idx + 1)}</span>
            ${p.section_title ? `<span class="reading-section-badge">📌 ${escapeHtml(p.section_title)}</span>` : ''}
          </div>
          <button class="btn-pronounce" title="朗讀此段落">
            <span>🔊</span>
          </button>
        </div>
        <div class="reading-eng">${interactiveEngHtml}</div>
        ${p.chi ? `<div class="reading-chi" style="display:${showChinese ? 'block' : 'none'};">${escapeHtml(p.chi)}</div>` : ''}
        ${keyNotesHtml}
      `;

      card.querySelector('.btn-pronounce').addEventListener('click', () => {
        speakWord(p.eng);
      });

      // 綁定課文內高亮單字點擊事件 -> 發音 + 彈出 7 大錨點單字小卡
      card.querySelectorAll('.reading-vocab-token').forEach(tok => {
        tok.addEventListener('click', (e) => {
          e.stopPropagation();
          const vIdx = parseInt(tok.dataset.vidx, 10);
          const vocabItem = unitVocabs[vIdx];
          if (vocabItem) {
            openVocabPopoverModal(vocabItem);
          }
        });
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

    // 題型分類篩選
    const catSelect = document.getElementById('quizCategorySelect');
    if (catSelect) {
      catSelect.addEventListener('change', (e) => {
        AppState.quizCategory = e.target.value;
        AppState.isErrorBookRetry = false;
        loadQuizForCurrentUnit();
      });
    }

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
    let questions = ENGLISH_DATA.quizzes.filter(q =>
      q.book_id === AppState.selectedBookId &&
      q.unit_id === AppState.selectedUnitId &&
      q.type !== 'brain_gym'
    );

    if (AppState.quizCategory && AppState.quizCategory !== 'all') {
      questions = questions.filter(q => (q.type || '').toLowerCase() === AppState.quizCategory);
    }
    
    AppState.quizQuestions = questions;
    AppState.quizIndex = 0;
    AppState.quizResults = {};

    renderQuizCard();
    renderQuizDotsNav();
  }

  function buildSmartOptionsForQuestion(q) {
    if (Array.isArray(q.options) && q.options.length >= 2) {
      return q.options;
    }
    // 當錯題本重測遇到原本是「點詞抓錯」或「長句改寫」無選項題時，智慧生成選項或自評按鈕
    const ans = String(q.answer || '').trim();
    if (!ans) return ['我已掌握正解', '還不太確定'];
    if (ans.length > 40 || ans.includes('➔')) {
      return [
        ans,
        '（紙筆寫錯 / 語序顛倒 — 點此記為再複習）'
      ];
    }
    const pool = ['more harder', 'do she', 'neither did I', 'will rain', 'most quickest', 'so did he', 'have lived'];
    const distractors = pool.filter(p => p.toLowerCase() !== ans.toLowerCase()).slice(0, 3);
    const merged = [ans, ...distractors];
    return merged;
  }

  function renderQuizCard() {
    const card = document.getElementById('quizCard');
    const progressText = document.getElementById('quizProgressText');
    const qTypeBadge = document.getElementById('quizTypeBadge');
    const expBox = document.getElementById('explanationBox');
    if (!card) return;

    if (expBox) expBox.classList.remove('active');

    if (AppState.quizQuestions.length === 0) {
      if (progressText) progressText.textContent = '0 / 0 題';
      if (qTypeBadge) qTypeBadge.textContent = 'NO QUESTIONS';
      const qStem = document.getElementById('qStem');
      if (qStem) qStem.textContent = '目前此分類下暫無題目，請將上方題型切換為「全部題型」或選擇其他單元。';
      const optionsContainer = document.getElementById('interactiveOptions');
      if (optionsContainer) optionsContainer.innerHTML = '';
      return;
    }

    if (AppState.quizIndex >= AppState.quizQuestions.length) {
      AppState.quizIndex = 0;
    }

    const q = AppState.quizQuestions[AppState.quizIndex];
    if (progressText) {
      const modePrefix = AppState.isErrorBookRetry ? '🔥 錯題消滅戰：' : '';
      progressText.textContent = `${modePrefix}第 ${AppState.quizIndex + 1} / ${AppState.quizQuestions.length} 題`;
    }
    const safeType = String(q.type || q.category_tag || 'comprehensive').toUpperCase();
    if (qTypeBadge) qTypeBadge.textContent = `${safeType} QUIZ`;

    const qDifficulty = document.getElementById('qDifficulty');
    const qStem = document.getElementById('qStem');
    if (qDifficulty) qDifficulty.textContent = q.difficulty || '★★★★☆';
    if (qStem) qStem.textContent = q.question;

    // 渲染 iPad 互動選項（自動補齊非選擇題的互動選項，確保 iPad 觸控軌不卡死）
    const optionsContainer = document.getElementById('interactiveOptions');
    if (optionsContainer) {
      optionsContainer.innerHTML = '';
      const opts = buildSmartOptionsForQuestion(q);
      opts.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = opt;
        btn.addEventListener('click', () => handleInteractiveOptionClick(opt, q, btn));
        optionsContainer.appendChild(btn);
      });
    }

    // 渲染詳解內容
    const expCorrectAns = document.getElementById('expCorrectAns');
    const expContent = document.getElementById('expContent');
    if (expCorrectAns) expCorrectAns.textContent = `正解：${q.answer}`;
    if (expContent) expContent.textContent = q.explanation || '請對照正解檢視時態、副詞三級變化與助動詞搭配。';

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
    const isCorrect = (String(selectedOpt).trim().toLowerCase() === String(question.answer).trim().toLowerCase());
    
    // 選項視覺反饋
    document.querySelectorAll('#interactiveOptions .option-btn').forEach(btn => {
      btn.classList.remove('selected-correct', 'selected-wrong');
      if (btn.textContent.trim().toLowerCase() === String(question.answer).trim().toLowerCase()) {
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
      btn.classList.toggle('active', Boolean(record && record.status === type));
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
    const tierBtns = document.querySelectorAll('#bgTierPills .bg-tier-btn');
    tierBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const tier = btn.dataset.tier || 'all';
        AppState.brainGymTier = tier;
        AppState.brainGymIndex = 0;
        tierBtns.forEach(b => b.classList.toggle('active', b.dataset.tier === tier));
        loadBrainGym();
      });
    });
  }

  function getFilteredBrainGymList() {
    if (!window.ENGLISH_DATA) return [];
    let list = ENGLISH_DATA.quizzes.filter(q => q.type === 'brain_gym');
    const tier = AppState.brainGymTier;
    if (tier === '1-3') {
      list = list.filter(q => (q.star || 1) >= 1 && (q.star || 1) <= 3);
    } else if (tier === '4-7') {
      list = list.filter(q => (q.star || 1) >= 4 && (q.star || 1) <= 7);
    } else if (tier === '8-10') {
      list = list.filter(q => (q.star || 1) >= 8 && (q.star || 1) <= 10);
    }
    return list;
  }

  function formatBrainGymDualExplanation(expText) {
    if (!expText) return '<div class="bg-exp-green">請熟記此核心句型與搭配詞。</div>';
    const greenIdx = expText.indexOf('🟢');
    const redIdx = expText.indexOf('🔴');
    if (greenIdx !== -1 && redIdx !== -1) {
      const greenPart = expText.slice(greenIdx, redIdx).trim();
      const redPart = expText.slice(redIdx).trim();
      return `
        <div class="bg-exp-green">${escapeHtml(greenPart)}</div>
        <div class="bg-exp-red">${escapeHtml(redPart)}</div>
      `;
    }
    return `<div class="bg-exp-green">${escapeHtml(expText)}</div>`;
  }

  function loadBrainGym() {
    const card = document.getElementById('braingymCard');
    if (!card || !window.ENGLISH_DATA) return;

    const bgList = getFilteredBrainGymList();
    if (bgList.length === 0) {
      card.innerHTML = '<div class="no-data-msg">目前此星級分類尚無題目。</div>';
      return;
    }

    const idx = AppState.brainGymIndex % bgList.length;
    const currentQ = bgList[idx];

    const comboBadge = document.getElementById('bgComboBadge');
    if (comboBadge) comboBadge.textContent = `🔥 連勝 Combo: ${AppState.brainGymCombo}`;
    const progBadge = document.getElementById('bgProgressBadge');
    if (progBadge) progBadge.textContent = `第 ${idx + 1} / ${bgList.length} 題`;

    card.innerHTML = `
      <div class="card-question-box">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
          <span style="font-weight:800; color:var(--accent-amber);">⚡ Level ${currentQ.star || 1}★ 六上期中考秒殺挑戰</span>
          <span class="q-difficulty">${currentQ.difficulty || '★★★★★'}</span>
        </div>
        <div class="q-stem" style="font-size:1.35rem; margin-top:0.5rem;">${escapeHtml(currentQ.question)}</div>
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
        <div class="exp-content">${formatBrainGymDualExplanation(currentQ.explanation)}</div>
        <div style="margin-top: 1.25rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem;">
          <button id="prevBgBtn" class="btn-secondary">
            <span>⬅️ 上一題</span>
          </button>
          <button id="nextBgBtn" class="btn-primary">
            <span>挑戰下一題 ⚡</span>
          </button>
        </div>
      </div>
    `;

    // 選項點選（含 Combo 計算與自動錯題本連動）
    let answered = false;
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
          if (!answered) {
            AppState.brainGymCombo = 0;
            logErrorQuestion(currentQ, 'wrong');
          }
        } else {
          if (!answered) {
            AppState.brainGymCombo++;
            removeErrorQuestion(currentQ.id);
          }
        }
        answered = true;

        if (comboBadge) comboBadge.textContent = `🔥 連勝 Combo: ${AppState.brainGymCombo}`;

        const expBox = document.getElementById('bgExpBox');
        if (expBox) expBox.classList.add('active');
      });
    });

    const prevBtn = document.getElementById('prevBgBtn');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        AppState.brainGymIndex = (AppState.brainGymIndex - 1 + bgList.length) % bgList.length;
        loadBrainGym();
      });
    }

    const nextBtn = document.getElementById('nextBgBtn');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        AppState.brainGymIndex = (AppState.brainGymIndex + 1) % bgList.length;
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

    // 一鍵匯入岱崙 (TEA 3C Quiz) 18 道真實考卷失分錯題
    const preloadTeaBtn = document.getElementById('preloadTeaErrorsBtn');
    if (preloadTeaBtn) {
      preloadTeaBtn.addEventListener('click', () => {
        const addedCount = preloadTeaRealExamErrors();
        renderErrorBook();
        const span = preloadTeaBtn.querySelector('span');
        if (span) {
          span.textContent = addedCount > 0
            ? `✅ 已匯入 ${addedCount} 道岱崙真實錯題！`
            : '⚡ 岱崙 18 道真實錯題已在錯題本中！';
          setTimeout(() => {
            span.textContent = '🔥 載入岱崙小考 18 道真實失分題';
          }, 2500);
        }
      });
    }

    // 印出專屬錯題 A4 重測卷
    const printErrBtn = document.getElementById('printErrorBookBtn');
    if (printErrBtn) {
      printErrBtn.addEventListener('click', () => {
        if (AppState.errors.length === 0) {
          alert('目前錯題本是空的！可先點擊「🔥 載入岱崙小考 18 道真實失分題」再列印專屬重測卷。');
          return;
        }
        const errRadio = document.querySelector('input[name="printType"][value="errorbook"]');
        if (errRadio) errRadio.checked = true;
        switchView('print');
      });
    }

    // 啟動錯題消滅戰
    const retryBtn = document.getElementById('retryErrorsBtn');
    if (retryBtn) {
      retryBtn.addEventListener('click', () => {
        if (AppState.errors.length === 0) {
          alert('太棒了！目前錯題本空空如也，沒有需要消滅的錯題！');
          return;
        }
        AppState.isErrorBookRetry = true;
        AppState.quizQuestions = AppState.errors.map(e => {
          const qData = e.questionData || {};
          return {
            ...qData,
            id: e.id || qData.id || `ERR_${Date.now()}`,
            book_id: e.book_id || qData.book_id || 'tea_midterm',
            unit_id: e.unit_id || qData.unit_id || 'tea_midterm_1',
            type: qData.type || 'error_retry'
          };
        });
        AppState.quizIndex = 0;
        AppState.quizResults = {};
        switchView('quiz');
      });
    }
  }

  function preloadTeaRealExamErrors() {
    let added = 0;
    // 從 ENGLISH_DATA 中抓取 tea_midterm_1 的核心考題與 MIDTERM_DATABASE 的 TEA_QUIZ_REVIEW 抓錯題
    if (window.ENGLISH_DATA) {
      const teaQuizzes = ENGLISH_DATA.quizzes.filter(q => q.book_id === 'tea_midterm');
      teaQuizzes.forEach(q => {
        if (!AppState.errors.some(e => e.id === q.id)) {
          AppState.errors.push({
            id: q.id,
            book_id: 'tea_midterm',
            unit_id: 'tea_midterm_1',
            status: 'wrong',
            lastAttempt: Date.now(),
            questionData: {
              ...q,
              book_id: 'tea_midterm',
              unit_id: 'tea_midterm_1',
              type: q.type || 'grammar'
            }
          });
          added++;
        }
      });
    }

    if (window.MIDTERM_DATABASE) {
      const teaUnit = window.MIDTERM_DATABASE.find(u => u.id === 'TEA_QUIZ_REVIEW');
      if (teaUnit && Array.isArray(teaUnit.mistake_buster)) {
        teaUnit.mistake_buster.forEach((item, idx) => {
          const errId = `TEA_MISTAKE_${idx + 1}`;
          if (!AppState.errors.some(e => e.id === errId)) {
            AppState.errors.push({
              id: errId,
              book_id: 'tea_midterm',
              unit_id: 'tea_midterm_1',
              status: 'wrong',
              lastAttempt: Date.now(),
              questionData: {
                id: errId,
                book_id: 'tea_midterm',
                unit_id: 'tea_midterm_1',
                type: 'grammar',
                question: `【岱崙真實考卷改錯】找出句中錯誤並訂正：${item.sentence}`,
                options: [
                  `${item.wrong_word} ➔ ${item.correct_word}`,
                  `${item.correct_word} ➔ ${item.wrong_word}`,
                  '全句無語法錯誤'
                ],
                answer: `${item.wrong_word} ➔ ${item.correct_word}`,
                explanation: `${item.reason}（正確完整句：${item.fixed_sentence}）`
              }
            });
            added++;
          }
        });
      }
    }

    if (added > 0) {
      saveErrorBook();
    }
    return added;
  }

  function logErrorQuestion(question, status) {
    if (!question) return;
    const qId = question.id || `ERR_${Date.now()}`;
    const bookId = question.book_id || AppState.selectedBookId || 'gra3';
    const unitId = question.unit_id || AppState.selectedUnitId || 'gra3_13';

    const existingIdx = AppState.errors.findIndex(e => e.id === qId);
    const record = {
      id: qId,
      book_id: bookId,
      unit_id: unitId,
      status: status, // 'wrong' or 'hesitant'
      lastAttempt: Date.now(),
      questionData: {
        ...question,
        id: qId,
        book_id: bookId,
        unit_id: unitId,
        type: question.type || 'grammar'
      }
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

    // 填充錯題課本篩選選單（包含所有課本與歷史考卷）
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
      filtered = filtered.filter(e => {
        const bId = e.book_id || (e.questionData && e.questionData.book_id) || '';
        return bId === selectedBook || bId.toLowerCase().includes(selectedBook.toLowerCase());
      });
    }
    if (selectedStatus !== 'all') {
      filtered = filtered.filter(e => e.status === selectedStatus);
    }

    list.innerHTML = '';
    if (filtered.length === 0) {
      list.innerHTML = '<div class="no-data-msg" style="padding: 2.5rem; text-align: center;">🎉 目前沒有符合篩選條件的錯題！可點擊右上方「🔥 載入岱崙 W2~W7 真實失分題」進行考前弱點特訓！</div>';
      return;
    }

    filtered.forEach(item => {
      const q = item.questionData || {};
      const safeBookLabel = String(item.book_id || q.book_id || 'MIDTERM').toUpperCase();
      const safeUnitLabel = String(item.unit_id || q.unit_id || '');
      const card = document.createElement('div');
      card.className = 'error-item-card';
      card.innerHTML = `
        <div class="error-left-col">
          <div style="display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
            <span class="error-status-tag ${item.status === 'wrong' ? 'status-wrong' : 'status-hesitant'}">
              ${item.status === 'wrong' ? '❌ 算錯 / 答錯' : '⏳ 猶豫 / 想很久'}
            </span>
            <span style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">${escapeHtml(safeBookLabel)} ｜ ${escapeHtml(safeUnitLabel)}</span>
          </div>
          <div class="error-q-stem">${escapeHtml(q.question || '')}</div>
          <div class="error-ans-row">正確答案：${escapeHtml(q.answer || '')}</div>
          <div style="font-size:0.88rem; color:var(--text-secondary); line-height:1.5;">${escapeHtml(q.explanation || '')}</div>
        </div>
        <div>
          <button class="btn-secondary btn-remove-err" data-id="${escapeHtml(item.id)}" title="已掌握，移出錯題本">
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

    let bookName = book ? book.book_name : '英語教材';
    let unitTitle = unit ? (unit.unit_title || unit.unit_id) : '單元評量';
    let subHeaderDesc = '';

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

    if (printType === 'errorbook') {
      bookName = '📕 終身錯題本 — 個人化弱點消滅重測卷';
      unitTitle = '六上期中考精準掃盲特訓';
      const errList = AppState.errors.slice(0, count);
      subHeaderDesc = `錯題重測專卷 ｜ 總題數：${errList.length} 題 ${isTeacher ? '（教師 / 家長詳解版）' : '（學生實戰作答版）'}`;

      if (errList.length === 0) {
        questionsHtml = `<div style="padding:2rem; text-align:center; color:#6B7280;">目前錯題本尚無題目，請先至「📕 錯題本」載入岱崙小考錯題或進行測驗。</div>`;
      } else {
        questionsHtml = `
          <div class="sheet-questions-grid">
            ${errList.map((e, i) => {
              const q = e.questionData || {};
              return `
                <div class="sheet-q-item">
                  <div class="sheet-q-stem">
                    <strong>${i + 1}.</strong> <span style="font-size:8.5pt; color:#4F46E5;">[${escapeHtml(String(e.book_id || '').toUpperCase())}]</span> ${escapeHtml(q.question || '')}
                  </div>
                  ${Array.isArray(q.options) && q.options.length > 0 ? `
                    <div class="sheet-options-row">
                      ${q.options.map((opt, oi) => `<span>(${String.fromCharCode(65 + oi)}) ${escapeHtml(opt)}</span>`).join('')}
                    </div>
                  ` : ''}
                  ${isTeacher
                    ? `<div class="sheet-teacher-ans">正解：${escapeHtml(q.answer || '')} ｜ ${escapeHtml(q.explanation || '')}</div>`
                    : `<div style="height: 20px; border-bottom: 1px solid #9CA3AF; margin-top: 6px;"></div>`
                  }
                </div>
              `;
            }).join('')}
          </div>
        `;
      }
    } else if (printType === 'spelling') {
      // Spelling Bee 單字聽寫卷
      const vocabs = ENGLISH_DATA.vocabulary.filter(v => v.book_id === AppState.selectedBookId && v.unit_id === AppState.selectedUnitId).slice(0, count);
      subHeaderDesc = `Spelling Bee 實體單字聽寫卷 ｜ 總題數：${vocabs.length} 題 ${isTeacher ? '（教師 / 家長解答版）' : ''}`;
      
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
      subHeaderDesc = `Grammar & Usage 文法診斷卷 ｜ 總題數：${qList.length} 題 ${isTeacher ? '（教師 / 家長解答版）' : ''}`;

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
          <p>${escapeHtml(subHeaderDesc)}</p>
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
    const errorSample = AppState.errors.slice(0, 8).map((e, i) => {
      const q = e.questionData || {};
      const bLabel = String(e.book_id || q.book_id || 'MIDTERM').toUpperCase();
      const uLabel = String(e.unit_id || q.unit_id || '');
      return `【錯題 ${i + 1}】(${bLabel} ${uLabel})\n題目：${q.question || ''}\n正解：${q.answer || ''}\n學生狀態：${e.status === 'wrong' ? '算錯/選錯' : '猶豫想很久'}\n詳解筆記：${q.explanation || '無'}`;
    }).join('\n\n');

    return `你是一位頂尖的小學六年級英語教研出題專家。
以下是一位 12 歲國小六年級學生在準備六上期中考（範圍涵蓋副詞三級比較、So/Neither 倒裝附和、未來式 will/going to、條件句與長篇閱讀）時遇到的錯題與盲點紀錄：

${errorSample}

請為這位學生執行「精準錯題消滅與自適應補強出題」：
1. 深入剖析學生在以上題目中的核心文法盲點（如副詞比較級與最高級混用、助動詞與時態脫鉤、動詞三態變化、介系詞搭配失誤）。
2. 針對上述每個錯題觀念，量身生成 2~3 題「相同語法觀念、不同日常生活情境」的深度變式題（包含選擇題與仿照岱崙小考的長句改寫題，並附上標註正解與詳細防坑破題思路）。
3. 難度對標校內名校段考滿分與全民英檢（GEPT 初級~中級）水準，請用繁體中文輸出。`;
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
        syncTopbarFromMidtermId(AppState.selectedMidtermUnitId);
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
        const unit = getSelectedMidtermUnit();
        if (!unit || !unit.mistake_buster) return;
        const item = unit.mistake_buster[AppState.currentMistakeIdx];
        const errId = `MISTAKE_${unit.id}_${AppState.currentMistakeIdx + 1}`;
        AppState.midtermMistakeStatus[errId] = 'correct';
        // 若先前曾加入錯題本，答對後自動從錯題本移除
        const prevLen = AppState.errors.length;
        AppState.errors = AppState.errors.filter(e => e.id !== errId);
        if (AppState.errors.length !== prevLen) saveErrorBook();

        const span = selfCorrectBtn.querySelector('span');
        if (span) span.textContent = '🎉 太棒了！已標記過關！';
        setTimeout(() => {
          if (span) span.textContent = '👍 我在紙上改對了';
          if (AppState.currentMistakeIdx < unit.mistake_buster.length - 1) {
            AppState.currentMistakeIdx++;
          }
          renderMistakeBuster();
        }, 450);
      });
    }

    const selfWrongBtn = document.getElementById('mistakeSelfWrongBtn');
    if (selfWrongBtn) {
      selfWrongBtn.addEventListener('click', () => {
        const unit = getSelectedMidtermUnit();
        if (unit && unit.mistake_buster) {
          const errId = `MISTAKE_${unit.id}_${AppState.currentMistakeIdx + 1}`;
          AppState.midtermMistakeStatus[errId] = 'wrong';
        }
        saveCurrentMistakeToErrors();
        const span = selfWrongBtn.querySelector('span');
        if (span) span.textContent = '📕 已收錄至錯題本！';
        setTimeout(() => {
          if (span) span.textContent = '❌ 我改錯了（加入錯題本）';
        }, 1200);
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
        const errId = `MISTAKE_${unit.id}_${i + 1}`;
        const st = AppState.midtermMistakeStatus[errId];
        const stClass = st === 'correct' ? 'dot-correct' : (st === 'wrong' ? 'dot-wrong' : '');
        dot.className = `mistake-dot ${i === AppState.currentMistakeIdx ? 'active' : ''} ${stClass}`.trim();
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
    const matchedEdUnit = window.ENGLISH_DATA ? window.ENGLISH_DATA.units.find(u => u.midterm_unit_id === unit.id) : null;
    const normBookId = matchedEdUnit ? matchedEdUnit.book_id : (unit.book || 'gra3');
    const normUnitId = matchedEdUnit ? matchedEdUnit.unit_id : (unit.display_title || unit.unit_title || unit.id);
    const errId = `MISTAKE_${unit.id}_${AppState.currentMistakeIdx + 1}`;

    const errObj = {
      id: errId,
      book_id: normBookId,
      unit_id: normUnitId,
      status: 'wrong',
      timestamp: Date.now(),
      questionData: {
        id: errId,
        book_id: normBookId,
        unit_id: normUnitId,
        type: 'grammar',
        question: `【點詞抓錯】${item.sentence}`,
        options: [
          `${item.wrong_word} ➔ ${item.correct_word}`,
          `${item.correct_word} ➔ ${item.wrong_word}`,
          '全句無語法錯誤'
        ],
        answer: `${item.wrong_word} ➔ ${item.correct_word}`,
        explanation: `${item.reason}（正確完整句：${item.fixed_sentence}）`
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
        const unit = getSelectedMidtermUnit();
        const quizzes = getFilteredMidtermQuizzes();
        if (!unit || quizzes.length === 0) return;
        const q = quizzes[AppState.currentMidtermQuizIdx];
        const qId = q.id || `QUIZ_${unit.id}_${AppState.currentMidtermQuizIdx + 1}`;
        AppState.midtermQuizStatus[qId] = 'correct';

        // 若先前在錯題本中，答對後自動消滅錯題
        const prevLen = AppState.errors.length;
        AppState.errors = AppState.errors.filter(e => e.id !== qId);
        if (AppState.errors.length !== prevLen) saveErrorBook();

        const span = correctBtn.querySelector('span');
        if (span) span.textContent = '🎉 答對過關！進入下一題...';
        setTimeout(() => {
          if (span) span.textContent = '👍 我寫對了 / 唸對了';
          if (AppState.currentMidtermQuizIdx < quizzes.length - 1) {
            AppState.currentMidtermQuizIdx++;
          }
          renderMidtermDualQuiz();
        }, 450);
      });
    }

    const wrongBtn = document.getElementById('midtermAnsWrongBtn');
    if (wrongBtn) {
      wrongBtn.addEventListener('click', () => {
        const unit = getSelectedMidtermUnit();
        const quizzes = getFilteredMidtermQuizzes();
        if (unit && quizzes.length > 0) {
          const q = quizzes[AppState.currentMidtermQuizIdx];
          const qId = q.id || `QUIZ_${unit.id}_${AppState.currentMidtermQuizIdx + 1}`;
          AppState.midtermQuizStatus[qId] = 'wrong';
        }
        saveCurrentQuizToErrors();
        const span = wrongBtn.querySelector('span');
        if (span) span.textContent = '📕 已收錄至【終身錯題本】！';
        setTimeout(() => {
          if (span) span.textContent = '❌ 寫錯 / 不熟（加入錯題本）';
        }, 1200);
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

    // 渲染選擇題選項區 (當 q.options 存在且非空時顯示選項按鈕，支援紙筆對照與直接點擊作答)
    const optionsBox = document.getElementById('midtermQuizOptions');
    if (optionsBox) {
      if (Array.isArray(q.options) && q.options.length > 0) {
        optionsBox.style.display = 'grid';
        optionsBox.innerHTML = '';
        const letters = ['A', 'B', 'C', 'D', 'E'];
        q.options.forEach((optText, idx) => {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'midterm-option-btn';
          btn.innerHTML = `<span class="opt-letter">${letters[idx] || idx + 1}</span><span class="opt-text">${escapeHtml(optText)}</span>`;
          btn.addEventListener('click', () => {
            const isCorrect = (optText.trim().toLowerCase() === String(q.answer).trim().toLowerCase());
            optionsBox.querySelectorAll('.midterm-option-btn').forEach((b, bIdx) => {
              const bText = q.options[bIdx] || '';
              if (bText.trim().toLowerCase() === String(q.answer).trim().toLowerCase()) {
                b.classList.add('opt-correct');
              } else if (b === btn && !isCorrect) {
                b.classList.add('opt-wrong');
              }
            });
            const qId = q.id || `QUIZ_${unit.id}_${AppState.currentMidtermQuizIdx + 1}`;
            AppState.midtermQuizStatus[qId] = isCorrect ? 'correct' : 'wrong';
            if (!isCorrect) {
              saveCurrentQuizToErrors();
            }
            if (drawer) drawer.style.display = 'block';
          });
          optionsBox.appendChild(btn);
        });
      } else {
        optionsBox.style.display = 'none';
        optionsBox.innerHTML = '';
      }
    }

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
        const qItem = quizzes[i];
        const qId = qItem ? (qItem.id || `QUIZ_${unit.id}_${i + 1}`) : '';
        const st = AppState.midtermQuizStatus[qId];
        const stClass = st === 'correct' ? 'dot-correct' : (st === 'wrong' ? 'dot-wrong' : '');
        dot.className = `mistake-dot ${i === AppState.currentMidtermQuizIdx ? 'active' : ''} ${stClass}`.trim();
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
    const matchedEdUnit = window.ENGLISH_DATA ? window.ENGLISH_DATA.units.find(u => u.midterm_unit_id === unit.id) : null;
    const normBookId = matchedEdUnit ? matchedEdUnit.book_id : (unit.book || 'gra3');
    const normUnitId = matchedEdUnit ? matchedEdUnit.unit_id : (unit.display_title || unit.unit_title || unit.id);
    const errId = q.id || `QUIZ_${unit.id}_${AppState.currentMidtermQuizIdx + 1}`;

    const expText = typeof q.explanation === 'object' && q.explanation !== null
      ? `【考點】${q.explanation.concept}\n【破題】${q.explanation.formula}\n【陷阱】${q.explanation.trap}`
      : (q.explanation || q.hint);

    const errObj = {
      id: errId,
      book_id: normBookId,
      unit_id: normUnitId,
      status: 'wrong',
      timestamp: Date.now(),
      questionData: {
        id: errId,
        book_id: normBookId,
        unit_id: normUnitId,
        type: q.type || 'grammar',
        options: Array.isArray(q.options) ? q.options : [],
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
      const uTitle = u.display_title || u.unit_title || u.id;
      (u.vocab || []).forEach(v => allVocab.push({ ...v, unit_title: uTitle }));
      (u.mistake_buster || []).forEach(m => allMistakes.push({ ...m, unit_title: uTitle }));
      (u.quizzes || []).forEach(q => {
        if (q.type === 'paper_rewrite') allRewrites.push({ ...q, unit_title: uTitle });
        else if (q.type !== 'spelling_listen') allQuizzes.push({ ...q, unit_title: uTitle });
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
        let optsLine = '';
        if (Array.isArray(q.options) && q.options.length > 0) {
          const letters = ['A', 'B', 'C', 'D'];
          optsLine = `<div style="margin-top:4px; margin-left:18px; color:#374151; font-size:9.5pt;">` +
            q.options.map((o, oi) => `(${letters[oi] || oi + 1}) ${escapeHtml(o)}`).join('&nbsp;&nbsp;&nbsp;&nbsp;') +
            `</div>`;
        }
        html += `
          <div class="print-q-item" style="margin-bottom:10px;">
            <span class="q-num">${idx + 1}.</span>
            <span class="q-text">${escapeHtml(q.question)} ${ansLine}</span>
            ${optsLine}
          </div>
        `;
      });
      html += `</div></div>`;
    }

    sheet.innerHTML = html;
  }

  function renderQuizOriginalExam(sheet, isTeacher, isContrast, today) {
    const title = '國小六年級 岱崙美語 3C Quiz 歷史真題 1:1 復原評量卷 (Week 2 / 4 / 5 / 6 / 7)';
    
    let html = `
      <div class="exam-header">
        <div class="exam-header-left">
          <div class="exam-grade-badge">岱崙美語 3C Quiz ｜ 歷史真實小考 1:1 復原重測</div>
          <h1 class="exam-title">${escapeHtml(title)}</h1>
          <div class="exam-meta-row">
            <span>出卷來源：Week 2, 4, 5, 6, 7 歷史真卷全收錄</span>
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

    // 考券 Part I: Spelling 單字聽寫 (Week 2, 4, 6 真實失分單字 20 題全收錄)
    const spellingItems = [
      { num: 1, zh: "楔子 (三角木) [W2]", ans: "wedge", student: "wadge", correct: false, note: "誤寫為 wadge，注意短母音 e" },
      { num: 2, zh: "小刀 [W2]", ans: "knife", student: "Knif", correct: false, note: "首字母誤大寫且漏字尾 e" },
      { num: 3, zh: "山脈 [W2]", ans: "mountain", student: "mountion", correct: false, note: "誤寫為 mountion，字尾為 -tain" },
      { num: 4, zh: "輪椅 [W2]", ans: "wheelchair", student: "whillchair", correct: false, note: "誤寫為 whillchair，輪子為 wheel" },
      { num: 5, zh: "熔爐 [W4]", ans: "furnace", student: "furnes", correct: false, note: "誤拼為 furnes，字尾為 -ace" },
      { num: 6, zh: "眼鏡鏡框 [W4]", ans: "frames", student: "France", correct: false, note: "誤寫成法國 France" },
      { num: 7, zh: "在...前面 [W4]", ans: "in front of", student: "infront off", correct: false, note: "三字需分開且介系詞為單 f 的 of" },
      { num: 8, zh: "花蜜 [W6]", ans: "nectar", student: "nector", correct: false, note: "誤拼為 nector，字尾為 -tar" },
      { num: 9, zh: "花瓣 [W6]", ans: "petals", student: "patels", correct: false, note: "母音顛倒誤拼為 patels" },
      { num: 10, zh: "墨西哥人/的 [W6]", ans: "Mexican", student: "Maxican", correct: false, note: "誤拼為 Maxican，開頭為 Mex-" },
      { num: 11, zh: "語言 [W6]", ans: "language", student: "langauges", correct: false, note: "ua 顛倒為 au 且誤加 s" },
      { num: 12, zh: "官方的 [W6]", ans: "official", student: "offical", correct: false, note: "c 後面漏寫 i (-cial)" },
      { num: 13, zh: "政府 [W6]", ans: "government", student: "goverment", correct: false, note: "漏寫中間的 n (govern + ment)" },
      { num: 14, zh: "法語 [W6]", ans: "French", student: "franch", correct: false, note: "忘記大寫 F 且把 e 寫成 a" },
      { num: 15, zh: "國家 (複數) [W6]", ans: "countries", student: "contries", correct: false, note: "漏寫 o 後面的 u (count + ries)" },
      { num: 16, zh: "例子 [W6]", ans: "example", student: "exemple", correct: false, note: "誤把 a 寫成 e" },
      { num: 17, zh: "華語/普通話 [W6]", ans: "Mandarin", student: "manderin", correct: false, note: "忘記大寫 M 且把 da 寫成 de" },
      { num: 18, zh: "千 (1,000) [W6]", ans: "thousand", student: "thoudnd", correct: false, note: "字尾應為沙子 sand (thou+sand)" },
      { num: 19, zh: "事實上 [W6]", ans: "in fact", student: "infecte", correct: false, note: "兩字須分開，誤拼成感染 infecte" },
      { num: 20, zh: "七片麵包 [W7]", ans: "seven slices of bread", student: "seven packet of breads", correct: false, note: "量詞用 slices，bread 不可數不加 s" }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">Part I. Spelling Bee & Measure Words 考場真實錯字重測 (每題 1 分，共 20 分)</div>
        <div class="exam-questions-grid" style="grid-template-columns: 1fr 1fr; display: grid; gap: 6px 20px;">
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
        <div class="print-q-item" style="font-size:10pt; margin-bottom:3px;">
          <span class="q-num">${sp.num}.</span>
          <span class="q-text">${sp.zh} ➔ ${ansDisplay}</span>
        </div>
      `;
    });
    html += `</div></div>`;

    // 考券 Part II: Grammar 3 (Unit 13) 倒裝附和句改寫 (Week 2 & Week 7 真題全收錄)
    const grammar13Items = [
      {
        q: "[W2] Ryan, Michael - 95% on quiz / too",
        ans: "Ryan got 95% on his quiz, and Michael did, too.",
        student: "Ryan 95% on quiz, Michael are too",
        redNote: "補動詞 got，刪 are too 改 did, too",
        reason: "肯定附和句：前面有一般動詞 got，後面用助動詞 did + too"
      },
      {
        q: "[W2] Olivia, Penny - 100% on quiz / so",
        ans: "Olivia got 100% on her quiz, and so did Penny.",
        student: "Olivia 100% on her quiz, 100% did Penny",
        redNote: "補動詞 got，改為 and so did Penny",
        reason: "倒裝附和句公式：so + 助動詞 (did) + 主詞 (Penny)"
      },
      {
        q: "[W2] Ray, Jim - not pass quiz / either",
        ans: "Ray didn't pass the quiz, and Jim didn't, either.",
        student: "Ray are not pass quiz, and Jim are either.",
        redNote: "劃掉 are not pass 改 didn't pass，後句改 Jim didn't, either",
        reason: "過去式否定句必須使用助動詞 didn't + 原形動詞 pass"
      },
      {
        q: "[W7] Roger, Sean – see new Iron Man movie tomorrow / so",
        ans: "Roger will see the new Iron Man movie tomorrow, and so will Sean.",
        student: "Roger see the new Iron Man movie tomorrow, so do Sean.",
        redNote: "tomorrow 為未來式，補 will see，倒裝改為 so will Sean",
        reason: "看到未來時間 tomorrow 必須使用助動詞 will，倒裝對齊用 so will + 主詞"
      },
      {
        q: "[W7] Rachel, Nicole – not learn to play the piano / either",
        ans: "Rachel doesn't learn to play the piano, and Nicole doesn't, either.",
        student: "Rachel do not learn to play the piano, Nicole do not learn to play the piano, either.",
        redNote: "單數主詞 Rachel / Nicole 否定助動詞必須用 doesn't (does not)",
        reason: "第三人稱單數現在式否定必用 doesn't，不可用 do not"
      },
      {
        q: "[W7] penguins, ostriches – can't fly / neither",
        ans: "Penguins can't fly, and neither can ostriches.",
        student: "Penguins can't fly, neither do ostriches.",
        redNote: "前句為情態助動詞 can't，倒裝必須對齊用 neither can ostriches",
        reason: "前句使用情態助動詞 can't，否定倒裝必須鏡像沿用 can，不可換成 do"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">Part II. Grammar 3 (U13) 倒裝附和句長句改寫 (W2 & W7 真題，每題 4 分，共 24 分)</div>
        <div class="exam-questions-grid">
    `;
    grammar13Items.forEach((g, idx) => {
      let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:22px; margin-top:4px;"></div>`;
      if (isTeacher) {
        ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：${escapeHtml(g.ans)}</div>`;
      } else if (isContrast) {
        ansLine = `
          <div class="contrast-box">
            <div>學生考場手寫：<span class="contrast-pencil">${escapeHtml(g.student)}</span> ❌</div>
            <div>老師紅筆批註：<span class="contrast-redpen">${escapeHtml(g.ans)}</span> <small>(${escapeHtml(g.redNote)})</small></div>
            <span class="contrast-explanation">💡 語法盲點剖析：${escapeHtml(g.reason)}</span>
          </div>
        `;
      }
      html += `
        <div class="print-q-item" style="margin-bottom:8px;">
          <span class="q-num">${idx + 1}.</span>
          <span class="q-text">Prompt: <strong>${escapeHtml(g.q)}</strong></span>
          ${ansLine}
        </div>
      `;
    });
    html += `</div></div>`;

    // 考券 Part III: Grammar 3 (Unit 14) 副詞三級比較長句合成 (Week 4, 5, 7 真題全收錄)
    const grammar14Items = [
      {
        q: "[W4] How fast do they run? (person, dog & lion)",
        ans: "A person runs fast, a dog runs faster than a person, but a lion runs the fastest.",
        student: "A person runs fast, a dog runs more faster than a dog, but a lion runs fastest.",
        redNote: "刪 more；than 後改 a person；fastest 前補 the",
        reason: "單音節副詞 fast 直接加 -er/-est 不可加 more；than 後接第一主詞；最高級必加 the"
      },
      {
        q: "[W5] How far can they jump? (frog, rabbit & kangaroo)",
        ans: "A frog can jump far, a rabbit can jump farther than a frog, but a kangaroo can jump the farthest.",
        student: "A frog can jump far, a rabbit can jump more farther than a frog, but a kangaroo can jump farthest.",
        redNote: "刪多餘的 more；最高級 farthest 前方補定冠詞 the",
        reason: "far 比較級 farther 已是比較級不可加 more；最高級 the farthest 必加 the"
      },
      {
        q: "[W5] How horribly do they laugh? (clown, ghost & witch)",
        ans: "A clown laughs horribly, a ghost laughs more horribly than a clown, but a witch laughs the most horribly.",
        student: "A clown laugh horribly, a ghost laugh more horribly than a clown, but a witch laugh the most horribly.",
        redNote: "三個單數主詞後的動詞 laugh 皆須補上第三人稱單數 -s (laughs)",
        reason: "題幹問 do they laugh，拆為單數主詞 A clown / A ghost / A witch 時動詞必加 -s"
      },
      {
        q: "[W7] How beautifully do they sing? (Beth, Vicky & Anne)",
        ans: "Beth sings beautifully, Vicky sings more beautifully than Beth, but Anne sings the most beautifully.",
        student: "Beth sings beautifully, Vicky sings more beautifully than Beth, but Anne is the most beautifully.",
        redNote: "把最後子句的 is 劃掉，改回一般動詞 sings",
        reason: "最高級副詞 the most beautifully 修飾動作唱歌，不可把動作動詞 sings 換成 be 動詞 is"
      },
      {
        q: "[W7] How well did they do their homework? (Hana, Ingrid & Jeremy)",
        ans: "Hana did her homework well, Ingrid did her homework better than Hana, but Jeremy did his homework the best.",
        student: "Hana did her homework well, Ingrid did will than Hana, but Jeremy do the best.",
        redNote: "will 改為不規則比較級 better；do 改為過去式 did",
        reason: "well 的比較級是 better（不是 will），且過去式問句 did they do 動詞須維持過去式 did"
      },
      {
        q: "[W7] How easily can you learn: Chinese, science & maths? (請依 makkelijk 程度排序)",
        ans: "I can learn maths easily, I can learn science more easily than maths, but I can learn Chinese the most easily.",
        student: "Maths is easily, science is easilier than maths, but Chinese is the easiliest.",
        redNote: "補出主詞動詞 I can learn；副詞比較級/最高級改為 more easily / the most easily",
        reason: "easily 是副詞修飾 learn，不可省略 I can learn 且不可自創 easilier / easiliest"
      },
      {
        q: "[W7] How badly do they play the electric guitar? (Fred, Ted & Bill)",
        ans: "Fred plays the electric guitar badly, Ted plays the electric guitar worse than Fred, but Bill plays the electric guitar the worst.",
        student: "Fred plays the electric guitar badly, Ted plays the electric guitar more badly than Fred, but Bill play the most badly.",
        redNote: "more badly 改 worse；Bill play 補 s (plays)；the most badly 改 the worst",
        reason: "badly 為不規則變化：badly ➔ worse than ➔ the worst（不可加 more / most）"
      },
      {
        q: "[W7] How early did they get up? (1. Elizabeth 05:40, 2. Sarah 06:15 & 3. Joanne 07:05)",
        ans: "Joanne got up early, Sarah got up earlier than Joanne, but Elizabeth got up the earliest.",
        student: "Joanne got up early, Sarah got up earlier than Joanne, but Elizebeth is the earliest.",
        redNote: "把最後子句的 is 改為過去式動詞片語 got up（注意 Elizabeth 拼字）",
        reason: "第三子句主詞 Elizabeth 後必須保留過去式動作動詞 got up，不可用 is 取代"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">Part III. Grammar 3 (U14) 副詞三級長句合成 (W4, W5 & W7 真題，每題 4.5 分，共 36 分)</div>
        <div style="font-size:9.5pt; background:#F8FAFC; border:1px solid #CBD5E1; padding:6px 10px; border-radius:4px; margin-bottom:10px; color:#1E293B;">
          <div><strong>📌 副詞字庫 Adverbs</strong>：<code>[fast, far, horribly, beautifully, well, easily, badly, early]</code></div>
          <div><strong>📐 必寫三段公式 Sentence form</strong>：<code>&lt;adverb clause&gt; , + &lt;comparative clause&gt; , + but + &lt;superlative clause&gt; .</code>（最高級子句嚴禁把一般動詞換成 is！）</div>
        </div>
        <div class="exam-questions-grid">
    `;
    grammar14Items.forEach((g, idx) => {
      let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:22px; margin-top:4px;"></div>`;
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
        <div class="print-q-item" style="margin-bottom:10px;">
          <span class="q-num">${idx + 1}.</span>
          <span class="q-text">Prompt: <strong>${escapeHtml(g.q)}</strong></span>
          ${ansLine}
        </div>
      `;
    });
    html += `</div></div>`;

    // 考券 Part IV: Week 6 Write Right 3 (Unit 5) 14 錯字挑錯與 Week 5 RWW6 聽寫精華 (共 20 分)
    html += `
      <div class="exam-section">
        <div class="section-title-print">Part IV. Week 6《If I Had 3000 Dollars》14 處抓錯重測與 RWW6 課文填空 (共 20 分)</div>
        <div class="print-q-item" style="line-height:1.75; font-size:10pt; background:#F8FAFC; border:1px solid #E2E8F0; padding:12px; border-radius:6px;">
    `;
    const dictationText = isTeacher ? 
      `<strong>【W6 抓錯題滿分訂正完本】</strong>If I <strong style="color:#DC2626;">had</strong> 3000 dollars, I would do three things. First, I love sports, so I would go <strong style="color:#DC2626;">to</strong> a baseball game <strong style="color:#DC2626;">with</strong> my sister. Next, I would <strong style="color:#DC2626;">buy</strong> a new bike <strong style="color:#DC2626;">for</strong> my brother. His bike is very old, and he <strong style="color:#DC2626;">needs</strong> a new <strong style="color:#DC2626;">one</strong>. Finally, I would spend some money <strong style="color:#DC2626;">on</strong> myself. I would <strong style="color:#DC2626;">buy</strong> a new computer, a watch, and some video <strong style="color:#DC2626;">games</strong>. Those things would <strong style="color:#DC2626;">cost</strong> me about 1500 dollars. With <strong style="color:#DC2626;">the</strong> rest of the money, I would <strong style="color:#DC2626;">put</strong> it in the bank. Wouldn't it <strong style="color:#DC2626;">be</strong> great to have 3000 dollars?` :
      (isContrast ?
      `<strong>【W6 考場紅黑批改對照（得分 5/7）】</strong>If I <span class="contrast-redpen">had ✓</span> 3000 dollars, I would do three things. First, I love sports, so I would go <span class="contrast-redpen">[漏抓補 to ❌]</span> a baseball game <span class="contrast-redpen">with ✓</span> my sister. Next, I would <span class="contrast-redpen">buy ✓</span> a new bike <span class="contrast-redpen">for ✓</span> my brother. His bike is very old, and he <span class="contrast-redpen">needs ✓</span> a new <span class="contrast-redpen">one ✓</span>. Finally, I would spend some money <span class="contrast-redpen">on ✓</span> myself. I would <span class="contrast-redpen">[漏抓 by ➔ buy ❌]</span> a new computer, a watch, and some video <span class="contrast-redpen">games ✓</span>. Those things would <span class="contrast-redpen">cost ✓</span> me about 1500 dollars. With <span class="contrast-redpen">[漏抓補 the ❌]</span> rest of the money, I would <span class="contrast-redpen">put ✓</span> <span class="contrast-pencil">it 誤改為 you ❌</span> in the bank. Wouldn't it <span class="contrast-redpen">be ✓</span> great to have 3000 dollars?` :
      `<strong>請在下列短文中圈出 14 個錯誤並於上方訂正：</strong><br>If I <u>have</u> 3000 dollars, I would do three things. First, I love sports, so I would <u>go a baseball game</u> <u>to</u> my sister. Next, I would <u>bought</u> a new bike <u>to</u> my brother. His bike is very old, and he <u>need</u> a new <u>it</u>. Finally, I would spend some money <u>in</u> myself. I would <u>by</u> a new computer, a watch, and some video <u>game</u>. Those things would <u>spend</u> me about 1500 dollars. <u>With rest</u> of the money, I would <u>putted</u> it in the bank. Wouldn't <u>it great</u> to have 3000 dollars?`);

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

    // Part I: AI 變式倒裝附和句改寫 (6 題，每題 4 分 = 24 分)
    const variantG13 = [
      {
        prompt: "Leo, Max - 100% on test / so",
        ans: "Leo got 100% on his test, and so did Max.",
        hint: "陷阱防範：記得先補過去式動詞 got！肯定倒裝用 so + did + 主詞 Max"
      },
      {
        prompt: "Emma, Chloe - 95% on quiz / too",
        ans: "Emma got 95% on her quiz, and Chloe did, too.",
        hint: "陷阱防範：前句動詞是 got，後句附和必用 Chloe did, too（不可寫 are, too）"
      },
      {
        prompt: "Noah, Liam - not pass the exam / either",
        ans: "Noah didn't pass the exam, and Liam didn't, either.",
        hint: "陷阱防範：過去式一般動詞否定必用 didn't pass（不可寫 are not pass）"
      },
      {
        prompt: "Sophia, Ava - did not play tennis / neither",
        ans: "Sophia did not play tennis, and neither did Ava.",
        hint: "陷阱防範：neither 本身已含否定，後面助動詞必用肯定形 did（neither did Ava）"
      },
      {
        prompt: "Edison, Swan - a famous inventor / so",
        ans: "Edison was a famous inventor, and so was Swan.",
        hint: "陷阱防範：身分名詞無一般動詞，前句用 was，後句倒裝必對齊用 so was Swan！"
      },
      {
        prompt: "Ethan, Mason - not late for school / neither",
        ans: "Ethan wasn't late for school, and neither was Mason.",
        hint: "陷阱防範：形容詞 late 搭配 be 動詞 wasn't，後句否定倒裝用 neither was Mason"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">I. AI 變式倒裝附和句改寫 (請用過去簡單式與指定連接詞合成句子，每題 4 分，共 24 分)</div>
        <div class="exam-questions-grid">
    `;
    variantG13.forEach((g, idx) => {
      let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:24px; margin-top:6px;"></div>`;
      if (isTeacher || isContrast) {
        ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：${escapeHtml(g.ans)} <small style="color:#4B5563;">(${escapeHtml(g.hint)})</small></div>`;
      }
      html += `
        <div class="print-q-item" style="margin-bottom:10px;">
          <span class="q-num">${idx + 1}.</span>
          <span class="q-text">Prompt: <strong>[${escapeHtml(g.prompt)}]</strong></span>
          ${ansLine}
        </div>
      `;
    });
    html += `</div></div>`;

    // Part II: AI 變式副詞三級長句合成 (6 題，每題 6 分 = 36 分)
    const variantG14 = [
      {
        prompt: "How did they do in their test? Mia: 100%, Zoe: 92% & Ben: 85%",
        ans: "Ben did well in his test, Zoe did better than Ben, but Mia did the best.",
        hint: "不規則副詞 well ➔ better than ➔ the best（必須從 85% 的 Ben 開始寫第一段原級！）"
      },
      {
        prompt: "How did they do in their game? Sam: 60%, Leo: 50% & Dan: 40%",
        ans: "Sam did badly in his game, Leo did worse than Sam, but Dan did the worst.",
        hint: "不規則副詞 badly ➔ worse than ➔ the worst（從 60% 的 Sam 往 40% 的 Dan 寫）"
      },
      {
        prompt: "The distance they flew: glider: 15km, helicopter: 120km & airplane: 900km",
        ans: "A glider flew far, a helicopter flew farther than a glider, but an airplane flew the farthest.",
        hint: "過去式動詞 flew；far ➔ farther/further than ➔ the farthest/furthest（注意 an airplane 冠詞）"
      },
      {
        prompt: "How do they sing? frog, cat & bird (用 beautifully)",
        ans: "A frog sings beautifully, a cat sings more beautifully than a frog, but a bird sings the most beautifully.",
        hint: "題幹問 How do they sing (現在式)！三單動詞必加 -s (sings)，比較級必加 more beautifully than"
      },
      {
        prompt: "How fast do they swim? turtle, penguin & dolphin",
        ans: "A turtle swims fast, a penguin swims faster than a turtle, but a dolphin swims the fastest.",
        hint: "現在式三單動詞 swims；單音節副詞 fast ➔ faster than ➔ the fastest（記得加 a 與 the！）"
      },
      {
        prompt: "How carefully can they paint? child, student & artist",
        ans: "A child can paint carefully, a student can paint more carefully than a child, but an artist can paint the most carefully.",
        hint: "助動詞 can + 原形動詞 paint；carefully ➔ more carefully than ➔ the most carefully（注意 an artist）"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">II. AI 變式副詞三級長句合成 (每題 6 分，共 36 分)</div>
        <div style="font-size:9.5pt; background:#F8FAFC; border:1px solid #CBD5E1; padding:6px 10px; border-radius:4px; margin-bottom:10px; color:#1E293B;">
          <div><strong>📌 副詞字庫 Adverbs</strong>：<code>[well, badly, far, beautifully, fast, carefully]</code></div>
          <div><strong>📐 必寫三段公式 Sentence form</strong>：<code>&lt;adverb clause&gt; , + &lt;comparative clause&gt; , + but + &lt;superlative clause&gt; .</code>（千萬別漏寫第一段原級！）</div>
        </div>
        <div class="exam-questions-grid">
    `;
    variantG14.forEach((g, idx) => {
      let ansLine = `<div class="write-line" style="border-bottom:1px solid #000; height:24px; margin-top:6px;"></div>`;
      if (isTeacher || isContrast) {
        ansLine = `<div style="color:#DC2626; font-weight:600; margin-top:4px;">正解：${escapeHtml(g.ans)} <small style="color:#4B5563;">(${escapeHtml(g.hint)})</small></div>`;
      }
      html += `
        <div class="print-q-item" style="margin-bottom:10px;">
          <span class="q-num">${idx + 1}.</span>
          <span class="q-text">Prompt: <strong>[${escapeHtml(g.prompt)}]</strong></span>
          ${ansLine}
        </div>
      `;
    });
    html += `</div></div>`;

    // Part III: 考場高頻語法與拼字改錯 (5 題，每題 4 分 = 20 分)
    const variantMistakes = [
      {
        sent: "A witch laughs horribly, and a vampire laughs horribly than a witch.",
        wrong: "horribly than",
        correct: "more horribly than",
        fixed: "A witch laughs horribly, and a vampire laughs more horribly than a witch.",
        reason: "多音節副詞比較級前面必須加 more (more horribly than)"
      },
      {
        sent: "An eight year old can walk more than a five year old.",
        wrong: "walk more than",
        correct: "walk more quickly than",
        fixed: "An eight year old can walk more quickly than a five year old.",
        reason: "比較走得多快時，more 後方不可漏寫副詞 quickly"
      },
      {
        sent: "A dog runs faster than a person, but lion runs fastest.",
        wrong: "lion runs fastest",
        correct: "a lion runs the fastest",
        fixed: "A dog runs faster than a person, but a lion runs the fastest.",
        reason: "單數可數名詞 lion 前須加 a，最高級 fastest 前須加 the"
      },
      {
        sent: "The new library is right infront off the city hall.",
        wrong: "infront off",
        correct: "in front of",
        fixed: "The new library is right in front of the city hall.",
        reason: "介系詞片語為 in front of（三字分開，介系詞是 of 不是 off）"
      },
      {
        sent: "The glassblower heated the glass in the hot furnes and made metal France.",
        wrong: "furnes / France",
        correct: "furnace / frames",
        fixed: "The glassblower heated the glass in the hot furnace and made metal frames.",
        reason: "熔爐拼寫為 furnace (-ace)；眼鏡框為 frames 而非法國 France"
      }
    ];

    html += `
      <div class="exam-section">
        <div class="section-title-print">III. 考場高頻語法與拼字改錯 (每題 4 分，共 20 分)</div>
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
