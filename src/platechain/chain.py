import json

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser
import pandas as pd

from platechain.prompts import (
    AI_REPONSE_DICT,
    FULL_PROMPT,
    USER_EXAMPLE_DICT,
    create_prompt,
)
from platechain.utils import (
    get_plate_dimensions,
    parse_llm_output,
    tidy_rectangular_plate_data,
)


llm = ChatOpenAI(temperature=0, model="gpt-4").with_fallbacks(
    [ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")]
)
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(FULL_PROMPT),
        ("human", "{user_example}"),
        ("ai", "{ai_response}"),
        ("human", "{input}"),
    ],
)
chain = (
    {
        # Should add validation to ensure numeric indices
        "input": lambda x: x["input"].to_csv(header=False),
        "hint": lambda x: create_prompt(
            num_plates=x.get("num_plates"),
            num_rows=x.get("num_rows"),
            num_cols=x.get("num_cols"),
        ),
        "col_range_str": lambda x: f"from 1 to {x.get('num_cols')}"
        if x.get("num_cols")
        else "",
        "json_format": lambda x: json.dumps(
            [
                {
                    "row_start": 12,
                    "row_end": 12 + x.get("num_rows", 8) - 1,
                    "col_start": 1,
                    "col_end": 1 + x.get("num_cols", 12) - 1,
                    "contents": "Entity ID",
                }
            ]
        ),
        "user_example": lambda x: USER_EXAMPLE_DICT[
            x.get("num_rows", 8) * x.get("num_cols", 12)
        ],
        "ai_response": lambda x: AI_REPONSE_DICT[
            x.get("num_rows", 8) * x.get("num_cols", 12)
        ],
    }
    | prompt
    | llm
    | StrOutputParser()
    | parse_llm_output
)


def parse_plates(
    df: pd.DataFrame,
    num_plates: int | None = None,
    num_rows: int | None = None,
    num_cols: int | None = None,
) -> list[pd.DataFrame]:
    """
    df must have a numeric index
    """
    # TODO: add validation around num_rows and num_cols
    inp_dict = {
        "input": df,
    }
    # Only add if not None so that `.get` can use the default value in our chain
    if num_plates is not None:
        inp_dict["num_plates"] = num_plates
    if num_rows is not None:
        inp_dict["num_rows"] = num_rows
    if num_cols is not None:
        inp_dict["num_cols"] = num_cols
    result = chain.invoke(inp_dict)

    plates: list[pd.DataFrame] = []
    for llm_response in result:
        plate_data = get_plate_dimensions(df, llm_response)
        plates.append(tidy_rectangular_plate_data(plate_data))
    # Returns a list of "tidy" plates so that a downstream user can decide what to do with them
    return plates
