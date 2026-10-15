"""`env_bool` and `env_int`: the shared env-var readers in app.utils.env_utils."""

from __future__ import annotations

import pytest

from app.utils.env_utils import env_bool, env_int

_NAME = "PIPESHUB_TEST_ENV_UTILS_VAR"


# ── env_bool ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("default", [True, False])
def test_env_bool_unset_returns_the_default(
    monkeypatch: pytest.MonkeyPatch, default: bool,
) -> None:
    monkeypatch.delenv(_NAME, raising=False)
    assert env_bool(_NAME, default) is default


@pytest.mark.parametrize("value", ["true", "TRUE", "  true  ", " True\t"])
def test_env_bool_true_in_any_case_or_padding_is_true(
    monkeypatch: pytest.MonkeyPatch, value: str,
) -> None:
    monkeypatch.setenv(_NAME, value)
    assert env_bool(_NAME, False) is True


@pytest.mark.parametrize("value", ["false", "yes", "1", ""])
@pytest.mark.parametrize("default", [True, False])
def test_env_bool_anything_but_true_is_false_even_with_a_true_default(
    monkeypatch: pytest.MonkeyPatch, value: str, default: bool,
) -> None:
    monkeypatch.setenv(_NAME, value)
    assert env_bool(_NAME, default) is False


# ── env_int ─────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("default", [None, 7])
def test_env_int_unset_returns_the_default(
    monkeypatch: pytest.MonkeyPatch, default: int | None,
) -> None:
    monkeypatch.delenv(_NAME, raising=False)
    assert env_int(_NAME, default) == default


@pytest.mark.parametrize("value", ["", "   ", "abc"])
@pytest.mark.parametrize("default", [None, 7])
def test_env_int_blank_or_unparseable_returns_the_default(
    monkeypatch: pytest.MonkeyPatch, value: str, default: int | None,
) -> None:
    monkeypatch.setenv(_NAME, value)
    assert env_int(_NAME, default) == default


@pytest.mark.parametrize("value", ["12", " 12 "])
def test_env_int_parses_an_integer_with_or_without_padding(
    monkeypatch: pytest.MonkeyPatch, value: str,
) -> None:
    monkeypatch.setenv(_NAME, value)
    assert env_int(_NAME, 5) == 12


def test_env_int_clamps_a_value_below_lo_up_to_lo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(_NAME, "1")
    assert env_int(_NAME, 5, lo=3) == 3


def test_env_int_clamps_a_value_above_hi_down_to_hi(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(_NAME, "9")
    assert env_int(_NAME, 5, hi=4) == 4


def test_env_int_leaves_a_value_inside_the_bounds_alone(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(_NAME, "4")
    assert env_int(_NAME, 5, lo=3, hi=6) == 4
