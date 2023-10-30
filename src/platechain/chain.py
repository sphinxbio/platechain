from __future__ import annotations

import json

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser
import pandas as pd
from pydantic import BaseModel, Field
from platechain.constants import COLS_TO_WELLS_DICT, ROWS_TO_WELLS_DICT

from platechain.prompts import (
    AI_REPONSE_DICT,
    FULL_PROMPT,
    USER_EXAMPLE_DICT,
    create_prompt,
)
from platechain.utils import (
    pluck_plate_from_df,
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


class ParsePlateRequest(BaseModel):
    df: pd.DataFrame
    num_plates: int | None
    num_rows: int | None
    num_cols: int | None

    class Config:
        # Needed to allow pandas dataframes as a type
        arbitrary_types_allowed = True


def _load_df(request: ParsePlateRequest):
    """
    Assumes the dataframe has a numeric index
    """
    return request.df.to_csv(header=False)


def _load_prompt(request: ParsePlateRequest):
    return create_prompt(
        num_plates=request.num_plates,
        num_rows=request.num_rows,
        num_cols=request.num_cols,
    )


def _get_col_range_str(request: ParsePlateRequest):
    if request.num_cols:
        return f"from 1 to {request.num_cols}"
    else:
        return ""


def _get_json_format(request: ParsePlateRequest):
    """
    Defaults to a 96-well plate example if no num_rows or num_cols are provided
    """
    num_rows = request.num_rows or 8
    num_cols = request.num_cols or 12
    row_start = 10
    col_start = 1
    return json.dumps(
        [
            {
                "row_start": row_start,
                "row_end": row_start + num_rows - 1,
                "col_start": col_start,
                "col_end": col_start + num_cols - 1,
                "contents": "Entity ID",
            }
        ]
    )


def _get_user_example(request: ParsePlateRequest):
    # Defaults to a 96-well plate example if no num_rows or num_cols are provided
    if request.num_rows is None and request.num_cols is None:
        return USER_EXAMPLE_DICT[96]

    if request.num_rows is None:
        assert (
            request.num_cols in COLS_TO_WELLS_DICT.keys()
        ), f"If num_rows is not provided, num_cols must be a standard value: {COLS_TO_WELLS_DICT.keys()}"  # noqa: E501
        return USER_EXAMPLE_DICT[COLS_TO_WELLS_DICT[request.num_cols]]

    if request.num_cols is None:
        assert (
            request.num_rows in ROWS_TO_WELLS_DICT.keys()
        ), f"If num_cols is not provided, num_rows must be a standard value: {ROWS_TO_WELLS_DICT.keys()}"  # noqa: E501
        return USER_EXAMPLE_DICT[ROWS_TO_WELLS_DICT[request.num_rows]]

    assert (
        request.num_cols * request.num_rows in USER_EXAMPLE_DICT.keys()
    ), f"Invalid plate size -- must be one of {USER_EXAMPLE_DICT.keys()}"
    return USER_EXAMPLE_DICT[request.num_rows * request.num_cols]


def _get_ai_response(request: ParsePlateRequest):
    if request.num_rows is None and request.num_cols is None:
        return AI_REPONSE_DICT[96]

    if request.num_rows is None:
        assert (
            request.num_cols in COLS_TO_WELLS_DICT.keys()
        ), f"If num_rows is not provided, num_cols must be a standard value: {COLS_TO_WELLS_DICT.keys()}"  # noqa: E501
        return AI_REPONSE_DICT[COLS_TO_WELLS_DICT[request.num_cols]]

    if request.num_cols is None:
        assert (
            request.num_rows in ROWS_TO_WELLS_DICT.keys()
        ), f"If num_cols is not provided, num_rows must be a standard value: {ROWS_TO_WELLS_DICT.keys()}"  # noqa: E501
        return AI_REPONSE_DICT[ROWS_TO_WELLS_DICT[request.num_rows]]

    assert (
        request.num_cols * request.num_rows in USER_EXAMPLE_DICT.keys()
    ), f"Invalid plate size -- must be one of {AI_REPONSE_DICT.keys()}"
    return AI_REPONSE_DICT[request.num_rows * request.num_cols]


chain = (
    {
        "input": _load_df,
        "hint": _load_prompt,
        "col_range_str": _get_col_range_str,
        "json_format": _get_json_format,
        "user_example": _get_user_example,
        "ai_response": _get_ai_response,
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
    req = ParsePlateRequest(
        df=df,
        num_plates=num_plates,
        num_rows=num_rows,
        num_cols=num_cols,
    )
    result = chain.invoke(req)

    plates: list[pd.DataFrame] = []
    for llm_response in result:
        plate_data = pluck_plate_from_df(df, llm_response)
        plates.append(tidy_rectangular_plate_data(plate_data))
    # Returns a list of "tidy" plates so that a downstream user can decide what to do with them
    return plates
