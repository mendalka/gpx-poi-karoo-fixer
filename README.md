# GPX POI Fixer for Hammerhead Karoo

A simple Python script to fix GPX files so that their custom POIs (waypoints) are successfully imported into the Hammerhead Karoo Dashboard.

## Web GUI / Android & iOS App

If you prefer a graphical user interface instead of a command-line script, a web application is available. It processes GPX files entirely in your web browser (locally and privately) and can be installed on Android and iOS/iPhone home screens for offline usage.

* **Live Web App:** [https://mendalka.github.io/gpx-poi-karoo-app/](https://mendalka.github.io/gpx-poi-karoo-app/)
* **App Repository:** [github.com/mendalka/gpx-poi-karoo-app](https://github.com/mendalka/gpx-poi-karoo-app)

## Why is this needed?

Let's face it: it's June 2026, and for **six long years**, Hammerhead has been unable to import arbitrary POIs from GPX files without silently ignoring them. While they have recently made some minor progress with standardizing POIs, the Karoo Dashboard is still extremely picky. 

To import a waypoint as a POI, the Karoo Dashboard requires **both** the `<type>` and `<sym>` tags to be present in each `<wpt>` block and match one of their **9 supported case-sensitive POI types** exactly:
* `Food`
* `Water`
* `Parking`
* `Camping`
* `Lodging`
* `Geocache`
* `Summit`
* `Generic`
* `Danger`

If a waypoint does not match one of these types, or if the `<sym>` tag is missing, it is simply discarded during the import process.

This script parses your GPX file, maps common or custom POI types (including exports from fantastic planners like [VeloPlanner](https://veloplanner.com/)), and outputs a compatible GPX file with matching `<type>` and `<sym>` tags.

## Supported Mappings

The script maps various common waypoint types to the 9 supported Karoo POIs:
* **Food**: `Food`, `Coffee`, `Grocery Store`, `Supermarket`, `Convenience Store`, `Bakery`, `Café`, `Restaurant`, `Fast Food`, `Ice Cream Parlor`, `Vending Machine`
* **Water**: `Water`, `Woda`, `Drinking Water`, `Water Point`, `Water Intake Point`, `Fountain`, `Spring`, `Cemetery (Drinking Water)`
* **Camping**: `Campsite`
* **Lodging**: `Shelter`, `Lodging`
* **Summit**: `Summit`
* **Parking**: `Parking`
* **Geocache**: `Geocache`
* **Danger**: `Alert`, `Danger`, `Warning`
* **Generic**: `Generic`, `Rest Area`, `Viewpoint`, `Attraction`, `Store`, `Bike Shop`, `Fuel Station`, `Gas Station`, `Information`, `Toilet`, `Toilets`, `First Aid`, `Kiosk`, `Other`

Any unmapped types will fall back to `Generic`.

## Usage

You can run the script directly:

```bash
# Convert a GPX file (writes output to KAROO_input.gpx by default)
./karoo_poi_fixer.py input.gpx

# Specify a custom output path
./karoo_poi_fixer.py input.gpx output.gpx

# Use stdin/stdout
cat input.gpx | ./karoo_poi_fixer.py > output.gpx
```

### Options

```
usage: karoo_poi_fixer.py [-h] [infile] [outfile]

Convert GPX waypoints into Hammerhead Karoo compatible POIs by mapping custom
types and ensuring correct <type> and <sym> tags.

positional arguments:
  infile      Input GPX file. Use '-' or omit to read from standard input.
  outfile     Output GPX file path. If input is a file and outfile is omitted,
              writes to 'KAROO_<infile>'. If input is stdin, writes to stdout.

options:
  -h, --help  show this help message and exit
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
