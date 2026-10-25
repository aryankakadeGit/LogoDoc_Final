import pytest

from app.api.rate_limit import RateLimiter, parse_limit


@pytest.mark.parametrize(
    "text, expected",
    [("10/minute", (10, 60)), ("1/second", (1, 1)), ("100/hour", (100, 3600)), ("5/day", (5, 86400))],
)
def test_parse_limit(text, expected):
    assert parse_limit(text) == expected


def test_sliding_window():
    limiter = RateLimiter()
    key = ("analyze", "1.2.3.4")
    assert limiter.allow(key, 2, 60, now=0)
    assert limiter.allow(key, 2, 60, now=10)
    assert not limiter.allow(key, 2, 60, now=20)  # 2 hits in the last 60 s
    assert limiter.allow(key, 2, 60, now=61)  # first hit expired


def test_ips_and_scopes_are_independent():
    limiter = RateLimiter()
    assert limiter.allow(("analyze", "a"), 1, 60, now=0)
    assert limiter.allow(("analyze", "b"), 1, 60, now=0)
    assert limiter.allow(("designer", "a"), 1, 60, now=0)
    assert not limiter.allow(("analyze", "a"), 1, 60, now=1)

def test_shared_daily_cap_counts_across_scopes_and_ips():
    limiter = RateLimiter()
    assert limiter.allow(("ai-total", "*"), 2, 86400, now=0)
    assert limiter.allow(("ai-total", "*"), 2, 86400, now=1)
    assert not limiter.allow(("ai-total", "*"), 2, 86400, now=2)
