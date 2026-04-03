# CHANGELOG


## v0.2.0 (2026-04-03)

### Features

- Add automated release workflow with semantic versioning
  ([`462b62b`](https://github.com/Jimdrews/fastmcp-trello/commit/462b62b1f5ffabf40f52a1a5e40d1cc0dc7ac408))

Add a manually-triggered GitHub Actions workflow that uses python-semantic-release to bump the
  version from conventional commits, create a tag, and publish a GitHub release — which then
  triggers the existing publish.yml for PyPI.


## v0.1.1 (2026-04-02)

### Bug Fixes

- Prevent credential leakage in unhandled HTTP error responses
  ([`92778d5`](https://github.com/Jimdrews/fastmcp-trello/commit/92778d50478a084260ecdcdfef29317b695c2a2d))

Replace raise_for_status() with a catch-all for unhandled 4xx status codes. Previously, status codes
  not in the known set (401, 404, 429, 500+) fell through to httpx's raise_for_status(), which
  includes the full request URL — with API key and token — in the exception message.

### Chores

- Bump version to 0.1.1
  ([`fef580e`](https://github.com/Jimdrews/fastmcp-trello/commit/fef580e6eab135db6cd03945ae90d71b2bd682f2))

### Documentation

- Fix Trello API key setup instructions
  ([`f5e1e13`](https://github.com/Jimdrews/fastmcp-trello/commit/f5e1e1377cc212209b113d074aac47681a3c7622))

The prerequisites now correctly describe creating a Power-Up first, then generating an API key, then
  clicking the Token link.

### Features

- Improve GitHub discoverability with banner, badges, and metadata
  ([`c982fe0`](https://github.com/Jimdrews/fastmcp-trello/commit/c982fe08ed4857af76212780d669149ea465126e))

- Add SVG banner and social preview images - Fix broken PyPI badges (switch to badge.fury.io) - Add
  MCP explainer and keyword-rich heading to README - Expand pyproject.toml keywords and add Homepage
  URL


## v0.1.0 (2026-04-02)

### Bug Fixes

- Add contents:read permission to publish job
  ([`64216a6`](https://github.com/Jimdrews/fastmcp-trello/commit/64216a69c14552f7f7cf8638e808182379a19b46))

The publish job's explicit permissions block overrides defaults, dropping contents:read needed for
  actions/checkout.

### Chores

- Add pre-commit hooks, ruff, pyrefly, and GitHub Actions CI
  ([`2daaa64`](https://github.com/Jimdrews/fastmcp-trello/commit/2daaa649fa5c51c0a2462c814a08872f329052ce))

Set up local quality gates (ruff lint/format, pyrefly type check, pytest) via pre-commit framework
  and mirror them in a GitHub Actions CI workflow. Fix existing lint violations and type errors
  across the codebase.

- Add PyPI publish workflow with trusted publishing
  ([`a4ce895`](https://github.com/Jimdrews/fastmcp-trello/commit/a4ce8953107f827ee36abd8b18c8bda76861d1a4))

Adds a GitHub Actions workflow that builds and publishes to PyPI on release using uv build/publish
  with OIDC trusted publishing.

- Initialize project with uv, fastmcp, and test infrastructure
  ([`ecdf1bb`](https://github.com/Jimdrews/fastmcp-trello/commit/ecdf1bbc25cc0417535446aaa087cb62c93e3f96))

Set up trello-mcp package with src layout, runtime deps (fastmcp, httpx, pydantic), dev deps
  (pytest, pytest-asyncio, pytest-httpx), and scaffolded source/test directory structure.

### Features

- Add async TrelloClient with error handling and full test coverage
  ([`6d34f58`](https://github.com/Jimdrews/fastmcp-trello/commit/6d34f58c85702dbd62b761079a4d45837c5639b8))

Implement TrelloClient wrapping Trello REST API with httpx.AsyncClient. Covers all Tier 1
  operations: boards, lists, cards, comments, search. Includes friendly error messages for
  401/404/429/5xx responses.

- Add FastMCP server with all 10 Tier 1 tools
  ([`03a2b95`](https://github.com/Jimdrews/fastmcp-trello/commit/03a2b956fb98e984e262eba3374023a7bebdc5a6))

Implement MCP tools for boards (get_boards, get_board, get_lists), cards (get_cards, get_card,
  create_card, update_card, archive_card), and interactions (add_comment, search_cards). All tools
  return formatted markdown and handle API errors gracefully. Full test coverage with mocked
  TrelloClient.

- Add Pydantic models with markdown rendering
  ([`f9e8c5a`](https://github.com/Jimdrews/fastmcp-trello/commit/f9e8c5afbf50701b6068a2d61bf7cc674d3ac791))

Implement Label, Member, Comment, Card, TrelloList, and Board models with to_markdown() and
  to_compact_markdown() methods for token-efficient output. Includes full test coverage for parsing
  and rendering.

- Add README, LICENSE, CONTRIBUTING, and rename package to fastmcp-trello
  ([`927b573`](https://github.com/Jimdrews/fastmcp-trello/commit/927b5730ce022ba8bca375ccd50a020822bf022c))

Adds project discoverability files (README with tool table, multi-client install configs, badges;
  MIT LICENSE; CONTRIBUTING guide) and enriches pyproject.toml with license, keywords, classifiers,
  URLs, and a console entry point. Renames package from trello-mcp to fastmcp-trello to avoid PyPI
  name conflict. Refactors __main__.py with a main() function and --transport flag supporting stdio
  and http.

### Testing

- Add integration tests, live smoke tests, and pytest config
  ([`16e1be0`](https://github.com/Jimdrews/fastmcp-trello/commit/16e1be0db5f17286699f9acdee44b8314ad6ef28))

Add end-to-end integration test calling all 10 tools through FastMCP in-memory client. Add opt-in
  live smoke tests against real Trello API. Configure pytest with asyncio_mode=auto and live marker
  filtering.
