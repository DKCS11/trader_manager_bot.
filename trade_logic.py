def suggest_trade(chart_caption):
    if "bullish" in chart_caption.lower():
        return "Consider a long position."
    elif "bearish" in chart_caption.lower():
        return "Consider a short position."
    else:
        return "No clear signal detected."