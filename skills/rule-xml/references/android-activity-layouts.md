# Android Activity-layout rule

Use `LinearLayout` as the default root and structural layout for every new or substantially changed Activity XML screen. Prefer a vertical `LinearLayout` for stacked screen sections and nested linear groups only where they make the hierarchy clear.

Use `ConstraintLayout` only when the screen genuinely needs relationships that a clear linear hierarchy cannot express without unnecessary nesting, such as:

- two or more siblings constrained to opposing edges or to each other;
- overlaying content;
- preserving a responsive relationship across different widths or heights;
- a prescribed component baseline that already requires `ConstraintLayout`, such as the search-field rule.

Do not introduce `ConstraintLayout` merely as a default root container. Do not refactor an unchanged existing screen just to replace its layout type. When using a `ConstraintLayout` inside a LinearLayout screen, keep it limited to the section that requires constraints.
