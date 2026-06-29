from datetime import datetime

def generate_report(open_price, close_price, date_str="N/A"):
    """
    Generates a dual format report: plain text and responsive HTML.
    Features conditional color coding (green for gain, red for loss).
    """
    change = close_price - open_price
    pct_change = (change / open_price) * 100 if open_price != 0 else 0
    
    color_green = "#10B981"
    color_red = "#EF4444"
    color_gray = "#6B7280"
    
    is_gain = change >= 0
    change_color = color_green if is_gain else color_red
    change_prefix = "+" if is_gain else ""
    status_text = "BULLISH" if is_gain else "BEARISH"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text_report = f"""
========================================
         SENSEX STOCK MARKET UPDATE
========================================
Trading Date : {date_str}
Market Trend : {status_text}
Open Price   : INR {open_price:,.2f}
Close Price  : INR {close_price:,.2f}
Net Change   : {change_prefix}{change:,.2f} ({change_prefix}{pct_change:.2f}%)
Report Time  : {timestamp}
========================================
"""

    html_report = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SENSEX Daily Report</title>
</head>
<body style="font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); border-top: 6px solid {change_color};">
        
        <!-- Header -->
        <div style="background-color: #1f2937; padding: 25px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 22px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase;">SENSEX Market Update</h1>
            <p style="color: #9ca3af; margin: 5px 0 0 0; font-size: 14px;">Trading Session: {date_str}</p>
        </div>
        
        <!-- Main Stats -->
        <div style="padding: 30px;">
            <div style="text-align: center; margin-bottom: 25px;">
                <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: {color_gray}; letter-spacing: 1px;">Market Trend</span>
                <div style="font-size: 28px; font-weight: 800; color: {change_color}; margin-top: 5px;">
                    {status_text}
                </div>
            </div>
            
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 25px;">
                <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #e5e7eb; color: #4b5563; font-weight: 500;">Open Price</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #e5e7eb; text-align: right; font-weight: 700; color: #111827;">₹{open_price:,.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #e5e7eb; color: #4b5563; font-weight: 500;">Close Price</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #e5e7eb; text-align: right; font-weight: 700; color: #111827;">₹{close_price:,.2f}</td>
                </tr>
                <tr style="background-color: {change_color}10;">
                    <td style="padding: 12px 8px; border-bottom: 1px solid #e5e7eb; color: #111827; font-weight: 600; border-radius: 6px 0 0 6px;">Net Change</td>
                    <td style="padding: 12px 8px; border-bottom: 1px solid #e5e7eb; text-align: right; font-weight: 800; color: {change_color}; border-radius: 0 6px 6px 0;">
                        {change_prefix}{change:,.2f} ({change_prefix}{pct_change:.2f}%)
                    </td>
                </tr>
            </table>

            <div style="text-align: center; font-size: 11px; color: {color_gray}; border-top: 1px dashed #e5e7eb; padding-top: 20px; margin-top: 20px;">
                Generated automatically on {timestamp} (local server time). <br>
                Financial data sourced in real-time from Yahoo Finance (^BSESN).
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f9fafb; padding: 15px 30px; text-align: center; border-top: 1px solid #f3f4f6;">
            <p style="margin: 0; font-size: 10px; color: {color_gray};">This is an automated system monitor report. Please do not reply directly to this email address.</p>
        </div>
    </div>
</body>
</html>
"""

    return {
        "text": text_report.strip(),
        "html": html_report.strip(),
        "is_gain": is_gain,
        "change_str": f"{change_prefix}{change:,.2f} ({change_prefix}{pct_change:.2f}%)"
    }