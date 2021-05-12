## LocresCSV2JSON
This script allows for the extraction of a Locres file in JSON format. It uses Python 3.8.
### Basic functionality
The script will run QuickBMS alognside the UnrealTournament4 BMS script to extract the Game.locres from the paks, it will then convert it to CSV using locres2csv and finally the resulting CSV file will be parsed to JSON.
### Instructions
1. Download [QuickBMS](http://aluigi.altervista.org/papers/quickbms.zip)
2. Download the [UnrealTournament4 script](http://aluigi.org/bms/unreal_tournament_4.bms)
3. Download [locres2csv](https://drive.google.com/open?id=1-ftM3xAukoogkU5SmNKmsXYLA4b6omgJ)
4. Run the script once, this will create a file called `locres_config.json`
5. Fill out the requested paths in `locres_config.json`
6. Run the script again
7. The converted JSON will now be in `output_path`, enjoy!
### Using in your program
Since LocresCSV2JSON is not yet a module, it is enough with copying `main.py` into a project and renaming it. The following function is enough to run the entire script:  
```
def locres_export(self):
    exporter = LocresExporter()
    exporter.export_locres()
    exporter.locres_to_csv()
    exporter.csv_to_json(exporter.config["output_path"], force_overwrite=True)
```
        
### Regarding `locres_config.json`
**quickbms_path**: path to the QuickBMS executable.

**ut4_path**: path to the UnrealTournament4 script.

**l2c_path**: path to the locres2csv executable.

**aes_path**: path to the AES key (a text file containing only the key).

**valorant_path**: path to your VALORANT installation folder.

**working_path**: path where the extraction of `Game.locres` and its parsing to CSV will take place.  
The `Game.locres` file will not be kept after the script ends.

**output_path**: path where the parsed JSON file will be placed.  
Use `{game_version}` to add the version this file was exported from.

### Credits
Luigi Auriemma for creating QuickBMS [Go](https://aluigi.altervista.org/)  
akintos for creating locres2csv [Go](https://zenhax.com/viewtopic.php?t=1022&start=40)