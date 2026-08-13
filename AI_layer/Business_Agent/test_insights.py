import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from insights_generator import InsightsGenerator

CURRENT_DASHBOARD = "opportunity"

generator = InsightsGenerator()

insights = generator.generate(
    CURRENT_DASHBOARD
)

print(f"\n{CURRENT_DASHBOARD.upper()} INSIGHTS\n")

for item in insights:
    print("•", item)

generator.close()