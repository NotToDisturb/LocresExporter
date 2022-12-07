## LocresExporter
LocresExporer is a Python 3.8 script that extracts VALORANT's localized text (in other words, the`Game.locres` file) into a JSON format for  general use and better readability.
### Installation
To install this package, execute the following command and download the required [dependencies](#dependencies):

`pip install git+https://github.com/NotToDisturb/LocresExporter.git#egg=LocresExporter`
### Dependencies
The dependencies required for LocresExporter to work are:
1. [QuickBMS](http://aluigi.altervista.org/papers/quickbms.zip)
2. [UnrealTournament4 (4.26+)](https://zenhax.com/download/file.php?id=12861)
3. [UnrealLocres](https://github.com/akintos/UnrealLocres)
## How to use
Here is an example of how to use LocresExporter:
```
from locresexporter.exporter import LocresExporter

def locres_export(self):
    exporter = LocresExporter()
    exporter.export_locres()
    exporter.locres_to_csv()
    exporter.csv_to_json(exporter.config["output_path"])
```
### First time execution
1. Run the script. This will create a file called `locres_config.json`.
2. Fill out the paths in `locres_config.json`. [See more](#filling-out-locres_configjson).
3. Run the script again.
4. The converted JSON will now be in `output_path`, enjoy!
### Filling out `locres_config.json`
|Path             |Description|
|-----------------|-----------|
|**quickbms_path**|Path to the QuickBMS executable.|
|**ut4_path**     |Path to the UnrealTournament4 script.|
|**ul_path**      |Path to the UnrealLocres executable.|
|**aes_path**:    |Path to the AES key (a text file containing only the key).|
|**valorant_path**|Path to your VALORANT installation folder.|
|**working_path** |Path where the extraction of `Game.locres` and its parsing to CSV will take place. The `Game.locres` file will not be kept after the execution ends.|
|**output_path**  |Path where the parsed JSON file will be placed.Use `{game_version}` to add the version of VALORANT this file was exported from.|
### Optional arguments
There are two additional arguments:
- `force_overwrite`: **False** by default. Toggles whether the script will overwrite a previously exported JSON.
- `sort_keys`: **False** by default. Enables sorting the keys when exporting the JSON.
## Credits
Luigi Auriemma for creating QuickBMS [Go](https://aluigi.altervista.org/)  
akintos for creating UnrealLocres [Go](https://zenhax.com/viewtopic.php?t=1022&start=40)