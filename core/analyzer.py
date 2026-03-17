import re
from typing import Dict, List, Any


# =========================================================
# Core 0.11x - analyzer.py
# Contract analysis with:
# 1) legal/non-legal precheck
# 2) sample template detection
# 3) friendly fallback for unsupported text
# 4) simple contract structure scan
# =========================================================


LEGAL_MARKERS = [
    "договір",
    "угода",
    "сторони",
    "сторона",
    "предмет договору",
    "права та обов'язки",
    "права та обов’язки",
    "відповідальність сторін",
    "строк дії",
    "розірвання",
    "оплата",
    "вартість",
    "послуги",
    "оренда",
    "кредит",
    "іпотека",
    "позичальник",
    "кредитор",
    "орендодавець",
    "орендар",
    "виконавець",
    "замовник",
    "пеня",
    "штраф",
    "зобов'язання",
    "зобов’язання",
    "цей договір",
    "уклали цей договір",
    "істотні умови",
]

TEMPLATE_MARKERS = [
    "зразок",
    "шаблон",
    "приклад договору",
    "[піб]",
    "[пiб]",
    "[адреса]",
    "[сума]",
    "[дата]",
    "[номер]",
    "_____",
    "________",
]

PERSONAL_FIELDS = [
    "ПІБ сторони",
    "ПІБ позичальника",
    "Паспортні дані",
    "Ідентифікаційний код",
    "Адреса сторони",
    "Реквізити сторони",
]

STRUCTURE_RULES = {
    "Parties": [
        "сторона",
        "сторони",
        "орендодавець",
        "орендар",
        "замовник",
        "виконавець",
        "позичальник",
        "кредитор",
    ],
    "Subject": [
        "предмет договору",
        "предмет",
    ],
    "Obligations": [
        "обов'язки",
        "обов’язки",
        "зобов'язання",
        "зобов’язання",
        "має право",
        "зобов'язаний",
        "зобов’язаний",
    ],
    "Payment": [
        "оплата",
        "вартість",
        "ціна",
        "платіж",
        "комісія",
        "процент",
        "ставка",
        "%",
        "грн",
        "uah",
        "usd",
        "eur",
    ],
    "Liability": [
        "відповідальність",
        "пеня",
        "штраф",
        "санкції",
        "неустойка",
    ],
    "Termination": [
        "розірвання",
        "припинення",
        "строк дії",
        "дострокове розірвання",
    ],
}

RISK_RULES = [
    {
        "title": "Можлива одностороння зміна умов",
        "level": "high",
        "patterns": [
            "в односторонньому порядку",
            "має право змінювати умови",
            "може змінити умови",
            "може змінювати тарифи",
            "може змінювати ставку",
        ],
        "explanation": "У тексті є ознаки того, що одна сторона може змінювати умови без рівноцінного погодження іншої сторони.",
    },
    {
        "title": "Штрафи або пеня",
        "level": "medium",
        "patterns": [
            "пеня",
            "штраф",
            "неустойка",
        ],
        "explanation": "У договорі виявлено штрафні санкції або пеню. Потрібно окремо оцінити розмір і умови застосування.",
    },
    {
        "title": "Додаткові платежі або комісії",
        "level": "medium",
        "patterns": [
            "комісія",
            "додаткові витрати",
            "додатковий платіж",
            "плата за обслуговування",
        ],
        "explanation": "У тексті є ознаки додаткових платежів або комісій, які можуть збільшувати загальну вартість договору.",
    },
    {
        "title": "Страхування як додаткова умова",
        "level": "medium",
        "patterns": [
            "страхування",
            "страховик",
            "страхова компанія",
            "обов'язкове страхування",
            "обов’язкове страхування",
        ],
        "explanation": "У договорі згадується страхування. Потрібно перевірити, чи воно є обов’язковим і хто саме визначає страхову компанію.",
    },
    {
        "title": "Складні умови розірвання",
        "level": "medium",
        "patterns": [
            "дострокове розірвання",
            "розірвання договору",
            "припинення договору",
        ],
        "explanation": "У договорі є умови розірвання, які потрібно окремо перевірити на практичні наслідки для сторін.",
    },
]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def has_many_words(text: str, min_words: int = 20) -> bool:
    words = re.findall(r"\w+", text, flags=re.UNICODE)
    return len(words) >= min_words


def count_legal_markers(text: str) -> Dict[str, Any]:
    normalized = normalize_text(text)
    found = [marker for marker in LEGAL_MARKERS if marker in normalized]
    return {
        "count": len(found),
        "found": found,
    }


def has_legal_structure(text: str) -> bool:
    lowered = text.lower()

    numbered_sections = len(re.findall(r"(?:^|\n)\s*\d{1,2}\.\s+", text))
    named_sections = 0

    section_names = [
        "предмет договору",
        "права та обов'язки",
        "права та обов’язки",
        "відповідальність",
        "строк дії",
        "розірвання",
        "оплата",
        "вартість",
    ]

    for name in section_names:
        if name in lowered:
            named_sections += 1

    return numbered_sections >= 2 or named_sections >= 2


def classify_input_document(text: str) -> str:
    """
    Returns:
    - legal_document
    - non_legal_text
    """
    normalized = normalize_text(text)

    if not has_many_words(text):
        return "non_legal_text"

    marker_result = count_legal_markers(normalized)
    marker_count = marker_result["count"]
    structure_flag = has_legal_structure(text)

    if marker_count >= 3:
        return "legal_document"

    if marker_count >= 2 and structure_flag:
        return "legal_document"

    return "non_legal_text"


def detect_document_type(text: str) -> str:
    normalized = normalize_text(text)

    for marker in TEMPLATE_MARKERS:
        if marker in normalized:
            return "sample_template"

    if re.search(r"\[[^\]]+\]", text):
        return "sample_template"

    if re.search(r"_{4,}", text):
        return "sample_template"

    return "filled_contract"


def extract_contract_structure(text: str) -> Dict[str, List[str]]:
    normalized = normalize_text(text)

    detected = []
    missing = []
    unclear = []

    for block_name, patterns in STRUCTURE_RULES.items():
        found = any(pattern in normalized for pattern in patterns)
        if found:
            detected.append(block_name)
        else:
            missing.append(block_name)

    if "Payment" in detected and not any(x in normalized for x in ["грн", "uah", "usd", "eur", "%", "сума", "ціна", "вартість"]):
        unclear.append("Payment details look incomplete or unspecified")

    return {
        "detected": detected,
        "missing_for_analysis": missing,
        "unclear": unclear,
    }


def detect_contract_risks(text: str, structure: Dict[str, List[str]]) -> List[Dict[str, str]]:
    normalized = normalize_text(text)
    risks = []

    for rule in RISK_RULES:
        if any(pattern in normalized for pattern in rule["patterns"]):
            risks.append(
                {
                    "title": rule["title"],
                    "level": rule["level"],
                    "explanation": rule["explanation"],
                }
            )

    if "Liability" not in structure.get("detected", []):
        risks.append(
            {
                "title": "Відсутній або слабко виражений блок відповідальності",
                "level": "medium",
                "explanation": "У тексті не виявлено чіткого блоку відповідальності сторін, що ускладнює оцінку наслідків порушення умов.",
            }
        )

    if "Termination" not in structure.get("detected", []):
        risks.append(
            {
                "title": "Відсутній або слабко виражений блок розірвання",
                "level": "medium",
                "explanation": "У тексті не виявлено чітких умов розірвання договору або припинення його дії.",
            }
        )

    return risks


def build_plain_meaning(text: str, structure: Dict[str, List[str]], risks: List[Dict[str, str]]) -> str:
    detected = structure.get("detected", [])
    missing = structure.get("missing_for_analysis", [])

    parts = []

    if detected:
        parts.append(
            "Текст схожий на юридичний документ або договір. "
            "Система виявила базові структурні елементи: "
            + ", ".join(detected)
            + "."
        )
    else:
        parts.append(
            "Текст має ознаки юридичного документа, але структура виявлена слабко."
        )

    if missing:
        parts.append(
            "Не всі типові блоки договору виражені чітко: "
            + ", ".join(missing)
            + "."
        )

    if risks:
        parts.append(
            f"Виявлено {len(risks)} потенційних ризиків або зон для додаткової перевірки."
        )
    else:
        parts.append(
            "Явні ризикові формулювання в межах базової перевірки не виявлені."
        )

    return " ".join(parts)


def build_practical_impact(text: str, structure: Dict[str, List[str]], risks: List[Dict[str, str]]) -> List[Dict[str, str]]:
    impacts = []

    titles = {risk["title"] for risk in risks}

    if "Можлива одностороння зміна умов" in titles:
        impacts.append(
            {
                "title": "Одностороння зміна умов",
                "impact": "На практиці це може означати, що одна сторона зможе змінити важливі умови договору без повноцінного погодження з вами.",
            }
        )

    if "Штрафи або пеня" in titles:
        impacts.append(
            {
                "title": "Фінансова відповідальність",
                "impact": "За порушення умов можуть застосовуватися штрафи, пеня або інші фінансові санкції.",
            }
        )

    if "Додаткові платежі або комісії" in titles:
        impacts.append(
            {
                "title": "Додаткові витрати",
                "impact": "Фактична вартість договору може бути вищою за базову суму через комісії або супутні платежі.",
            }
        )

    if "Страхування як додаткова умова" in titles:
        impacts.append(
            {
                "title": "Страхування",
                "impact": "Оформлення або виконання договору може вимагати додаткових витрат на страхування.",
            }
        )

    if "Termination" not in structure.get("detected", []):
        impacts.append(
            {
                "title": "Складність припинення договору",
                "impact": "Без чітких умов розірвання може бути складніше припинити договір без спорів або додаткових втрат.",
            }
        )

    return impacts


def build_financial_impact(text: str) -> List[Dict[str, str]]:
    lowered = text.lower()
    impacts = []

    if "%" in text or "процент" in lowered or "ставка" in lowered:
        impacts.append(
            {
                "title": "Процентна ставка / відсотки",
                "effect": "У тексті є ознаки процентної ставки або відсоткових умов. Їх варто окремо перевірити на можливість зміни та реальне збільшення навантаження.",
            }
        )

    if "комісія" in lowered:
        impacts.append(
            {
                "title": "Комісії",
                "effect": "У договорі є ознаки комісійних платежів, які можуть збільшувати загальну вартість зобов’язань.",
            }
        )

    if "страхування" in lowered or "страхов" in lowered:
        impacts.append(
            {
                "title": "Страхові витрати",
                "effect": "У тексті є ознаки додаткових витрат на страхування. Потрібно перевірити, чи це обов’язкова умова.",
            }
        )

    if "штраф" in lowered or "пеня" in lowered:
        impacts.append(
            {
                "title": "Штрафи / пеня",
                "effect": "Порушення умов договору може спричинити додаткові фінансові втрати через штрафи або пеню.",
            }
        )

    currency_or_sum_patterns = [
        r"\d+\s*грн",
        r"\d+\s*uah",
        r"\d+\s*usd",
        r"\d+\s*eur",
    ]

    if any(re.search(pattern, lowered) for pattern in currency_or_sum_patterns):
        impacts.append(
            {
                "title": "Грошові суми в договорі",
                "effect": "У тексті присутні конкретні суми. Їх потрібно оцінювати разом з комісіями, штрафами, страховими витратами та умовами зміни платежів.",
            }
        )

    return impacts


def remove_personal_fields(items: List[str]) -> List[str]:
    return [item for item in items if item not in PERSONAL_FIELDS]


def generate_questions(structure: Dict[str, List[str]], risks: List[Dict[str, str]], is_supported_document: bool) -> List[str]:
    if not is_supported_document:
        return []

    questions = []

    if "Payment" in structure.get("missing_for_analysis", []):
        questions.append("Чи містить договір чітко визначену суму, порядок оплати або формулу розрахунку?")

    if "Liability" in structure.get("missing_for_analysis", []):
        questions.append("Чи прописано відповідальність сторін за порушення умов договору?")

    if "Termination" in structure.get("missing_for_analysis", []):
        questions.append("Чи містить договір чіткі умови розірвання або дострокового припинення?")

    risk_titles = {risk["title"] for risk in risks}

    if "Страхування як додаткова умова" in risk_titles:
        questions.append("Чи є страхування обов’язковим, і чи можна обрати страхову компанію самостійно?")

    if "Можлива одностороння зміна умов" in risk_titles:
        questions.append("Чи має інша сторона право змінювати ставку, тарифи або інші істотні умови без вашого погодження?")

    return questions


def generate_notes(document_type: str, structure: Dict[str, List[str]], is_supported_document: bool) -> List[str]:
    if not is_supported_document:
        return [
            "Поточний режим призначений для аналізу договорів та інших юридичних текстів."
        ]

    notes = []

    if document_type == "sample_template":
        notes.append(
            "Документ визначено як зразок / шаблон. Відсутність персональних даних сторін не вважається помилкою."
        )

    if not structure.get("detected"):
        notes.append(
            "Структуру документа виявлено слабко. Потрібна додаткова ручна перевірка."
        )

    return notes


def calculate_contract_strength(structure: Dict[str, List[str]], risks: List[Dict[str, str]], is_supported_document: bool) -> Dict[str, Any]:
    if not is_supported_document:
        return {
            "score": 0,
            "label": "not_applicable",
        }

    detected_count = len(structure.get("detected", []))
    risk_penalty = len(risks) * 10

    score = 20 + detected_count * 12 - risk_penalty

    if score < 0:
        score = 0
    if score > 100:
        score = 100

    if score >= 70:
        label = "strong"
    elif score >= 40:
        label = "moderate"
    else:
        label = "weak"

    return {
        "score": score,
        "label": label,
    }


def build_non_legal_response() -> Dict[str, Any]:
    return {
        "mode": "contract_analysis",
        "document_type": "non_legal_text",
        "is_supported_document": False,
        "message": (
            "Вибачте, зараз Infacta у цьому режимі аналізує переважно юридичні "
            "документи та договори простою мовою. Схоже, що наданий текст не є "
            "договором або іншим юридичним документом для цього типу перевірки. "
            "Аналіз звичайних текстів і неюридичних документів буде додано в "
            "наступних версіях сайту."
        ),
        "summary": (
            "Наданий текст не визначено як юридичний документ для поточного режиму аналізу."
        ),
        "simplified_text": "",
        "structure_coverage": {
            "detected": [],
            "missing": [],
            "unclear": [],
        },
        "risks": [],
        "practical_impact": [],
        "financial_impact": [],
        "questions": [],
        "notes": [
            "Поточний режим призначений для аналізу договорів та інших юридичних текстів."
        ],
        "contract_strength_index": {
            "score": 0,
            "label": "not_applicable",
        },
    }


def analyze_contract(text: str, language: str = "uk") -> Dict[str, Any]:
    """
    Main contract analyzer for Core 0.11x
    """
    if not text or not text.strip():
        return {
            "mode": "contract_analysis",
            "document_type": "unknown",
            "is_supported_document": False,
            "message": "Текст для аналізу порожній.",
            "summary": "Немає вхідного тексту для аналізу.",
            "simplified_text": "",
            "structure_coverage": {
                "detected": [],
                "missing": [],
                "unclear": [],
            },
            "risks": [],
            "practical_impact": [],
            "financial_impact": [],
            "questions": [],
            "notes": ["Вставте текст договору або іншого юридичного документа."],
            "contract_strength_index": {
                "score": 0,
                "label": "not_applicable",
            },
        }

    input_class = classify_input_document(text)

    if input_class == "non_legal_text":
        return build_non_legal_response()

    document_type = detect_document_type(text)
    structure = extract_contract_structure(text)
    risks = detect_contract_risks(text, structure)
    practical_impact = build_practical_impact(text, structure, risks)
    financial_impact = build_financial_impact(text)
    summary = build_plain_meaning(text, structure, risks)

    structure_coverage = {
        "detected": structure.get("detected", []),
        "missing": structure.get("missing_for_analysis", []),
        "unclear": structure.get("unclear", []),
    }

    if document_type == "sample_template":
        structure_coverage["missing"] = remove_personal_fields(structure_coverage["missing"])

    strength = calculate_contract_strength(
        structure=structure,
        risks=risks,
        is_supported_document=True,
    )

    return {
        "mode": "contract_analysis",
        "document_type": document_type,
        "is_supported_document": True,
        "message": "",
        "summary": summary,
        "simplified_text": summary,
        "structure_coverage": structure_coverage,
        "risks": risks,
        "practical_impact": practical_impact,
        "financial_impact": financial_impact,
        "questions": generate_questions(
            structure=structure,
            risks=risks,
            is_supported_document=True,
        ),
        "notes": generate_notes(
            document_type=document_type,
            structure=structure,
            is_supported_document=True,
        ),
        "contract_strength_index": strength,
    }


def analyze_text(text: str, mode: str = "contract_analysis", language: str = "uk") -> Dict[str, Any]:
    """
    Generic entry point.
    If your API calls analyze_text(...), it will continue to work.
    """
    if mode == "contract_analysis":
        return analyze_contract(text=text, language=language)

    return {
        "mode": mode,
        "document_type": "unknown",
        "is_supported_document": False,
        "message": "Поточний режим аналізу ще не реалізований.",
        "summary": "Цей режим поки недоступний.",
        "simplified_text": "",
        "structure_coverage": {
            "detected": [],
            "missing": [],
            "unclear": [],
        },
        "risks": [],
        "practical_impact": [],
        "financial_impact": [],
        "questions": [],
        "notes": ["Підтримується лише contract_analysis."],
        "contract_strength_index": {
            "score": 0,
            "label": "not_applicable",
        },
    }
