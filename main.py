from typing import Literal

from pydantic import BaseModel, Field
from rich.prompt import Prompt

from pydantic_ai import Agent, ModelMessage, RunContext, RunUsage, UsageLimits

"""
Input from user will look like 
Caption
Methodology section

And probably flag if its a methodology diagram or statistical plot

"""

class PaperInput(BaseModel):
    caption: str
    methodology: str
    diagram_or_plot: str    # Methodology diagram or Statistical Plot, TODO Enum


class ReferenceExamples(BaseModel):
    examples: list


retrieval_agent = Agent[None, ReferenceExamples](  
    'openrouter:anthropic/claude-sonnet-4-5',
    output_type=ReferenceExamples,  # type: ignore
    instructions=(
        'Use the `examples_search` tool to find a visual examples for given prompt '
        # TODO insert prompt from prompts/retrieval.md
    ),
)

#@retrieval_agent.tool
#async def examples_search(ctx: RunContext[None], prompt: str) -> ReferenceExamples | None:
#    return ReferenceExamples(examples=[])

async def retrieve_examples(usage: RunUsage, ctx: PaperInput):
    # TODO outsource loading of examples
    
    template = f"""Target Input:
    Caption: {ctx.caption}
    Methodology section: {ctx.methodology}
    """
    
    result = await retrieval_agent.run(
        template,
        usage=usage
    )
    
    return result

def gather_input() -> PaperInput:
    methodology_section = Prompt.ask("Please provide methodology section of your paper")
    meth_or_stats = Prompt.ask("Do you want to generate a methodology diagram or statistical plot?", choices=["diagram", "plot"])
    if meth_or_stats == "diagram":
        caption = Prompt.ask("Please provide caption of your target schema")
    elif meth_or_stats == "plot":
        caption = Prompt.ask("Please provide caption of your statistical plot")
    else:
        caption = ""
    
    return PaperInput(caption=caption, methodology=methodology_section, diagram_or_plot=meth_or_stats)

if __name__ == "__main__":
    #asyncio.run(main())
    
    