import json

import pandas as pd
from pydantic import BaseModel, conint, Field

from platechain.constants import ROW_LETTERS


class LLMPlateResponse(BaseModel):
    row_start: conint(ge=0) = Field(
        ..., description="The starting row of the plate (0-indexed)"
    )
    row_end: conint(ge=0) = Field(
        ..., description="The ending row of the plate (0-indexed)"
    )
    col_start: conint(ge=0) = Field(
        ..., description="The starting column of the plate (0-indexed)"
    )
    col_end: conint(ge=0) = Field(
        ..., description="The ending column of the plate (0-indexed)"
    )
    contents: str


def create_well_str(row: int, col: int, zpad: int = 2) -> str:
    return f"{ROW_LETTERS[row-1]}{col:0{zpad}}"


def tidy_rectangular_plate_data(
    df: pd.DataFrame,
    value_col: str = "value",
    **kwargs,
) -> pd.DataFrame:
    """
    Tidy rectangular plate data

    Assumes that the plate is rectangular and that the data is in the top left
    """
    df = df.reset_index(drop=True)
    new_rows = []
    for i, row in enumerate(df.itertuples()):
        # Skip the first column because it contains the column ID
        for j, val in enumerate(row[1:]):
            # Plates aren't 0 indexed
            row = i + 1
            col = j + 1
            well = create_well_str(row, col)
            plate_info = {
                "row": row,
                "column": col,
                "well": well,
                value_col: val,
                **kwargs,
            }
            new_rows.append(plate_info)
    return pd.DataFrame(new_rows)


def pluck_plate_from_df(df: pd.DataFrame, plate_loc: LLMPlateResponse) -> pd.DataFrame:
    row_start, row_end = plate_loc.row_start, plate_loc.row_end + 1
    col_start, col_end = plate_loc.col_start, plate_loc.col_end + 1
    proposed_plate = df.iloc[
        row_start:row_end,
        col_start:col_end,
    ]
    return proposed_plate


def parse_llm_output(result: str):
    """
    Based on the prompt we expect the result to be a string that looks like:

    '[{"row_start": 12, "row_end": 19, "col_start": 1, "col_end": 12, "contents": "Entity ID"}]'

    We'll load that JSON and turn it into a Pydantic model
    """
    return [LLMPlateResponse(**plate_r) for plate_r in json.loads(result)]
