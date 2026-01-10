'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, AreaChart, Area
} from 'recharts';
import {
  Globe, Zap, Target, BarChart3, TrendingUp, ShieldCheck,
  Users, MessageSquare, Award, Globe2
} from 'lucide-react';
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
  { handle: 'ID:519043552', name: 'Anastasiia', score: 10, category: 'marketing_pro', reason_en: 'Recruiting for affiliate marketing roles, focusing on traffic, CPA, and conversions.', reason_ru: 'Рекрутинг в арбитраже, фокус на трафик, CPA и конверсии', source: 'CPA HR | Вакансии', keywords: ['traff', 'cpa', 'manager'] },
  { handle: 'ID:8104231262', name: 'Spider 🕷️🕸️', score: 10, category: 'traffic_buyer', reason_en: 'Offers traffic services for crypto and other niches, high volume ability', reason_ru: 'Предлагает услуги по заливу трафика для крипты и других ниш', source: 'CPA HR | Вакансии', keywords: ['крипто', 'трафик', 'traff'] },
  { handle: '@xboss01', name: 'Mohit Pal', score: 9, category: 'traffic_buyer', reason_en: 'Has 2M daily FB traffic, seeks dating offers, runs campaigns', reason_ru: 'Имеет 2М трафа в день, ищет датинг офферы, запускает кампании', source: 'Zeydoo CPA 📣 ENG', keywords: ['offer', 'traff', 'manager'] },
  { handle: 'ID:6825323525', name: 'Michael Walker', score: 9, category: 'traffic_buyer', reason_en: 'Offers live traffic and native ads for crypto-forex.', reason_ru: 'Предлагает живой трафик и нативные объявления для крипто-форекс', source: 'УБТ ЧАТ | АРБИТРАЖ ТРАФИКА', keywords: ['partnership', 'ads', 'traff'] },
  { handle: '@biggTraff', name: 'B I G_TRAFFA', score: 9, category: 'traffic_buyer', reason_en: 'Offers traffic services for crypto and other niches, professional setup', reason_ru: 'Предлагает услуги по заливу трафа в крипту и другие ниши', source: 'СPA | Арбитраж вакансии', keywords: ['крипто', 'трафик', 'traff'] },
  { handle: 'ID:7299216494', name: 'Yuliya Aff', score: 9, category: 'marketing_pro', reason_en: 'Hiring Media Buyer for Gambling ads, FB campaigns, conversions', reason_ru: 'Ищет Media Buyer для Gambling, FB кампании, конверт', source: 'Чат траферов | Арбитраж трафика', keywords: ['buy', 'manager', 'ads'] },
  { handle: '@zagrtmsh', name: 'Daniil', score: 9, category: 'traffic_buyer', reason_en: 'Actively seeking gambling traffic for multiple GEOs', reason_ru: 'Ищет трафик на гемблинг для множества гео', source: 'СPA | Арбитраж вакансии', keywords: ['арбитраж', 'трафик'] },
  { handle: '@aaroninc', name: 'Aaron Ch', score: 9, category: 'traffic_buyer', reason_en: 'Promoting high-EPC offers and targeting traffic buyers', reason_ru: 'Продвигает офферы с высоким EPC и ищет трафик', source: 'СPA | Арбитраж вакансии', keywords: ['traff', 'offer'] },
  { handle: '@Trafik_01_01', name: 'Alexxx XXX💸', score: 9, category: 'traffic_buyer', reason_en: 'Experienced traffic buyer, offers CPA conversions', reason_ru: 'Опытный трафер, работает по CPA, делает крео', source: 'Вакансии Арбитраж CPA', keywords: ['реклама', 'трафик'] },
];

const stats = {
  chatsProcessed: 42,
  usersAnalyzed: 781,
  leadsFound: 204,
  hotLeads: 151,
};

const categories = [
  { name: 'potential', count: 144, icon: '🔮' },
  { name: 'traffic_buyer', count: 100, icon: '💰' },
  { name: 'marketing_pro', count: 25, icon: '🎯' },
  { name: 'agency_owner', count: 12, icon: '🏢' },
  { name: 'influencer', count: 5, icon: '⭐' },
];

// ========== ANALYTICS DATA ==========
const geoData = [
  { name: 'India', value: 40, color: '#00d4ff' },
  { name: 'CIS', value: 25, color: '#7b2cbf' },
  { name: 'USA', value: 15, color: '#ff00c8' },
  { name: 'Brazil', value: 10, color: '#00ff88' },
  { name: 'Other', value: 10, color: '#555555' },
];

const sourceData = [
  { name: 'FB Ads', value: 35 },
  { name: 'TikTok', value: 25 },
  { name: 'Google', value: 15 },
  { name: 'In-app', value: 15 },
  { name: 'SEO/UBT', value: 10 },
];

const verticalData = [
  { name: 'Gambling', value: 38 },
  { name: 'Crypto', value: 22 },
  { name: 'Dating', value: 18 },
  { name: 'Nutra', value: 12 },
  { name: 'E-com', value: 10 },
];

const velocityData = [
  { time: '00:00', leads: 12 },
  { time: '04:00', leads: 8 },
  { time: '08:00', leads: 24 },
  { time: '12:00', leads: 42 },
  { time: '16:00', leads: 38 },
  { time: '20:00', leads: 56 },
  { time: '23:59', leads: 45 },
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
        '204 hot leads with Telegram handles',
        'AI-scored (7-10) traffic buyers',
        'Category breakdown & source info',
        'Bilingual report (EN/RU)',
        'CSV export ready',
      ],
      analytics: 'Market Intelligence',
      geoDist: 'Geo Distribution',
      trafficTrends: 'Traffic Source Trends',
      verticals: 'Vertical Concentration',
      signalVelocity: 'Signal Velocity (Pulse)',
      whaleScore: 'Whale Score',
      marketHealth: 'Base Quality Index',
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
        '204 горячих лида с Telegram handle',
        'AI-оценка (7-10) байеров трафа',
        'Разбивка по категориям и источникам',
        'Билингвальный отчёт (EN/RU)',
        'Готовый CSV экспорт',
      ],
      analytics: 'Бизнес-Аналитика',
      geoDist: 'География Трафика',
      trafficTrends: 'Тренды Источников',
      verticals: 'Концентрация Ниш',
      signalVelocity: 'Скорость Пульса (FOMO)',
      whaleScore: 'Whale Score',
      marketHealth: 'Индекс Качества Базы',
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
        <div className="grid grid-cols-2 md:grid-cols-5 gap-5 mb-8">
          <StatCard icon={<MessageSquare size={20} />} number={stats.chatsProcessed} label={text.chatsProcessed} />
          <StatCard icon={<Users size={20} />} number={stats.usersAnalyzed} label={text.usersAnalyzed} />
          <StatCard icon={<Target size={20} />} number={stats.leadsFound} label={text.leadsFound} />
          <StatCard icon={<Zap size={20} className="text-orange-400" />} number={stats.hotLeads} label={text.hotLeads} emoji="🔥" />
          <StatCard
            icon={<Award size={20} className="text-yellow-400" />}
            number={89}
            suffix="%"
            label={text.whaleScore}
            sublabel={text.marketHealth}
          />
        </div>

        {/* Analytics Section */}
        <section className="mb-8 overflow-hidden">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <BarChart3 className="text-[#00d4ff]" /> {text.analytics}
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Geo Distribution */}
            <div className="bg-white/5 backdrop-blur-md rounded-2xl p-6 border border-white/10 flex flex-col items-center">
              <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2 self-start uppercase tracking-wider">
                <Globe size={16} className="text-cyan-400" /> {text.geoDist}
              </h3>
              <div className="w-full h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={geoData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {geoData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1a1a2e', borderColor: '#333', color: '#fff' }}
                      itemStyle={{ color: '#fff' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="grid grid-cols-2 gap-2 w-full mt-2">
                {geoData.map((g) => (
                  <div key={g.name} className="flex items-center gap-2 text-xs">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: g.color }} />
                    <span className="text-gray-400">{g.name}</span>
                    <span className="ml-auto font-bold">{g.value}%</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Traffic Sources */}
            <div className="bg-white/5 backdrop-blur-md rounded-2xl p-6 border border-white/10 lg:col-span-1">
              <h3 className="text-sm font-semibold text-gray-400 mb-6 flex items-center gap-2 uppercase tracking-wider">
                <TrendingUp size={16} className="text-purple-400" /> {text.trafficTrends}
              </h3>
              <div className="w-full h-[220px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={sourceData} layout="vertical">
                    <XAxis type="number" hide />
                    <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{ fill: '#aaa', fontSize: 11 }} width={80} />
                    <Tooltip
                      cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                      contentStyle={{ backgroundColor: '#1a1a2e', border: 'none', borderRadius: '8px' }}
                    />
                    <Bar dataKey="value" fill="#7b2cbf" radius={[0, 4, 4, 0]} barSize={20} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Vertical Concentration */}
            <div className="bg-white/5 backdrop-blur-md rounded-2xl p-6 border border-white/10">
              <h3 className="text-sm font-semibold text-gray-400 mb-6 flex items-center gap-2 uppercase tracking-wider">
                <ShieldCheck size={16} className="text-emerald-400" /> {text.verticals}
              </h3>
              <div className="space-y-4">
                {verticalData.map((v) => (
                  <div key={v.name} className="relative pt-1">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-semibold text-gray-300">{v.name}</span>
                      <span className="text-xs font-bold text-[#00d4ff]">{v.value}%</span>
                    </div>
                    <div className="overflow-hidden h-1.5 text-xs flex rounded bg-white/10">
                      <div
                        style={{ width: `${v.value}%` }}
                        className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gradient-to-r from-[#00d4ff] to-[#7b2cbf]"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Signal Velocity */}
            <div className="bg-white/5 backdrop-blur-md rounded-2xl p-6 border border-white/10">
              <h3 className="text-sm font-semibold text-gray-400 mb-6 flex items-center gap-2 uppercase tracking-wider">
                <Zap size={16} className="text-orange-400" /> {text.signalVelocity}
              </h3>
              <div className="w-full h-[180px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={velocityData}>
                    <defs>
                      <linearGradient id="colorLeads" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#ff8c00" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#ff8c00" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1a1a2e', border: 'none', borderRadius: '8px' }}
                    />
                    <Area type="monotone" dataKey="leads" stroke="#ff8c00" fillOpacity={1} fill="url(#colorLeads)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
              <p className="text-[10px] text-gray-500 mt-4 italic text-center">
                Real-time message density across 42 target nodes
              </p>
            </div>
          </div>
        </section>

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

function StatCard({ number, label, emoji, icon, suffix, sublabel }: { number: number; label: string; emoji?: string; icon?: React.ReactNode; suffix?: string; sublabel?: string }) {
  return (
    <div className="bg-white/5 backdrop-blur-md rounded-[20px] p-6 text-center border border-white/10 relative overflow-hidden group hover:border-[#00d4ff]/50 transition-all">
      <div className="absolute top-0 right-0 p-3 opacity-20 text-gray-400 group-hover:text-cyan-400 transition-colors">
        {icon}
      </div>
      <div className="text-4xl font-bold bg-gradient-to-r from-[#00d4ff] to-[#7b2cbf] bg-clip-text text-transparent">
        {number}{suffix}
      </div>
      <div className="text-gray-300 text-xs font-bold uppercase tracking-widest mt-2">
        {emoji && <span className="mr-1">{emoji}</span>}
        {label}
      </div>
      {sublabel && (
        <div className="text-[10px] text-gray-500 mt-1 uppercase tracking-tighter italic">
          {sublabel}
        </div>
      )}
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
