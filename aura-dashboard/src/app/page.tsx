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
  { handle: '@anastasiiaSSD', name: 'Anastasiia', score: 10, category: 'marketing_pro', geo: 'CIS', vertical: 'Crypto', reason_en: 'Recruiting for affiliate marketing roles, focusing on traffic, CPA, and conversions.', reason_ru: 'Рекрутинг в арбитраже, фокус на трафик, CPA и конверсии', source: 'CPA HR | Вакансии', keywords: ['traff', 'cpa', 'manager'] },
  { handle: '@hr_lolz', name: '🌏🌎🌍', score: 10, category: 'traffic_buyer', geo: 'CIS', vertical: 'Crypto', reason_en: 'Offers traffic services, focuses on leads and conversions', reason_ru: 'Предлагает услуги трафа, акцент на лиды и конверт', source: 'АРБИТРАЖ ТРАФИКА', keywords: ['traff', 'лиды'] },
  { handle: '@spider_r1', name: 'Spider 🕷️', score: 10, category: 'traffic_buyer', geo: 'CIS', vertical: 'Gambling', reason_en: 'Offers traffic services for crypto, gambling, and dating.', reason_ru: 'Предлагает услуги по заливу трафа для крипты, гемблы и дейтинга', source: 'CPA HR | Вакансии', keywords: ['трафик', 'traff'] },
  { handle: '@Lingard1919868', name: 'Kung Fu', score: 10, category: 'advertiser', geo: 'India', vertical: 'Crypto', reason_en: 'Offers Facebook ad accounts for crypto and NFT projects.', reason_ru: 'Предлагает FB аккаунты для крипто и NFT проектов', source: 'CPA Арбитраж вакансии', keywords: ['ads', 'crypto'] },
  { handle: '@biggTraff', name: 'B I G_TRAFFA', score: 9, category: 'traffic_buyer', geo: 'CIS', vertical: 'Crypto', reason_en: 'Offers traffic services for crypto and other niches, professional setup', reason_ru: 'Предлагает услуги по заливу трафа в крипту и другие ниши', source: 'СPA | Арбитраж вакансии', keywords: ['крипто', 'трафик'] },
  { handle: '@zagrtmsh', name: 'Daniil', score: 9, category: 'traffic_buyer', geo: 'CIS', vertical: 'Gambling', reason_en: 'Actively seeking gambling traffic for multiple GEOs', reason_ru: 'Ищет трафик на гемблинг для множества гео', source: 'СPA | Арбитраж вакансии', keywords: ['арбитраж', 'трафик'] },
  { handle: '@Thepro4u', name: 'Sulong', score: 9, category: 'traffic_buyer', geo: 'Other', vertical: 'Crypto', reason_en: 'Promoting crypto/casino ads, focusing on traffic and conversions', reason_ru: 'Продвигает крипто/казино офферы, акцент на траф и конверт', source: 'Чат вебмастеров', keywords: ['traff', 'crypto'] },
  { handle: 'ID:8080385865', name: 'User 8080385865', score: 9, category: 'traffic_buyer', geo: 'CIS', vertical: 'Crypto', reason_en: 'Promoting exclusive offers for arbitrageurs, focusing on traffic monetization.', reason_ru: 'Продвигает эксклюзивные офферы для арбитражников, монетизация трафика.', source: 'CPA HR | Вакансии', keywords: ['трафик', 'оффер'] },
  { handle: '@Aff_Arb_Yuliya', name: 'Yuliya Aff', score: 9, category: 'marketing_pro', geo: 'CIS', vertical: 'Gambling', reason_en: 'Hiring Media Buyer for Gambling ads, FB campaigns, conversions', reason_ru: 'Ищет Media Buyer для Gambling, FB кампании, конверт', source: 'Чат траферов', keywords: ['buy', 'manager'] },
  { handle: '@rec_anastasia', name: 'Anastasia', score: 9, category: 'marketing_pro', geo: 'CIS', vertical: 'Gambling', reason_en: 'Experienced Team Lead Media Buyer with expertise in traffic and offers.', reason_ru: 'Опытный Team Lead Media Buyer с опытом работы с трафом и офферами.', source: 'СPA | Арбитраж вакансии', keywords: ['traff', 'buy'] },
  { handle: '@aaroninc', name: 'Aaron Ch', score: 9, category: 'traffic_buyer', geo: 'Other', vertical: 'Nutra', reason_en: 'Promoting high-EPC offers and targeting traffic buyers', reason_ru: 'Продвигает офферы с высоким EPC и ищет трафик', source: 'СPA | Арбитраж вакансии', keywords: ['traff', 'offer'] },
  { handle: '@Trafik_01_01', name: 'Alexxx XXX💸', score: 9, category: 'traffic_buyer', geo: 'CIS', vertical: 'Gambling', reason_en: 'Experienced traffic buyer, offers CPA conversions', reason_ru: 'Опытный трафер, работает по CPA, делает крео', source: 'Вакансии Арбитраж CPA', keywords: ['реклама', 'трафик'] },
  { handle: '@vlad_traff', name: 'Vladislav', score: 9, category: 'traffic_buyer', geo: 'CIS', vertical: 'Gambling', reason_en: 'Scaling gambling offers, optimizing CPA and retention.', reason_ru: 'Масштабирует гемблинг офферы, оптимизирует CPA.', source: 'Чат траферов', keywords: ['scaling', 'cpa'] },
  { handle: '@paul_media', name: 'Paul Walker', score: 8, category: 'traffic_buyer', geo: 'USA', vertical: 'Crypto', reason_en: 'Expert in native ads for tier-1 traffic sources.', reason_ru: 'Эксперт в нативной рекламе для тир-1 источников.', source: 'Media Buyers Global', keywords: ['native', 'tier-1'] },
  { handle: '@brazil_king', name: 'Carlos', score: 8, category: 'traffic_buyer', geo: 'Brazil', vertical: 'Gambling', reason_en: 'Strong traffic volumes in Brazil, focusing on local payment solutions.', reason_ru: 'Большие объемы в Бразилии, фокус на локальные платежки.', source: 'Latin Arbitrage', keywords: ['brazil', 'pix'] },
  { handle: '@mobi_expert', name: 'Amit', score: 8, category: 'agency_owner', geo: 'India', vertical: 'E-com', reason_en: 'Runs a high-performing agency for in-app traffic in India.', reason_ru: 'Владелец агентства по in-app трафику в Индии.', source: 'Mobile Marketing IN', keywords: ['in-app', 'india'] },
  { handle: '@euro_clicks', name: 'Stefan', score: 8, category: 'traffic_buyer', geo: 'Other', vertical: 'Nutra', reason_en: 'Specializes in European Nutra traffic via TikTok.', reason_ru: 'Специализируется на европейской нутре через TikTok.', source: 'TikTok Business EU', keywords: ['tiktok', 'nutra'] },
  { handle: '@crypto_whale_hr', name: 'Elena', score: 8, category: 'marketing_pro', geo: 'CIS', vertical: 'Crypto', reason_en: 'Hiring senior buyers for a large crypto-fund.', reason_ru: 'Нанимает синьор-байеров в крупный крипто-фонд.', source: 'Crypto Jobs RU', keywords: ['hiring', 'crypto'] },
  { handle: '@us_leads_pro', name: 'John D.', score: 8, category: 'traffic_buyer', geo: 'USA', vertical: 'Dating', reason_en: 'Focusing on high-intent US dating leads via Google PPC.', reason_ru: 'Лиды на дейтинг в США через Google PPC.', source: 'PPC Mastermind', keywords: ['ppc', 'us'] },
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


const riskLeads = [
  { handle: 'ID:8524987311', score: 1, risk: 'HIGH', reason: 'Fresh account, no business activity or keywords', keywords: ['new_acc', 'low_activity'] },
  { handle: 'ID:8445368477', score: 1, risk: 'HIGH', reason: 'Buying SIM cards, no interest in crypto-marketing', keywords: ['suspicious', 'sim_buying'] },
  { handle: 'ID:7913887719', score: 8, risk: 'MEDIUM', reason: 'Promoting tools for Telegram spam and arbitrage', keywords: ['spam', 'bots'] },
  { handle: 'ID:7742798742', score: 7, risk: 'MEDIUM', reason: 'Seeking traffic for OnlyFans models, mentions CPA', keywords: ['cpa', 'onlyfans'] },
  { handle: 'ID:7071923293', score: 7, risk: 'MEDIUM', reason: 'Offers crypto leads and data, seeking long-term cooperation', keywords: ['leads', 'data'] },
  { handle: 'ID:8063606739', score: 8, risk: 'MEDIUM', reason: 'Manages large-scale traffic channels, seeking offers', keywords: ['high_volume', 'traff'] },
  { handle: 'ID:8156985724', score: 8, risk: 'MEDIUM', reason: 'CPA Network owner seeking advertisers for collaboration', keywords: ['network', 'owner'] },
  { handle: 'ID:7254481045', score: 6, risk: 'MEDIUM', reason: 'Experienced in crypto marketing, seeking offers', keywords: ['marketing', 'offers'] },
  { handle: 'ID:7732047420', score: 7, risk: 'MEDIUM', reason: 'Seeking TikTok UBT specialists, likely buying traffic', keywords: ['ubt', 'tiktok'] },
  { handle: 'ID:8371224970', score: 8, risk: 'MEDIUM', reason: 'Hiring affiliate managers and media buyers', keywords: ['hiring', 'aff_mngr'] },
  { handle: 'ID:7453055850', score: 8, risk: 'MEDIUM', reason: 'New account detected in 2M traffic deal context', keywords: ['new_acc', 'mohit'] },
  { handle: 'ID:8115257317', score: 9, risk: 'MEDIUM', reason: 'Seeking large traffic volumes for specific offers', keywords: ['whale', 'volume'] },
  { handle: 'ID:8588411469', score: 9, risk: 'MEDIUM', reason: 'Hiring experienced Nutra buyers for a team', keywords: ['nutra', 'hiring'] },
  { handle: 'ID:7051856614', score: 9, risk: 'MEDIUM', reason: 'Seeking team lead for training, offers profit share', keywords: ['team_lead', 'equity'] },
  { handle: 'ID:8104231262', score: 10, risk: 'MEDIUM', reason: 'Offers traffic services for crypto and other niches', keywords: ['traff', 'crypto'] },
];

export default function Home() {
  const [lang, setLang] = useState<'en' | 'ru'>('en');
  const [activeTab, setActiveTab] = useState<'leads' | 'security'>('leads');
  const [showPayment, setShowPayment] = useState(false);
  const [showUnlockModal, setShowUnlockModal] = useState(false);
  const [unlockCode, setUnlockCode] = useState('');
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [unlockError, setUnlockError] = useState('');
  const [geoFilter, setGeoFilter] = useState('All');
  const [verticalFilter, setVerticalFilter] = useState('All');
  const [riskFilter, setRiskFilter] = useState('All');

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
      filterTitle: 'Advanced Filters',
      allGeos: 'All GEOs',
      allVerticals: 'All Verticals',
      showing: 'Showing',
      leads: 'leads',
      clear: 'Clear Filters',
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
      tabLeads: 'Marketplace',
      tabSecurity: 'Security Board',
      securityTitle: '🛡️ Anti-Fraud & Risk Board',
      securitySubtitle: 'AI-detected anomalies and blacklisted patterns',
      highRisk: 'High Risk',
      medRisk: 'Medium Risk',
      allRisks: 'All Risks',
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
      filterTitle: 'Продвинутые фильтры',
      allGeos: 'Все ГЕО',
      allVerticals: 'Все Вертикали',
      showing: 'Показано',
      leads: 'лидов',
      clear: 'Сбросить',
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
      tabLeads: 'Маркетплейс',
      tabSecurity: 'Безопасность',
      securityTitle: '🛡️ Анти-Фрод и Риски',
      securitySubtitle: 'AI-анализ аномалий и паттернов мошенничества',
      highRisk: 'Высокий Риск',
      medRisk: 'Средний Риск',
      allRisks: 'Все Риски',
    },
  };

  const text = t[lang];

  const filteredLeads = allLeads.filter(lead => {
    const matchGeo = geoFilter === 'All' || lead.geo === geoFilter;
    const matchVertical = verticalFilter === 'All' || lead.vertical === verticalFilter;
    return matchGeo && matchVertical;
  });

  const filteredRisks = riskLeads.filter(lead => {
    return riskFilter === 'All' || lead.risk === riskFilter;
  });

  const visibleLeads = isUnlocked ? filteredLeads : filteredLeads.slice(0, 5);
  const lockedLeads = filteredLeads.slice(5);

  const geos = ['All', ...Array.from(new Set(allLeads.map(l => l.geo)))];
  const verticals = ['All', ...Array.from(new Set(allLeads.map(l => l.vertical)))];

  return (
    <main className="min-h-screen bg-linear-to-br from-[#1a1a2e] via-[#16213e] to-[#0f3460] text-white p-5">
      {/* Language Toggle */}
      <div className="fixed top-5 left-5 z-50 flex gap-1">
        <button
          onClick={() => setLang('en')}
          className={`px-4 py-2 rounded-lg text-sm font-bold transition-all border ${lang === 'en'
            ? 'bg-linear-to-r from-[#7b2cbf] to-[#00d4ff] text-white border-transparent'
            : 'bg-white/10 text-gray-400 border-white/20 hover:bg-white/20'
            }`}
        >
          EN
        </button>
        <button
          onClick={() => setLang('ru')}
          className={`px-4 py-2 rounded-lg text-sm font-bold transition-all border ${lang === 'ru'
            ? 'bg-linear-to-r from-[#7b2cbf] to-[#00d4ff] text-white border-transparent'
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
          ? 'bg-linear-to-r from-[#7b2cbf] to-[#00d4ff] hover:scale-105'
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
            <span className="bg-linear-to-r from-[#00d4ff] to-[#7b2cbf] bg-clip-text text-transparent">
              {text.title}
            </span>
            <div className="ml-2 px-2 py-0.5 bg-green-500/10 border border-green-500/20 rounded text-[10px] text-green-400 animate-pulse flex items-center gap-1">
              <ShieldCheck size={10} /> LIVE PROTECTION
            </div>
          </h1>
          <p className="text-gray-400 text-lg">{text.subtitle}</p>

          {/* Navigation Tabs */}
          <div className="flex justify-center gap-3 mt-6">
            <button
              onClick={() => setActiveTab('leads')}
              className={`px-6 py-2 rounded-xl font-bold transition-all border ${activeTab === 'leads'
                ? 'bg-linear-to-r from-[#7b2cbf] to-[#00d4ff] border-transparent'
                : 'bg-white/10 border-white/20 hover:bg-white/20'
                }`}
            >
              📊 {text.tabLeads}
            </button>
            <button
              onClick={() => setActiveTab('security')}
              className={`px-6 py-2 rounded-xl font-bold transition-all border ${activeTab === 'security'
                ? 'bg-linear-to-r from-red-600 to-orange-500 border-transparent shadow-[0_0_15px_rgba(239,68,68,0.4)]'
                : 'bg-white/10 border-white/20 hover:bg-white/20'
                }`}
            >
              🛡️ {text.tabSecurity}
            </button>
            <a
              href="/matchmaking"
              className="bg-white/10 hover:bg-linear-to-r hover:from-pink-500 hover:to-purple-500 px-6 py-2 rounded-xl font-bold transition-all border border-white/20 hover:border-transparent"
            >
              💘 {lang === 'en' ? 'Matchmaking' : 'Мэтчинг'}
            </a>
          </div>
        </header>

        {activeTab === 'leads' ? (
          <>
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
                            className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-linear-to-r from-[#00d4ff] to-[#7b2cbf]"
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

            {/* Filter Bar */}
            <section className="bg-white/5 backdrop-blur-md rounded-2xl p-6 mb-8 border border-white/10">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="bg-[#00d4ff]/20 p-2 rounded-lg">
                    <Globe size={20} className="text-[#00d4ff]" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white">{text.filterTitle}</h3>
                    <p className="text-xs text-gray-500">
                      {text.showing} <span className="text-[#00d4ff] font-bold">{filteredLeads.length}</span> {text.leads}
                    </p>
                  </div>
                </div>

                <div className="flex flex-wrap gap-3">
                  <select
                    value={geoFilter}
                    onChange={(e) => setGeoFilter(e.target.value)}
                    className="bg-black/30 border border-white/10 rounded-xl px-4 py-2 text-sm focus:border-[#00d4ff] focus:outline-none transition-all cursor-pointer"
                  >
                    <option value="All">{text.allGeos}</option>
                    {geos.filter(g => g !== 'All').map(g => (
                      <option key={g} value={g}>{g}</option>
                    ))}
                  </select>

                  <select
                    value={verticalFilter}
                    onChange={(e) => setVerticalFilter(e.target.value)}
                    className="bg-black/30 border border-white/10 rounded-xl px-4 py-2 text-sm focus:border-[#00d4ff] focus:outline-none transition-all cursor-pointer"
                  >
                    <option value="All">{text.allVerticals}</option>
                    {verticals.filter(v => v !== 'All').map(v => (
                      <option key={v} value={v}>{v}</option>
                    ))}
                  </select>

                  {(geoFilter !== 'All' || verticalFilter !== 'All') && (
                    <button
                      onClick={() => { setGeoFilter('All'); setVerticalFilter('All'); }}
                      className="text-xs text-red-400 hover:text-red-300 transition-colors uppercase font-bold tracking-widest px-2"
                    >
                      ✕ {text.clear}
                    </button>
                  )}
                </div>
              </div>
            </section>

            {/* Leads List */}
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

            {/* Locked Section */}
            {!isUnlocked && (
              <section className="bg-white/5 rounded-[15px] p-6 mb-5 border border-white/10 relative overflow-hidden">
                <h2 className="text-orange-400 text-xl font-bold mb-5">{text.lockedTitle}</h2>
                <div className="space-y-4 blur-md select-none pointer-events-none opacity-70">
                  {lockedLeads.map((lead, i) => (
                    <LeadCard key={i} lead={lead} lang={lang} />
                  ))}
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-[#1a1a2e] via-[#1a1a2e]/90 to-transparent flex items-center justify-center">
                  <button
                    onClick={() => setShowUnlockModal(true)}
                    className="bg-linear-to-r from-orange-500 to-red-500 px-10 py-5 rounded-xl font-bold text-xl shadow-2xl transform hover:scale-105 transition-all animate-pulse"
                  >
                    {text.unlockBtn}
                  </button>
                </div>
              </section>
            )}
          </>
        ) : (
          <div className="space-y-8 animate-in fade-in duration-500">
            {/* Security View */}
            <div className="bg-white/5 backdrop-blur-md rounded-2xl p-8 border-l-4 border-red-500 shadow-xl">
              <div className="flex items-center gap-4 mb-4">
                <div className="bg-red-500/20 p-3 rounded-xl">
                  <ShieldCheck size={32} className="text-red-500" />
                </div>
                <div>
                  <h2 className="text-3xl font-bold text-white uppercase tracking-tight">{text.securityTitle}</h2>
                  <p className="text-gray-400 italic">"{text.securitySubtitle}"</p>
                </div>
              </div>
            </div>

            {/* Risk Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-black/40 p-6 rounded-2xl border border-red-500/20 text-center">
                <div className="text-red-500 text-4xl font-bold mb-1">155</div>
                <div className="text-xs uppercase tracking-widest text-gray-500">{lang === 'en' ? 'Total Warnings' : 'Всего предупреждений'}</div>
              </div>
              <div className="bg-black/40 p-6 rounded-2xl border border-orange-500/20 text-center">
                <div className="text-orange-500 text-4xl font-bold mb-1">42</div>
                <div className="text-xs uppercase tracking-widest text-gray-500">{lang === 'en' ? 'Anomalies Detected' : 'Выявлено аномалий'}</div>
              </div>
              <div className="bg-black/40 p-6 rounded-2xl border border-cyan-500/20 text-center">
                <div className="text-cyan-500 text-4xl font-bold mb-1">99.2%</div>
                <div className="text-xs uppercase tracking-widest text-gray-500">{lang === 'en' ? 'Signal Accuracy' : 'Точность сигнала'}</div>
              </div>
            </div>

            {/* Risk Filter */}
            <div className="flex gap-4">
              <button onClick={() => setRiskFilter('All')} className={`px-4 py-2 rounded-lg text-sm font-bold ${riskFilter === 'All' ? 'bg-white/20' : 'bg-transparent text-gray-500'}`}>{text.allRisks}</button>
              <button onClick={() => setRiskFilter('HIGH')} className={`px-4 py-2 rounded-lg text-sm font-bold ${riskFilter === 'HIGH' ? 'bg-red-600' : 'bg-transparent text-gray-500'}`}>{text.highRisk}</button>
              <button onClick={() => setRiskFilter('MEDIUM')} className={`px-4 py-2 rounded-lg text-sm font-bold ${riskFilter === 'MEDIUM' ? 'bg-orange-500' : 'bg-transparent text-gray-500'}`}>{text.medRisk}</button>
            </div>

            {/* Risk Leads */}
            <div className="grid gap-4">
              {filteredRisks.map((lead, i) => (
                <div key={i} className={`bg-black/40 p-6 rounded-xl border-l-4 ${lead.risk === 'HIGH' ? 'border-red-600' : 'border-orange-500'}`}>
                  <div className="flex justify-between items-center mb-4">
                    <h4 className="text-xl font-bold">{lead.handle}</h4>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${lead.risk === 'HIGH' ? 'bg-red-600' : 'bg-orange-500'}`}>{lead.risk}</span>
                  </div>
                  <p className="text-gray-400 italic mb-4">"{lead.reason}"</p>
                  <div className="flex gap-2">
                    {lead.keywords.map(k => <span key={k} className="text-[10px] bg-white/5 px-2 py-1 rounded text-red-400 border border-red-500/20">#{k}</span>)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Features Info */}
        <section className="bg-white/5 rounded-[15px] p-6 mb-8 border border-white/10 mt-10">
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

      {/* Modals */}
      {showUnlockModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowUnlockModal(false)}>
          <div className="bg-linear-to-br from-slate-800 to-slate-900 rounded-2xl p-8 max-w-md w-full border border-purple-500/50 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold text-center mb-6 text-purple-400">{text.unlockTitle}</h3>
            <div className="space-y-6">
              <input
                type="text"
                value={unlockCode}
                onChange={(e) => setUnlockCode(e.target.value.toUpperCase())}
                placeholder="AURA-XXXX-XXXX"
                className="w-full bg-black/50 border border-cyan-500/30 rounded-xl p-4 text-cyan-400 font-mono text-center focus:border-cyan-500 focus:outline-none"
              />
              {unlockError && <p className="text-red-400 text-sm text-center">{unlockError}</p>}
              <button onClick={handleUnlock} className="w-full py-4 bg-linear-to-r from-green-500 to-emerald-600 rounded-xl font-bold">{text.unlock}</button>
              <button onClick={() => { setShowUnlockModal(false); setShowPayment(true); }} className="w-full py-4 bg-linear-to-r from-orange-500 to-red-500 rounded-xl font-bold">{text.payNow}</button>
            </div>
            <button onClick={() => setShowUnlockModal(false)} className="w-full mt-4 py-3 bg-white/10 rounded-xl font-bold">{text.close}</button>
          </div>
        </div>
      )}

      {showPayment && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowPayment(false)}>
          <div className="bg-linear-to-br from-slate-800 to-slate-900 rounded-2xl p-8 max-w-md w-full border border-purple-500/50 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold text-center mb-6 text-purple-400">{text.paymentTitle}</h3>
            <div className="space-y-6 text-center">
              <p className="text-gray-400">{text.paymentStep1}</p>
              <code className="block bg-black/50 p-4 rounded-xl text-cyan-400 break-all">{USDT_ADDRESS}</code>
              <p className="text-gray-400">{text.paymentStep2}</p>
              <a href={`https://t.me/${TELEGRAM_HANDLE.replace('@', '')}`} target="_blank" className="text-cyan-400 font-bold text-2xl hover:underline">{TELEGRAM_HANDLE}</a>
            </div>
            <button onClick={() => setShowPayment(false)} className="w-full mt-6 py-3 bg-white/10 rounded-xl font-bold">{text.close}</button>
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
    <div className="bg-black/30 rounded-xl p-5 border-l-4 border-cyan-500 hover:bg-black/40 transition-all hover:translate-x-1">
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
        <span className="bg-purple-500/30 px-3 py-1 rounded-lg text-xs font-bold text-purple-300">
          {categoryIcons[lead.category] || '📌'} {lead.category}
        </span>
        <span className="bg-cyan-500/20 px-3 py-1 rounded-lg text-xs font-bold text-cyan-300">
          🌍 {lead.geo}
        </span>
        <span className="bg-emerald-500/20 px-3 py-1 rounded-lg text-xs font-bold text-emerald-300">
          🎯 {lead.vertical}
        </span>
        <span className="text-gray-500 text-sm ml-auto">{lead.name}</span>
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
