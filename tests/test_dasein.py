"""Tests for the Heideggerian phenomenological analysis module.

Verifies Dasein (world assumptions), Zuhandenheit (transparency conditions),
and Vorhandenheit (breakdown conditions) for various function schemas.
"""

from __future__ import annotations

import pytest

from core.dasein import (
    BreakdownCondition,
    DaseinAnalysis,
    WorldAssumption,
    analyze_dasein,
)


WEATHER_SCHEMA: dict = {
    "name": "get_weather",
    "description": "Get the current weather for a location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
}

AUTH_SCHEMA: dict = {
    "name": "get_user_profile",
    "description": "Retrieve a user profile from the API server",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "User identifier"},
            "api_key": {"type": "string", "description": "API authentication key"},
        },
        "required": ["user_id", "api_key"],
    },
}

MINIMAL_SCHEMA: dict = {
    "name": "ping",
}


class TestDaseinBasics:
    """Basic structure tests."""

    def test_returns_dasein_analysis(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        assert isinstance(result, DaseinAnalysis)

    def test_function_name(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        assert result.function_name == "get_weather"

    def test_missing_name_raises(self) -> None:
        with pytest.raises(ValueError, match="name"):
            analyze_dasein({"description": "no name"})


class TestWorldAssumptions:
    """Tests for Dasein world-state assumptions."""

    def test_callable_context_always_present(self) -> None:
        result = analyze_dasein(MINIMAL_SCHEMA)
        aspects = [wa.aspect for wa in result.world_assumptions]
        assert "callable_context" in aspects

    def test_weather_has_geographic_assumption(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        aspects = [wa.aspect for wa in result.world_assumptions]
        assert "geographic_reality" in aspects

    def test_auth_schema_has_auth_assumption(self) -> None:
        result = analyze_dasein(AUTH_SCHEMA)
        aspects = [wa.aspect for wa in result.world_assumptions]
        assert "auth_state" in aspects

    def test_auth_schema_has_entity_assumption(self) -> None:
        result = analyze_dasein(AUTH_SCHEMA)
        aspects = [wa.aspect for wa in result.world_assumptions]
        assert "entity_existence" in aspects

    def test_auth_schema_has_service_assumption(self) -> None:
        """Description mentions 'API server', so service_availability applies."""
        result = analyze_dasein(AUTH_SCHEMA)
        aspects = [wa.aspect for wa in result.world_assumptions]
        assert "service_availability" in aspects

    def test_world_assumption_has_derived_from(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        for wa in result.world_assumptions:
            assert wa.derived_from
            assert isinstance(wa.derived_from, str)


class TestTransparencyConditions:
    """Tests for Zuhandenheit (ready-to-hand) conditions."""

    def test_always_has_transparency_conditions(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        assert len(result.transparency_conditions) > 0

    def test_valid_args_condition(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        combined = " ".join(result.transparency_conditions).lower()
        assert "valid" in combined or "ready-to-hand" in combined

    def test_required_params_mentioned(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        combined = " ".join(result.transparency_conditions)
        assert "location" in combined

    def test_enum_params_mentioned(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        combined = " ".join(result.transparency_conditions)
        assert "unit" in combined


class TestBreakdownConditions:
    """Tests for Vorhandenheit (present-at-hand) breakdown conditions."""

    def test_always_has_breakdown_conditions(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        assert len(result.breakdown_conditions) > 0

    def test_missing_required_is_major(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        major_breakdowns = [bc for bc in result.breakdown_conditions if bc.severity == "major"]
        assert len(major_breakdowns) > 0

    def test_invalid_enum_breakdown(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        triggers = [bc.trigger.lower() for bc in result.breakdown_conditions]
        assert any("enum" in t for t in triggers)

    def test_general_error_breakdown(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        triggers = [bc.trigger.lower() for bc in result.breakdown_conditions]
        assert any("error" in t or "unexpected" in t for t in triggers)

    def test_breakdown_has_consequence(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        for bc in result.breakdown_conditions:
            assert bc.consequence
            assert isinstance(bc.consequence, str)


class TestDaseinSerialization:
    """Tests for to_dict serialization."""

    def test_to_dict_structure(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        d = result.to_dict()
        assert "function_name" in d
        assert "dasein" in d
        assert "zuhandenheit" in d
        assert "vorhandenheit" in d

    def test_dasein_section(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        d = result.to_dict()
        assert "world_assumptions" in d["dasein"]
        for wa in d["dasein"]["world_assumptions"]:
            assert "aspect" in wa
            assert "description" in wa
            assert "derived_from" in wa

    def test_vorhandenheit_section(self) -> None:
        result = analyze_dasein(WEATHER_SCHEMA)
        d = result.to_dict()
        assert "breakdown_conditions" in d["vorhandenheit"]
        for bc in d["vorhandenheit"]["breakdown_conditions"]:
            assert "trigger" in bc
            assert "consequence" in bc
            assert "severity" in bc
