# The Living Container — Formal Architecture

A directory hierarchy where every directory IS a system. The hierarchy self-describes.
The container hosts natural, social, digital systems as nested envelopes. Each envelope
defines what can and cannot exist within it. Couplings between systems are declared,
not implicit. The same structural pattern recurs at every scale.

---

## 1. The Axioms

```
AXIOM 1:  Every directory is a system.
AXIOM 2:  Every system is enveloped by exactly one supersystem and envelopes zero or more subsystems.
AXIOM 3:  A system's function, purpose, and limits define what can exist within it.
AXIOM 4:  The same schema governs every level from macro container to micro primitive.
AXIOM 5:  Systems couple through declared inputs and outputs. Undeclared coupling is a defect.
AXIOM 6:  The hierarchy self-describes. Traversing it yields complete knowledge of the whole.
AXIOM 7:  Ideal forms at higher levels are reflected and refracted at lower levels.
          Reflected = structural isomorphism across scales.
          Refracted = transformation through the medium of each level's constraints.
```

---

## 2. The System-as-Directory Schema

Every directory contains a `system.yaml` manifest declaring its identity within the hierarchy.
The schema is identical at all levels. Scale changes; structure does not.

```yaml
# system.yaml — present in every directory at every level

$SYSTEM_ID:            # unique identifier (matches directory name)
$SYSTEM_NAME:          # human-readable name
$LEVEL_INDEX:          # integer: 0 (root) through N (deepest primitive)
$DOMAIN_TYPE:          # physical | biological | cognitive | social | symbolic | technical
$PARENT_ID:            # $SYSTEM_ID of the enveloping directory
$CHILD_IDS:            # [$SYSTEM_ID, ...] of enveloped directories

$FUNCTION:             # WHAT this system does (transformation it performs)
$PURPOSE:              # WHY this system exists (the need it serves in the supersystem)
$BOUNDARY:             # WHERE this system begins and ends (what defines inside vs outside)
$LIMITS:               # WHAT CANNOT happen here (constraints, exclusions, prohibitions)

$INPUTS:               # [{source: $SYSTEM_ID, type: string, description: text}, ...]
$OUTPUTS:              # [{target: $SYSTEM_ID, type: string, description: text}, ...]

$RULES:                # [invariants that govern internal behavior]
$FAILURE_MODES:        # [ways this system can break]
$TRANSFORMATION_RULES: # [how inputs become outputs]
```

---

## 3. The Levels

The container nests from macro (Level 0) to micro (Level 6+).
Not every branch requires all levels. Depth follows necessity.

```
Level 0    CONTAINER        The total system. One per hierarchy.
                            Envelopes all domains. Enveloped by the OS home directory.
                            Function: contain and organize the complete directed system.

Level 1    DOMAIN           Partitions by ontological kind.
                            Each domain admits only systems of its $DOMAIN_TYPE.
                            Function: enforce the categorical boundary.

Level 2    FIELD            A coherent area of activity within a domain.
                            Groups related systems that share context, vocabulary, and purpose.
                            Function: provide shared context for constituent systems.

Level 3    SYSTEM           An operational unit that transforms inputs to outputs.
                            Has a defined function, produces observable results.
                            Function: perform a specific transformation.

Level 4    SUBSYSTEM        A component of a system. Cannot operate independently.
                            Makes sense only in context of its parent system.
                            Function: contribute a partial transformation.

Level 5    MODULE           A functional unit. Reusable. Composable.
                            May serve multiple subsystems.
                            Function: encapsulate a single capability.

Level 6    PRIMITIVE        The micro container. Contains only leaf artifacts.
                            No subdirectories. Only files: scripts, configs, data, schemas.
                            Function: hold the atomic operations.
                            This is the floor. Below this, there are only files.
```

### Level characteristics

| Level | What it defines | What enters | What it contains |
|-------|----------------|-------------|------------------|
| 0 | The whole | Everything the user designs | Domains |
| 1 | Ontological kind | Only systems of matching $DOMAIN_TYPE | Fields |
| 2 | Shared context | Systems sharing vocabulary and purpose | Systems |
| 3 | Transformation | Inputs from declared sources | Subsystems or Modules |
| 4 | Partial transformation | Components of parent system only | Modules or Primitives |
| 5 | Single capability | Reusable functions | Primitives |
| 6 | Atomic operation | Leaf files only | Files (no directories) |

---

## 4. The Naming Grammar

```
CONVENTION 1:  Single hyphen (-) separates words within a concept.
               natural-systems, version-control, signal-processing

CONVENTION 2:  Double hyphen (--) separates function from descriptor.
               domain--physical, system--thermodynamics, module--hash-verify

CONVENTION 3:  The function prefix declares what the directory IS in the hierarchy.
               domain--    field--    system--    sub--    module--    prim--

CONVENTION 4:  The descriptor is the specific identity within that function.
               domain--cognitive, field--perception, system--attention-allocation

CONVENTION 5:  The root container has no prefix. It IS the container.
               Its name is its identity.
```

### Prefix table

| Level | Prefix | Example |
|-------|--------|---------|
| 0 | (none) | `source--all-ever/` |
| 1 | `domain--` | `domain--physical/`, `domain--social/`, `domain--technical/` |
| 2 | `field--` | `field--thermodynamics/`, `field--governance/`, `field--computation/` |
| 3 | `system--` | `system--heat-exchange/`, `system--consensus/`, `system--version-control/` |
| 4 | `sub--` | `sub--radiator/`, `sub--voting-protocol/`, `sub--branch-management/` |
| 5 | `module--` | `module--conduction/`, `module--quorum-check/`, `module--merge-strategy/` |
| 6 | `prim--` | `prim--fourier-transform/`, `prim--majority-rule/`, `prim--three-way-diff/` |

---

## 5. The Coupling Protocol

Systems interact through declared couplings. A coupling is an input/output pair
connecting two systems. Undeclared coupling is structural debt.

### Coupling declaration

In the source system's `system.yaml`:
```yaml
$OUTPUTS:
  - target: "system--consensus"
    type: "proposal"
    description: "Formatted proposal document ready for review"
```

In the target system's `system.yaml`:
```yaml
$INPUTS:
  - source: "system--authoring"
    type: "proposal"
    description: "Formatted proposal document for consensus evaluation"
```

### Coupling types

```
DIRECT COUPLING      A outputs to B. B inputs from A.
                     Both systems declare the coupling.
                     The type and description must match.

BROADCAST COUPLING   A outputs to [B, C, D]. Each declares the input.
                     One-to-many. A does not need to know all consumers.

MEDIATED COUPLING    A outputs to M (mediator). M transforms and outputs to B.
                     Neither A nor B knows the other directly.
                     M's $FUNCTION is the transformation.

REFLEXIVE COUPLING   A outputs to A. The system feeds back into itself.
                     Declared in both $INPUTS and $OUTPUTS with self-reference.
```

### Coupling rules

```
RULE 1:  Every $INPUT must name an existing $SYSTEM_ID as source.
RULE 2:  Every $OUTPUT must name an existing $SYSTEM_ID as target.
RULE 3:  Couplings can cross domain boundaries. (Physical outputs feed social inputs.)
RULE 4:  Couplings cannot skip levels. A Level 3 system couples to Level 3 systems.
         To couple across levels, the coupling passes through the intermediary levels.
RULE 5:  The root container (Level 0) has external inputs (from the OS, from the user)
         and external outputs (artifacts published to the world). These are the system's
         interface with everything outside the container.
```

### Coupling map

A `couplings.yaml` at the root level can declare the complete coupling graph
for computational traversal. This is derived from individual system.yaml files,
not authoritative over them.

```yaml
# couplings.yaml — derived index, not source of truth
couplings:
  - from: "system--research"
    to: "system--authoring"
    type: "findings"
  - from: "system--authoring"
    to: "system--publication"
    type: "manuscript"
  - from: "system--publication"
    to: "system--distribution"
    type: "published-artifact"
```

---

## 6. The Reflection and Refraction Protocol

### Reflection (structural isomorphism)

The same pattern recurs at different scales. This is not coincidence —
it is the container's design principle. Examples:

```
PATTERN: intake → process → output → archive

At Level 1 (domain):
  domain--physical:    matter arrives → transforms → product emitted → waste stored
  domain--social:      proposal arrives → deliberated → decision emitted → record stored
  domain--technical:   data arrives → computed → result emitted → log stored

At Level 3 (system):
  system--research:    sources arrive → analyzed → findings emitted → bibliography stored
  system--build:       source code arrives → compiled → binary emitted → build log stored

At Level 6 (primitive):
  prim--parse:         raw text arrives → tokenized → AST emitted → parse errors stored
```

The pattern is REFLECTED across levels: intake → process → output → archive.
The implementation REFRACTS through each level's medium and constraints.

### How to encode reflection

In `system.yaml`, an optional `$REFLECTS` field names the pattern this system instantiates:

```yaml
$REFLECTS:
  pattern: "intake-process-output-archive"
  role: "process"                    # which position in the pattern this system occupies
  note: "This system is the 'process' stage of the research pipeline"
```

This allows traversal: "show me every system that instantiates the intake-process-output-archive
pattern" returns hits across all levels and all domains.

---

## 7. The Domain Ontology

Level 1 partitions the container into six domains. Each domain constrains
what $DOMAIN_TYPE its children may declare.

```
domain--physical/
  Admits: systems governing matter, energy, space, time, mechanics, thermodynamics.
  Boundary: what exists independent of observers.
  Characteristic transformation: physical state change.

domain--biological/
  Admits: systems governing life, growth, adaptation, evolution, metabolism.
  Boundary: what self-organizes and reproduces.
  Characteristic transformation: adaptation.
  Supersystem constraint: must obey domain--physical laws.

domain--cognitive/
  Admits: systems governing perception, thought, memory, attention, intention.
  Boundary: what processes information within a mind.
  Characteristic transformation: representation.
  Supersystem constraint: requires domain--biological substrate.

domain--social/
  Admits: systems governing communication, institutions, culture, governance, exchange.
  Boundary: what emerges between minds.
  Characteristic transformation: coordination.
  Supersystem constraint: requires domain--cognitive agents.

domain--symbolic/
  Admits: systems governing language, mathematics, logic, notation, representation.
  Boundary: what encodes meaning in transmissible form.
  Characteristic transformation: formalization.
  Supersystem constraint: requires domain--social conventions (shared meaning).

domain--technical/
  Admits: systems governing tools, machines, software, networks, infrastructure.
  Boundary: what extends human capability through designed artifacts.
  Characteristic transformation: automation.
  Supersystem constraint: requires domain--symbolic specifications.
```

### The emergence ladder

```
physical → biological → cognitive → social → symbolic → technical
   ↑                                                        │
   └────────────────── constrains ──────────────────────────┘

Each domain EMERGES from the one below it.
Each domain is CONSTRAINED by all domains below it.
The technical domain feeds back into the physical (machines act on matter).
This creates a cycle, not a ladder — the container is reflexive.
```

---

## 8. The Micro Container (Primitives)

Level 6 is the floor. A primitive directory contains only files. No subdirectories.
It is the atomic unit — the smallest collected envelope.

### Primitive structure

```
prim--three-way-diff/
├── system.yaml          # manifest (same schema as every other level)
├── function.sh          # the operation itself (or .py, .rs, .js, etc.)
├── input.schema.json    # defines what the primitive accepts
├── output.schema.json   # defines what the primitive produces
├── test.sh              # verification of the primitive's behavior
└── README               # human-readable description (optional)
```

### Primitive rules

```
RULE 1:  No subdirectories. If it needs subdirectories, it is a module, not a primitive.
RULE 2:  One function per primitive. If it does two things, split it.
RULE 3:  Input and output schemas are declared. The primitive is a typed function.
RULE 4:  The primitive is testable in isolation.
RULE 5:  Primitives are the only level that contains executable code.
         All higher levels contain only system.yaml manifests and subdirectories.
         (Exception: higher levels may contain derived/generated artifacts.)
```

---

## 9. Example Instantiation

```
source--all-ever/                                    L0  CONTAINER
├── system.yaml
├── couplings.yaml                                       (derived coupling index)
│
├���─ domain--physical/                                L1  DOMAIN
│   ├── system.yaml
│   └── field--thermodynamics/                       L2  FIELD
│       ├── system.yaml
│       └── system--heat-exchange/                   L3  SYSTEM
│           ├── system.yaml
│           ├── sub--conduction/                     L4  SUBSYSTEM
│           │   ├── system.yaml
│           │   └── prim--fourier-law/               L6  PRIMITIVE
│           │       ├── system.yaml
│           │       ├── function.py
│           │       ├── input.schema.json
│           │       └── output.schema.json
│           └── sub--convection/                     L4  SUBSYSTEM
│               ├── system.yaml
│               └── prim--newton-cooling/            L6  PRIMITIVE
│                   └── ...
│
├── domain--cognitive/                               L1  DOMAIN
│   ├── system.yaml
│   └── field--attention/                            L2  FIELD
│       ├── system.yaml
│       └── system--attention-allocation/            L3  SYSTEM
│           ├── system.yaml
│           ├── sub--filtering/                      L4  SUBSYSTEM
│           │   └── prim--salience-threshold/        L6  PRIMITIVE
│           │       └── ...
│           └── sub--switching/                      L4  SUBSYSTEM
│               └── prim--context-switch/            L6  PRIMITIVE
│                   └── ...
│
├── domain--social/                                  L1  DOMAIN
│   ├── system.yaml
│   └── field--governance/                           L2  FIELD
│       ├── system.yaml
│       ├── system--consensus/                       L3  SYSTEM
│       │   ├── system.yaml                              $INPUTS: [{source: system--proposal-drafting}]
│       │   ├── sub--deliberation/                   L4
│       │   │   └── prim--majority-rule/             L6
│       │   └── sub--ratification/                   L4
│       │       └── prim--quorum-check/              L6
│       └── system--proposal-drafting/               L3  SYSTEM
│           ├── system.yaml                              $OUTPUTS: [{target: system--consensus}]
│           └── ...
│
├── domain--symbolic/                                L1  DOMAIN
│   ├── system.yaml
│   └── field--notation/                             L2  FIELD
│       ├── system.yaml
│       └── system--ontological-naming/              L3  SYSTEM
│           ├── system.yaml
│           └── prim--double-hyphen-parse/           L6  PRIMITIVE
│               └── ...
│
├── domain--technical/                               L1  DOMAIN
│   ├── system.yaml
│   ├── field--computation/                          L2  FIELD
│   │   ├── system.yaml
│   │   └── system--version-control/                 L3  SYSTEM
│   │       ├── system.yaml
│   │       ├── sub--branching/                      L4
│   │       ├── sub--merging/                        L4
│   │       └── sub--history/                        L4
│   └── field--infrastructure/                       L2  FIELD
│       ├── system.yaml
│       └── system--container-self-describe/         L3  SYSTEM
│           ├── system.yaml
│           ├── module--manifest-validator/          L5  MODULE
│           │   └── prim--yaml-schema-check/        L6
│           ├── module--coupling-grapher/            L5  MODULE
│           │   └── prim--input-output-resolve/     L6
│           └── module--hierarchy-walker/            L5  MODULE
│               └── prim--depth-first-traverse/     L6
│
└── domain--biological/                              L1  DOMAIN
    ├── system.yaml
    └── field--adaptation/                           L2  FIELD
        └── system--selection-pressure/              L3  SYSTEM
            └── ...
```

---

## 10. Cross-Domain Coupling Example

The power of the container is that systems in different domains couple through
declared interfaces. A technical system consumes symbolic notation. A social
system consumes cognitive judgments. The couplings make these dependencies
explicit and traversable.

```
domain--cognitive/field--attention/system--attention-allocation
    │
    │  $OUTPUT: {target: system--proposal-drafting, type: "focused-topic"}
    │
    ▼
domain--social/field--governance/system--proposal-drafting
    │
    │  $OUTPUT: {target: system--consensus, type: "proposal"}
    │
    ▼
domain--social/field--governance/system--consensus
    │
    │  $OUTPUT: {target: system--version-control, type: "ratified-decision"}
    │
    ▼
domain--technical/field--computation/system--version-control
    │
    │  $OUTPUT: {target: system--ontological-naming, type: "committed-artifact"}
    │
    ▼
domain--symbolic/field--notation/system--ontological-naming
    │
    │  $OUTPUT: {target: system--attention-allocation, type: "named-concept"}
    │           (reflexive — feeds back to cognitive domain)
    ▼
    ╰──→ cycle complete
```

The cycle: attention → drafting → consensus → commit → naming → attention.
Cross-domain couplings form the circulatory system of the living container.

---

## 11. The Container's Relationship to the OS

```
OS HOME DIRECTORY (~/):
├── [OS-provisioned dirs]     ← SYSTEM-CLAIMED (do not touch)
├── [dotfile stratum]         ← TOOL-CLAIMED (managed by chezmoi)
│
└── source--all-ever/         ← THE CONTAINER (the void, self-governed)
    ├── system.yaml           ← root manifest
    ├── domain--physical/
    ├── domain--biological/
    ├── domain--cognitive/
    ├── domain--social/
    ├── domain--symbolic/
    └── domain--technical/

BOUNDARY:  The container occupies the void in the OS's ontology.
           Nothing in the OS references it.
           Nothing in the OS governs it.
           Its isolation is maintained by the system's indifference to it.

INTERFACE: The container's $INPUTS from the outside world:
           - user intention (cognitive → the container)
           - data from network (downloads → ingress → the container)
           - tool state (dotfile stratum → technical domain)

           The container's $OUTPUTS to the outside world:
           - published artifacts (the container → OS → network)
           - committed code (the container → git → remote)
           - deployed configurations (the container → chezmoi → OS)
```

---

## 12. Validation Rules

A valid container satisfies:

```
VALID 1:   Every directory has a system.yaml.
VALID 2:   Every $PARENT_ID in a system.yaml matches the actual parent directory.
VALID 3:   Every $CHILD_IDS entry matches an actual subdirectory.
VALID 4:   Every $INPUT source is a real $SYSTEM_ID somewhere in the hierarchy.
VALID 5:   Every $OUTPUT target is a real $SYSTEM_ID somewhere in the hierarchy.
VALID 6:   No $DOMAIN_TYPE mismatch: a child's domain must match or be
           compatible with its parent domain's admission rules.
VALID 7:   Level 6 (primitive) directories contain no subdirectories.
VALID 8:   Levels 1-5 contain no executable code (only system.yaml and subdirectories).
           Exception: derived/generated artifacts at any level.
VALID 9:   The coupling graph has no orphan references (every named target exists).
VALID 10:  The hierarchy is a tree (no cycles in containment; cycles in coupling are permitted).
```

---

## 13. Lifecycle Operations

```
CREATE:    mkdir domain--new/ && write system.yaml with schema fields
           → parent's $CHILD_IDS updated
           → couplings.yaml regenerated

ARCHIVE:   mv system--old/ _archive/system--old/
           → parent's $CHILD_IDS updated
           → all coupling references marked stale
           → couplings.yaml regenerated with warnings

COUPLE:    Add $OUTPUT to source system.yaml, add $INPUT to target system.yaml
           → couplings.yaml regenerated
           → coupling graph validated (VALID 4, 5, 9)

DECOUPLE:  Remove $OUTPUT and $INPUT entries
           → couplings.yaml regenerated

PROMOTE:   mv sub--x/ to system--x/ (or module to sub, etc.)
           → system.yaml $LEVEL_INDEX updated
           → parent/child references updated

SPLIT:     One system becomes two. Both inherit subset of original couplings.
           → original archived, two new systems created
           → couplings redistributed

MERGE:     Two systems become one. Couplings unified.
           → both originals archived, new system created
```

---

## Summary

The living container is:
- A directory hierarchy where every directory is a system
- Self-describing (system.yaml at every level)
- Hierarchically nested (Level 0 macro → Level 6 micro)
- Domain-partitioned (physical → biological → cognitive → social → symbolic → technical)
- Explicitly coupled (inputs/outputs declared, traversable)
- Reflexive (patterns reflect across scales, couplings form cycles)
- Situated in the OS's void (not governed by any OS convention)
- Validated by structural rules (tree integrity, coupling integrity, domain compatibility)

The container is living because it changes: systems are created, archived, coupled,
decoupled, promoted, split, merged. The system.yaml manifests track these changes.
The hierarchy is the organism. The manifests are its self-description. The couplings
are its circulatory system. The domains are its organs.
