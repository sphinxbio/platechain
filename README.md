# platechain

[![release](https://github.com/sphinxbio/platechain/actions/workflows/release.yml/badge.svg)](https://github.com/sphinxbio/platechain/actions/workflows/release.yml)

Parsing microplate data is an extremely common task in the life sciences. This package provides a simple, universal interface for parsing all different types of microplate data into a [tidy](https://r4ds.had.co.nz/tidy-data.html) format.

**Note: this package is still early in development and may not work with all machines and data formats. If you are having trouble with a specific usecase, please [reach out](mailto:platechain@sphinxbio.com?subject=Platechain)**

<p align="center">
    <img src="images/platechain.png?raw=true" width="400" height="400" alt="Platechain">
</p>

## Motivation

One of the core problems of dealing with plate based data is that every manufacturer and machine has a different output format. Rather than build hundreds of separate parsers, we leverage the latest advancements in LLMs to build a single parser that can handle many different formats.

<p align="center">
    <img src="images/spark_raw.png?raw=true" alt="Raw Spark data" style="width: 250px; height: 300px" hspace="30" />
    <img src="images/spark_parsed.png?raw=true" alt="Parsed dataframe" style="width: 200px; height:300px" hspace="30" />
    <p align="center" style="text-align: center;">
        <strong>Platechain:</strong> From raw data output (left) to a parsed, structured format (right).
    </p>
</p>

## Getting started

```bash
pip install platechain
```

## Usage

```python
import pandas as pd
from platechain import parse_plates

# Load your data
df = pd.read_csv('examples/byonoy_absolute_example.csv')

# Parse the plates
plate_dfs = parse_plates(df)
# Output: [[96 rows x 4 columns], [96 rows x 4 columns]]
```

See the [notebooks](./notebooks) directory for more examples.

## Implementation

The core logic is implemented in [chain.py](./src/platechain/chain.py).
This file contains a single function, `parse_plates`, which takes a dataframe and returns a list of dataframes, one for each plate.

It also exposes a [LangChain](langchain.com) chain using [LCEL](https://python.langchain.com/docs/expression_language/) which can be modified to support your specific usecase.

## Limitations

- Currently only supports 24, 96, and 384 well plates. 1536 well plates are coming soon!
- Only handles plate data that is visually laid out in a grid. If your plate data is already in a table (e.g. a timeseries), this package will not parse it correctly.

## Contributing

We welcome contributions! If you'd like to contribute, please check out our [contribution guidelines](./CONTRIBUTING.md).

## License

This project is licensed under the terms of the [Apache 2.0 license](./LICENSE).

## Acknowledgements

This is a [Sphinx Bio](sphinxbio.com) project! If you're interested in a hosted solution for your lab, please [reach out](mailto:platechain@sphinxbio.com?subject=Platechain).

Thanks to [Harrison](@hwchase17) and the [Langchain](langchain.com) team for their help as well!
