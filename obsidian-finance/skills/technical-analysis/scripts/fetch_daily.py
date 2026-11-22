"""Fetch completed U.S. equity sessions and emit a portable JSON snapshot."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import re
import sys
from zoneinfo import ZoneInfo


NEW_YORK = "America/New_York"
US_EXCHANGES = {
    "ASE", "BTS", "IEX", "NGM", "NCM", "NMS", "NYQ", "PCX",
}


def _utc_now():
    return datetime.now(timezone.utc)


def fetch_daily(symbol, *, provider=None, calendar=None, now=_utc_now):
    """Acquire the latest snapshot with optional provider, calendar and clock injections."""
    symbol = symbol.strip().upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)?", symbol):
        raise ValueError("Use one U.S. ticker such as AAPL or BRK-B.")
    calendar_version = None
    if provider is None or calendar is None:
        try:
            if provider is None:
                import yfinance as provider
            if calendar is None:
                import exchange_calendars

                calendar = exchange_calendars.get_calendar("XNYS")
                calendar_version = exchange_calendars.__version__
        except ImportError as exc:
            raise ValueError(
                "Install yfinance and exchange-calendars in the isolated fetch environment."
            ) from exc

    ticker = provider.Ticker(symbol)
    options = {
        "period": "2y",
        "interval": "1d",
        "auto_adjust": True,
        "back_adjust": False,
        "prepost": False,
        "repair": False,
        "actions": False,
        "timeout": 15,
    }
    started_at = now()
    history = ticker.history(**options)
    metadata = ticker.get_history_metadata()
    available_at = now()
    exchange = metadata.get("exchangeName")
    if (
        metadata.get("symbol") != symbol
        or metadata.get("instrumentType") != "EQUITY"
        or exchange not in US_EXCHANGES
        or metadata.get("exchangeTimezoneName") != NEW_YORK
        or metadata.get("currency") != "USD"
    ):
        raise ValueError("Provider metadata did not verify a supported U.S. equity listing.")

    bars = []
    skipped_rows = []
    for session, row in history.iterrows():
        if session.tzinfo is not None:
            session = session.astimezone(ZoneInfo(NEW_YORK))
        day = session.date().isoformat()
        if not calendar.is_session(day):
            skipped_rows.append(f"{day}: not an exchange session.")
            continue
        close = calendar.session_close(day)
        if close > started_at:
            skipped_rows.append(f"{day}: session had not closed at request start.")
            continue
        prices = {key.lower(): float(row[key]) for key in ("Open", "High", "Low", "Close")}
        if not all(math.isfinite(price) and price > 0 for price in prices.values()):
            skipped_rows.append(f"{day}: missing or invalid price.")
            continue
        if not prices["low"] <= min(prices["open"], prices["close"]) <= max(
            prices["open"], prices["close"]
        ) <= prices["high"]:
            skipped_rows.append(f"{day}: open or close is outside the high-low range.")
            continue
        volume = row["Volume"]
        if volume is not None:
            volume = float(volume)
            volume = int(volume) if math.isfinite(volume) and volume >= 0 else None
        bars.append({
            "date": day,
            "session_close": close.isoformat(),
            **prices,
            "volume": volume,
        })
    if not bars:
        raise ValueError("The provider returned no usable completed daily bars.")

    bars.sort(key=lambda bar: bar["date"])
    available_dates = {bar["date"] for bar in bars}
    request_day = started_at.astimezone(ZoneInfo(NEW_YORK)).date().isoformat()
    expected_dates = []
    missing_completed_sessions = []
    for session in calendar.sessions_in_range(bars[0]["date"], request_day):
        day = session.date().isoformat()
        if calendar.session_close(day) <= started_at:
            expected_dates.append(day)
            if day not in available_dates:
                missing_completed_sessions.append(day)
                skipped_rows.append(f"{day}: completed exchange session missing from provider data.")

    source = f"https://finance.yahoo.com/quote/{symbol}/history/"
    provider_version = str(getattr(provider, "__version__", "unknown"))
    capture = available_at.isoformat()
    return {
        "ticker": symbol,
        "exchange": exchange,
        "currency": "USD",
        "timezone": NEW_YORK,
        "source": source,
        "source_version": f"yfinance/{provider_version} captured {capture}",
        "adjustment": "Yahoo adjusted OHLC (auto_adjust=True); volume as provided",
        "available_at": capture,
        "evidence": f"{source} retrieved {capture} via yfinance/{provider_version}",
        "request_started_at": started_at.isoformat(),
        "fetch_settings": options,
        "session_calendar": "XNYS",
        "session_calendar_version": calendar_version,
        "latest_expected_session": expected_dates[-1],
        "missing_completed_sessions": missing_completed_sessions,
        "fetch_exclusions": skipped_rows,
        "bars": bars,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker", help="One U.S. equity symbol")
    args = parser.parse_args()
    try:
        snapshot = fetch_daily(args.ticker)
    except Exception as exc:
        print(f"Daily history unavailable: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(snapshot, allow_nan=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
