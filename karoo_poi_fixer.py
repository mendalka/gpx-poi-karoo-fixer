#!/usr/bin/env python3
"""
GPX POI Fixer for Hammerhead Karoo
Author: Kmen
License: MIT License

Copyright (c) 2026 Kmen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---
Hammerhead Karoo GPX POI Format Notes:
Karoo Dashboard only imports GPX waypoints if both <type> and <sym> tags are present and match
one of the 9 supported POI types case-sensitively (Food, Water, Parking, Camping, Lodging, Geocache, Summit, Generic, Danger).
Any unrecognized types or missing <sym> tags will cause the waypoints to be stripped during import.
"""

import sys
import os
import re
import argparse

# Mapping from common GPX/VeloPlanner POI types to the 8 supported Karoo POI types
mapping = {
    # Original types
    "generic": "Generic",
    "campsite": "Camping",
    "shelter": "Lodging",
    "rest_area": "Generic",
    "summit": "Summit",
    "viewpoint": "Generic",
    "attraction": "Generic",
    "lodging": "Lodging",
    "grocery_store": "Food",
    "store": "Generic",
    "bike_shop": "Generic",
    "fuel_station": "Generic",
    "food": "Food",
    "coffee": "Food",
    "water": "Water",
    "information": "Generic",
    "toilet": "Generic",
    "first_aid": "Generic",
    "alert": "Danger",
    "parking": "Parking",
    "geocache": "Geocache",
    "danger": "Danger",
    "warning": "Danger",
    
    # Extended/extracted types from various GPX files
    "bakery": "Food",
    "café": "Food",
    "cafe": "Food",
    "cemetery (drinking water)": "Water",
    "convenience store": "Food",
    "drinking water": "Water",
    "drinking_water": "Water",
    "fast food": "Food",
    "fountain": "Water",
    "gas station": "Generic",
    "ice cream parlor": "Food",
    "kiosk": "Generic",
    "other": "Generic",
    "restaurant": "Food",
    "spring": "Water",
    "supermarket": "Food",
    "toilets": "Generic",
    "vending machine": "Food",
    "water intake point": "Water",
    "water point": "Water",
    "woda": "Water",

    # Additional types (Komoot, RideWithGPS, etc.)
    "aid station": "Food",
    "art": "Generic",
    "beach": "Generic",
    "bike shop": "Generic",
    "bridge": "Generic",
    "checkpoint": "Generic",
    "crossing": "Generic",
    "first aid": "Generic",
    "gear": "Generic",
    "info": "Generic",
    "meeting point": "Generic",
    "obstacle": "Danger",
    "park": "Generic",
    "pub": "Food",
    "rest area": "Generic",
    "segment end": "Generic",
    "segment start": "Generic",
    "service": "Generic",
    "sharp curve": "Danger",
    "shower": "Water",
    "steep incline": "Danger",
    "transition": "Generic",
    "transport": "Generic",
    "tunnel": "Generic",
    "valley": "Generic"
}

def process_gpx(gpx_content):
    def replace_wpt(match):
        wpt_block = match.group(0)
        # Match type tag and its indentation
        type_match = re.search(r"(\s*)<type>(.*?)</type>", wpt_block)
        if type_match:
            indent = type_match.group(1)
            original_type = type_match.group(2)
            normalized_type = original_type.strip().lower()
            mapped_type = mapping.get(normalized_type, "Generic")
            
            # If type changed, preserve original type in <name> and <desc>
            if original_type.strip().lower() != mapped_type.lower():
                suffix = f" ({original_type.strip()})"
                wpt_block = re.sub(r"(<name>)(.*?)(</name>)", lambda m: f"{m.group(1)}{m.group(2)}{suffix}{m.group(3)}", wpt_block)
                wpt_block = re.sub(r"(<desc>)(.*?)(</desc>)", lambda m: f"{m.group(1)}{m.group(2)}{suffix}{m.group(3)}", wpt_block)
            
            # Replace type tag
            wpt_block = re.sub(r"<type>.*?</type>", f"<type>{mapped_type}</type>", wpt_block)
            
            # Add or replace sym tag
            if "<sym>" in wpt_block:
                wpt_block = re.sub(r"<sym>.*?</sym>", f"<sym>{mapped_type}</sym>", wpt_block)
            else:
                # Insert sym tag with the same indentation right after type tag
                wpt_block = re.sub(f"<type>{mapped_type}</type>", f"<type>{mapped_type}</type>{indent}<sym>{mapped_type}</sym>", wpt_block)
        return wpt_block

    # Find and process all <wpt ...> ... </wpt> blocks
    return re.sub(r"<wpt\s+.*?>.*?</wpt>", replace_wpt, gpx_content, flags=re.DOTALL)

def main():
    parser = argparse.ArgumentParser(
        description="Convert GPX waypoints into Hammerhead Karoo compatible POIs by mapping custom types and ensuring correct <type> and <sym> tags."
    )
    parser.add_argument(
        "infile",
        nargs="?",
        type=str,
        default="-",
        help="Input GPX file. Use '-' or omit to read from standard input."
    )
    parser.add_argument(
        "outfile",
        nargs="?",
        type=str,
        default=None,
        help="Output GPX file path. If input is a file and outfile is omitted, writes to 'KAROO_<infile>'. If input is stdin, writes to stdout."
    )

    args = parser.parse_args()

    # Read content
    if args.infile == "-":
        content = sys.stdin.read()
    else:
        if not os.path.exists(args.infile):
            print(f"Error: File '{args.infile}' not found.", file=sys.stderr)
            sys.exit(1)
        with open(args.infile, "r", encoding="utf-8") as f:
            content = f.read()

    # Process content
    output_content = process_gpx(content)

    # Write output
    if args.infile == "-":
        if args.outfile:
            with open(args.outfile, "w", encoding="utf-8") as f:
                f.write(output_content)
        else:
            sys.stdout.write(output_content)
    else:
        # File input
        if args.outfile:
            out_path = args.outfile
        else:
            dir_name = os.path.dirname(args.infile)
            base_name = os.path.basename(args.infile)
            out_path = os.path.join(dir_name, f"KAROO_{base_name}")
            
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"Successfully converted '{args.infile}' to '{out_path}'.", file=sys.stderr)

if __name__ == "__main__":
    main()
