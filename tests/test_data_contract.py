from pathlib import Path
import pandas as pd

TARGET = "Machine failure"
REQUIRED = {
    TARGET,
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Type",
}


def load_data():
    project_root = (
        Path(__file__).resolve().parent.parent
    )  # Localiza la raíz del proyecto de forma robusta
    csv_path = project_root / "data" / "raw" / "dataset.csv"
    return pd.read_csv(csv_path)


def test_dataset_is_not_empty():
    assert not load_data().empty


def test_required_columns_exist():
    assert REQUIRED <= set(load_data().columns)


def test_target_has_no_missing_and_two_classes():
    y = load_data()[TARGET]
    assert y.notna().all()
    assert y.nunique() >= 2