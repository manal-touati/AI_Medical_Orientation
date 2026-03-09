from app.services.scoring_service import ScoringService


def test_compute_location_bonus_match():
    bonus = ScoringService.compute_location_bonus("chest", "Cardiology")
    assert bonus == 0.10


def test_compute_location_bonus_no_match():
    bonus = ScoringService.compute_location_bonus("eye", "Cardiology")
    assert bonus == 0.0


def test_compute_intensity_bonus_high_priority_specialty():
    bonus = ScoringService.compute_intensity_bonus("high", "Cardiology")
    assert bonus == 0.05


def test_compute_intensity_bonus_non_priority_specialty():
    bonus = ScoringService.compute_intensity_bonus("low", "Cardiology")
    assert bonus == 0.0


def test_detect_red_flags_match():
    user_text = "I have severe chest pain and fainting"
    specialty = {
        "name": "Cardiology",
        "red_flags": "severe chest pain, fainting, sudden collapse"
    }

    detected, bonus = ScoringService.detect_red_flags(user_text, specialty)

    assert detected is True
    assert bonus == 0.08


def test_detect_red_flags_no_match():
    user_text = "I have mild skin itching"
    specialty = {
        "name": "Cardiology",
        "red_flags": "severe chest pain, fainting, sudden collapse"
    }

    detected, bonus = ScoringService.detect_red_flags(user_text, specialty)

    assert detected is False
    assert bonus == 0.0


def test_compute_final_score():
    score = ScoringService.compute_final_score(
        semantic_score=0.70,
        location_bonus=0.10,
        intensity_bonus=0.05,
        red_flag_bonus=0.08
    )

    assert score == 0.79