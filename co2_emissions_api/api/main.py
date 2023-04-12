from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from co2_emissions_api.api import backend

description = """
The CO2 emissions REST API.

This API can return the following information:

1. The countries ranked by their CO2 emissions per capita (ex.: the top 10 countries with highest CO2 emissions per capita)
2. The CO2 emissions and yearly change of countries given a list of country codes (ex: can,lux,est)
3. The countries ranked by their averaged life expectancy (ex.: The top 10 Countries with highest life expectancy)
4. the cumulated CO2 emissions given a list of countries codes (ex: can,lux,est)

"""

app = FastAPI(
    title="CO2 Emissions by countries",
    description=description,
    version="0.0.1",
    terms_of_service="https://creativecommons.org/licenses/by-nd/4.0/",
    contact={
        "name": "Patrick Merlot",
        "url": "https://github.com/Patechoc",
        "email": "patrick.merlot@gmail.com",
    },
    license_info={
        "name": "GNU General Public License",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)


@app.get("/")
async def read_root():
    return RedirectResponse("/docs")


@app.get(
    "/country_names",
    response_model=List[str],
    description="List of countries present in this dataset.",
)
async def get_country_names():
    return backend.get_list_country_names()


@app.get(
    "/country_codes",
    response_model=Dict[str, str],
    description="Mapping of country names to country codes.",
)
async def get_country_codes():
    return backend.get_country_codes()


@app.get(
    "/countries_ranked_co2_emissions_per_capita",
    response_model=List[dict],
    description="Countries ranked by their CO2 emissions per capita (limit set to 10 by default).",
)
async def rank_countries_ordered_by_co2_emissions_per_capita(
    limit: int = None, descending: bool = True
):
    return backend.get_countries_ordered_by_co2_emission_per_person(
        limit=limit, descending=descending
    )


@app.get(
    "/countries_ranked_by_life_expectancy",
    response_model=List[dict],
    description="Countries ranked by life expectancy (limit set to 10 by default).",
)
async def rank_countries_by_life_expectancy(limit: int = None, descending: bool = True):
    return backend.get_countries_ordered_by_life_expectancy(limit=limit, descending=descending)


@app.get(
    "/countries_co2_emissions",
    response_model=List[dict],
    description="CO2 emissions and yearly change for countries identified by their codes.",
)
async def co2_emissions_and_change(country_codes: str = "CAN,LUX,EST", descending: bool = True):
    return backend.get_countries_co2_emissions_and_change(
        country_codes=country_codes, descending=descending
    )


# Define endpoint for total of Emissions given a list of country codes
@app.get(
    "/total_co2_emissions",
    response_model=dict,
    description="Cumulated CO2 emissions for countries identified by a list of country codes",
)
async def total_co2_emissions(country_codes: str = "CAN,LUX,EST"):
    return backend.sum_countries_co2_emissions(country_codes=country_codes)
