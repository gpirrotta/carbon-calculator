import json
from .services import LighthouseService, GreenWebService
from .exceptions import CarbonCalculatorException
from datetime import date, datetime, timezone


class PageStatistics(object):
    """Statistics component"""

    KWH_PER_GB = 1.805
    FIRST_TIME_VIEWING_PERCENTAGE = 0.75
    RETURNING_VISITOR_PERCENTAGE = 0.25
    PERCENTAGE_OF_DATA_LOADED_ON_SUBSEQUENT_LOAD = 0.02
    CARBON_PER_KWH_GRID = 475
    CARBON_PER_KWH_RENEWABLE = 33.4
    PERCENTAGE_OF_ENERGY_IN_DATACENTER = 0.1008
    PERCENTAGE_OF_ENERGY_IN_TRANSMISSION_AND_END_USER = 0.8992
    CO2_GRAMS_TO_LITRES = 0.5562

    def __init__(self, url: str, resources: dict, green: bool) -> None:
        self._adjusted_bytes = 0
        self._energy = 0
        self._co2 = 0
        self._co2_grid_grams = 0
        self._co2_grid_litres = 0
        self._co2_renewable_grams = 0
        self._co2_renewable_litres = 0
        self._green = green
        self._resources = resources
        self._transfered_bytes = 0
        self._resources_bytes = 0
        self._url = url
        self._litres = 0
        self._created_at = None

        self._calculate_stats()

    def _calculate_stats(self) -> None:
        """
        It build the statistics (co2, energy, litres)

        Parameters
        ----------
        bytes: int
            The transfered bytes of the website

        """
        self._transfered_bytes = self._resources["transfer_size_bytes"]["total"]
        self._adjusted_bytes = self._adjust_data_transfer(self._transfered_bytes)

        self._resources["transfer_size_bytes"]["total_weighted"] = self._adjusted_bytes
        self._resources_bytes = self._resources["resources_size_bytes"]["total"]

        self._energy = self._energy_consumption(self._adjusted_bytes)

        self._co2_grid_grams = self._get_co2_grid(self._energy)
        self._co2_grid_litres = self._co2_to_litres(self._co2_grid_grams)

        self._co2_renewable_grams = self._get_co2_renewable(self._energy)
        self._co2_renewable_litres = self._co2_to_litres(self._co2_renewable_grams)

        self._co2 = self._co2_renewable_grams if self._green else self._co2_grid_grams
        self._litres = (
            self._co2_renewable_litres if self._green else self._co2_grid_litres
        )

        self._created_at = datetime.now(timezone.utc).astimezone().isoformat()

    def _adjust_data_transfer(self, val: int) -> int:
        return int(
            (val * self.FIRST_TIME_VIEWING_PERCENTAGE)
            + (
                self.PERCENTAGE_OF_DATA_LOADED_ON_SUBSEQUENT_LOAD
                * val
                * self.RETURNING_VISITOR_PERCENTAGE
            )
        )

    def _energy_consumption(self, bytes: int) -> float:
        return bytes * (self.KWH_PER_GB / 1073741824)

    def _get_co2_grid(self, energy: float) -> float:
        return energy * self.CARBON_PER_KWH_GRID

    def _get_co2_renewable(self, energy: float) -> float:
        return (
            (energy * self.PERCENTAGE_OF_ENERGY_IN_DATACENTER)
            * self.CARBON_PER_KWH_RENEWABLE
        ) + (
            (energy * self.PERCENTAGE_OF_ENERGY_IN_TRANSMISSION_AND_END_USER)
            * self.CARBON_PER_KWH_GRID
        )

    def _co2_to_litres(self, co2: float) -> float:
        return co2 * self.CO2_GRAMS_TO_LITRES

    @property
    def created_at(self) -> int:
        return self._created_at

    @property
    def url(self) -> str:
        return self._url

    @property
    def hosting_green(self) -> bool:
        return self._green

    @property
    def co2_grams(self) -> float:
        return self._co2

    @property
    def energy_kWh(self) -> float:
        return self._energy

    @property
    def water_litres(self) -> float:
        return self._litres

    @property
    def resources(self) -> int:
        return self._resources

    @property
    def transfer_size_bytes(self) -> int:
        return self._transfered_bytes

    @property
    def resources_size_bytes(self) -> int:
        return self._resources_bytes


class StatisticsBuilder(object):
    def __init__(
        self, greenweb: GreenWebService, lighthouse: LighthouseService
    ) -> None:
        self._greenweb = greenweb
        self._lighthouse = lighthouse

    def build(self, url: str) -> PageStatistics:
        statistics = None
        try:
            green = self._greenweb.check(url)
            self._lighthouse.analyze(url)
            resources = self._lighthouse.resources
            statistics = PageStatistics(url, resources, green)

            return statistics

        except Exception as e:
            raise CarbonCalculatorException(e)
