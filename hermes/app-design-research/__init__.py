"""Registration for Hugging App's bounded AppLlama compatibility tool."""

from .research import TOOL_SCHEMA, app_design_research


def register(ctx) -> None:
    def handler(args, **kwargs):
        return app_design_research(args, ctx=ctx, **kwargs)

    ctx.register_tool(
        name="app_design_research",
        toolset="app-design-research",
        schema=TOOL_SCHEMA,
        handler=handler,
        description="Report that AppLlama website research is disabled in this public candidate.",
    )
