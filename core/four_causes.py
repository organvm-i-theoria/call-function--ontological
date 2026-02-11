"""Aristotelian four-causes analysis for function-calling schemas.

Given a function signature (as a dict), this module determines the material,
formal, efficient, and final causes. The analysis is purely structural and
deterministic — it inspects parameter names, types, descriptions, and naming
conventions to infer each cause.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CauseAnalysis:
    """Result of analyzing a single Aristotelian cause.

    Attributes:
        cause_type: One of 'material', 'formal', 'efficient', 'final'.
        summary: Human-readable one-line summary.
        evidence: Specific schema elements that ground this analysis.
        confidence: How strongly the evidence supports the analysis
            ('high', 'medium', 'low').
    """

    cause_type: str
    summary: str
    evidence: list[str] = field(default_factory=list)
    confidence: str = "medium"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {
            "cause_type": self.cause_type,
            "summary": self.summary,
            "evidence": self.evidence,
            "confidence": self.confidence,
        }


@dataclass
class FourCausesReport:
    """Complete Aristotelian four-causes analysis of a function.

    Attributes:
        function_name: The name of the analyzed function.
        material: What the function is made of (parameters, types).
        formal: The shape/signature/schema of the function.
        efficient: What triggers the function.
        final: The purpose/telos of the function.
    """

    function_name: str
    material: CauseAnalysis
    formal: CauseAnalysis
    efficient: CauseAnalysis
    final: CauseAnalysis

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full report."""
        return {
            "function_name": self.function_name,
            "material": self.material.to_dict(),
            "formal": self.formal.to_dict(),
            "efficient": self.efficient.to_dict(),
            "final": self.final.to_dict(),
        }

    @property
    def all_causes(self) -> list[CauseAnalysis]:
        """Return all four causes as a list."""
        return [self.material, self.formal, self.efficient, self.final]


def _extract_parameters(schema: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract parameter info from a function schema."""
    params = schema.get("parameters", {})
    properties = params.get("properties", {})
    required = set(params.get("required", []))

    result: list[dict[str, Any]] = []
    for param_name, param_spec in properties.items():
        result.append(
            {
                "name": param_name,
                "type": param_spec.get("type", "unknown"),
                "description": param_spec.get("description", ""),
                "required": param_name in required,
                "enum": param_spec.get("enum"),
            }
        )
    return result


def _analyze_material(
    function_name: str, params: list[dict[str, Any]]
) -> CauseAnalysis:
    """Determine the material cause: what the function is made of."""
    if not params:
        return CauseAnalysis(
            cause_type="material",
            summary=f"{function_name} takes no parameters — its material is empty.",
            evidence=["No parameters defined in schema."],
            confidence="high",
        )

    type_counts: dict[str, int] = {}
    for p in params:
        t = p["type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    param_names = [p["name"] for p in params]
    required_names = [p["name"] for p in params if p["required"]]

    type_summary = ", ".join(f"{count} {t}" for t, count in type_counts.items())
    evidence = [
        f"Parameters: {', '.join(param_names)}",
        f"Required: {', '.join(required_names) if required_names else 'none'}",
        f"Type composition: {type_summary}",
    ]

    summary = (
        f"{function_name} is materially composed of {len(params)} parameter(s) "
        f"({type_summary}), of which {len(required_names)} are required."
    )

    return CauseAnalysis(
        cause_type="material",
        summary=summary,
        evidence=evidence,
        confidence="high",
    )


def _analyze_formal(
    function_name: str,
    schema: dict[str, Any],
    params: list[dict[str, Any]],
) -> CauseAnalysis:
    """Determine the formal cause: the shape/signature of the function."""
    param_type = schema.get("parameters", {}).get("type", "unknown")
    has_required = bool(schema.get("parameters", {}).get("required"))
    has_enum = any(p.get("enum") is not None for p in params)

    evidence = [
        f"Top-level parameter type: {param_type}",
        f"Has required constraints: {has_required}",
        f"Has enum constraints: {has_enum}",
        f"Parameter count: {len(params)}",
    ]

    constraints = []
    if has_required:
        constraints.append("required-field constraints")
    if has_enum:
        constraints.append("enumerated-value constraints")
    if not constraints:
        constraints.append("no additional constraints")

    summary = (
        f"The formal shape of {function_name} is a {param_type} schema "
        f"with {len(params)} properties and {', '.join(constraints)}."
    )

    return CauseAnalysis(
        cause_type="formal",
        summary=summary,
        evidence=evidence,
        confidence="high",
    )


# Verb-to-purpose mapping for efficient/final cause inference.
_VERB_PURPOSES: dict[str, str] = {
    "get": "retrieval",
    "fetch": "retrieval",
    "read": "retrieval",
    "list": "enumeration",
    "search": "search",
    "find": "search",
    "create": "creation",
    "add": "creation",
    "insert": "creation",
    "update": "mutation",
    "set": "mutation",
    "modify": "mutation",
    "patch": "mutation",
    "delete": "destruction",
    "remove": "destruction",
    "send": "transmission",
    "post": "transmission",
    "notify": "notification",
    "validate": "validation",
    "check": "validation",
    "convert": "transformation",
    "transform": "transformation",
    "calculate": "computation",
    "compute": "computation",
}


def _infer_verb_and_purpose(function_name: str) -> tuple[str, str]:
    """Extract the leading verb and map it to a purpose category."""
    # Split on underscores or camelCase boundaries.
    parts = function_name.replace("-", "_").lower().split("_")
    verb = parts[0] if parts else ""
    purpose = _VERB_PURPOSES.get(verb, "general operation")
    return verb, purpose


def _analyze_efficient(
    function_name: str, schema: dict[str, Any]
) -> CauseAnalysis:
    """Determine the efficient cause: what triggers the function."""
    description = schema.get("description", "")
    verb, _ = _infer_verb_and_purpose(function_name)

    evidence = [
        f"Function name verb: '{verb}'",
        f"Description: '{description}'",
    ]

    # The efficient cause in function-calling is always the caller/agent.
    summary = (
        f"{function_name} is triggered by an external caller (agent, user, or "
        f"system event). The verb '{verb}' indicates the initiating action."
    )

    return CauseAnalysis(
        cause_type="efficient",
        summary=summary,
        evidence=evidence,
        confidence="medium",
    )


def _analyze_final(
    function_name: str, schema: dict[str, Any]
) -> CauseAnalysis:
    """Determine the final cause: the purpose/telos of the function."""
    description = schema.get("description", "")
    _, purpose = _infer_verb_and_purpose(function_name)

    evidence = [
        f"Inferred purpose category: {purpose}",
        f"Description: '{description}'",
    ]

    if description:
        summary = (
            f"The telos of {function_name} is {purpose}: {description}"
        )
        confidence = "high"
    else:
        summary = (
            f"The telos of {function_name} is inferred as {purpose} "
            f"based on naming convention alone."
        )
        confidence = "low"

    return CauseAnalysis(
        cause_type="final",
        summary=summary,
        evidence=evidence,
        confidence=confidence,
    )


def analyze_four_causes(schema: dict[str, Any]) -> FourCausesReport:
    """Perform a complete Aristotelian four-causes analysis.

    Args:
        schema: A function-calling schema dict with at minimum 'name'
            and optionally 'description' and 'parameters'.

    Returns:
        A FourCausesReport containing all four cause analyses.

    Raises:
        ValueError: If 'name' is missing from the schema.
    """
    function_name = schema.get("name", "")
    if not function_name:
        raise ValueError("Schema must include a 'name' field.")

    params = _extract_parameters(schema)

    return FourCausesReport(
        function_name=function_name,
        material=_analyze_material(function_name, params),
        formal=_analyze_formal(function_name, schema, params),
        efficient=_analyze_efficient(function_name, schema),
        final=_analyze_final(function_name, schema),
    )
