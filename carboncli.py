import argparse
from carbon.calculator import CarbonCalculator
from carbon.services import LighthouseService, GreenWebService


def main():
    """ """
    parser = argparse.ArgumentParser(
        description="Carbon Calculator - the tool calculates the carbon emissions (CO2) and green infos of any website"
    )

    parser.add_argument(
        "-db",
        "--greenweb",
        type=str,
        help="(Mandatory) - The path of the Green Web Foundation DB (SQL3Lite DB file)",
        required=True,
    )
    parser.add_argument(
        "-lh",
        "--lighthouse",
        type=str,
        help="(Optional) - The path of the Lighthouse tool",
        required=False,
    )
    parser.add_argument("website", type=str, help="The URL to analyze")

    args = parser.parse_args()

    try:
        lighthouse = (
            LighthouseService()
            if not args.lighthouse
            else LighthouseService(args.lighthouse)
        )
        greenweb = GreenWebService(args.greenweb)
        website = args.website

        carbon = CarbonCalculator(lighthouse=lighthouse, greenweb=greenweb)
        carbon.footprint(website)

        print(carbon.to_json())
    except Exception as e:
        print(e)
