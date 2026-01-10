'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
// ========== CONFIGURATION ==========
// Add your valid unlock codes here (you generate these manually after payment)
const VALID_CODES = [
  'AURA-2026-LUKE',
  'AURA-2026-DEMO',  // Demo code for testing
  'AURA-PAID-001',
  'AURA-PAID-002',
  'AURA-PAID-003',
];

const USDT_ADDRESS = 'TG3J6rQPBNfQgAg9e4esdY4zjpCRPrATq9';  // USDT TRC20 (Tron)
const TELEGRAM_HANDLE = '@SergAI_BY';                         // Telegram for contact
// ====================================

// Real leads data from scraper
const allLeads = [
  { handle: '@LukeKling', name: 'Luke Kling', score: 9, category: 'traffic_buyer', reason_en: 'Runs traffic via Facebook Ads to Zeydoo, discusses offers and conversions', reason_ru: 'Льёт траф на Zeydoo через Facebook Ads, обсуждает офферы и конверт', source: 'Zeydoo CPA 📣 ENG', keywords: ['ads', 'defi', 'offer'] },
  { handle: '@RRapril', name: 'April', score: 9, category: 'traffic_buyer', reason_en: 'Looking for gaming offers for Asian geo, runs organic traffic', reason_ru: 'Ищет офферы для азиатского и индийского трафа, льёт органику', source: 'Zeydoo CPA 📣 ENG', keywords: ['cpa', 'manager', 'offer'] },
  { handle: '@arc_abdulkareem', name: 'Abdulkareem Lawal', score: 8, category: 'traffic_buyer', reason_en: 'Runs Facebook traffic, looking for Tier 3 offers', reason_ru: 'Льёт траф с Facebook, ищет офферы для Tier 3', source: 'Zeydoo CPA 📣 ENG', keywords: ['traff', 'ads', 'offer'] },
  { handle: '@xboss01', name: 'Mohit Pal', score: 8, category: 'traffic_buyer', reason_en: 'Has 2M daily views, runs traffic to US/UK/India, looking for dating offers', reason_ru: 'Имеет 2 млн просмотров в день, льёт траф в США, UK, Индию', source: 'Zeydoo CPA 📣 ENG', keywords: ['traff', 'manager', 'offer'] },
  { handle: '@SenhaySpace', name: 'Andrew', score: 8, category: 'marketing_pro', reason_en: 'Works with CPA offers, helps with selection and optimization', reason_ru: 'Работает с CPA-офферами, помогает с выбором и оптимизацией', source: 'Zeydoo CPA 📣 ENG', keywords: ['promotion', 'cpa', 'affiliate'] },
  { handle: '@Pragnesh_babariya', name: 'Pragnesh Babariya', score: 8, category: 'potential', reason_en: 'Has 5K influencers in India, looking for offers to collab', reason_ru: 'Имеет 5к инфлюенсеров в Индии, ищет офферы для коллаба', source: 'Zeydoo CPA 📣 ENG', keywords: ['manager', 'offer'] },
  { handle: '@Zainking908', name: 'Zain', score: 8, category: 'traffic_buyer', reason_en: 'Runs traffic, discusses offers and deposits', reason_ru: 'Льёт траф, обсуждает офферы и депы', source: 'Zeydoo CPA 📣 ENG', keywords: ['offer'] },
  { handle: '@Tp8000', name: 'Lucky', score: 8, category: 'traffic_buyer', reason_en: 'Looking for CPI campaigns, mentions app installs', reason_ru: 'Ищет траф для CPI кампаний, упоминает апп-инсталлы', source: 'Zeydoo CPA 📣 ENG', keywords: ['traff'] },
  { handle: '@NotoriousPPC', name: 'PPC Expert', score: 8, category: 'traffic_buyer', reason_en: 'PPC expert with high volume campaigns', reason_ru: 'PPC эксперт с большими объёмами', source: 'Affiliate Chat', keywords: ['ads', 'ppc'] },
  { handle: '@dzentraffic', name: 'Dzen Traffic', score: 8, category: 'traffic_buyer', reason_en: 'Traffic arbitrage specialist with experience', reason_ru: 'Специалист по арбитражу трафика', source: 'CPA Cash', keywords: ['traff', 'arbitrage'] },
  { handle: '@cryptowhale', name: 'Crypto Whale', score: 8, category: 'advertiser', reason_en: 'Looking for crypto traffic sources', reason_ru: 'Ищет источники крипто-трафа', source: 'DR Cash', keywords: ['crypto', 'traffic'] },
  { handle: '@mediabuyer_pro', name: 'Media Pro', score: 7, category: 'traffic_buyer', reason_en: 'Professional media buyer with FB experience', reason_ru: 'Профи медиабайер с опытом в FB', source: 'Traffic Cardinal', keywords: ['fb', 'ads'] },
];

const stats = {
  chatsProcessed: 9,
  usersAnalyzed: 100,
  leadsFound: 93,
  hotLeads: 48,
};

const categories = [
  { name: 'potential', count: 76, icon: '🔮' },
  { name: 'traffic_buyer', count: 12, icon: '💰' },
  { name: 'not_lead', count: 7, icon: '❌' },
  { name: 'marketing_pro', count: 4, icon: '🎯' },
  { name: 'influencer', count: 1, icon: '⭐' },
];

export default function Home() {
  const [lang, setLang] = useState<'en' | 'ru'>('en');
  const [showPayment, setShowPayment] = useState(false);
  const [showUnlockModal, setShowUnlockModal] = useState(false);
  const [unlockCode, setUnlockCode] = useState('');
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [unlockError, setUnlockError] = useState('');

  // Check for unlock on mount
  useEffect(() => {
    // Check localStorage
    const savedUnlock = localStorage.getItem('aura_unlocked');
    if (savedUnlock === 'true') {
      setIsUnlocked(true);
      return;
    }

    // Check URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const keyParam = urlParams.get('key');
    if (keyParam && VALID_CODES.includes(keyParam.toUpperCase())) {
      setIsUnlocked(true);
      localStorage.setItem('aura_unlocked', 'true');
      localStorage.setItem('aura_code', keyParam.toUpperCase());
      // Clean URL
      window.history.replaceState({}, '', window.location.pathname);
    }
  }, []);

  // Handle unlock code submission
  const handleUnlock = () => {
    const code = unlockCode.trim().toUpperCase();
    if (VALID_CODES.includes(code)) {
      setIsUnlocked(true);
      localStorage.setItem('aura_unlocked', 'true');
      localStorage.setItem('aura_code', code);
      setShowUnlockModal(false);
      setUnlockError('');
    } else {
      setUnlockError(lang === 'en' ? 'Invalid code. Please check and try again.' : 'Неверный код. Проверьте и попробуйте снова.');
    }
  };

  const t = {
    en: {
      title: 'AURA LEAD HUNTER',
      subtitle: 'Report generated: ' + new Date().toLocaleDateString('en-GB') + ' ' + new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }),
      chatsProcessed: 'Chats Processed',
      usersAnalyzed: 'Users Analyzed',
      leadsFound: 'Leads Found',
      hotLeads: 'Hot Leads',
      categories: 'Categories',
      hotLeadsTitle: '🔥 Hot Leads (Score 7-10)',
      allLeadsTitle: '🔥 All Hot Leads (UNLOCKED)',
      lockedTitle: '🔒 LOCKED: 43 More Hot Leads',
      unlockBtn: '🔓 UNLOCK FULL REPORT — $50 USDT',
      savePdf: '📄 Save PDF',
      savePdfLocked: '🔒 PDF Locked',
      included: "What's Included:",
      features: [
        '48 hot leads with Telegram handles',
        'AI-scored (7-10) traffic buyers',
        'Category breakdown & source info',
        'Bilingual report (EN/RU)',
        'CSV export ready',
      ],
      paymentTitle: 'Payment Instructions',
      paymentStep1: 'Send $50 USDT (TRC20) to:',
      paymentStep2: 'After payment, DM for your unlock code:',
      close: 'Close',
      unlockTitle: '🔓 Unlock Full Report',
      enterCode: 'Enter your unlock code:',
      unlock: 'UNLOCK',
      noCode: "Don't have a code?",
      payNow: 'Pay $50 USDT',
      unlocked: '✅ UNLOCKED',
    },
    ru: {
      title: 'AURA LEAD HUNTER',
      subtitle: 'Отчёт от ' + new Date().toLocaleDateString('ru-RU') + ' ' + new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' }),
      chatsProcessed: 'Чатов обработано',
      usersAnalyzed: 'Пользователей',
      leadsFound: 'Лидов найдено',
      hotLeads: 'Горячих',
      categories: 'Категории',
      hotLeadsTitle: '🔥 Горячие лиды (Score 7-10)',
      allLeadsTitle: '🔥 Все горячие лиды (РАЗБЛОКИРОВАНО)',
      lockedTitle: '🔒 ЗАБЛОКИРОВАНО: Ещё 43 лида',
      unlockBtn: '🔓 РАЗБЛОКИРОВАТЬ — $50 USDT',
      savePdf: '📄 Сохранить PDF',
      savePdfLocked: '🔒 PDF заблокирован',
      included: 'Что включено:',
      features: [
        '48 горячих лидов с Telegram handle',
        'AI-оценка (7-10) байеров трафа',
        'Разбивка по категориям и источникам',
        'Билингвальный отчёт (EN/RU)',
        'Готовый CSV экспорт',
      ],
      paymentTitle: 'Инструкция по оплате',
      paymentStep1: 'Отправьте $50 USDT (TRC20) на:',
      paymentStep2: 'После оплаты напишите для получения кода:',
      close: 'Закрыть',
      unlockTitle: '🔓 Разблокировать отчёт',
      enterCode: 'Введите код разблокировки:',
      unlock: 'РАЗБЛОКИРОВАТЬ',
      noCode: 'Нет кода?',
      payNow: 'Оплатить $50 USDT',
      unlocked: '✅ РАЗБЛОКИРОВАНО',
    },
  };

  const text = t[lang];
  const visibleLeads = isUnlocked ? allLeads : allLeads.slice(0, 5);
  const lockedLeads = allLeads.slice(5);

  return (
    <main className="min-h-screen bg-gradient-to-br from-[#1a1a2e] via-[#16213e] to-[#0f3460] text-white p-5">
      {/* Language Toggle */}
      <div className="fixed top-5 left-5 z-50 flex gap-1">
        <button
          onClick={() => setLang('en')}
          className={`px-4 py-2 rounded-lg text-sm font-bold transition-all border ${lang === 'en'
            ? 'bg-gradient-to-r from-[#7b2cbf] to-[#00d4ff] text-white border-transparent'
            : 'bg-white/10 text-gray-400 border-white/20 hover:bg-white/20'
            }`}
        >
          EN
        </button>
        <button
          onClick={() => setLang('ru')}
          className={`px-4 py-2 rounded-lg text-sm font-bold transition-all border ${lang === 'ru'
            ? 'bg-gradient-to-r from-[#7b2cbf] to-[#00d4ff] text-white border-transparent'
            : 'bg-white/10 text-gray-400 border-white/20 hover:bg-white/20'
            }`}
        >
          RU
        </button>
        {isUnlocked && (
          <span className="ml-2 px-3 py-2 bg-green-500/20 text-green-400 rounded-lg text-sm font-bold border border-green-500/30">
            {text.unlocked}
          </span>
        )}
      </div>

      {/* Save PDF Button */}
      <button
        onClick={() => isUnlocked ? window.print() : setShowUnlockModal(true)}
        className={`fixed top-5 right-5 z-50 px-6 py-3 rounded-xl font-bold shadow-lg transition-all ${isUnlocked
          ? 'bg-gradient-to-r from-[#7b2cbf] to-[#00d4ff] hover:scale-105'
          : 'bg-gray-600 cursor-pointer hover:bg-gray-500'
          }`}
      >
        {isUnlocked ? text.savePdf : text.savePdfLocked}
      </button>

      <div className="max-w-[1200px] mx-auto">
        {/* Header */}
        <header className="text-center py-10 px-5 bg-white/5 rounded-[20px] mb-8 backdrop-blur-sm">
          <h1 className="text-4xl md:text-5xl font-bold mb-2 flex items-center justify-center gap-3">
            <Image src="/aura.png" alt="Aura" width={140} height={48} className="h-12 w-auto" />
            <span className="bg-gradient-to-r from-[#00d4ff] to-[#7b2cbf] bg-clip-text text-transparent">
              {text.title}
            </span>
          </h1>
          <p className="text-gray-400 text-lg">{text.subtitle}</p>

          {/* Navigation Tabs */}
          <div className="flex justify-center gap-3 mt-6">
            <div className="bg-gradient-to-r from-[#7b2cbf] to-[#00d4ff] px-6 py-2 rounded-xl font-bold">
              📊 {lang === 'en' ? 'Leads' : 'Лиды'}
            </div>
            <a
              href="/matchmaking"
              className="bg-white/10 hover:bg-gradient-to-r hover:from-pink-500 hover:to-purple-500 px-6 py-2 rounded-xl font-bold transition-all border border-white/20 hover:border-transparent"
            >
              💘 {lang === 'en' ? 'Matchmaking' : 'Мэтчинг'}
            </a>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-5 mb-8">
          <StatCard number={stats.chatsProcessed} label={text.chatsProcessed} />
          <StatCard number={stats.usersAnalyzed} label={text.usersAnalyzed} />
          <StatCard number={stats.leadsFound} label={text.leadsFound} />
          <StatCard number={stats.hotLeads} label={text.hotLeads} emoji="🔥" />
        </div>

        {/* Categories */}
        <section className="bg-white/5 rounded-[15px] p-6 mb-5 border border-white/10">
          <h2 className="text-[#00d4ff] text-xl font-bold mb-5 flex items-center gap-2">
            📊 {text.categories}
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {categories.map((cat) => (
              <div key={cat.name} className="bg-black/30 p-4 rounded-xl text-center">
                <div className="text-3xl font-bold text-[#00d4ff]">{cat.count}</div>
                <div className="text-gray-400 text-sm mt-1">{cat.icon} {cat.name}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Hot Leads Section */}
        <section className="bg-white/5 rounded-[15px] p-6 mb-5 border border-white/10">
          <h2 className="text-[#00d4ff] text-xl font-bold mb-5">
            {isUnlocked ? text.allLeadsTitle : text.hotLeadsTitle}
          </h2>
          <div className="space-y-4">
            {visibleLeads.map((lead, i) => (
              <LeadCard key={i} lead={lead} lang={lang} />
            ))}
          </div>
        </section>

        {/* Locked Section (only show if not unlocked) */}
        {!isUnlocked && (
          <section className="bg-white/5 rounded-[15px] p-6 mb-5 border border-white/10 relative overflow-hidden">
            <h2 className="text-orange-400 text-xl font-bold mb-5">{text.lockedTitle}</h2>

            {/* Blurred Content */}
            <div className="space-y-4 blur-md select-none pointer-events-none opacity-70">
              {lockedLeads.map((lead, i) => (
                <LeadCard key={i} lead={lead} lang={lang} />
              ))}
              {[...Array(6)].map((_, i) => (
                <div key={`fake-${i}`} className="bg-black/30 rounded-xl p-5 border-l-4 border-orange-500">
                  <div className="flex justify-between items-center">
                    <span className="text-cyan-400 font-bold">@hidden_lead_{i + 1}</span>
                    <span className="bg-gradient-to-r from-[#7b2cbf] to-[#00d4ff] px-4 py-1 rounded-full text-sm font-bold">
                      {8 - Math.floor(i / 3)}/10
                    </span>
                  </div>
                  <p className="text-gray-500 mt-2 italic">Premium lead information...</p>
                </div>
              ))}
            </div>

            {/* Overlay with Unlock Button */}
            <div className="absolute inset-0 bg-gradient-to-t from-[#1a1a2e] via-[#1a1a2e]/90 to-transparent flex items-center justify-center">
              <button
                onClick={() => setShowUnlockModal(true)}
                className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 px-10 py-5 rounded-xl font-bold text-xl shadow-2xl transform hover:scale-105 transition-all animate-pulse"
              >
                {text.unlockBtn}
              </button>
            </div>
          </section>
        )}

        {/* What's Included */}
        <section className="bg-white/5 rounded-[15px] p-6 mb-8 border border-white/10">
          <h3 className="text-purple-400 text-lg font-bold mb-4">📋 {text.included}</h3>
          <ul className="grid md:grid-cols-2 gap-3">
            {text.features.map((f, i) => (
              <li key={i} className="flex items-center gap-3 text-gray-300">
                <span className="text-green-400 text-lg">✓</span>
                {f}
              </li>
            ))}
          </ul>
        </section>

        {/* Footer */}
        <footer className="text-center text-gray-500 py-6">
          <p>Generated by Aura Lead Hunter 2.0 | AI-Powered CPA Intelligence</p>
        </footer>
      </div>

      {/* Unlock Modal */}
      {showUnlockModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowUnlockModal(false)}>
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 max-w-md w-full border border-purple-500/50 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold text-center mb-6 text-purple-400">
              {text.unlockTitle}
            </h3>

            <div className="space-y-6">
              {/* Code Input */}
              <div>
                <label className="text-gray-400 mb-2 block">{text.enterCode}</label>
                <input
                  type="text"
                  value={unlockCode}
                  onChange={(e) => setUnlockCode(e.target.value.toUpperCase())}
                  placeholder="AURA-XXXX-XXXX"
                  className="w-full bg-black/50 border border-cyan-500/30 rounded-xl p-4 text-cyan-400 font-mono text-lg text-center placeholder-gray-600 focus:border-cyan-500 focus:outline-none"
                  onKeyDown={(e) => e.key === 'Enter' && handleUnlock()}
                />
                {unlockError && (
                  <p className="text-red-400 text-sm mt-2 text-center">{unlockError}</p>
                )}
              </div>

              <button
                onClick={handleUnlock}
                className="w-full py-4 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 rounded-xl font-bold text-lg transition-all"
              >
                {text.unlock}
              </button>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-600"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-slate-800 text-gray-500">{text.noCode}</span>
                </div>
              </div>

              <button
                onClick={() => { setShowUnlockModal(false); setShowPayment(true); }}
                className="w-full py-4 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 rounded-xl font-bold text-lg transition-all"
              >
                💳 {text.payNow}
              </button>
            </div>

            <button
              onClick={() => setShowUnlockModal(false)}
              className="w-full mt-4 py-3 bg-white/10 hover:bg-white/20 rounded-xl font-bold transition-all border border-white/20"
            >
              {text.close}
            </button>
          </div>
        </div>
      )}

      {/* Payment Modal */}
      {showPayment && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowPayment(false)}>
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 max-w-md w-full border border-purple-500/50 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold text-center mb-6 text-purple-400">
              💳 {text.paymentTitle}
            </h3>

            <div className="space-y-6">
              <div>
                <p className="text-gray-400 mb-2">{text.paymentStep1}</p>
                <div className="bg-black/50 p-4 rounded-xl border border-cyan-500/30">
                  <code className="text-cyan-400 text-sm break-all font-mono">{USDT_ADDRESS}</code>
                </div>
                <p className="text-xs text-gray-500 mt-2">Network: TRC20 (Tron)</p>
              </div>

              {/* QR Code Placeholder */}
              <div className="flex justify-center">
                <div className="w-48 h-48 bg-white rounded-xl flex items-center justify-center p-2">
                  <div className="text-center">
                    <div className="text-6xl mb-2">📱</div>
                    <span className="text-black text-xs">Scan QR Code</span>
                  </div>
                </div>
              </div>

              <div>
                <p className="text-gray-400 mb-2">{text.paymentStep2}</p>
                <div className="bg-black/50 p-4 rounded-xl text-center border border-cyan-500/30">
                  <a
                    href={`https://t.me/${TELEGRAM_HANDLE.replace('@', '')}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-cyan-400 font-bold text-2xl hover:underline"
                  >
                    {TELEGRAM_HANDLE}
                  </a>
                </div>
              </div>
            </div>

            <button
              onClick={() => setShowPayment(false)}
              className="w-full mt-6 py-3 bg-white/10 hover:bg-white/20 rounded-xl font-bold transition-all border border-white/20"
            >
              {text.close}
            </button>
          </div>
        </div>
      )}
    </main>
  );
}

function StatCard({ number, label, emoji }: { number: number; label: string; emoji?: string }) {
  return (
    <div className="bg-white/5 backdrop-blur-sm rounded-[15px] p-6 text-center border border-white/10">
      <div className="text-4xl font-bold bg-gradient-to-r from-[#00d4ff] to-[#7b2cbf] bg-clip-text text-transparent">
        {number}
      </div>
      <div className="text-gray-400 text-sm mt-2">
        {emoji && <span className="mr-1">{emoji}</span>}
        {label}
      </div>
    </div>
  );
}

function LeadCard({ lead, lang }: { lead: typeof allLeads[0]; lang: 'en' | 'ru' }) {
  const categoryIcons: Record<string, string> = {
    traffic_buyer: '💰',
    advertiser: '📢',
    marketing_pro: '🎯',
    community_owner: '👑',
    influencer: '⭐',
    potential: '🔮',
  };

  return (
    <div className="bg-black/30 rounded-xl p-5 border-l-4 border-red-500 hover:bg-black/40 transition-all hover:translate-x-1">
      <div className="flex justify-between items-center mb-3">
        <a
          href={`https://t.me/${lead.handle.replace('@', '')}`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-[#00d4ff] font-bold text-lg hover:underline"
        >
          {lead.handle}
        </a>
        <span className="bg-gradient-to-r from-[#7b2cbf] to-[#00d4ff] px-4 py-1 rounded-full text-sm font-bold">
          {lead.score}/10
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-2 mb-3">
        <span className="bg-purple-500/30 px-3 py-1 rounded-lg text-sm">
          {categoryIcons[lead.category] || '📌'} {lead.category}
        </span>
        <span className="text-gray-500 text-sm">{lead.name}</span>
      </div>

      <p className="text-gray-400 italic mb-3">
        "{lang === 'en' ? lead.reason_en : lead.reason_ru}"
      </p>

      <div className="flex flex-wrap gap-2 mb-2">
        {lead.keywords?.slice(0, 4).map((k, i) => (
          <span key={i} className="bg-cyan-500/20 text-[#00d4ff] px-2 py-1 rounded text-xs">
            {k}
          </span>
        ))}
      </div>

      <p className="text-gray-500 text-sm">📍 {lead.source}</p>
    </div>
  );
}
