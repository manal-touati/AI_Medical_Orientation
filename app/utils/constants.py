RED_FLAG_KEYWORDS = {
    "severe chest pain": {
        "severity": "high",
        "message": "Severe chest pain may require urgent medical attention."
    },
    "crushing chest pain": {
        "severity": "high",
        "message": "Crushing chest pain may require urgent medical attention."
    },
    "chest pain with sweating": {
        "severity": "high",
        "message": "Chest pain associated with autonomic symptoms may require urgent evaluation."
    },
    "chest pain with nausea": {
        "severity": "high",
        "message": "Chest pain associated with nausea may require urgent evaluation."
    },
    "fainting": {
        "severity": "high",
        "message": "Fainting may indicate a serious condition and should be evaluated promptly."
    },
    "syncope": {
        "severity": "high",
        "message": "Syncope may require urgent medical attention."
    },
    "seizure": {
        "severity": "high",
        "message": "Seizure-like symptoms require urgent medical evaluation."
    },
    "convulsion": {
        "severity": "high",
        "message": "Convulsion-like symptoms require urgent medical evaluation."
    },
    "sudden paralysis": {
        "severity": "high",
        "message": "Sudden paralysis is a neurological red flag and may require emergency care."
    },
    "sudden weakness": {
        "severity": "high",
        "message": "Sudden weakness may indicate an urgent neurological issue."
    },
    "speech difficulty": {
        "severity": "high",
        "message": "Sudden speech difficulty may require urgent neurological assessment."
    },
    "facial droop": {
        "severity": "high",
        "message": "Facial droop may require urgent neurological assessment."
    },
    "difficulty breathing": {
        "severity": "high",
        "message": "Difficulty breathing may require urgent medical attention."
    },
    "shortness of breath at rest": {
        "severity": "high",
        "message": "Breathing difficulty at rest may require urgent medical attention."
    },
    "bluish lips": {
        "severity": "high",
        "message": "Bluish lips may indicate low oxygen and urgent evaluation is recommended."
    },
    "coughing blood": {
        "severity": "high",
        "message": "Coughing blood is a red flag and should be evaluated urgently."
    },
    "vomiting blood": {
        "severity": "high",
        "message": "Vomiting blood is a red flag and requires urgent medical attention."
    },
    "blood in stool": {
        "severity": "high",
        "message": "Blood in stool should be medically evaluated."
    },
    "black stools": {
        "severity": "high",
        "message": "Black stools may indicate gastrointestinal bleeding."
    },
    "blood in urine": {
        "severity": "medium",
        "message": "Blood in urine should be medically evaluated."
    },
    "sudden vision loss": {
        "severity": "high",
        "message": "Sudden vision loss requires urgent ophthalmologic or emergency evaluation."
    },
    "confusion": {
        "severity": "high",
        "message": "Acute confusion may require urgent medical evaluation."
    },
    "stiff neck": {
        "severity": "high",
        "message": "A stiff neck with systemic symptoms may require urgent evaluation."
    },
    "suicidal thoughts": {
        "severity": "critical",
        "message": "Suicidal thoughts require immediate support and urgent professional help."
    },
    "self-harm thoughts": {
        "severity": "critical",
        "message": "Self-harm thoughts require immediate support and urgent professional help."
    },
    "want to die": {
        "severity": "critical",
        "message": "Suicidal intent requires immediate support and urgent professional help."
    },
    "wanna suicide": {
        "severity": "critical",
        "message": "Suicidal intent requires immediate support and urgent professional help."
    },
    "kill myself": {
        "severity": "critical",
        "message": "Suicidal intent requires immediate support and urgent professional help."
    },
    "heavy vaginal bleeding": {
        "severity": "high",
        "message": "Heavy vaginal bleeding may require urgent medical evaluation."
    },
    "unable to urinate": {
        "severity": "high",
        "message": "Inability to urinate may require urgent medical evaluation."
    },
}

SPECIALTY_ALIASES = {
    "ENT": "Otorhinolaryngology (ENT)",
    "Otorhinolaryngology": "Otorhinolaryngology (ENT)",
    "Ear Nose Throat": "Otorhinolaryngology (ENT)",
    "Ear, Nose and Throat": "Otorhinolaryngology (ENT)",
}

SPECIALTY_LOCATION_KEYWORDS = {
    "Cardiology": ["chest", "thorax", "heart", "left chest"],
    "Pulmonology": ["chest", "lungs", "breathing", "thorax"],
    "Neurology": ["head", "brain", "face", "arm", "leg", "left arm", "right arm"],
    "Gastroenterology": ["abdomen", "stomach", "belly", "digestive", "lower abdomen"],
    "Dermatology": ["skin", "scalp", "face", "nails", "hair"],
    "Otorhinolaryngology (ENT)": ["ear", "ears", "nose", "throat", "sinus", "neck"],
    "Ophthalmology": ["eye", "eyes", "vision", "eyelid"],
    "Rheumatology": ["joint", "joints", "back", "hand", "hands", "wrist", "knee", "shoulder"],
    "Endocrinology": ["general", "whole body"],
    "Nephrology": ["flank", "kidney", "kidneys", "back", "feet", "legs"],
    "Urology": ["pelvis", "pelvic", "urinary", "bladder", "flank"],
    "Gynecology": ["pelvis", "pelvic", "lower abdomen"],
    "Psychiatry": ["general", "mental", "sleep"],
    "Infectious Diseases": ["general", "whole body", "throat", "lungs"],
    "Orthopedics": ["bone", "bones", "joint", "joints", "back", "knee", "shoulder", "arm", "leg"],
}

INTENSITY_BONUS_SPECIALTIES = {
    "high": {
        "Cardiology",
        "Pulmonology",
        "Neurology",
        "Infectious Diseases",
        "Orthopedics",
        "Gynecology",
    },
    "medium": {
        "Gastroenterology",
        "Urology",
        "Rheumatology",
        "Dermatology",
        "Endocrinology",
        "Nephrology",
    },
    "low": set(),
}