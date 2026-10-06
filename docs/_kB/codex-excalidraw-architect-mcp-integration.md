# Codex + Excalidraw Architect MCP Integration

## Purpose

This workstation has a user-level integration for
[BV-Venky/excalidraw-architect-mcp](https://github.com/BV-Venky/excalidraw-architect-mcp).
It lets Codex create, inspect, modify, and export real Excalidraw diagrams
through a local stdio MCP server, without a diagram API key.

The setup is user-scoped: it changes neither system Python nor project
configuration, requires no `sudo`, and is available to future Codex sessions.

## Runtime configuration

Codex configuration is stored outside this repository at
`~/.codex/config.toml`:

```toml
[mcp_servers.excalidraw-architect]
command = "uvx"
args = ["--from", "excalidraw-architect-mcp[png]", "excalidraw-architect-mcp"]
```

The server name is `excalidraw-architect` and its transport is stdio.
`uvx` supplies an isolated runtime. The `[png]` extra enables CairoSVG-based
PNG export, alongside the normal `.excalidraw` and SVG support.

Validate the entry with:

```bash
codex mcp list
codex mcp get excalidraw-architect --json
```

## Upstream checkout and skills

The upstream source checkout is `~/.local/share/excalidraw-architect-mcp`.
The verified version is v2.0.0 (commit `6280bb3`), which requires Python
`>=3.10`. The host has Python 3.14 and uvx 0.12.7.

The upstream skills are symlinked—not copied—into Codex's user skill
directory. Updating the checkout therefore updates their content without
creating stale duplicates.

| Skill | User-level location | Use |
| --- | --- | --- |
| `excalidraw-architect` | `~/.agents/skills/excalidraw-architect` | Diagram selection, density, and composition. |
| `excalidraw-diagram-design` | `~/.agents/skills/excalidraw-diagram-design` | Readable graph topology, labels, and component metadata. |
| `architecture-knowledge-graph` | `~/.agents/skills/architecture-knowledge-graph` | Persistent service/dependency graph workflows through `kg_*` tools. |

Start a new Codex session after an upstream skill update so discovery refreshes.

## MCP capabilities

Principal diagram tools:

- `list_diagram_types` and `get_diagram_schema`
- `create_diagram`, `get_diagram_info`, and `modify_diagram`
- `mermaid_to_excalidraw` and `export_diagram`

Knowledge-graph tools include `kg_init`, `kg_add_service`, `kg_link`,
`kg_lint`, `kg_render`, `kg_render_view`, `kg_render_domain`,
`kg_render_around`, `whats_connected_to`, `kg_diff`, and `kg_drift`.

For architecture diagrams, pass `nodes` and `connections`; never invent
coordinates. The MCP performs layout, routing, bindings, and
technology-aware styling. For typed diagrams such as `sequence`, `swimlane`,
`er`, or `timeline`, call `get_diagram_schema` first.

## Export behavior

`export_diagram` requires an explicit format:

```text
SVG: format = "svg"  (default)
PNG: format = "png"
```

A `.png` filename alone does not select PNG; without `format: "png"`, the
upstream API writes SVG content. PNG also accepts an optional `scale`.

## Verified smoke test

The exact configured uvx command successfully:

1. initialized over MCP protocol `2025-06-18`;
2. discovered 28 tools;
3. created `Browser → API Gateway → Backend Service → PostgreSQL` plus
   `Backend Service → Redis`;
4. wrote valid `.excalidraw`, SVG, and PNG artifacts; and
5. passed a fresh `codex exec` discovery test, which called
   `list_diagram_types` and `create_diagram`.

Evidence artifacts are deliberately temporary under
`/tmp/excalidraw-architect-test/`.

## Maintenance

Inspect upstream changes before updating:

```bash
git -C ~/.local/share/excalidraw-architect-mcp fetch --prune
git -C ~/.local/share/excalidraw-architect-mcp log --oneline HEAD..origin/main
```

After review, fast-forward the skills checkout:

```bash
git -C ~/.local/share/excalidraw-architect-mcp pull --ff-only
```

To refresh the uvx cache after reviewing a PyPI release:

```bash
uvx --refresh --from 'excalidraw-architect-mcp[png]' excalidraw-architect-mcp
```

That command starts a stdio server; stop it after confirming startup. Do not
replace unrelated sections of `~/.codex/config.toml` or use a global `pip`
installation.

## Prompt patterns

- “Analyze this repository and create a high-level architecture diagram at
  `/tmp/system-overview.excalidraw`.”
- “Create a sequence diagram for login, including retry and error paths.”
- “Convert this Mermaid flowchart to Excalidraw, then export SVG.”
- “Read `docs/architecture.excalidraw` and add Redis before the database.”
- “Build and lint a persistent architecture knowledge graph, then render the
  payments-domain view.”
