"""
Price-Guard Module
Detects over-invoicing by comparing extracted prices with market rates
"""

import pytesseract
from PIL import Image
from io import BytesIO
import re

# Market price database (hardcoded for demo)
MARKET_PRICES = {
    'laptop': 80000,
    'gaming laptop': 80000,
    'high-end gaming laptop': 80000,
    'computer': 50000,
    'desktop': 40000,
    'printer': 15000,
    'scanner': 10000
}


def extract_price_from_image(image_bytes):
    """Extract text and price from invoice image using OCR"""
    image = Image.open(BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text


def parse_invoice_items(ocr_text):
    """Parse OCR text to extract items and prices"""
    items = []
    
    # Look for price patterns (Rs. 1,50,000 or Rs. 150000)
    price_pattern = r'Rs\.?\s*(\d{1,3}(?:,\d{3})*|\d+)'
    
    lines = ocr_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        
        # Check if line contains item description
        for item_name in MARKET_PRICES.keys():
            if item_name in line_lower:
                # Find price in this line or nearby
                matches = re.findall(price_pattern, line)
                if matches:
                    # Remove commas and convert to int
                    price_str = matches[0].replace(',', '')
                    extracted_price = int(price_str)
                    
                    items.append({
                        'item': item_name.title(),
                        'extracted_price': extracted_price,
                        'line': line.strip()
                    })
    
    return items


def analyze_invoice(image_bytes):
    """
    Analyze invoice image for over-invoicing
    Returns flagged items where price is 50% higher than market rate
    """
    # Extract text using OCR
    ocr_text = extract_price_from_image(image_bytes)
    
    # Parse items and prices
    items = parse_invoice_items(ocr_text)
    
    # Check for over-invoicing
    flagged_items = []
    for item in items:
        item_key = item['item'].lower()
        if item_key in MARKET_PRICES:
            market_price = MARKET_PRICES[item_key]
            extracted_price = item['extracted_price']
            
            # Check if price is 50% or more above market rate
            if extracted_price >= market_price * 1.5:
                inflation_percent = ((extracted_price - market_price) / market_price) * 100
                flagged_items.append({
                    'item': item['item'],
                    'extracted_price': extracted_price,
                    'market_price': market_price,
                    'inflation_percent': round(inflation_percent, 2),
                    'status': 'OVER-INVOICING DETECTED'
                })
    
    return {
        'ocr_text': ocr_text,
        'total_items_found': len(items),
        'flagged_items': flagged_items,
        'status': 'WARNING' if flagged_items else 'CLEAR'
    }

