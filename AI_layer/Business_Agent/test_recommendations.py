import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from recommendation_engine import RecommendationEngine

# =====================================
# CHANGE DASHBOARD NAME HERE
# =====================================

DASHBOARD = "opportunity"

# executive
# customer
# product
# revenue
# geographic
# sales
# ml
# opportunity

# =====================================

engine = RecommendationEngine()

recommendations = engine.generate(DASHBOARD)

print(f"\n{DASHBOARD.upper()} RECOMMENDATIONS\n")

for rec in recommendations:

    print(f"Priority : {rec['priority']}")
    print(f"Title    : {rec['title']}")
    print(f"Action   : {rec['recommendation']}")
    print(f"Impact   : {rec['expected_impact']}")
    print("-" * 60)

engine.close()