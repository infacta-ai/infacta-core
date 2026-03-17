export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({
      error: "Method not allowed"
    });
  }

  try {
    const { mode, text, language } = req.body || {};

    if (mode !== "contract_analysis") {
      return res.status(400).json({
        error: "Unsupported mode"
      });
    }

    if (!text || typeof text !== "string" || !text.trim()) {
      return res.status(400).json({
        error: "Empty text"
      });
    }

    const analysis = runContractAnalysis(text, language || "uk");
    return res.status(200).json(analysis);
  } catch (error) {
    return res.status(500).json({
      error: "Internal server error",
      details: error.message
    });
  }
}

function runContractAnalysis(text, language) {
  const normalized = text.toLowerCase();
  const isTemplate = detectTemplate(normalized);

  const structureMap = {
    parties: hasAny(normalized, [
      "сторони",
      "сторона 1",
      "сторона 2",
      "позичальник",
      "кредитодавець",
      "орендодавець",
      "орендар",
      "замовник",
      "виконавець"
    ]),
    subject: hasAny(normalized, [
      "предмет договору",
      "предмет",
      "цей договір регулює",
      "зобов'язується надати",
      "надає послуги",
      "передає у користування"
    ]),
    obligations: hasAny(normalized, [
      "права та обов'язки",
      "обов'язки сторін",
      "зобов'язаний",
      "має право",
      "зобов'язуються"
    ]),
    payment: hasAny(normalized, [
      "ціна",
      "вартість",
      "оплата",
      "платіж",
      "відсотк",
      "коміс",
      "щомісячний платіж",
      "тариф"
    ]),
    liability: hasAny(normalized, [
      "відповідальність сторін",
      "відповідальність",
      "штраф",
      "пеня",
      "неустойка"
    ]),
    termination: hasAny(normalized, [
      "розірвання",
      "припинення",
      "строк дії",
      "термін дії",
      "достроково"
    ])
  };

  const missingElements = [];

  if (!structureMap.parties && !isTemplate) {
    missingElements.push("Недостатньо чітко визначені сторони договору");
  }
  if (!structureMap.subject) {
    missingElements.push("Слабко або нечітко визначений предмет договору");
  }
  if (!structureMap.obligations) {
    missingElements.push("Недостатньо виписані права та обов’язки сторін");
  }
  if (!structureMap.payment) {
    missingElements.push("Слабко визначені умови оплати / вартості");
  }
  if (!structureMap.liability) {
    missingElements.push("Не виявлено або слабо виписано відповідальність сторін");
  }
  if (!structureMap.termination) {
    missingElements.push("Не виявлено або слабо виписано порядок припинення / розірвання");
  }

  const risks = [];
  const practicalImpact = [];
  const financialImpact = [];
  const questions = [];
  const notes = [];

  if (hasAny(normalized, [
    "в односторонньому порядку",
    "має право змінити",
    "може змінювати тарифи",
    "без додаткового погодження"
  ])) {
    risks.push("Є ознаки можливості односторонньої зміни умов другою стороною.");
    practicalImpact.push("Інша сторона може змінити окремі умови без реального балансу впливу з вашого боку.");
    questions.push("Які саме умови можуть змінюватися в односторонньому порядку і як вас мають повідомити?");
  }

  if (hasAny(normalized, [
    "штраф",
    "пеня",
    "неустойка"
  ])) {
    risks.push("Передбачені штрафні санкції або пеня.");
    practicalImpact.push("При порушенні строків чи умов договору можуть виникнути додаткові витрати.");
    questions.push("За які саме дії або прострочення нараховується штраф чи пеня?");
  }

  if (hasAny(normalized, [
    "автоматично продовжується",
    "автопролонгація",
    "вважається продовженим"
  ])) {
    risks.push("Є ознаки автоматичного продовження договору.");
    practicalImpact.push("Договір може продовжитися автоматично, якщо ви вчасно не подасте заперечення або заяву.");
    questions.push("Який строк і форма повідомлення для відмови від продовження договору?");
  }

  if (hasAny(normalized, [
    "страхування",
    "страховка",
    "страховий платіж"
  ])) {
    risks.push("У договорі є умови щодо страхування.");
    practicalImpact.push("Окрім базового платежу можуть бути додаткові витрати на страхування.");
    financialImpact.push("Потрібно окремо перевірити чи страхування є обов’язковим, добровільним, разовим чи щорічним.");
    questions.push("Чи можна обрати іншу страхову компанію, чи дозволена лише компанія, пов’язана з банком/контрагентом?");
  }

  if (hasAny(normalized, [
    "комісія",
    "разова комісія",
    "щомісячна комісія",
    "адміністративний збір"
  ])) {
    risks.push("Є додаткові комісії або збори понад основний платіж.");
    practicalImpact.push("Фактична вартість договору може бути вищою, ніж здається з основної суми.");
    financialImpact.push("Слід окремо порахувати суму всіх комісій, супутніх платежів та обов’язкових зборів.");
    questions.push("Який повний перелік додаткових платежів при укладенні та виконанні договору?");
  }

  if (hasAny(normalized, [
    "відсоткова ставка",
    "процентна ставка",
    "річних",
    "%"
  ])) {
    practicalImpact.push("Фінансові умови мають прямий вплив на реальні витрати користувача.");
    financialImpact.push(extractFinancialNote(text));
    questions.push("Чи ставка є фіксованою чи змінною, і за яких умов вона може збільшитися?");
  }

  if (!structureMap.liability) {
    risks.push("Немає чітко видимого блоку відповідальності сторін.");
    practicalImpact.push("У разі спору може бути складніше зрозуміти наслідки порушення умов.");
  }

  if (!structureMap.termination) {
    risks.push("Немає чітко видимого механізму розірвання або дострокового припинення.");
    practicalImpact.push("Вихід із договору може виявитися складнішим або дорожчим, ніж очікується.");
  }

  if (isTemplate) {
    notes.push("Виявлено ознаки того, що документ є зразком/шаблоном договору.");
    notes.push("Для шаблону відсутність персональних даних сторін не вважається проблемою.");
  }

  if (!risks.length) {
    risks.push("Явних критичних ризиків на базовому патерн-рівні не виявлено, але потрібна ручна перевірка тексту.");
  }

  if (!practicalImpact.length) {
    practicalImpact.push("Практичні наслідки залежать від деталей виконання договору та прихованих умов у повному тексті.");
  }

  if (!financialImpact.length) {
    financialImpact.push("Явних числових фінансових наслідків автоматично не виділено. Потрібен глибший розрахунок.");
  }

  if (!questions.length) {
    questions.push("Чи є у договорі додатки, тарифи, правила або інші документи, на які він посилається?");
  }

  if (!notes.length) {
    notes.push("Результат базується на первинному структурному аналізі тексту.");
  }

  const strengthIndex = calculateStrengthIndex(structureMap, risks);

  return {
    mode: "contract_analysis",
    language,
    summary: buildSummary(structureMap, risks, isTemplate),
    structure_map: structureMap,
    risks,
    practical_impact: practicalImpact,
    financial_impact: financialImpact,
    contract_strength_index: strengthIndex,
    missing_elements: missingElements,
    questions,
    notes
  };
}

function hasAny(text, patterns) {
  return patterns.some(pattern => text.includes(pattern));
}

function detectTemplate(text) {
  return hasAny(text, [
    "зразок договору",
    "шаблон договору",
    "типовий договір",
    "проект договору",
    "проєкт договору"
  ]);
}

function extractFinancialNote(text) {
  const percentMatches = text.match(/\d+[.,]?\d*\s*%/g);
  const moneyMatches = text.match(/\d[\d\s]*([.,]\d+)?\s*(грн|uah|usd|євро|eur)/gi);

  const parts = [];

  if (percentMatches && percentMatches.length) {
    parts.push("Виявлені відсоткові значення: " + percentMatches.slice(0, 5).join(", "));
  }

  if (moneyMatches && moneyMatches.length) {
    parts.push("Виявлені суми: " + moneyMatches.slice(0, 5).join(", "));
  }

  if (!parts.length) {
    return "У тексті є фінансові умови, але їх треба окремо порахувати вручну або в наступній версії ядра.";
  }

  return parts.join(" | ");
}

function calculateStrengthIndex(structureMap, risks) {
  let score = 0;

  Object.values(structureMap).forEach(value => {
    if (value) score += 1;
  });

  if (risks.length <= 2) score += 2;
  else if (risks.length <= 4) score += 1;

  if (score >= 7) return "Відносно сильний / структурно достатній";
  if (score >= 5) return "Середній / потребує ручної перевірки";
  if (score >= 3) return "Слабкий / є суттєві прогалини";
  return "Високий ризик / слабка конструкція";
}

function buildSummary(structureMap, risks, isTemplate) {
  const presentBlocks = Object.values(structureMap).filter(Boolean).length;

  if (isTemplate) {
    return "Документ схожий на зразок договору. Аналіз сфокусовано на умовах, ризиках, структурі та практичних наслідках, без врахування відсутніх персональних реквізитів сторін.";
  }

  if (presentBlocks >= 5 && risks.length <= 3) {
    return "Договір виглядає структурно відносно повним, але окремі умови все одно потребують ручної перевірки перед підписанням.";
  }

  if (presentBlocks >= 3) {
    return "У договорі є базові структурні елементи, але помітні прогалини або ризикові умови, які потрібно перевірити уважніше.";
  }

  return "Договір виглядає структурно слабким або неповним. Перед підписанням потрібна детальна ручна перевірка.";
}
