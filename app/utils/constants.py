RED_FLAG_KEYWORDS = {
    "douleur thoracique intense": {
        "severity": "high",
        "message": "Une douleur thoracique intense peut nécessiter une prise en charge urgente."
    },
    "crushing chest pain": {
        "severity": "high",
        "message": "Une douleur thoracique écrasante peut nécessiter une prise en charge urgente."
    },
    "douleur thoracique avec sueurs": {
        "severity": "high",
        "message": "Une douleur thoracique avec sueurs est un signal d'alarme cardiovasculaire."
    },
    "douleur thoracique avec nausées": {
        "severity": "high",
        "message": "Une douleur thoracique avec nausées doit être évaluée rapidement."
    },
    "douleur thoracique avec essoufflement": {
        "severity": "high",
        "message": "Douleur thoracique et essoufflement associés peuvent relever d'une urgence."
    },
    "essoufflement au repos": {
        "severity": "high",
        "message": "Un essoufflement au repos peut être une urgence médicale."
    },
    "difficulté respiratoire": {
        "severity": "high",
        "message": "Une difficulté respiratoire peut nécessiter une prise en charge urgente."
    },
    "difficulty breathing": {
        "severity": "high",
        "message": "Une difficulté respiratoire peut nécessiter une prise en charge urgente."
    },
    "lèvres bleues": {
        "severity": "high",
        "message": "Des lèvres bleues peuvent traduire un manque d'oxygène."
    },
    "crachats de sang": {
        "severity": "high",
        "message": "Cracher du sang nécessite une évaluation urgente."
    },
    "coughing blood": {
        "severity": "high",
        "message": "Cracher du sang nécessite une évaluation urgente."
    },
    "vomissements de sang": {
        "severity": "high",
        "message": "Des vomissements de sang nécessitent une prise en charge urgente."
    },
    "vomiting blood": {
        "severity": "high",
        "message": "Des vomissements de sang nécessitent une prise en charge urgente."
    },
    "sang dans les selles": {
        "severity": "high",
        "message": "Du sang dans les selles doit être évalué médicalement rapidement."
    },
    "blood in stool": {
        "severity": "high",
        "message": "Du sang dans les selles doit être évalué médicalement rapidement."
    },
    "selles noires": {
        "severity": "high",
        "message": "Des selles noires peuvent évoquer un saignement digestif."
    },
    "malaise avec perte de connaissance": {
        "severity": "high",
        "message": "Un malaise avec perte de connaissance nécessite une évaluation urgente."
    },
    "syncope": {
        "severity": "high",
        "message": "Une syncope nécessite une évaluation urgente."
    },
    "convulsions": {
        "severity": "high",
        "message": "Une crise convulsive nécessite une évaluation urgente."
    },
    "seizure": {
        "severity": "high",
        "message": "Une crise convulsive nécessite une évaluation urgente."
    },
    "paralysie brutale": {
        "severity": "high",
        "message": "Une paralysie brutale est un signal d'alarme neurologique."
    },
    "faiblesse brutale": {
        "severity": "high",
        "message": "Une faiblesse brutale peut correspondre à une urgence neurologique."
    },
    "trouble brutal de la parole": {
        "severity": "high",
        "message": "Un trouble brutal de la parole nécessite une évaluation urgente."
    },
    "speech difficulty": {
        "severity": "high",
        "message": "Un trouble brutal de la parole nécessite une évaluation urgente."
    },
    "perte brutale de la vision": {
        "severity": "high",
        "message": "Une perte brutale de la vision nécessite une évaluation urgente."
    },
    "confusion": {
        "severity": "high",
        "message": "Une confusion aiguë nécessite une évaluation urgente."
    },
    "raideur de nuque": {
        "severity": "high",
        "message": "Une raideur de nuque associée à un syndrome infectieux est un signal d'alerte."
    },
    "sang dans les urines": {
        "severity": "medium",
        "message": "Du sang dans les urines doit être évalué médicalement."
    },
    "blood in urine": {
        "severity": "medium",
        "message": "Du sang dans les urines doit être évalué médicalement."
    },
    "impossibilité d uriner": {
        "severity": "high",
        "message": "L'impossibilité d'uriner est une urgence médicale."
    },
    "impossibilité d'uriner": {
        "severity": "high",
        "message": "L'impossibilité d'uriner est une urgence médicale."
    },
    "saignement vaginal abondant": {
        "severity": "high",
        "message": "Un saignement vaginal abondant peut nécessiter une prise en charge urgente."
    },
    "heavy vaginal bleeding": {
        "severity": "high",
        "message": "Un saignement vaginal abondant peut nécessiter une prise en charge urgente."
    },
    "idées suicidaires": {
        "severity": "critical",
        "message": "Urgence détectée : contactez immédiatement le SAMU (15)."
    },
    "envie de mourir": {
        "severity": "critical",
        "message": "Urgence détectée : contactez immédiatement le SAMU (15)."
    },
    "penser au suicide": {
        "severity": "critical",
        "message": "Urgence détectée : contactez immédiatement le SAMU (15)."
    },
    "suicidal thoughts": {
        "severity": "critical",
        "message": "Urgence détectée : contactez immédiatement le SAMU (15)."
    },
    "kill myself": {
        "severity": "critical",
        "message": "Urgence détectée : contactez immédiatement le SAMU (15)."
    }
}

SPECIALTY_ALIASES = {
    "Cardiology": "Cardiologie",
    "Pulmonology": "Pneumologie",
    "Neurology": "Neurologie",
    "Gastroenterology": "Gastro-entérologie",
    "Dermatology": "Dermatologie",
    "Otorhinolaryngology (ENT)": "ORL",
    "ENT": "ORL",
    "Ophthalmology": "Ophtalmologie",
    "Rheumatology": "Rhumatologie",
    "Endocrinology": "Endocrinologie",
    "Nephrology": "Néphrologie",
    "Urology": "Urologie",
    "Gynecology": "Gynécologie",
    "Psychiatry": "Psychiatrie",
    "Infectious Diseases": "Infectiologie",
    "Orthopedics": "Orthopédie",
    "O.R.L.": "ORL"
}

SPECIALTY_LOCATION_KEYWORDS = {
    "Cardiologie": ["thorax", "poitrine", "cœur", "chest", "heart"],
    "Pneumologie": ["thorax", "poitrine", "poumons", "respiration", "lungs", "breathing", "chest"],
    "Neurologie": ["tête", "cerveau", "visage", "bras", "jambe", "head", "brain", "face", "arm", "leg"],
    "Gastro-entérologie": ["abdomen", "ventre", "estomac", "digestif", "abdomen", "stomach", "belly"],
    "Dermatologie": ["peau", "cuir chevelu", "visage", "ongles", "skin", "scalp", "nails"],
    "ORL": ["oreille", "oreilles", "nez", "gorge", "sinus", "cou", "ear", "ears", "nose", "throat"],
    "Ophtalmologie": ["œil", "yeux", "vision", "paupière", "eye", "eyes", "vision"],
    "Rhumatologie": ["articulation", "dos", "main", "poignet", "genou", "épaule", "joint", "back", "knee", "shoulder"],
    "Endocrinologie": ["général", "general", "whole body"],
    "Néphrologie": ["flanc", "rein", "reins", "lombes", "flank", "kidney", "back"],
    "Urologie": ["bassin", "pelvis", "pelvien", "urinaire", "vessie", "bladder", "flanc"],
    "Gynécologie": ["bassin", "pelvis", "pelvien", "bas ventre", "lower abdomen"],
    "Psychiatrie": ["général", "sommeil", "mental", "general", "sleep", "mood"],
    "Infectiologie": ["général", "whole body", "gorge", "poumons", "throat", "lungs"],
    "Orthopédie": ["os", "articulation", "dos", "genou", "épaule", "bras", "jambe", "bone", "joint", "arm", "leg"]
}

INTENSITY_BONUS_SPECIALTIES = {
    "high": {
        "Cardiologie",
        "Pneumologie",
        "Neurologie",
        "Infectiologie",
        "Orthopédie",
        "Gynécologie"
    },
    "medium": {
        "Gastro-entérologie",
        "Urologie",
        "Rhumatologie",
        "Dermatologie",
        "Endocrinologie",
        "Néphrologie",
        "Psychiatrie"
    },
    "low": set()
}

SAMU_TRIGGER_SEVERITIES = {"high", "critical"}
SAMU_ALERT_MESSAGE = "Urgence détectée : Contactez immédiatement le SAMU (15)"