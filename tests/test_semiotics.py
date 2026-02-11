"""Tests for the Peircean semiotic analysis module.

Verifies Representamen (sign), Object (referent), and Interpretant (meaning)
for various function schemas.
"""

from __future__ import annotations

import pytest

from core.semiotics import SemioticAnalysis, SignAnalysis, analyze_semiotics


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

DELETE_SCHEMA: dict = {
    "name": "delete_record",
    "description": "Permanently delete a record from the database",
    "parameters": {
        "type": "object",
        "properties": {
            "record_id": {"type": "string", "description": "Record identifier"},
        },
        "required": ["record_id"],
    },
}

CAMEL_CASE_SCHEMA: dict = {
    "name": "getUserProfile",
    "description": "Retrieve the profile for a user",
    "parameters": {
        "type": "object",
        "properties": {
            "userId": {"type": "string"},
        },
    },
}

MINIMAL_SCHEMA: dict = {
    "name": "ping",
}


class TestSemioticBasics:
    """Basic structure tests."""

    def test_returns_semiotic_analysis(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        assert isinstance(result, SemioticAnalysis)

    def test_function_name(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        assert result.function_name == "get_weather"

    def test_three_components(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        assert len(result.all_components) == 3

    def test_component_types(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        types = {c.component for c in result.all_components}
        assert types == {"representamen", "object", "interpretant"}

    def test_missing_name_raises(self) -> None:
        with pytest.raises(ValueError, match="name"):
            analyze_semiotics({"description": "no name"})


class TestRepresentamen:
    """Tests for the sign (function identifier)."""

    def test_function_name_in_summary(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        assert "get_weather" in result.representamen.summary

    def test_verb_identified(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        evidence = " ".join(result.representamen.evidence)
        assert "get" in evidence.lower()

    def test_noun_identified(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        evidence = " ".join(result.representamen.evidence)
        assert "weather" in evidence.lower()

    def test_camel_case_parsed(self) -> None:
        result = analyze_semiotics(CAMEL_CASE_SCHEMA)
        evidence = " ".join(result.representamen.evidence)
        assert "get" in evidence.lower()

    def test_param_names_included(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        evidence = " ".join(result.representamen.evidence)
        assert "location" in evidence


class TestObject:
    """Tests for the referent (what the function acts upon)."""

    def test_weather_referent(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        assert "weather" in result.object.summary.lower()

    def test_record_referent(self) -> None:
        result = analyze_semiotics(DELETE_SCHEMA)
        assert "record" in result.object.summary.lower()

    def test_minimal_has_unspecified(self) -> None:
        result = analyze_semiotics(MINIMAL_SCHEMA)
        assert "unspecified" in result.object.summary.lower()


class TestInterpretant:
    """Tests for the meaning (what the caller understands)."""

    def test_weather_meaning_includes_description(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        assert "weather" in result.interpretant.summary.lower()

    def test_delete_meaning(self) -> None:
        result = analyze_semiotics(DELETE_SCHEMA)
        summary_lower = result.interpretant.summary.lower()
        assert "delete" in summary_lower or "destroy" in summary_lower

    def test_enum_sharpens_meaning(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        evidence = " ".join(result.interpretant.evidence).lower()
        assert "enum" in evidence or "unit" in evidence

    def test_minimal_still_has_meaning(self) -> None:
        result = analyze_semiotics(MINIMAL_SCHEMA)
        assert result.interpretant.summary
        assert len(result.interpretant.summary) > 10


class TestSemioticSerialization:
    """Tests for to_dict serialization."""

    def test_to_dict_structure(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        d = result.to_dict()
        assert "function_name" in d
        assert "representamen" in d
        assert "object" in d
        assert "interpretant" in d

    def test_component_dict_structure(self) -> None:
        result = analyze_semiotics(WEATHER_SCHEMA)
        d = result.to_dict()
        for comp_key in ("representamen", "object", "interpretant"):
            comp = d[comp_key]
            assert "component" in comp
            assert "summary" in comp
            assert "evidence" in comp
