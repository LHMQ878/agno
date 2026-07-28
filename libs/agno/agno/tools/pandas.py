import json
from typing import Callable, Dict, List

from agno.tools import Toolkit
from agno.utils.log import log_debug, logger

try:
    import pandas as pd
except ImportError:
    raise ImportError("`pandas` not installed. Please install using `pip install pandas`.")


class PandasTools(Toolkit):
    # Allowlist of safe pandas functions for creating dataframes
    SAFE_CREATE_FUNCTIONS = frozenset(
        {
            "read_csv",
            "read_json",
            "read_excel",
            "read_parquet",
            "read_feather",
            "read_orc",
            "read_sql",
            "read_sql_query",
            "read_sql_table",
            "read_html",
            "read_xml",
            "read_clipboard",
            "read_fwf",
            "read_table",
            "DataFrame",
            "json_normalize",
        }
    )

    # Allowlist of safe dataframe operations
    SAFE_OPERATIONS = frozenset(
        {
            "head",
            "tail",
            "info",
            "describe",
            "shape",
            "columns",
            "dtypes",
            "index",
            "values",
            "to_string",
            "to_dict",
            "to_json",
            "to_csv",
            "to_markdown",
            "to_html",
            "count",
            "sum",
            "mean",
            "median",
            "std",
            "var",
            "min",
            "max",
            "abs",
            "round",
            "sort_values",
            "sort_index",
            "groupby",
            "pivot",
            "pivot_table",
            "melt",
            "merge",
            "join",
            "concat",
            "drop",
            "drop_duplicates",
            "dropna",
            "fillna",
            "replace",
            "rename",
            "reset_index",
            "set_index",
            "transpose",
            "T",
            "loc",
            "iloc",
            "at",
            "iat",
            "query",
            "filter",
            "select_dtypes",
            "sample",
            "nlargest",
            "nsmallest",
            "unique",
            "nunique",
            "value_counts",
            "isnull",
            "isna",
            "notna",
            "notnull",
            "any",
            "all",
            "corr",
            "cov",
            "cumsum",
            "cumprod",
            "cummax",
            "cummin",
            "diff",
            "pct_change",
            "rank",
            "clip",
            "between",
            "isin",
            "copy",
            "astype",
        }
    )

    def __init__(
        self,
        create_pandas_dataframe: bool = False,
        run_dataframe_operation: bool = False,
        all: bool = False,
        **kwargs,
    ):
        """Initialize Pandas toolkit for dataframe operations.

        Args:
            create_pandas_dataframe: Enable the create_pandas_dataframe tool. Disabled by default (can load arbitrary files).
            run_dataframe_operation: Enable the run_dataframe_operation tool. Disabled by default (runs operations).
            all: Enable all tools.
        """
        self.dataframes: Dict[str, pd.DataFrame] = {}

        tools: List[Callable] = []
        if all or create_pandas_dataframe:
            tools.append(self.create_pandas_dataframe)
        if all or run_dataframe_operation:
            tools.append(self.run_dataframe_operation)

        super().__init__(name="pandas_tools", tools=tools, **kwargs)

    def create_pandas_dataframe(
        self, dataframe_name: str, create_using_function: str, function_parameters: Dict[str, object]
    ) -> str:
        """Create a pandas dataframe using a pandas function.

        Args:
            dataframe_name: Name to assign to the created dataframe.
            create_using_function: Pandas function to use (e.g., read_csv, read_json).
            function_parameters: Parameters to pass to the function.

        Returns:
            JSON with dataframe_name on success or error message.

        Example:
            create_pandas_dataframe("csv_data", "read_csv", {"filepath_or_buffer": "data.csv"})
        """
        try:
            log_debug(f"Creating dataframe: {dataframe_name}")
            log_debug(f"Using function: {create_using_function}")
            log_debug(f"With parameters: {function_parameters}")

            if dataframe_name in self.dataframes:
                return json.dumps({"error": f"Dataframe already exists: {dataframe_name}"})

            if create_using_function not in self.SAFE_CREATE_FUNCTIONS:
                return json.dumps({"error": f"Function '{create_using_function}' not allowed. Use: {', '.join(sorted(self.SAFE_CREATE_FUNCTIONS))}"})

            dataframe = getattr(pd, create_using_function)(**function_parameters)
            if dataframe is None:
                return json.dumps({"error": f"Error creating dataframe: {dataframe_name}"})
            if not isinstance(dataframe, pd.DataFrame):
                return json.dumps({"error": f"Error creating dataframe: {dataframe_name}"})
            if dataframe.empty:
                return json.dumps({"error": f"Dataframe is empty: {dataframe_name}"})
            self.dataframes[dataframe_name] = dataframe
            log_debug(f"Created dataframe: {dataframe_name}")
            return json.dumps({"dataframe_name": dataframe_name, "shape": list(dataframe.shape)})
        except Exception as e:
            logger.exception("Error creating dataframe")
            return json.dumps({"error": f"Error creating dataframe: {e}"})

    def run_dataframe_operation(self, dataframe_name: str, operation: str, operation_parameters: Dict[str, object]) -> str:
        """Run an operation on a dataframe.

        Args:
            dataframe_name: Name of the dataframe to operate on.
            operation: Operation to run (e.g., head, tail, describe).
            operation_parameters: Parameters to pass to the operation.

        Returns:
            JSON with result or error message.

        Example:
            run_dataframe_operation("csv_data", "head", {"n": 5})
        """
        try:
            log_debug(f"Running operation: {operation}")
            log_debug(f"On dataframe: {dataframe_name}")
            log_debug(f"With parameters: {operation_parameters}")

            if operation not in self.SAFE_OPERATIONS:
                return json.dumps({"error": f"Operation '{operation}' not allowed. Use: {', '.join(sorted(self.SAFE_OPERATIONS))}"})

            dataframe = self.dataframes.get(dataframe_name)
            if dataframe is None:
                return json.dumps({"error": f"Dataframe '{dataframe_name}' not found"})

            result = getattr(dataframe, operation)(**operation_parameters)
            log_debug(f"Ran operation: {operation}")

            try:
                if hasattr(result, "to_string"):
                    return json.dumps({"result": result.to_string()})
                return json.dumps({"result": str(result)})
            except Exception:
                return json.dumps({"status": "success"})
        except Exception as e:
            logger.exception("Error running operation")
            return json.dumps({"error": f"Error running operation: {e}"})
