# concern: A known missing exchange session invalidates exact-session inputs.
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[5] /
                       "obsidian-finance/skills/technical-analysis/scripts"))
from analyze import analyze
from snapshot import validate_snapshot


def test_missing_session_cannot_support_exact_moving_average():
    first = date(2026, 7, 1)
    missing = date(2026, 8, 12)
    cutoff = "2026-08-21T22:00:00+00:00"
    bars = []
    for index in range(52):
        day = first + timedelta(days=index)
        if day.weekday() >= 5 or day == missing:
            continue
        price = 100 + index
        bars.append({
            "date": day.isoformat(),
            "session_close": datetime(day.year, day.month, day.day, 20,
                                      tzinfo=timezone.utc).isoformat(),
            "open": price, "high": price + 1, "low": price - 1,
            "close": price, "volume": 1000 + index,
        })
    snapshot = validate_snapshot({
        "ticker": "TEST", "timezone": "America/New_York",
        "source": "Synthetic exchange-calendar capture", "adjustment": "unadjusted",
        "evidence": "Synthetic retained exact version", "available_at": cutoff,
        "latest_expected_session": "2026-08-21",
        "fetch_exclusions": [f"{missing}: completed exchange session missing from provider data."],
        "bars": bars,
    }, cutoff)

    short = analyze(snapshot)["horizons"][0]
    assert short["metrics"]["sma"]["20"] is None
    assert short["metrics"]["volume_ratio"] is None
    assert short["trend"] == "insufficient"
