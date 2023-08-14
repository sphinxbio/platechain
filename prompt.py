# This is pretty good, but often off by 1
FIND_PLATES_PLATE_ORIENTATION = """Plate based data is always rectangular in nature, typically consisting of 24 (4x6), 96 (8x12), 384 (16x24), or 1536 (32 x 48) wells, and may be located anywhere within a dataset.
- There may be gaps in the data or surrounding rows and columns
- The plate data may be partial
- There may be multiple plates.
- Use heuristics, like looking for numbers and patterns consistent with plate dimensions.
- The sequence of the wells might also be a clue, as they are usually arranged in rows or columns and numbered sequentially.
- The header row for each plate (often consisting of monotonically increasing integers) should NOT be considered as the start of the plate.

Each chunk of data might contain multiple plates and there may be multiple chunks.
Use the `contents` field to describe the contents of the plate.

Use 0-indexing for row and column numbers in the final JSON output.

Where are the plates in this data?

Be concise.

Produce your output as JSON. The format should be:
```json
[{"row_start": 25, "row_end": 30, "col_start": 1, "col_end": 12, "contents": "Entity ID"}]
```
"""  # noqa: E501

FIND_PLATES_CONDITION_ORIENTATION = """Plate based data is always rectangular in nature, typically consisting of 24 (4x6), 96 (8x12), 384 (16x24), or 1536 (32 x 48) wells, and may be located anywhere within a dataset.
- There may be gaps in the data or surrounding rows and columns
- The plate data may be partial
- There may be multiple plates.
- Use heuristics, like looking for numbers and patterns consistent with plate dimensions.
- The sequence of the wells might also be a clue, as they are usually arranged in rows or columns and numbered sequentially.
- The header row for each plate (often consisting of monotonically increasing integers) should NOT be considered as the start of the plate.

Each chunk of data might contain multiple plates and there may be multiple chunks.
Use the `contents` field to describe the contents of the plate.

Use 0-indexing for row and column numbers in the final JSON output.

Where are the plates in this data?

Be concise.

Produce your output as JSON. The format should be:
```json
[{"row_start": 25, "row_end": 30, "col_start": 1, "col_end": 12, "contents": "Plate 01"}]
```
"""  # noqa: E501

USER_PLATE_ORIENTATION = """,,,,\nChemical,,1,2,3\n,A,SB123,SB124,SB125\n,B,SB123,SB124,SB126\n,C,,,\n,D,SB123,SB124,SB128\n,Control,1,2,3\n,A,Negative,Positive,Library\n,B,Negative,Positive,Library\n,C,Negative,Positive,Library\n,D,Negative,Positive,Library\nDox Concentration,,,,\n,1,2,3,\nA,0.005,,0.005,\nB,0.005,,0.005,\nC,0.005,,0.005,\nD,0.005,,0.005,\n,,,,\n,,,,\nPrimer,1,2,3,\nA,PR-001,PR-001,PR-001,\nB,PR-002,PR-002,PR-002,\nC,PR-003,PR-003,PR-003,\nD,PR-004,PR-004,PR-004,\n""" # noqa: E501
USER_CONDITION_ORIENTATION = """,,,,\nPlate01,,1,2,3\n,A,SB-001,SB-001,SB-001\n,B,SB-002,SB-002,SB-002\n,C,SB-003,SB-003,SB-003\n,D,SB-004,SB-004,SB-004\n,Plate 2,1,2,3\n,A,SB-005,SB-005,SB-005\n,B,SB-006,SB-006,SB-006\n,C,SB-007,SB-007,SB-007\n,D,SB-008,SB-008,SB-008\nplate3,,,,\n,1,2,3,\nA,SB-193,SB-194,SB-195,\nB,SB-193,SB-194,SB-195,\nC,SB-193,SB-194,SB-195,\nD,SB-193,SB-194,SB-195,\n,,,,\n,,,,\nplate 04,1,2,3,\nA,PR-001,PR-001,PR-001,\nB,PR-002,PR-002,PR-002,\nC,PR-003,PR-003,PR-003,\nD,PR-004,PR-004,PR-004,\n"""  # noqa: E501

ASSISTANT_PLATE_ORIENTATION = """
[{"row_start": 1, "row_end": 4, "col_start": 2, "col_end": 4, "contents": "Chemical"}, {"row_start": 6, "row_end": 9, "col_start": 2, "col_end": 4, "contents": "Control"},{"row_start": 12, "row_end": 15, "col_start": 1, "col_end": 3, "contents": "Dox Concentration"},{"row_start": 19, "row_end": 22, "col_start": 1, "col_end": 3, "contents": "Primer"}]
"""  # noqa: E501
ASSISTANT_CONDITION_ORIENTATION = """
[{"row_start": 1, "row_end": 4, "col_start": 2, "col_end": 4, "contents": "Plate01"}, {"row_start": 6, "row_end": 9, "col_start": 2, "col_end": 4, "contents": "Plate 2"},{"row_start": 12, "row_end": 15, "col_start": 1, "col_end": 3, "contents": "plate3"},{"row_start": 19, "row_end": 22, "col_start": 1, "col_end": 3, "contents": "plate 04"}]
"""  # noqa: E501
