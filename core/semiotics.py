"""Peircean semiotic analysis for function-calling schemas.

This module applies Peirce's triadic sign model to function-calling:

- **Representamen** (the sign): The function name, identifier, and syntactic
  form that stands for the operation.
- **Object** (the referent): What the function acts upon in the world — the
  external entity, state, or resource it reads, writes, or transforms.
- **Interpretant** (the meaning): What the caller understands when they see
  and invoke the function — the mental model or expectation produced.

The analysis is deterministic, based on naming conventions, parameter
inspection, and description parsing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SignAnalysis:
    """Analysis of a single semiotic component.

    Attributes:
        component: 'representamen', 'object', or 'interpretant'.
        summary: Human-readable description of this semiotic element.
        evidence: Schema elements that ground the analysis.
    """

    component: str
    summary: str
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {
            "component": self.component,
            "summary": self.summary,
            "evidence": self.evidence,
        }


@dataclass
class SemioticAnalysis:
    """Complete Peircean semiotic analysis of a function.

    Attributes:
        function_name: The analyzed function's name.
        representamen: The sign — the function's syntactic identity.
        object: The referent — what the function acts upon.
        interpretant: The meaning — what the caller understands.
    """

    function_name: str
    representamen: SignAnalysis
    object: SignAnalysis
    interpretant: SignAnalysis

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full analysis."""
        return {
            "function_name": self.function_name,
            "representamen": self.representamen.to_dict(),
            "object": self.object.to_dict(),
            "interpretant": self.interpretant.to_dict(),
        }

    @property
    def all_components(self) -> list[SignAnalysis]:
        """Return all three semiotic components as a list."""
        return [self.representamen, self.object, self.interpretant]


# ---------------------------------------------------------------------------
# Name-parsing utilities
# ---------------------------------------------------------------------------

def _split_function_name(name: str) -> list[str]:
    """Split a function name into constituent words.

    Handles snake_case, kebab-case, and camelCase.
    """
    # Replace hyphens with underscores, then split on underscores.
    normalized = name.replace("-", "_")
    parts: list[str] = []
    for segment in normalized.split("_"):
        # Split camelCase within each segment.
        current = ""
        for char in segment:
            if char.isupper() and current:
                parts.append(current.lower())
                current = char
            else:
                current += char
        if current:
            parts.append(current.lower())
    return parts


def _extract_verb_and_noun(name: str) -> tuple[str, str]:
    """Extract the leading verb and trailing noun from a function name."""
    parts = _split_function_name(name)
    if not parts:
        return "", ""
    verb = parts[0]
    noun = "_".join(parts[1:]) if len(parts) > 1 else ""
    return verb, noun


# Verb-to-action-type mapping for interpretant inference.
_ACTION_TYPES: dict[str, str] = {
    "get": "retrieve",
    "fetch": "retrieve",
    "read": "retrieve",
    "list": "enumerate",
    "search": "query",
    "find": "query",
    "create": "construct",
    "add": "construct",
    "insert": "construct",
    "update": "modify",
    "set": "modify",
    "modify": "modify",
    "patch": "modify",
    "delete": "destroy",
    "remove": "destroy",
    "send": "transmit",
    "post": "transmit",
    "notify": "signal",
    "validate": "verify",
    "check": "verify",
    "convert": "transform",
    "transform": "transform",
    "calculate": "compute",
    "compute": "compute",
}


def _analyze_representamen(
    function_name: str, schema: dict[str, Any]
) -> SignAnalysis:
    """Analyze the sign — the function's syntactic identity."""
    parts = _split_function_name(function_name)
    verb, noun = _extract_verb_and_noun(function_name)

    param_names = list(
        schema.get("parameters", {}).get("properties", {}).keys()
    )

    evidence = [
        f"Function name: '{function_name}'",
        f"Name components: {parts}",
        f"Verb: '{verb}', Noun: '{noun}'",
        f"Parameter names: {param_names}",
    ]

    summary = (
        f"The representamen (sign) is the identifier '{function_name}', "
        f"composed of the action verb '{verb}' "
        + (f"and the target noun '{noun}'" if noun else "with no explicit target noun")
        + f". Together with {len(param_names)} parameter name(s), "
        f"this sign constitutes the syntactic surface the caller encounters."
    )

    return SignAnalysis(
        component="representamen",
        summary=summary,
        evidence=evidence,
    )


def _analyze_object(
    function_name: str, schema: dict[str, Any]
) -> SignAnalysis:
    """Analyze the referent — what the function acts upon in the world."""
    _, noun = _extract_verb_and_noun(function_name)
    description = schema.get("description", "")
    params = schema.get("parameters", {}).get("properties", {})

    evidence = [
        f"Target noun from name: '{noun}'",
        f"Description: '{description}'",
    ]

    # Infer the referent from the noun and description.
    if noun:
        referent = noun.replace("_", " ")
    elif description:
        referent = "the entity described as: " + description[:80]
    else:
        referent = "an unspecified target"

    # Check if parameters hint at specific objects.
    object_hints: list[str] = []
    for param_name, param_spec in params.items():
        param_desc = param_spec.get("description", "")
        if param_desc:
            object_hints.append(f"'{param_name}': {param_desc}")

    if object_hints:
        evidence.append(f"Parameter-level referents: {'; '.join(object_hints)}")

    summary = (
        f"The object (referent) is {referent}. "
        f"The function acts upon this entity in the world"
        + (f", parameterized by {len(params)} input(s) that further specify "
           f"the target." if params else ".")
    )

    return SignAnalysis(
        component="object",
        summary=summary,
        evidence=evidence,
    )


def _analyze_interpretant(
    function_name: str, schema: dict[str, Any]
) -> SignAnalysis:
    """Analyze the meaning — what the caller understands."""
    verb, noun = _extract_verb_and_noun(function_name)
    description = schema.get("description", "")
    action_type = _ACTION_TYPES.get(verb, "perform an operation on")

    evidence = [
        f"Verb '{verb}' maps to action type '{action_type}'",
        f"Description: '{description}'",
    ]

    # Build the interpretant from verb-mapping and description.
    if description:
        meaning = description
    elif noun:
        meaning = f"{action_type} {noun.replace('_', ' ')}"
    else:
        meaning = f"{action_type} an unspecified target"

    # Enum parameters sharpen the interpretant.
    params = schema.get("parameters", {}).get("properties", {})
    enum_params = {
        name: spec.get("enum")
        for name, spec in params.items()
        if spec.get("enum")
    }
    if enum_params:
        enum_desc = "; ".join(
            f"'{name}' can be {opts}" for name, opts in enum_params.items()
        )
        evidence.append(f"Enum constraints sharpen meaning: {enum_desc}")

    summary = (
        f"The interpretant (meaning the caller derives) is: '{meaning}'. "
        f"The caller understands this sign as an invitation to {action_type}"
        + (f" {noun.replace('_', ' ')}" if noun else "")
        + (f", with constrained choices ({', '.join(enum_params.keys())})"
           if enum_params else "")
        + "."
    )

    return SignAnalysis(
        component="interpretant",
        summary=summary,
        evidence=evidence,
    )


def analyze_semiotics(schema: dict[str, Any]) -> SemioticAnalysis:
    """Perform a complete Peircean semiotic analysis.

    Args:
        schema: A function-calling schema dict with at minimum 'name'.

    Returns:
        A SemioticAnalysis with representamen, object, and interpretant.

    Raises:
        ValueError: If 'name' is missing from the schema.
    """
    function_name = schema.get("name", "")
    if not function_name:
        raise ValueError("Schema must include a 'name' field.")

    return SemioticAnalysis(
        function_name=function_name,
        representamen=_analyze_representamen(function_name, schema),
        object=_analyze_object(function_name, schema),
        interpretant=_analyze_interpretant(function_name, schema),
    )
