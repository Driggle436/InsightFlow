def generate_recommendations(
    revenue_change,
    worst_region,
    worst_change,
    negative_reviews_count,
    anomaly_count,
):
    recommendations = []

    # Priority 1
    if worst_change < -5:
        recommendations.append({
            "priority": "P1",
            "title": f"Investigate {worst_region} region performance",
            "impact": "High",
            "effort": "Medium",
            "owner": "Regional Sales Manager",
            "evidence": [
                f"{worst_region} declined {worst_change:.1f}%",
                "Revenue trend shows deterioration."
            ]
        })

    # Priority 2
    if negative_reviews_count >= 2:
        recommendations.append({
            "priority": "P2",
            "title": "Review customer delivery issues",
            "impact": "Medium",
            "effort": "Low",
            "owner": "Customer Support",
            "evidence": [
                f"{negative_reviews_count} negative reviews detected."
            ]
        })

    # Priority 3
    if anomaly_count > 0:
        recommendations.append({
            "priority": "P3",
            "title": "Monitor unusual revenue movements",
            "impact": "Medium",
            "effort": "Low",
            "owner": "Business Analyst",
            "evidence": [
                f"{anomaly_count} revenue anomalies detected."
            ]
        })

    return recommendations