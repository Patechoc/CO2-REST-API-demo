from enum import Enum
from pathlib import Path
from typing import Dict, List

import pandas as pd
from joblib import Memory


class MeaningfulHeaders(Enum):
    per_capita = "CO2_emissions_in_tonnes_per_capita"
    co2_emissions = "CO2_emissions_in_tonnes"
    yearly_change = "yearly_change_in_percent"
    life_expectancy = "life_expectancy"


memory = Memory(location="cache", verbose=0)


@memory.cache
def read_csv() -> pd.DataFrame:
    root_folder = Path(__file__).parent.parent.parent
    file_path = root_folder / "data" / "CO2-emissions.csv"
    return pd.read_csv(file_path)


def get_list_country_names() -> List[str]:
    df = read_csv()
    return df.Country.to_list()


def get_country_codes() -> Dict[str, str]:
    df = read_csv()
    return df.set_index("Country")["Code"].to_dict()


def get_countries_ordered_by_life_expectancy(
    limit: int = 10, descending: bool = True
) -> List[dict]:
    df = read_csv()
    df_sorted = df.sort_values("LifeExpectancy", ascending=not (descending)).head(limit)
    df_sorted.rename(columns={"LifeExpectancy": MeaningfulHeaders.life_expectancy}, inplace=True)
    return df_sorted[["Country", MeaningfulHeaders.life_expectancy]].head(limit).to_dict("records")


def get_countries_ordered_by_co2_emission_per_person(
    limit: int = 10, descending: bool = True
) -> List[dict]:
    df = read_csv()
    df_sorted = df.sort_values("Percapita", ascending=not (descending))
    df_sorted.rename(columns={"Percapita": MeaningfulHeaders.per_capita}, inplace=True)
    return (
        df_sorted[["Country", MeaningfulHeaders.per_capita]].head(limit).to_dict(orient="records")
    )


def get_countries_co2_emissions_and_change(
    country_codes: str, descending: bool = True
) -> List[dict]:
    df = read_csv()
    codes = [c.upper() for c in country_codes.split(",")]
    unique_legit_codes = sorted(list(set([c.upper() for c in get_country_codes().values()])))
    codes_not_legit = [c for c in codes if c not in unique_legit_codes]
    if codes_not_legit:
        raise AttributeError(
            f"The codes {','.join(codes_not_legit)} are not valid country codes in this dataset."
        )
    df_filtered = df[df["Code"].isin(codes)][["Country", "Code", "CO2Emissions", "YearlyChange"]]
    df_sorted = df_filtered.sort_values(
        ["CO2Emissions", "YearlyChange"], ascending=not (descending)
    )
    df_sorted.rename(
        columns={
            "CO2Emissions": MeaningfulHeaders.co2_emissions,
            "YearlyChange": MeaningfulHeaders.yearly_change,
        },
        inplace=True,
    )
    return df_sorted.to_dict(orient="records")


def sum_countries_co2_emissions(country_codes: str) -> dict:
    df = read_csv()
    codes = [c.upper() for c in country_codes.split(",")]
    countries = df[df["Code"].isin(codes)]["Country"].to_list()
    total_co2_emissions = float(df[df["Code"].isin(codes)]["CO2Emissions"].sum())
    return {"countries": countries, "total_co2_emissions_in_tonnes": total_co2_emissions}
