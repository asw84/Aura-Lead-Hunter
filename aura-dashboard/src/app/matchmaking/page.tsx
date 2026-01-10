'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { domToPng } from 'modern-screenshot';
import { QRCodeCanvas } from 'qrcode.react';

// ========== CONFIGURATION (same as main page) ==========
const VALID_CODES = [
    'AURA-2026-LUKE',
    'AURA-2026-DEMO',
    'AURA-PAID-001',
    'AURA-PAID-002',
    'AURA-PAID-003',
];

const USDT_ADDRESS = 'TG3J6rQPBNfQgAg9e4esdY4zjpCRPrATq9';
const TELEGRAM_HANDLE = '@SergAI_BY';
// ====================================

// ========== MATCHING DATA ==========
// Generated from match_leads.py

interface Employer {
    contact: string;
    category: string;
    language: string;
    reason: string;
    conditions: string;
    vertical: string;
}

interface Buyer {
    contact: string;
    name: string;
    score: number;
    vertical: string;
    trafficType: string;
    volume: string;
    reason: string;
}

interface Match {
    employer: Employer;
    buyers: {
        buyer: Buyer;
        matchScore: number;
        messageToEmployer: string;
        messageToBuyer: string;
    }[];
}

const matchesData: Match[] = [
    {
        employer: {
            contact: '@ArbiTalent',
            category: 'agency_owner',
            language: '🇷🇺 RU',
            reason: 'Тимлид ищет байеров и лидеров с большими бюджетами',
            conditions: 'VIP Условия',
            vertical: 'General',
        },
        buyers: [
            {
                buyer: {
                    contact: 'ID:7453055850',
                    name: 'Mohit pal',
                    score: 9,
                    vertical: 'General',
                    trafficType: 'FB',
                    volume: '2M daily',
                    reason: 'Имеет 2М трафа в день, ищет прямой выход на реклов и эксклюзивные условия',
                },
                matchScore: 98,
                messageToEmployer: 'Здравствуйте! У меня есть топ-байер Mohit pal с объемами 2M daily. Как раз под ваши требования по большим бюджетам. Готовы обсудить? 📈',
                messageToBuyer: 'Mohit, this is a Tier-1 match! 🏢 @ArbiTalent (Agency Owner) is looking for whales with Traffic 2M+. This is a serious professional team. 💎',
            },
        ],
    },
    {
        employer: {
            contact: '@anastasiiaSSD',
            category: 'agency_owner',
            language: '🇷🇺 RU',
            reason: 'Набирает байеров и тимлидов для арбитражной команды',
            conditions: 'Ставка + %',
            vertical: 'General',
        },
        buyers: [
            {
                buyer: {
                    contact: 'ID:7453055850',
                    name: 'Mohit pal',
                    score: 9,
                    vertical: 'General',
                    trafficType: 'FB',
                    volume: '2M daily',
                    reason: 'Имеет 2М трафа в день, ищет стабильную команду',
                },
                matchScore: 95,
                messageToEmployer: 'Привет! Есть мощный байер Mohit pal (2M daily views). Идеально подходит для усиления вашей команды. 🤝',
                messageToBuyer: 'Mohit, check this: @anastasiiaSSD (Agency Owner) is expanding. Very stable team, looking for seniors. High level stuff! 🏢',
            },
        ],
    },
    {
        employer: {
            contact: '@viktori950',
            category: 'team_lead',
            language: '🇷🇺 RU',
            reason: 'Тимлид ищет крипто-байера с опытом и креативом',
            conditions: 'Стандартные',
            vertical: 'Crypto',
        },
        buyers: [
            {
                buyer: {
                    contact: 'ID:552056',
                    name: 'Elnara Petrova',
                    score: 8,
                    vertical: 'Crypto',
                    trafficType: 'Mixed',
                    volume: '-',
                    reason: 'Владелец канала обсуждает крипту и NFT',
                },
                matchScore: 98,
                messageToEmployer: 'Привет! 👋 Elnara Petrova (ID:552056) — владелец канала, эксперт в Crypto/NFT. Подходит под ваш крипто-запрос на 98%. 💎',
                messageToBuyer: 'Эльнара, нашел отличного тимлида @viktori950. Ищут именно крипто-байеров с опытом. Твой профиль подходит идеально! 🚀',
            },
        ],
    },
    {
        employer: {
            contact: '@malina_off',
            category: 'team_lead',
            language: '🇷🇺 RU',
            reason: 'Тимлид ищет байеров и менеджеров для своей тимы',
            conditions: 'Бонусы',
            vertical: 'General',
        },
        buyers: [
            {
                buyer: {
                    contact: 'ID:7453055850',
                    name: 'Mohit pal',
                    score: 9,
                    vertical: 'General',
                    trafficType: 'FB',
                    volume: '2M daily',
                    reason: 'Ищет адекватную команду для долгосрока',
                },
                matchScore: 91,
                messageToEmployer: 'Привет! Mohit pal (2M daily) ищет команду. Ваши условия по расширению как раз подходят. Коннектим? 🤝',
                messageToBuyer: 'Mohit, another solid one: @malina_off is actively hiring. Very good reviews, professional environment. No more "bad vibes"! ✨',
            },
        ],
    },
    {
        employer: {
            contact: '@reklama_hunter',
            category: 'team_lead',
            language: '🇷🇺 RU',
            reason: 'Ищет байера с опытом в крипте, предлагает ставку и бонусы',
            conditions: 'Ставка + Бонусы',
            vertical: 'Crypto',
        },
        buyers: [
            {
                buyer: {
                    contact: '@arc_abdulkareem',
                    name: 'Abdulkareem Lawal',
                    score: 9,
                    vertical: 'General',
                    trafficType: 'FB',
                    volume: '-',
                    reason: 'Ищет офферы, управляет трафом, оптимизирует конверт.',
                },
                matchScore: 99,
                messageToEmployer: 'Привет! 👋\n\nУвидел, что ищете байера. У меня есть кандидат под ваш запрос:\n\n📌 Abdulkareem Lawal\n• льёт FB, Score: 9/10\n• Описание: Ищет офферы, управляет трафом, оптимизирует конверт.\n\nКонтакт: ID:1254927282',
                messageToBuyer: 'Привет! 👋\n\nНашёл тимлида под твой профиль:\n\n📌 @reklama_hunter\n• Категория: team_lead\n• 🇷🇺 RU\n\nОписание: Ищет байера с опытом в крипте, предлагает ставку и бонусы\n\nЕсли интересно — могу дать контакт. 🚀',
            },
        ],
    },
    {
        employer: {
            contact: '@aliona_nda',
            category: 'team_lead',
            language: '🇷🇺 RU',
            reason: 'Тимлид шукает байера с опытом в команду',
            conditions: 'Стандартные',
            vertical: 'General',
        },
        buyers: [
            {
                buyer: {
                    contact: '@realsteel2022',
                    name: 'RealSteel',
                    score: 8,
                    vertical: 'General',
                    trafficType: 'FB/TT',
                    volume: '-',
                    reason: 'Ищет офферы, запускает рекламу в FB/TT, опыт в IM.',
                },
                matchScore: 99,
                messageToEmployer: 'Привет! 👋\n\nЕсть сильный байер под вашу вакансию:\n\n📌 RealSteel\n• FB/TT, Score: 8/10\n• Опыт в арбитраже и оптимизации\n\nКонтакт: ID:548043583',
                messageToBuyer: 'Привет! 👋\n\nНашёл тимлида, который ищет опытных в команду:\n\n📌 @aliona_nda\n• 🇷🇺 RU\n• Сильный коллектив\n\nХочешь познакомиться? 🚀',
            },
        ],
    },
    {
        employer: {
            contact: '@cpatrackmaster',
            category: 'agency_owner',
            language: '🇷🇺 RU',
            reason: 'Владелец CPA сети ищет рекламодателей и сильные команды для коллаба',
            conditions: 'Эксклюзив',
            vertical: 'CPA / Network',
        },
        buyers: [
            {
                buyer: {
                    contact: '@xboss01',
                    name: 'Mohit pal',
                    score: 9,
                    vertical: 'Dating',
                    trafficType: 'FB',
                    volume: '2M daily',
                    reason: 'Имеет 2М трафа в день, ищет прямой выход на реклов и эксклюзивные условия',
                },
                matchScore: 95,
                messageToEmployer: 'Привет! 👋\n\nУ меня есть топ-байер с огромными объемами (2M daily) на Dating. \n\n📌 Mohit pal\n• Ищет эксклюзивные офферы и прямой выход.\n\nКонтакт: ID:7453055850',
                messageToBuyer: 'Привет! 👋\n\nНашёл для тебя Agency Owner-а (владелец CPA сети):\n\n📌 @cpatrackmaster\n• Прямые офферы, эксклюзивные условия для больших объемов.\n\nИнтересно пообщаться? 🚀',
            },
        ],
    },
    {
        employer: {
            contact: '@gelukster',
            category: 'potential_employer',
            language: '🇺🇦 UA',
            reason: 'Шукає байера для ліття трафіку, пропонує 70% від з',
            conditions: '70% Profit Share',
            vertical: 'General',
        },
        buyers: [
            {
                buyer: {
                    contact: '@Tp8000',
                    name: 'Lucky',
                    score: 8,
                    vertical: 'General',
                    trafficType: 'CPI',
                    volume: '-',
                    reason: 'Ищет CPI кампании и источники трафика',
                },
                matchScore: 89,
                messageToEmployer: 'Привет! 👋\n\nЕсть байер под ваши условия (70%):\n\n📌 Lucky\n• Специалист по CPI, Score: 8/10\n\nКонтакт: ID:7013566461',
                messageToBuyer: 'Привет! 👋\n\nНашёл предложение: 70% от профита.\n\n📌 @gelukster\n• 🇺🇦 UA\n• Ищет байеров на долгосрок\n\nХочешь обсудить? 🚀',
            },
        ],
    },
];


export default function Matchmaking() {
    const [lang, setLang] = useState<'en' | 'ru'>('ru');
    const [selectedMatch, setSelectedMatch] = useState<{
        employer: Employer;
        buyer: Match['buyers'][0];
    } | null>(null);
    const [copiedMessage, setCopiedMessage] = useState<string | null>(null);
    const [isUnlocked, setIsUnlocked] = useState(false);
    const [showUnlockModal, setShowUnlockModal] = useState(false);
    const [showPayment, setShowPayment] = useState(false);
    const [unlockCode, setUnlockCode] = useState('');
    const [unlockError, setUnlockError] = useState('');
    const [isGeneratingImage, setIsGeneratingImage] = useState<number | null>(null);

    // Refs for capturing match cards
    const matchRefs = useRef<Map<number, HTMLDivElement>>(new Map());

    // Share match as image
    const shareAsImage = async (matchIndex: number) => {
        const element = matchRefs.current.get(matchIndex);
        if (!element) return;

        setIsGeneratingImage(matchIndex);

        try {
            // Use modern-screenshot which supports modern CSS including oklab
            const dataUrl = await domToPng(element, {
                scale: 2, // Higher resolution
                backgroundColor: '#1a1a2e',
                filter: (node: Node) => {
                    // Filter out the share button from the screenshot
                    if (node instanceof HTMLElement && node.tagName === 'BUTTON') {
                        return !node.textContent?.includes('PNG');
                    }
                    return true;
                },
            });

            // Download the image
            const match = visibleMatches[matchIndex];
            const fileName = `aura_match_${match.employer.contact.replace('@', '')}_${Date.now()}.png`;

            const a = document.createElement('a');
            a.href = dataUrl;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

        } catch (error) {
            console.error('Error generating image:', error);
            alert(lang === 'en' ? 'Image generation failed. Please try taking a screenshot.' : 'Ошибка генерации. Попробуйте сделать скриншот.');
        } finally {
            setIsGeneratingImage(null);
        }
    };

    // Check for unlock on mount (same logic as main page)
    useEffect(() => {
        const savedUnlock = localStorage.getItem('aura_unlocked');
        if (savedUnlock === 'true') {
            setIsUnlocked(true);
            return;
        }

        const urlParams = new URLSearchParams(window.location.search);
        const keyParam = urlParams.get('key');
        if (keyParam && VALID_CODES.includes(keyParam.toUpperCase())) {
            setIsUnlocked(true);
            localStorage.setItem('aura_unlocked', 'true');
            localStorage.setItem('aura_code', keyParam.toUpperCase());
            window.history.replaceState({}, '', window.location.pathname);
        }
    }, []);

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

    // Show only 2 matches for free
    const FREE_MATCHES = 2;
    const visibleMatches = isUnlocked ? matchesData : matchesData.slice(0, FREE_MATCHES);
    const lockedMatches = matchesData.slice(FREE_MATCHES);

    const t = {
        en: {
            title: 'AI MATCHMAKING',
            subtitle: 'Tinder for Affiliate Marketing',
            backToLeads: '← Back to Leads',
            employers: 'Employers',
            matchedBuyers: 'Matched Buyers',
            matchScore: 'Match',
            conditions: 'Conditions',
            vertical: 'Vertical',
            viewMessages: 'View Messages',
            copyMessage: 'Copy',
            copied: 'Copied!',
            messageToEmployer: 'Message to Employer',
            messageToBuyer: 'Message to Buyer',
            close: 'Close',
            totalMatches: 'Total Matches',
            employers_label: 'Employers',
            avgScore: 'Avg Match Score',
        },
        ru: {
            title: 'AI MATCHMAKING',
            subtitle: 'Tinder для арбитража',
            backToLeads: '← К лидам',
            employers: 'Работодатели',
            matchedBuyers: 'Подходящие байеры',
            matchScore: 'Мэтч',
            conditions: 'Условия',
            vertical: 'Вертикаль',
            viewMessages: 'Сообщения',
            copyMessage: 'Копировать',
            copied: 'Скопировано!',
            messageToEmployer: 'Сообщение работодателю',
            messageToBuyer: 'Сообщение байеру',
            close: 'Закрыть',
            totalMatches: 'Всего мэтчей',
            employers_label: 'Работодателей',
            avgScore: 'Средний мэтч',
        },
    };

    const text = t[lang];

    const totalMatches = matchesData.reduce((acc, m) => acc + m.buyers.length, 0);
    const avgScore = Math.round(
        matchesData.reduce((acc, m) => acc + m.buyers.reduce((a, b) => a + b.matchScore, 0), 0) / totalMatches
    );

    const copyToClipboard = (message: string, type: string) => {
        navigator.clipboard.writeText(message);
        setCopiedMessage(type);
        setTimeout(() => setCopiedMessage(null), 2000);
    };

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
            </div>

            {/* Back Button */}
            <Link
                href="/"
                className="fixed top-5 right-5 z-50 px-6 py-3 rounded-xl font-bold bg-white/10 hover:bg-white/20 transition-all border border-white/20"
            >
                {text.backToLeads}
            </Link>

            <div className="max-w-[1400px] mx-auto pt-16">
                {/* Header */}
                <header className="text-center py-10 px-5 bg-white/5 rounded-[20px] mb-8 backdrop-blur-sm border border-white/10">
                    <h1 className="text-4xl md:text-5xl font-bold mb-2 flex items-center justify-center gap-3">
                        <span className="text-5xl">💘</span>
                        <span className="bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 bg-clip-text text-transparent">
                            {text.title}
                        </span>
                    </h1>
                    <p className="text-gray-400 text-lg">{text.subtitle}</p>
                    <p className="text-sm text-gray-500 mt-2">Powered by Aura Lead Hunter 2.0</p>
                </header>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-5 mb-8">
                    <div className="bg-white/5 backdrop-blur-sm rounded-[15px] p-6 text-center border border-white/10">
                        <div className="text-4xl font-bold bg-gradient-to-r from-pink-500 to-purple-500 bg-clip-text text-transparent">
                            {totalMatches}
                        </div>
                        <div className="text-gray-400 text-sm mt-2">💘 {text.totalMatches}</div>
                    </div>
                    <div className="bg-white/5 backdrop-blur-sm rounded-[15px] p-6 text-center border border-white/10">
                        <div className="text-4xl font-bold bg-gradient-to-r from-purple-500 to-cyan-500 bg-clip-text text-transparent">
                            {matchesData.length}
                        </div>
                        <div className="text-gray-400 text-sm mt-2">🏢 {text.employers_label}</div>
                    </div>
                    <div className="bg-white/5 backdrop-blur-sm rounded-[15px] p-6 text-center border border-white/10">
                        <div className="text-4xl font-bold bg-gradient-to-r from-cyan-500 to-green-500 bg-clip-text text-transparent">
                            {avgScore}%
                        </div>
                        <div className="text-gray-400 text-sm mt-2">🎯 {text.avgScore}</div>
                    </div>
                </div>

                {/* Matches */}
                <div className="space-y-8">
                    {visibleMatches.map((match, idx) => (
                        <div
                            key={idx}
                            ref={(el) => {
                                if (el) matchRefs.current.set(idx, el);
                            }}
                            className="bg-white/5 rounded-[20px] p-6 border border-white/10 hover:border-purple-500/50 transition-all"
                        >
                            <div className="grid md:grid-cols-[1fr_auto_1fr] gap-6 items-start">
                                {/* Employer Card */}
                                <div className="bg-gradient-to-br from-purple-900/50 to-pink-900/30 rounded-xl p-5 border border-purple-500/30">
                                    <div className="flex items-center gap-2 mb-3">
                                        <span className="text-2xl">🏢</span>
                                        <span className="text-xs bg-purple-500/30 px-2 py-1 rounded-full text-purple-300">
                                            {match.employer.category}
                                        </span>
                                        <span className="text-xs bg-white/10 px-2 py-1 rounded-full">
                                            {match.employer.language}
                                        </span>
                                    </div>

                                    <a
                                        href={`https://t.me/${match.employer.contact.replace('@', '')}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-xl font-bold text-purple-400 hover:text-purple-300 transition-colors"
                                    >
                                        {match.employer.contact}
                                    </a>

                                    <p className="text-gray-300 mt-3 text-sm leading-relaxed">
                                        "{match.employer.reason}"
                                    </p>

                                    <div className="flex flex-wrap gap-2 mt-4">
                                        <span className="bg-pink-500/20 text-pink-300 px-3 py-1 rounded-lg text-xs">
                                            💼 {match.employer.conditions}
                                        </span>
                                        <span className="bg-cyan-500/20 text-cyan-300 px-3 py-1 rounded-lg text-xs">
                                            📊 {match.employer.vertical}
                                        </span>
                                    </div>
                                </div>

                                {/* Arrow/Connection */}
                                <div className="flex items-center justify-center py-4">
                                    <div className="relative">
                                        <div className="text-4xl animate-pulse">💘</div>
                                        <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-xs text-gray-500">
                                            AI Match
                                        </div>
                                    </div>
                                </div>

                                {/* Buyers Cards */}
                                <div className="space-y-3">
                                    {match.buyers.map((b, bidx) => (
                                        <div
                                            key={bidx}
                                            className="bg-gradient-to-br from-cyan-900/50 to-blue-900/30 rounded-xl p-4 border border-cyan-500/30 hover:border-cyan-400/50 transition-all group cursor-pointer"
                                            onClick={() => setSelectedMatch({ employer: match.employer, buyer: b })}
                                        >
                                            <div className="flex justify-between items-start mb-2">
                                                <div className="flex items-center gap-2">
                                                    <span className="text-xl">👤</span>
                                                    <a
                                                        href={`https://t.me/${b.buyer.contact.replace('@', '')}`}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="font-bold text-cyan-400 hover:text-cyan-300"
                                                        onClick={(e) => e.stopPropagation()}
                                                    >
                                                        {b.buyer.contact}
                                                    </a>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <span className={`px-3 py-1 rounded-full text-sm font-bold ${b.matchScore >= 90 ? 'bg-green-500/30 text-green-300' :
                                                        b.matchScore >= 80 ? 'bg-yellow-500/30 text-yellow-300' :
                                                            'bg-orange-500/30 text-orange-300'
                                                        }`}>
                                                        {b.matchScore}%
                                                    </span>
                                                    <span className="bg-gradient-to-r from-[#7b2cbf] to-[#00d4ff] px-2 py-1 rounded-full text-xs font-bold">
                                                        {b.buyer.score}/10
                                                    </span>
                                                </div>
                                            </div>

                                            <p className="text-sm text-gray-400 mb-2">{b.buyer.name}</p>
                                            <p className="text-xs text-gray-500">{b.buyer.reason}</p>

                                            <div className="flex flex-wrap gap-2 mt-3">
                                                {b.buyer.trafficType && (
                                                    <span className="bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded text-xs">
                                                        🚀 {b.buyer.trafficType}
                                                    </span>
                                                )}
                                                {b.buyer.volume && (
                                                    <span className="bg-green-500/20 text-green-300 px-2 py-0.5 rounded text-xs">
                                                        📊 {b.buyer.volume}
                                                    </span>
                                                )}
                                                <span className="bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded text-xs">
                                                    📁 {b.buyer.vertical}
                                                </span>
                                            </div>

                                            <div className="mt-3 text-center opacity-0 group-hover:opacity-100 transition-opacity">
                                                <span className="text-xs bg-white/10 px-3 py-1 rounded-full text-gray-400">
                                                    👆 {text.viewMessages}
                                                </span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Branding footer for image export */}
                            <div className="mt-4 pt-4 border-t border-white/10 flex justify-between items-center text-xs text-gray-500">
                                <span>💘 AI Matchmaking by Aura Lead Hunter 2.0</span>
                                <div className="flex items-center gap-3">
                                    <span>@SergAI_BY</span>
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            shareAsImage(idx);
                                        }}
                                        disabled={isGeneratingImage === idx}
                                        className="bg-gradient-to-r from-cyan-500/80 to-purple-500/80 hover:from-cyan-500 hover:to-purple-500 px-3 py-1 rounded-lg text-xs font-bold transition-all disabled:opacity-50 disabled:cursor-wait flex items-center gap-1 text-white"
                                    >
                                        {isGeneratingImage === idx ? (
                                            <>
                                                <span className="animate-spin">⏳</span>
                                                {lang === 'en' ? 'Saving...' : 'Сохранение...'}
                                            </>
                                        ) : (
                                            <>
                                                📸 {lang === 'en' ? 'Save PNG' : 'Сохранить PNG'}
                                            </>
                                        )}
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Locked Matches Section */}
                {!isUnlocked && lockedMatches.length > 0 && (
                    <section className="bg-white/5 rounded-[20px] p-6 mt-8 border border-orange-500/30 relative overflow-hidden">
                        <h2 className="text-orange-400 text-xl font-bold mb-5">
                            🔒 {lang === 'en' ? `LOCKED: ${lockedMatches.length} More Matches` : `ЗАБЛОКИРОВАНО: Ещё ${lockedMatches.length} мэтчей`}
                        </h2>

                        {/* Blurred Content */}
                        <div className="space-y-4 blur-md select-none pointer-events-none opacity-70">
                            {lockedMatches.slice(0, 3).map((match, idx) => (
                                <div key={idx} className="bg-black/30 rounded-xl p-5 border-l-4 border-orange-500">
                                    <div className="flex justify-between items-center">
                                        <span className="text-purple-400 font-bold">{match.employer.contact}</span>
                                        <span className="bg-gradient-to-r from-[#7b2cbf] to-[#00d4ff] px-4 py-1 rounded-full text-sm font-bold">
                                            💘 {match.buyers.length} matches
                                        </span>
                                    </div>
                                    <p className="text-gray-500 mt-2 italic">Premium match data...</p>
                                </div>
                            ))}
                        </div>

                        {/* Overlay with Unlock Button */}
                        <div className="absolute inset-0 bg-gradient-to-t from-[#1a1a2e] via-[#1a1a2e]/90 to-transparent flex items-center justify-center">
                            <button
                                onClick={() => setShowUnlockModal(true)}
                                className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 px-10 py-5 rounded-xl font-bold text-xl shadow-2xl transform hover:scale-105 transition-all animate-pulse"
                            >
                                {lang === 'en' ? '🔓 UNLOCK ALL MATCHES — $50 USDT' : '🔓 РАЗБЛОКИРОВАТЬ ВСЕ — $50 USDT'}
                            </button>
                        </div>
                    </section>
                )}

                {/* Unlocked Badge */}
                {isUnlocked && (
                    <div className="text-center py-4">
                        <span className="bg-green-500/20 text-green-400 px-6 py-2 rounded-full font-bold border border-green-500/30">
                            ✅ {lang === 'en' ? 'FULL ACCESS UNLOCKED' : 'ПОЛНЫЙ ДОСТУП РАЗБЛОКИРОВАН'}
                        </span>
                    </div>
                )}

                {/* Footer */}
                <footer className="text-center text-gray-500 py-10">
                    <p>Generated by Aura Lead Hunter 2.0 | AI-Powered Matchmaking Engine</p>
                    <p className="text-xs mt-2">Solution Architecture by @SergAI_BY</p>
                </footer>
            </div>

            {/* Unlock Modal */}
            {showUnlockModal && (
                <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowUnlockModal(false)}>
                    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 max-w-md w-full border border-purple-500/50 shadow-2xl" onClick={(e) => e.stopPropagation()}>
                        <h3 className="text-2xl font-bold text-center mb-6 text-purple-400">
                            {lang === 'en' ? '🔓 Unlock All Matches' : '🔓 Разблокировать все мэтчи'}
                        </h3>

                        <div className="space-y-6">
                            <div>
                                <label className="text-gray-400 mb-2 block">{lang === 'en' ? 'Enter your unlock code:' : 'Введите код разблокировки:'}</label>
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
                                {lang === 'en' ? 'UNLOCK' : 'РАЗБЛОКИРОВАТЬ'}
                            </button>

                            <div className="relative">
                                <div className="absolute inset-0 flex items-center">
                                    <div className="w-full border-t border-gray-600"></div>
                                </div>
                                <div className="relative flex justify-center text-sm">
                                    <span className="px-2 bg-slate-800 text-gray-500">{lang === 'en' ? "Don't have a code?" : 'Нет кода?'}</span>
                                </div>
                            </div>

                            <button
                                onClick={() => { setShowUnlockModal(false); setShowPayment(true); }}
                                className="w-full py-4 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 rounded-xl font-bold text-lg transition-all"
                            >
                                💳 {lang === 'en' ? 'Pay $50 USDT' : 'Оплатить $50 USDT'}
                            </button>
                        </div>

                        <button
                            onClick={() => setShowUnlockModal(false)}
                            className="w-full mt-4 py-3 bg-white/10 hover:bg-white/20 rounded-xl font-bold transition-all border border-white/20"
                        >
                            {lang === 'en' ? 'Close' : 'Закрыть'}
                        </button>
                    </div>
                </div>
            )}

            {/* Payment Modal */}
            {showPayment && (
                <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowPayment(false)}>
                    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 max-w-md w-full border border-purple-500/50 shadow-2xl" onClick={(e) => e.stopPropagation()}>
                        <h3 className="text-2xl font-bold text-center mb-6 text-purple-400">
                            💳 {lang === 'en' ? 'Payment Instructions' : 'Инструкция по оплате'}
                        </h3>

                        <div className="space-y-6">
                            <div>
                                <p className="text-gray-400 mb-2">{lang === 'en' ? 'Send $50 USDT (TRC20) to:' : 'Отправьте $50 USDT (TRC20) на:'}</p>
                                <div className="bg-black/50 p-4 rounded-xl border border-cyan-500/30">
                                    <code className="text-cyan-400 text-sm break-all font-mono">{USDT_ADDRESS}</code>
                                </div>
                                <p className="text-xs text-gray-500 mt-2">Network: TRC20 (Tron)</p>
                            </div>

                            <div className="flex justify-center">
                                <div className="bg-white p-3 rounded-xl shadow-lg border-4 border-purple-500/20">
                                    <QRCodeCanvas
                                        value={USDT_ADDRESS}
                                        size={180}
                                        level="H"
                                        includeMargin={false}
                                        imageSettings={{
                                            src: "/aura.png",
                                            x: undefined,
                                            y: undefined,
                                            height: 40,
                                            width: 40,
                                            excavate: true,
                                        }}
                                    />
                                </div>
                            </div>

                            <div>
                                <p className="text-gray-400 mb-2">{lang === 'en' ? 'After payment, DM for your unlock code:' : 'После оплаты напишите для получения кода:'}</p>
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
                            {lang === 'en' ? 'Close' : 'Закрыть'}
                        </button>
                    </div>
                </div>
            )}

            {/* Message Modal */}
            {selectedMatch && (
                <div
                    className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
                    onClick={() => setSelectedMatch(null)}
                >
                    <div
                        className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 max-w-2xl w-full border border-purple-500/50 shadow-2xl max-h-[90vh] overflow-y-auto"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="flex justify-between items-center mb-6">
                            <h3 className="text-xl font-bold text-purple-400">
                                💬 Ready-to-Send Messages
                            </h3>
                            <button
                                onClick={() => setSelectedMatch(null)}
                                className="text-gray-400 hover:text-white text-2xl"
                            >
                                ✕
                            </button>
                        </div>

                        <div className="space-y-6">
                            {/* Message to Employer */}
                            <div>
                                <div className="flex justify-between items-center mb-2">
                                    <h4 className="text-sm font-bold text-pink-400 flex items-center gap-2">
                                        <span>📤</span> {text.messageToEmployer}
                                        <span className="text-xs text-gray-500">→ {selectedMatch.employer.contact}</span>
                                    </h4>
                                    <button
                                        onClick={() => copyToClipboard(selectedMatch.buyer.messageToEmployer, 'employer')}
                                        className={`px-3 py-1 rounded-lg text-sm transition-all ${copiedMessage === 'employer'
                                            ? 'bg-green-500 text-white'
                                            : 'bg-white/10 hover:bg-white/20 text-gray-300'
                                            }`}
                                    >
                                        {copiedMessage === 'employer' ? text.copied : text.copyMessage}
                                    </button>
                                </div>
                                <div className="bg-black/50 rounded-xl p-4 border border-pink-500/20">
                                    <pre className="text-gray-300 text-sm whitespace-pre-wrap font-sans">
                                        {selectedMatch.buyer.messageToEmployer}
                                    </pre>
                                </div>
                            </div>

                            {/* Message to Buyer */}
                            <div>
                                <div className="flex justify-between items-center mb-2">
                                    <h4 className="text-sm font-bold text-cyan-400 flex items-center gap-2">
                                        <span>📤</span> {text.messageToBuyer}
                                        <span className="text-xs text-gray-500">→ {selectedMatch.buyer.buyer.contact}</span>
                                    </h4>
                                    <button
                                        onClick={() => copyToClipboard(selectedMatch.buyer.messageToBuyer, 'buyer')}
                                        className={`px-3 py-1 rounded-lg text-sm transition-all ${copiedMessage === 'buyer'
                                            ? 'bg-green-500 text-white'
                                            : 'bg-white/10 hover:bg-white/20 text-gray-300'
                                            }`}
                                    >
                                        {copiedMessage === 'buyer' ? text.copied : text.copyMessage}
                                    </button>
                                </div>
                                <div className="bg-black/50 rounded-xl p-4 border border-cyan-500/20">
                                    <pre className="text-gray-300 text-sm whitespace-pre-wrap font-sans">
                                        {selectedMatch.buyer.messageToBuyer}
                                    </pre>
                                </div>
                            </div>
                        </div>

                        <button
                            onClick={() => setSelectedMatch(null)}
                            className="w-full mt-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-xl font-bold transition-all"
                        >
                            {text.close}
                        </button>
                    </div>
                </div>
            )}
        </main>
    );
}
