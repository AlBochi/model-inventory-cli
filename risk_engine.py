#!/usr/bin/env python3
"""
Saillent Model Risk Quantification Engine
Calculates risk scores using the Saillent Risk Framework (SRF-1).
Implements Monte Carlo simulation for model impact assessment.
"""

import math
import random
import json
from datetime import datetime
from collections import defaultdict

class SaillentRiskEngine:
    """
    Saillent Risk Framework (SRF-1)
    Quantifies model risk using three dimensions:
    - Materiality (financial impact)
    - Complexity (model architecture)
    - Exposure (regulatory sensitivity)
    """
    
    RISK_WEIGHTS = {
        "materiality": 0.40,
        "complexity": 0.35,
        "exposure": 0.25
    }
    
    REGULATORY_PENALTIES = {
        "OSFI_E23": {"max_fine": 50000000, "probability": 0.15},
        "SR11_7": {"max_fine": 75000000, "probability": 0.12},
        "CFPB": {"max_fine": 25000000, "probability": 0.08},
        "GDPR": {"max_fine": 100000000, "probability": 0.05}
    }
    
    def __init__(self, institution_aum=1_000_000_000):
        self.institution_aum = institution_aum
        self.models = []
    
    def add_model(self, name, materiality_score, complexity_score, exposure_score, 
                  annual_revenue_impact=0, customer_impact=0):
        """Add a model to the risk assessment."""
        raw_score = (
            materiality_score * self.RISK_WEIGHTS["materiality"] +
            complexity_score * self.RISK_WEIGHTS["complexity"] +
            exposure_score * self.RISK_WEIGHTS["exposure"]
        )
        
        # Apply Saillent Risk Adjustment Factor (SRAF)
        sraf = 1.0 + (customer_impact / 1_000_000) * 0.1
        adjusted_score = min(raw_score * sraf, 100)
        
        tier = self._classify_tier(adjusted_score)
        
        self.models.append({
            "name": name,
            "raw_score": round(raw_score, 2),
            "sraf": round(sraf, 3),
            "adjusted_score": round(adjusted_score, 2),
            "tier": tier,
            "materiality": materiality_score,
            "complexity": complexity_score,
            "exposure": exposure_score,
            "annual_revenue_impact": annual_revenue_impact,
            "customer_impact": customer_impact
        })
    
    def _classify_tier(self, score):
        if score >= 75: return "TIER_1_CRITICAL"
        elif score >= 50: return "TIER_2_HIGH"
        elif score >= 25: return "TIER_3_MODERATE"
        else: return "TIER_4_LOW"
    
    def monte_carlo_simulation(self, iterations=10000):
        """Run Monte Carlo simulation for regulatory penalty exposure."""
        results = []
        for _ in range(iterations):
            total_penalty = 0
            for reg, params in self.REGULATORY_PENALTIES.items():
                if random.random() < params["probability"]:
                    penalty = random.uniform(0, params["max_fine"])
                    total_penalty += penalty
            results.append(total_penalty)
        
        results.sort()
        return {
            "iterations": iterations,
            "mean_exposure": round(sum(results) / len(results), 2),
            "median_exposure": round(results[len(results)//2], 2),
            "worst_case_95th": round(results[int(len(results) * 0.95)], 2),
            "worst_case_99th": round(results[int(len(results) * 0.99)], 2),
            "probability_of_exceeding_10m": round(sum(1 for r in results if r > 10_000_000) / len(results) * 100, 2)
        }
    
    def generate_risk_matrix(self):
        """Generate a risk matrix CSV for board reporting."""
        matrix = []
        for model in self.models:
            matrix.append({
                "model": model["name"],
                "tier": model["tier"],
                "score": model["adjusted_score"],
                "materiality_pct": model["materiality"],
                "complexity_pct": model["complexity"],
                "exposure_pct": model["exposure"],
                "revenue_impact_millions": round(model["annual_revenue_impact"] / 1_000_000, 2),
                "customers_affected": model["customer_impact"]
            })
        return sorted(matrix, key=lambda x: x["score"], reverse=True)
    
    def export_report(self, filepath):
        """Generate full risk quantification report."""
        mc = self.monte_carlo_simulation()
        matrix = self.generate_risk_matrix()
        
        report = {
            "report_type": "Saillent Model Risk Quantification Report",
            "framework": "SRF-1 (Saillent Risk Framework v1.0)",
            "generated_at": datetime.now().isoformat(),
            "institution_aum": self.institution_aum,
            "institution_aum_formatted": f"${self.institution_aum:,.0f}",
            "risk_models_assessed": len(self.models),
            "model_risk_matrix": matrix,
            "monte_carlo_penalty_exposure": mc,
            "tier_summary": {},
            "regulatory_coverage": list(self.REGULATORY_PENALTIES.keys()),
            "executive_summary": ""
        }
        
        tier_counts = defaultdict(int)
        for m in self.models:
            tier_counts[m["tier"]] += 1
        report["tier_summary"] = dict(tier_counts)
        
        critical = tier_counts.get("TIER_1_CRITICAL", 0)
        if critical > 0:
            report["executive_summary"] = f"IMMEDIATE ACTION: {critical} critical-risk models identified. Estimated regulatory exposure at 95th percentile: ${mc['worst_case_95th']:,.0f}."
        else:
            report["executive_summary"] = f"Portfolio within acceptable risk parameters. {len(self.models)} models assessed. Continue monitoring cadence."
        
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        
        return report

if __name__ == "__main__":
    print("Saillent Risk Framework (SRF-1) — Model Risk Quantification Engine")
    print("=" * 70)
    
    engine = SaillentRiskEngine(institution_aum=5_000_000_000)
    
    # Add demo models with realistic financial parameters
    engine.add_model("Credit Risk Scoring v3", 85, 72, 90, annual_revenue_impact=450_000_000, customer_impact=2_500_000)
    engine.add_model("AML Transaction Monitor", 90, 88, 95, annual_revenue_impact=800_000_000, customer_impact=5_000_000)
    engine.add_model("Wealth Portfolio Optimizer", 45, 65, 30, annual_revenue_impact=120_000_000, customer_impact=150_000)
    engine.add_model("Mortgage Underwriting AI", 78, 55, 85, annual_revenue_impact=600_000_000, customer_impact=1_200_000)
    engine.add_model("Customer Churn Predictor", 25, 40, 20, annual_revenue_impact=35_000_000, customer_impact=500_000)
    engine.add_model("Fraud Detection Engine", 92, 90, 88, annual_revenue_impact=300_000_000, customer_impact=8_000_000)
    
    report = engine.export_report("risk_quantification_report.json")
    
    print(f"\n📊 Risk Assessment Complete")
    print(f"   Models assessed: {report['risk_models_assessed']}")
    print(f"   Institution AUM: {report['institution_aum_formatted']}")
    print(f"\n📋 Tier Distribution:")
    for tier, count in report["tier_summary"].items():
        print(f"   {tier}: {count} models")
    print(f"\n💰 Monte Carlo Penalty Exposure (10,000 iterations):")
    mc = report["monte_carlo_penalty_exposure"]
    print(f"   Mean: ${mc['mean_exposure']:,.0f}")
    print(f"   95th Percentile: ${mc['worst_case_95th']:,.0f}")
    print(f"   99th Percentile: ${mc['worst_case_99th']:,.0f}")
    print(f"   P(>$10M): {mc['probability_of_exceeding_10m']}%")
    print(f"\n⚠️  {report['executive_summary']}")
