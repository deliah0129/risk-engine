import json
import random
from datetime import datetime, timezone
from pathlib import Path

# -------------------------
# Paths / Files
# -------------------------
ROOT = Path(__file__).resolve().parents[1]  # .../risk_engine
STATE_DIR = ROOT / "state"
LOG_DIR = ROOT / "logs"
STATE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

SESSION_FILE = STATE_DIR / "session.json"
PLAYERS_FILE = STATE_DIR / "players.json"
COUNTRIES_FILE = STATE_DIR / "countries.json"
LOG_FILE = LOG_DIR / "phase2.log"


# -------------------------
# Helpers
# -------------------------
def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(msg: str) -> None:
    existing = LOG_FILE.read_text(encoding="utf-8") if LOG_FILE.exists() else ""
    LOG_FILE.write_text(existing + f"[{utc_now()}] {msg}\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def normalize_pool(pool_text: str) -> list[str]:
    # Uppercase, trim, drop blanks, de-dupe while preserving order
    seen = set()
    out = []
    for raw in pool_text.splitlines():
        name = raw.strip()
        if not name:
            continue
        # allow comments in the text block
        if name.startswith("#"):
            continue
        name = name.upper()
        if name not in seen:
            seen.add(name)
            out.append(name)
    return out


# -------------------------
# Phase 2: Country Selection (STUB)
# -------------------------
def run_phase_2() -> None:
    print("RISK: Global Power - Phase 2 (Country Selection - STUB)")
    log("PHASE 2 START")

    if not SESSION_FILE.exists():
        print("Missing state/session.json. Run Phase 0 first.")
        log("PHASE 2 FAIL (NO SESSION)")
        return

    if not PLAYERS_FILE.exists():
        print("Missing state/players.json. Run Phase 1 first.")
        log("PHASE 2 FAIL (NO PLAYERS)")
        return

    session = load_json(SESSION_FILE)
    players = load_json(PLAYERS_FILE)

    # Guard: only run Phase 2 if Phase 1 is complete
    if session.get("phase") != 1:
        print(f"Wrong phase: {session.get('phase')} (expected 1)")
        log("PHASE 2 BLOCKED (WRONG PHASE)")
        return

    humans = players.get("humans", [])
    ais = players.get("ais", [])
    seats_total = int(players.get("seats_total", len(humans) + len(ais)))

    # 200+ country/territory pool as multiline text (no comma/quote misery)
    COUNTRY_POOL_TEXT = """
AFGHANISTAN
ALBANIA
ALGERIA
ANDORRA
ANGOLA
ANTIGUA AND BARBUDA
ARGENTINA
ARMENIA
AUSTRALIA
AUSTRIA
AZERBAIJAN
BAHAMAS
BAHRAIN
BANGLADESH
BARBADOS
BELARUS
BELGIUM
BELIZE
BENIN
BHUTAN
BOLIVIA
BOSNIA AND HERZEGOVINA
BOTSWANA
BRAZIL
BRUNEI
BULGARIA
BURKINA FASO
BURUNDI
CABO VERDE
CAMBODIA
CAMEROON
CANADA
CENTRAL AFRICAN REPUBLIC
CHAD
CHILE
CHINA
COLOMBIA
COMOROS
CONGO (REPUBLIC OF THE)
CONGO (DEMOCRATIC REPUBLIC OF THE)
COSTA RICA
COTE D'IVOIRE
CROATIA
CUBA
CYPRUS
CZECHIA
DENMARK
DJIBOUTI
DOMINICA
DOMINICAN REPUBLIC
ECUADOR
EGYPT
EL SALVADOR
EQUATORIAL GUINEA
ERITREA
ESTONIA
ESWATINI
ETHIOPIA
FIJI
FINLAND
FRANCE
GABON
GAMBIA
GEORGIA
GERMANY
GHANA
GREECE
GRENADA
GUATEMALA
GUINEA
GUINEA-BISSAU
GUYANA
HAITI
HONDURAS
HUNGARY
ICELAND
INDIA
INDONESIA
IRAN
IRAQ
IRELAND
ISRAEL
ITALY
JAMAICA
JAPAN
JORDAN
KAZAKHSTAN
KENYA
KIRIBATI
KUWAIT
KYRGYZSTAN
LAOS
LATVIA
LEBANON
LESOTHO
LIBERIA
LIBYA
LIECHTENSTEIN
LITHUANIA
LUXEMBOURG
MADAGASCAR
MALAWI
MALAYSIA
MALDIVES
MALI
MALTA
MARSHALL ISLANDS
MAURITANIA
MAURITIUS
MEXICO
MICRONESIA
MOLDOVA
MONACO
MONGOLIA
MONTENEGRO
MOROCCO
MOZAMBIQUE
MYANMAR
NAMIBIA
NAURU
NEPAL
NETHERLANDS
NEW ZEALAND
NICARAGUA
NIGER
NIGERIA
NORTH KOREA
NORTH MACEDONIA
NORWAY
OMAN
PAKISTAN
PALAU
PANAMA
PAPUA NEW GUINEA
PARAGUAY
PERU
PHILIPPINES
POLAND
PORTUGAL
QATAR
ROMANIA
RUSSIA
RWANDA
SAINT KITTS AND NEVIS
SAINT LUCIA
SAINT VINCENT AND THE GRENADINES
SAMOA
SAN MARINO
SAO TOME AND PRINCIPE
SAUDI ARABIA
SENEGAL
SERBIA
SEYCHELLES
SIERRA LEONE
SINGAPORE
SLOVAKIA
SLOVENIA
SOLOMON ISLANDS
SOMALIA
SOUTH AFRICA
SOUTH KOREA
SOUTH SUDAN
SPAIN
SRI LANKA
SUDAN
SURINAME
SWEDEN
SWITZERLAND
SYRIA
TAJIKISTAN
TANZANIA
THAILAND
TIMOR-LESTE
TOGO
TONGA
TRINIDAD AND TOBAGO
TUNISIA
TURKEY
TURKMENISTAN
TUVALU
UGANDA
UKRAINE
UNITED ARAB EMIRATES
UNITED KINGDOM
UNITED STATES
URUGUAY
UZBEKISTAN
VANUATU
VENEZUELA
VIETNAM
YEMEN
ZAMBIA
ZIMBABWE

# Extras / territories / non-UN observers (pushes comfortably over 200)
TAIWAN
PALESTINE
KOSOVO
HONG KONG
MACAO
GREENLAND
PUERTO RICO
FAROE ISLANDS
WESTERN SAHARA
VATICAN CITY
CURACAO
ARUBA
BONAIRE
SINT MAARTEN
SINT EUSTATIUS
SABA
GIBRALTAR
BERMUDA
CAYMAN ISLANDS
BRITISH VIRGIN ISLANDS
US VIRGIN ISLANDS
GUAM
AMERICAN SAMOA
NORTHERN MARIANA ISLANDS
FRENCH POLYNESIA
NEW CALEDONIA
WALLIS AND FUTUNA
SAINT PIERRE AND MIQUELON
MARTINIQUE
GUADELOUPE
REUNION
MAYOTTE
FRENCH GUIANA
"""
    country_pool = normalize_pool(COUNTRY_POOL_TEXT)

    # Make sure we have enough countries for all seats
    if len(country_pool) < seats_total:
        print(f"Not enough countries in pool for all seats. Have {len(country_pool)}, need {seats_total}.")
        log("PHASE 2 FAIL (POOL TOO SMALL)")
        return

    random.shuffle(country_pool)
    assigned = country_pool[:seats_total]

    # Map seat -> country
    country_map = []
    for seat in range(1, seats_total + 1):
        country_map.append({
            "seat": seat,
            "country": assigned[seat - 1],
        })

    countries_state = {
        "phase": 2,
        "mode": session.get("mode"),
        "assignments": country_map,
        "created_utc": utc_now(),
    }

    save_json(COUNTRIES_FILE, countries_state)

    # Bump session phase -> 2
    session["phase"] = 2
    save_json(SESSION_FILE, session)

    print("\nCountry Assignments:")
    for entry in country_map:
        print(f"Seat {entry['seat']}: {entry['country']}")

    print("\nPhase 2 complete (stub). Next: Initial Resources (Phase 3).")
    log("PHASE 2 COMPLETE (STUB)")


if __name__ == "__main__":
    run_phase_2()
