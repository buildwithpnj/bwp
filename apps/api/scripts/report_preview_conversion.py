import sys
import os

# Append project path to load app packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.preview_analytics_service import PreviewAnalyticsService

def main():
    metrics = PreviewAnalyticsService.get_metrics()
    print("=== WARBORN CONVERSION REPORT ===")
    print(f"Landing Page Visits: {metrics['landing_page_visits']}")
    print(f"Login CTA Clicks: {metrics['login_cta_clicks']}")
    print(f"Request Access Clicks: {metrics['request_access_clicks']}")
    print(f"Conversion Rate: {metrics['conversion_rate_percentage']}%")
    print("=================================")

if __name__ == "__main__":
    main()
