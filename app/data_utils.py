"""Data loading and normalization for the historical NBA team dashboard."""

from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().with_name("nba_clean.csv")

REQUIRED_COLUMNS = {
    "Team",
    "Season",
    "PTS",
    "AST",
    "TRB",
    "STL",
    "BLK",
    "TOV",
    "FG_Percent",
    "3P_Percent",
    "2P_Percent",
    "FT_Percent",
}

NUMERIC_COLUMNS = (
    "PTS",
    "AST",
    "TRB",
    "STL",
    "BLK",
    "TOV",
    "FG_Percent",
    "3P_Percent",
    "2P_Percent",
    "FT_Percent",
)

PERCENT_COLUMNS = {"FG_Percent", "3P_Percent", "2P_Percent", "FT_Percent"}

# Canonical franchise names for historical labels present in this dataset.
# `Source_Team` below keeps the original name from the source file for traceability.
FRANCHISE_ALIASES = {
    "Charlotte Bobcats": "Charlotte Hornets",
    "New Jersey Nets": "Brooklyn Nets",
    "New Orleans Hornets": "New Orleans Pelicans",
    "New Orleans/Oklahoma City Hornets": "New Orleans Pelicans",
    "Seattle SuperSonics": "Oklahoma City Thunder",
    "Vancouver Grizzlies": "Memphis Grizzlies",
}


def prepare_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate source columns and add canonical franchise/playoff fields."""
    if frame.empty:
        raise ValueError("O arquivo de dados não contém registros.")

    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(
            "Colunas obrigatórias ausentes: " + ", ".join(sorted(missing))
        )

    data = frame.copy()
    if data["Team"].isna().any():
        raise ValueError("Há registros sem identificação de equipe.")

    seasons = pd.to_numeric(data["Season"], errors="coerce")
    if seasons.isna().any() or (seasons % 1 != 0).any():
        raise ValueError("A coluna Season contém rótulos inválidos.")
    data["Season"] = seasons.astype(int)

    for column in NUMERIC_COLUMNS:
        values = pd.to_numeric(data[column], errors="coerce")
        if values.isna().any():
            raise ValueError(f"A coluna {column} contém valores não numéricos ou vazios.")
        data[column] = values

    for column in PERCENT_COLUMNS:
        if not data[column].between(0, 1).all():
            raise ValueError(
                f"A coluna {column} deve armazenar proporções entre 0 e 1."
            )

    source_names = data["Team"].astype(str).str.strip()
    data["Playoffs"] = source_names.str.endswith("*")
    data["Source_Team"] = source_names.str.removesuffix("*").str.strip()
    data["Is_League_Average"] = data["Source_Team"].eq("League Average")
    data["Franchise"] = data["Source_Team"].replace(FRANCHISE_ALIASES)

    duplicates = data.duplicated(["Franchise", "Season"], keep=False)
    if duplicates.any():
        examples = data.loc[duplicates, ["Franchise", "Season"]].drop_duplicates()
        raise ValueError(
            "Há mais de uma linha para a mesma franquia e temporada: "
            + examples.head(3).to_dict(orient="records").__repr__()
        )

    return data.sort_values(["Season", "Franchise"], kind="stable").reset_index(drop=True)


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Read the bundled CSV and return its validated, normalized form."""
    try:
        frame = pd.read_csv(path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Arquivo de dados não encontrado: {path}") from exc
    except (UnicodeDecodeError, pd.errors.ParserError) as exc:
        raise ValueError("Não foi possível ler o CSV de estatísticas da NBA.") from exc

    return prepare_data(frame)
