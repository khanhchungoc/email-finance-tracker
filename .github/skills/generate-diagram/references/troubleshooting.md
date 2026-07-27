# Troubleshooting — Common Mistakes

Read this when something looks wrong in the output (rendering, layout, edges) or when a CLI invocation fails.

| Mistake | Fix |
|---------|-----|
| Missing `id="0"` and `id="1"` root cells | Always include both at the top of `<root>` |
| Shapes not connected | `source` and `target` on edge must match existing shape `id` values |
| Self-closing edge `mxCell` (`<mxCell ... edge="1" />`) | Use the expanded form with `<mxGeometry relative="1" as="geometry" />` child — self-closing edges won't render |
| `--` inside XML comments | Illegal per XML spec — use single hyphens or rephrase |
| Special characters in `value` | Use XML entities: `&amp;` `&lt;` `&gt;` `&quot;` |
| Exposed `<b>` or HTML tags in label text | Remove inline `<b>` / `<i>` tags from `value="..."`; draw.io renders `&lt;b&gt;` as literal text. Use plain text formatting, `---` dividers, or `fontStyle=1` |
| Cluttered activity boxes / arbitrary step numbers | Keep labels concise and direct; omit step numbers unless explicitly requested. Let directional connectors communicate sequence |
| Literal `\n` in label text | Use `&#xa;` for line breaks in `value` attributes |
| Overlapping shapes | Scale spacing with complexity (200–350px); leave routing corridors |
| Edges crossing through shapes | Add waypoints, distribute entry/exit points, or increase spacing |
| "Up-then-down" arch loop on return connectors | Exit from **BOTTOM** of source (`exitX=0.5;exitY=1`), enter **LEFT** of target (`entryX=0;entryY=0.5`); remove hardcoded top-margin waypoints |
| Decision gateway label text overlapping process box | Expand horizontal gap between gateway and downstream box to $\ge 120\text{px}$; set `labelBackgroundColor=#ffffff;fontSize=11` |
| Vertical handoff line routing through decision diamond | Stagger handoff nodes into a column $\ge 120\text{px}$ right/left of gateway; align source/target center X |
| Arrowhead overlaps bend | Final edge segment before target must be ≥20px — increase spacing or add waypoints |
| `command not found: draw.io` after `brew install --cask drawio` | Homebrew installs the binary as `drawio` (no dot). Use `drawio --version`, not `draw.io --version`. |
| Export command not found on macOS | Try full path `/Applications/draw.io.app/Contents/MacOS/draw.io` |
| Linux: blank/error output headlessly | Prefix command with `xvfb-run -a` |
| Linux: `--no-sandbox` placed before input file | Move `--no-sandbox` to the very end of the command |
| Linux: `Failed to get 'appData' path` / `Home directory not accessible` | `export HOME=/tmp` before invoking drawio |
| Linux server: segfault / EGL / MESA `failed to load driver` errors | Add `--disable-gpu` |
| PDF export fails | Ensure Chromium is available |
| Background color wrong in CLI export | Known CLI bug; add `--transparent` flag or set background via style |
| Final `-e` PNG won't open in image viewers | Run `python3 <this-skill-dir>/scripts/repair_png.py <path>`. |
