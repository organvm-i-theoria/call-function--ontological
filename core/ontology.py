"""Twelve ontological concepts for function-calling analysis.

This module defines the foundational ontological categories drawn from three
philosophical traditions — Aristotelian, Heideggerian, and Peircean — plus
two synthetic bridging concepts. Each concept is a frozen dataclass with a
validate() method that checks structural integrity.

The twelve concepts form a complete analytic lens for examining any
function-calling interface: what it is made of, what shape it takes,
what triggers it, what it aims at, what world it assumes, how transparent
it is as a tool, what happens when it breaks, what sign it presents,
what it refers to, what meaning the caller derives, how categories anchor
it, and how purpose connects to system-level telos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Domain(Enum):
    """Philosophical tradition a concept belongs to."""

    ARISTOTELIAN = "aristotelian"
    HEIDEGGERIAN = "heideggerian"
    PEIRCEAN = "peircean"
    SYNTHETIC = "synthetic"


@dataclass(frozen=True)
class OntologicalConcept:
    """Base representation of a single ontological concept.

    Attributes:
        name: Human-readable concept label.
        domain: Philosophical tradition the concept originates from.
        description: One-paragraph explanation of what the concept captures
            when applied to function-calling analysis.
        key: Machine-friendly identifier (snake_case).
    """

    name: str
    domain: Domain
    description: str
    key: str = field(default="")

    def __post_init__(self) -> None:
        if not self.key:
            # Derive key from name if not explicitly set.
            object.__setattr__(
                self, "key", self.name.lower().replace(" ", "_").replace("-", "_")
            )

    def validate(self) -> bool:
        """Check that the concept has all required non-empty fields.

        Returns:
            True if the concept is structurally valid.

        Raises:
            ValueError: If any required field is empty or malformed.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Concept name must be non-empty.")
        if not isinstance(self.domain, Domain):
            raise ValueError(f"Domain must be a Domain enum, got {type(self.domain)}.")
        if not self.description or not self.description.strip():
            raise ValueError("Concept description must be non-empty.")
        if not self.key or not self.key.strip():
            raise ValueError("Concept key must be non-empty.")
        return True

    def to_dict(self) -> dict[str, Any]:
        """Serialize the concept to a plain dictionary."""
        return {
            "name": self.name,
            "domain": self.domain.value,
            "description": self.description,
            "key": self.key,
        }


# ---------------------------------------------------------------------------
# Aristotelian causes
# ---------------------------------------------------------------------------

MATERIAL_CAUSE = OntologicalConcept(
    name="Material Cause",
    domain=Domain.ARISTOTELIAN,
    description=(
        "What a function is made of — its parameters, types, and data "
        "structures. The raw material that the function receives and "
        "transforms."
    ),
    key="material_cause",
)

FORMAL_CAUSE = OntologicalConcept(
    name="Formal Cause",
    domain=Domain.ARISTOTELIAN,
    description=(
        "The shape, signature, and schema of a function. The formal "
        "specification that constrains how inputs relate to outputs — "
        "type signatures, JSON schemas, protocol definitions."
    ),
    key="formal_cause",
)

EFFICIENT_CAUSE = OntologicalConcept(
    name="Efficient Cause",
    domain=Domain.ARISTOTELIAN,
    description=(
        "What triggers the function — the caller, event, or agent that "
        "initiates execution. The proximate cause that sets the function "
        "in motion."
    ),
    key="efficient_cause",
)

FINAL_CAUSE = OntologicalConcept(
    name="Final Cause",
    domain=Domain.ARISTOTELIAN,
    description=(
        "The purpose or telos of the function. Why it exists in the "
        "system, what goal it serves, and what end-state it aims to "
        "bring about."
    ),
    key="final_cause",
)

# ---------------------------------------------------------------------------
# Heideggerian phenomenology
# ---------------------------------------------------------------------------

DASEIN = OntologicalConcept(
    name="Dasein",
    domain=Domain.HEIDEGGERIAN,
    description=(
        "The being-in-the-world context of the function — what world "
        "state does the function assume? What must already be true for "
        "this function to make sense? The existential preconditions."
    ),
    key="dasein",
)

ZUHANDENHEIT = OntologicalConcept(
    name="Zuhandenheit",
    domain=Domain.HEIDEGGERIAN,
    description=(
        "Ready-to-hand: the function experienced as a transparent tool. "
        "When the function works seamlessly, the caller does not notice "
        "it — it withdraws into the background of purposeful activity."
    ),
    key="zuhandenheit",
)

VORHANDENHEIT = OntologicalConcept(
    name="Vorhandenheit",
    domain=Domain.HEIDEGGERIAN,
    description=(
        "Present-at-hand: the function as an object of explicit analysis. "
        "When the tool breaks down or becomes the focus of inspection, "
        "it shifts from ready-to-hand to present-at-hand — the mode of "
        "debugging, documentation, and ontological inquiry."
    ),
    key="vorhandenheit",
)

# ---------------------------------------------------------------------------
# Peircean semiotics
# ---------------------------------------------------------------------------

REPRESENTAMEN = OntologicalConcept(
    name="Representamen",
    domain=Domain.PEIRCEAN,
    description=(
        "The sign — the function name, identifier, or symbol that stands "
        "for the operation. The syntactic handle by which the caller "
        "refers to the function."
    ),
    key="representamen",
)

OBJECT = OntologicalConcept(
    name="Object",
    domain=Domain.PEIRCEAN,
    description=(
        "The referent — what the function acts upon in the world. The "
        "external entity, state, or resource that the function reads, "
        "writes, or transforms."
    ),
    key="object",
)

INTERPRETANT = OntologicalConcept(
    name="Interpretant",
    domain=Domain.PEIRCEAN,
    description=(
        "The meaning — what the caller understands when they invoke the "
        "function. The mental model or expectation that the sign "
        "produces in the interpreter."
    ),
    key="interpretant",
)

# ---------------------------------------------------------------------------
# Synthetic bridging concepts
# ---------------------------------------------------------------------------

GROUNDING = OntologicalConcept(
    name="Grounding",
    domain=Domain.SYNTHETIC,
    description=(
        "How ontological categories anchor the function to its operational "
        "context. The synthetic mapping from abstract philosophical "
        "concepts to concrete function-calling mechanics."
    ),
    key="grounding",
)

TELOS_BRIDGE = OntologicalConcept(
    name="Telos Bridge",
    domain=Domain.SYNTHETIC,
    description=(
        "The connection between a function's final cause (its immediate "
        "purpose) and the broader system-level purpose it serves. Bridges "
        "micro-telos (this function call) to macro-telos (the system's "
        "reason for being)."
    ),
    key="telos_bridge",
)

# ---------------------------------------------------------------------------
# Registry: all 12 concepts in canonical order
# ---------------------------------------------------------------------------

ALL_CONCEPTS: tuple[OntologicalConcept, ...] = (
    MATERIAL_CAUSE,
    FORMAL_CAUSE,
    EFFICIENT_CAUSE,
    FINAL_CAUSE,
    DASEIN,
    ZUHANDENHEIT,
    VORHANDENHEIT,
    REPRESENTAMEN,
    OBJECT,
    INTERPRETANT,
    GROUNDING,
    TELOS_BRIDGE,
)

CONCEPTS_BY_KEY: dict[str, OntologicalConcept] = {c.key: c for c in ALL_CONCEPTS}

CONCEPTS_BY_DOMAIN: dict[Domain, list[OntologicalConcept]] = {}
for _concept in ALL_CONCEPTS:
    CONCEPTS_BY_DOMAIN.setdefault(_concept.domain, []).append(_concept)
