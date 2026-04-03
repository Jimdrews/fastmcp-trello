import argparse

from trello_mcp.server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Trello MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    args = parser.parse_args()
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
