def calculate_risk(data):
    risk_score = 0
    risk_factors = []

    weekly_sessions = data["weekly_sessions"]
    training_duration = data["training_duration"]
    intensity = data["intensity"]
    fatigue = data["fatigue"]
    sleep_quality = data["sleep_quality"]
    pain_level = data["pain_level"]
    rest_days = data["rest_days"]
    previous_injury = data["previous_injury"]

    # Broj treninga
    if weekly_sessions >= 6:
        risk_score += 15
        risk_factors.append("Visok broj treninga u toku nedelje")
    elif weekly_sessions >= 4:
        risk_score += 8

    # Trajanje treninga
    if training_duration >= 120:
        risk_score += 12
        risk_factors.append("Dugo trajanje poslednjeg treninga")
    elif training_duration >= 90:
        risk_score += 6

    # Intenzitet
    if intensity >= 8:
        risk_score += 15
        risk_factors.append("Visok intenzitet treninga")
    elif intensity >= 6:
        risk_score += 8

    # Umor
    if fatigue >= 8:
        risk_score += 15
        risk_factors.append("Izražen subjektivni umor")
    elif fatigue >= 6:
        risk_score += 8

    # San
    if sleep_quality <= 4:
        risk_score += 15
        risk_factors.append("Loš kvalitet sna")
    elif sleep_quality <= 6:
        risk_score += 8

    # Bol / nelagodnost
    if pain_level >= 7:
        risk_score += 20
        risk_factors.append("Prisutan visok nivo bola ili nelagodnosti")
    elif pain_level >= 4:
        risk_score += 12
        risk_factors.append("Prisutan umeren bol ili nelagodnost")

    # Dani odmora
    if rest_days == 0:
        risk_score += 15
        risk_factors.append("Nema dana odmora u poslednjih 7 dana")
    elif rest_days == 1:
        risk_score += 8

    # Prethodna povreda
    if previous_injury == "yes":
        risk_score += 12
        risk_factors.append("Postoji istorija prethodne povrede")

    # Ograničavamo skor na maksimum 100
    risk_score = min(risk_score, 100)

    # Određivanje nivoa rizika
    if risk_score <= 35:
        risk_level = "Nizak rizik"
        recommendation = "Sportista može nastaviti sa planiranim treningom, uz redovno praćenje umora i oporavka."
    elif risk_score <= 65:
        risk_level = "Umeren rizik"
        recommendation = "Preporučuje se smanjenje intenziteta treninga i dodatni fokus na oporavak."
    else:
        risk_level = "Visok rizik"
        recommendation = "Preporučuje se odmor, smanjenje opterećenja i dodatna provera stanja sportiste pre nastavka intenzivnog treninga."

    if not risk_factors:
        risk_factors.append("Nisu detektovani značajni faktori rizika")

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "recommendation": recommendation
    }