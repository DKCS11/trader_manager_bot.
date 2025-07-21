import logging

logger = logging.getLogger(__name__)

def suggest_trade(chart_analysis):
    """Generate trading suggestion with better logic"""
    if not chart_analysis or "⚠️" in chart_analysis:
        return "No clear signal detected (analysis failed)"
    
    analysis_lower = chart_analysis.lower()
    
    bullish_terms = ["bull", "upward", "rising", "buy", "long"]
    bearish_terms = ["bear", "downward", "falling", "sell", "short"]
    
    bull_score = sum(term in analysis_lower for term in bullish_terms)
    bear_score = sum(term in analysis_lower for term in bearish_terms)
    
    if bull_score > bear_score and bull_score >= 2:
        return "Strong bullish signal - Consider LONG position"
    elif bear_score > bull_score and bear_score >= 2:
        return "Strong bearish signal - Consider SHORT position"
    elif bull_score == bear_score and bull_score > 0:
        return "Mixed signals - Wait for clearer trend"
    else:
        return "No clear trend detected - Maintain current position"
