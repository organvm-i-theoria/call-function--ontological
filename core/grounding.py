"""Grounding module: maps function-call signatures to ontological categories.

This module takes a dict describing a function (name, params, description)
and produces a GroundingReport listing which of the 12 ontological concepts
apply and how they anchor the function to its operational context.

Grounding is the synthetic step that connects the three philosophical
traditions (Aristotelian, Heideggerian, Peircean) into a unified view.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.ontology import (
    ALL_CONCEPTS,
    CONCEPTS_BY_KEY,
    Domain,
    OntologicalConcept,
)


@dataclass
class GroundingMapping:
    """A single mapping from an ontological concept to a function element.

    Attributes:
        concept: The ontological concept being applied.
        applies: Whether this concept is applicable to the function.
        anchor: The specific schema element(s) that ground this concept.
        explanation: Why this concept applies (or does not apply).
    """

    concept: OntologicalConcept
    applies: bool
    anchor: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {
            "concept": self.concept.name,
            "key": self.concept.key,
            "domain": self.concept.domain.value,
            "applies": self.applies,
            "anchor": self.anchor,
            "explanation": self.explanation,
        }


@dataclass
class GroundingReport:
    """Complete grounding report for a function.

    Attributes:
        function_name: The analyzed function's name.
        mappings: One GroundingMapping per ontological concept.
        applicable_count: How many of the 12 concepts apply.
        coverage_ratio: Fraction of concepts that apply (0.0 to 1.0).
    """

    function_name: str
    mappings: list[GroundingMapping] = field(default_factory=list)

    @property
    def applicable_count(self) -> int:
        """Count of concepts that apply."""
        return sum(1 for m in self.mappings if m.applies)

    @property
    def coverage_ratio(self) -> float:
        """Fraction of concepts that apply."""
        if not self.mappings:
            return 0.0
        return self.applicable_count / len(self.mappings)

    def applicable_mappings(self) -> list[GroundingMapping]:
        """Return only the mappings where the concept applies."""
        return [m for m in self.mappings if m.applies]

    def mappings_by_domain(self, domain: Domain) -> list[GroundingMapping]:
        """Return mappings filtered by philosophical domain."""
        return [m for m in self.mappings if m.concept.domain == domain]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full report."""
        return {
            "function_name": self.function_name,
            "applicable_count": self.applicable_count,
            "total_concepts": len(self.mappings),
            "coverage_ratio": round(self.coverage_ratio, 3),
            "mappings": [m.to_dict() for m in self.mappings],
        }


def _has_parameters(schema: dict[str, Any]) -> bool:
    """Check if the schema defines any parameters."""
    return bool(schema.get("parameters", {}).get("properties"))


def _has_description(schema: dict[str, Any]) -> bool:
    """Check if the schema has a description."""
    return bool(schema.get("description", "").strip())


def _has_required(schema: dict[str, Any]) -> bool:
    """Check if the schema has required parameters."""
    return bool(schema.get("parameters", {}).get("required"))


def _has_enums(schema: dict[str, Any]) -> bool:
    """Check if any parameters use enum constraints."""
    props = schema.get("parameters", {}).get("properties", {})
    return any(spec.get("enum") for spec in props.values())


def ground_function(schema: dict[str, Any]) -> GroundingReport:
    """Map a function-calling schema to all 12 ontological categories.

    Args:
        schema: A function-calling schema dict with at minimum 'name'.

    Returns:
        A GroundingReport with one mapping per concept.

    Raises:
        ValueError: If 'name' is missing from the schema.
    """
    function_name = schema.get("name", "")
    if not function_name:
        raise ValueError("Schema must include a 'name' field.")

    has_params = _has_parameters(schema)
    has_desc = _has_description(schema)
    has_req = _has_required(schema)
    has_enum = _has_enums(schema)
    description = schema.get("description", "")

    mappings: list[GroundingMapping] = []

    # --- Aristotelian ---

    # Material Cause: always applies if there are parameters.
    material = CONCEPTS_BY_KEY["material_cause"]
    if has_params:
        props = schema["parameters"]["properties"]
        param_list = ", ".join(props.keys())
        mappings.append(GroundingMapping(
            concept=material,
            applies=True,
            anchor=f"parameters: {param_list}",
            explanation=(
                f"The function's material consists of {len(props)} parameter(s) "
                f"({param_list}) that constitute its raw input substance."
            ),
        ))
    else:
        mappings.append(GroundingMapping(
            concept=material,
            applies=False,
            anchor="no parameters",
            explanation="The function takes no parameters; material cause is vacuous.",
        ))

    # Formal Cause: always applies (every function has a schema shape).
    formal = CONCEPTS_BY_KEY["formal_cause"]
    constraints = []
    if has_req:
        constraints.append("required-field constraints")
    if has_enum:
        constraints.append("enum constraints")
    constraint_text = ", ".join(constraints) if constraints else "no additional constraints"
    mappings.append(GroundingMapping(
        concept=formal,
        applies=True,
        anchor=f"schema structure with {constraint_text}",
        explanation=(
            f"The formal shape is defined by the schema: an object type "
            f"with {constraint_text}."
        ),
    ))

    # Efficient Cause: always applies (something must trigger the function).
    efficient = CONCEPTS_BY_KEY["efficient_cause"]
    mappings.append(GroundingMapping(
        concept=efficient,
        applies=True,
        anchor="caller/agent invocation",
        explanation=(
            f"'{function_name}' is triggered by an external caller — an agent, "
            f"user, or system event that initiates the function call."
        ),
    ))

    # Final Cause: applies if there is a description or recognizable verb.
    final = CONCEPTS_BY_KEY["final_cause"]
    if has_desc:
        mappings.append(GroundingMapping(
            concept=final,
            applies=True,
            anchor=f"description: '{description[:60]}'",
            explanation=f"The function's telos is stated: {description}",
        ))
    else:
        mappings.append(GroundingMapping(
            concept=final,
            applies=True,
            anchor=f"function name: '{function_name}'",
            explanation=(
                f"The telos is implicit in the name '{function_name}', "
                f"though no explicit description is provided."
            ),
        ))

    # --- Heideggerian ---

    # Dasein: always applies (every function assumes a world).
    dasein = CONCEPTS_BY_KEY["dasein"]
    mappings.append(GroundingMapping(
        concept=dasein,
        applies=True,
        anchor="function existence presupposes a callable world",
        explanation=(
            f"'{function_name}' assumes a world in which it can be called — "
            f"a runtime, data sources, and the entities its parameters reference."
        ),
    ))

    # Zuhandenheit: applies when function can operate transparently.
    zuhandenheit = CONCEPTS_BY_KEY["zuhandenheit"]
    mappings.append(GroundingMapping(
        concept=zuhandenheit,
        applies=True,
        anchor="valid-input happy path",
        explanation=(
            f"When called with valid arguments, '{function_name}' is ready-to-hand: "
            f"the caller uses it without reflecting on the function itself."
        ),
    ))

    # Vorhandenheit: applies (breakdown is always possible).
    vorhandenheit = CONCEPTS_BY_KEY["vorhandenheit"]
    breakdown_triggers = []
    if has_req:
        breakdown_triggers.append("missing required parameters")
    if has_enum:
        breakdown_triggers.append("invalid enum values")
    breakdown_triggers.append("unexpected errors")
    mappings.append(GroundingMapping(
        concept=vorhandenheit,
        applies=True,
        anchor=f"breakdown conditions: {', '.join(breakdown_triggers)}",
        explanation=(
            f"'{function_name}' becomes present-at-hand when breakdown occurs: "
            f"{', '.join(breakdown_triggers)}."
        ),
    ))

    # --- Peircean ---

    # Representamen: always applies (the function has a name).
    representamen = CONCEPTS_BY_KEY["representamen"]
    mappings.append(GroundingMapping(
        concept=representamen,
        applies=True,
        anchor=f"identifier: '{function_name}'",
        explanation=(
            f"The sign is the identifier '{function_name}' together with "
            f"its parameter names — the syntactic surface the caller encounters."
        ),
    ))

    # Object: applies if we can identify what the function acts upon.
    obj = CONCEPTS_BY_KEY["object"]
    name_parts = function_name.replace("-", "_").lower().split("_")
    noun = "_".join(name_parts[1:]) if len(name_parts) > 1 else ""
    if noun or has_desc:
        referent = noun.replace("_", " ") if noun else description[:60]
        mappings.append(GroundingMapping(
            concept=obj,
            applies=True,
            anchor=f"referent: '{referent}'",
            explanation=(
                f"The function's referent (what it acts upon) is identifiable "
                f"as '{referent}'."
            ),
        ))
    else:
        mappings.append(GroundingMapping(
            concept=obj,
            applies=False,
            anchor="no identifiable referent",
            explanation=(
                "Neither the function name nor description identifies a clear "
                "referent for the function to act upon."
            ),
        ))

    # Interpretant: applies if there is enough information for meaning.
    interpretant = CONCEPTS_BY_KEY["interpretant"]
    if has_desc or noun:
        mappings.append(GroundingMapping(
            concept=interpretant,
            applies=True,
            anchor="name + description convey meaning",
            explanation=(
                f"The caller can derive meaning from '{function_name}'"
                + (f" and its description" if has_desc else "")
                + "."
            ),
        ))
    else:
        mappings.append(GroundingMapping(
            concept=interpretant,
            applies=False,
            anchor="insufficient semiotic information",
            explanation=(
                "Without a description or meaningful noun, the caller cannot "
                "reliably derive the function's intended meaning."
            ),
        ))

    # --- Synthetic ---

    # Grounding: always applies (this analysis itself is the grounding).
    grounding_concept = CONCEPTS_BY_KEY["grounding"]
    applicable_so_far = sum(1 for m in mappings if m.applies)
    mappings.append(GroundingMapping(
        concept=grounding_concept,
        applies=True,
        anchor=f"{applicable_so_far}/10 concepts grounded",
        explanation=(
            f"This grounding analysis anchors {applicable_so_far} of 10 "
            f"tradition-specific concepts to concrete schema elements."
        ),
    ))

    # Telos Bridge: applies if both final cause and system context exist.
    telos_bridge = CONCEPTS_BY_KEY["telos_bridge"]
    if has_desc:
        mappings.append(GroundingMapping(
            concept=telos_bridge,
            applies=True,
            anchor="final cause + system context",
            explanation=(
                f"The function's micro-telos ('{description[:50]}') can be "
                f"connected to a broader system purpose through this bridge."
            ),
        ))
    else:
        mappings.append(GroundingMapping(
            concept=telos_bridge,
            applies=False,
            anchor="no explicit telos to bridge",
            explanation=(
                "Without an explicit description, the bridge from micro-telos "
                "to system purpose cannot be reliably constructed."
            ),
        ))

    return GroundingReport(
        function_name=function_name,
        mappings=mappings,
    )
