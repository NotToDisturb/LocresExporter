## LocresExporter
LocresExporer is a Python 3.8 script that extracts VALORANT's localized text (in other words, the `Game.locres` file) 
into a JSON format for  general use and better readability.
## Package usage
#### Installation

`pip install git+https://github.com/NotToDisturb/LocresExporter.git#egg=LocresExporter`

The following tools are also required:
1. [QuickBMS](http://aluigi.altervista.org/papers/quickbms.zip)
1. [UnrealTournament4 (4.25 downward)](https://zenhax.com/download/file.php?id=13415) (needed for backwards compatibility)
1. [UnrealTournament4 (4.26 upward)](https://zenhax.com/download/file.php?id=12861)
1. [UnrealLocres](https://github.com/akintos/UnrealLocres)

<br>
   
#### Documentation

- [`LocresExporter`](#locresexporterpak_language-str-folder_language-str-game_path-str--none)
- [`<LocresExporter instance>.export_locres`](#locresexporter-instanceexport_locres)
- [`<LocresExporter instance>.extract_locres`](#locresexporter-instanceextract_locreslocres_pak_path-str)
- [`<LocresExporter instance>.locres_to_csv`](#locresexporter-instancelocres_to_csvcsv_path-str--none)
- [`<LocresExporter instance>.csv_to_json`](#locresexporter-instancecsv_to_json)

<br>

> ##### `LocresExporter(pak_language: str, folder_language: str, game_path: str = None)`
> 
> Creates an instace of LocresExporter, loading the config. If `game_path` is provided, 
> it should be a path to a `VALORANT-Win64-Shipping.exe`, see more in [Example paths](#example-paths).
> 
> Check the [Config file](#config-file) section and the [ConfigLoader repo](https://github.com/NotToDisturb/ConfigLoader)
> to learn more about how the config file works.

<br>

> ##### `<LocresExporter instance>.export_locres(`
> &nbsp;&nbsp;&nbsp;&nbsp;`locres_pak_path: str, json_path: str = None, force_overwrite: bool = False, `<br>
> &nbsp;&nbsp;&nbsp;&nbsp;`sort_keys: bool = False, archive: bool = False`<br>
> `) -> dict`
> 
> Executes [`extract_locres`](#locresexporter-instanceextract_locreslocres_pak_path-str), 
> [`locres_to_csv`](#locresexporter-instancelocres_to_csvcsv_path-str--none) and 
> [`csv_to_json`](#locresexporter-instancecsv_to_json) in one go. 
> Check their individual documentations for more information.

<br>

> ##### `<LocresExporter instance>.extract_locres(locres_pak_path: str)`
> 
> Extracts `Game.locres` from the pak proved in `locres_pak_path` into the working path 
> (`working_path` in the config) by running two QuickBMS (`quickbms_path` in the config) scripts:
> 1. First the UnrealTournament4 script (4.26 upward) (`ut4_path` in the config)
> 1. If no result is obtained, the UnrealTournament4 (4.25 downward) script (`ut4_old_path` in the config)
> 
> `locres_pak_path` should be a path to a `{language}_Text-WindowsClient.pak` file

<br>

> ##### `<LocresExporter instance>.locres_to_csv(csv_path: str = None)`
>
> Runs UnrealLocres (`ul_path` in the config) to parse `Game.locres` into a CSV and removes `Game.locres`. 
> 
> If `csv_path` is provided, the parsed CSV will be copied to that location. 

<br>

> ##### `<LocresExporter instance>.csv_to_json(`
> &nbsp;&nbsp;&nbsp;&nbsp;`json_path: str = None, force_overwrite: bool = False, `<br>
> &nbsp;&nbsp;&nbsp;&nbsp;`sort_keys: bool = False, archive: bool = False`<br>
> `) -> dict`
>
> Converts the CSV file resulting from [`locres_to_csv`](#locresexporter-instancelocres_to_csvcsv_path-str--none) to JSON.
> 
> - If `json_path` is provided, the JSON will be saved there. Otherwise, 
>   it will be saved in the output path (`output_path` in the config) .
> - If true, `force_overwrite` skips the overwrite dialogue when the JSON already exists.
> - If true, `sort_keys` sorts the keys within each group in natural order.
> - If true, `archive` also copies the JSON to an archival path. 
>   See more in the [Archiving](#Archiving) section.

<br><br>
#### Config file
LocresExporter uses a configuration file to know where the needed tools and other paths are:

|Path             |Validation type|Description|
|-----------------|---------------|-----------|
|**quickbms_path**|File           |Path to the QuickBMS executable.|
|**ut4_path**     |File           |Path to the UnrealTournament4 (4.25 downward) script.|
|**ut4_old_path** |File           |Path to the UnrealTournament4 (4.26 upward) script.|
|**ul_path**      |File           |Path to the UnrealLocres executable.|
|**aes_path**:    |File           |Path to the AES key, a text file containing only the key in `0x<key>` format.|
|**valorant_path**|Folder         |Path to your VALORANT installation folder. See more on [Example paths](#example-paths)|
|**working_path** |Folder         |Path where the extraction of `Game.locres` and its parsing to CSV will take place. The `Game.locres` file will not be kept after the execution ends.|
|**output_path**  |Not empty path |Path where the parsed JSON file will be placed. Check out the available [output path keywords](#output-path-keywords).|

<br>

#### Example paths

|Found in|Path               |Example|
|--------|-------------------|-------|
|Code    |`game_path`        |`C:\Riot Games\VALORANT\live\ShooterGame\Binaries\Win64\VALORANT-Win64-Shipping.exe`|
|Code    |`locres_pak_path`  |`C:\Riot Games\VALORANT\live\ShooterGame\Content\Paks\en_US_Text-WindowsClient.pak`
|Config  |`valorant_path`    |`C:\Riot Games\VALORANT\live\ `

<br>

#### Output path keywords

|Keyword            |Description|
|-------------------|-----------|
|`{pak_language}`   |Replaced by the language of the `Game.locres` in `xx_YY` format|
|`{folder_language}`|Replaced by the language of the `Game.locres` in `xx-YY` format|
|`{game_version}`   |Replaced by the game version on the provided executable|

<br>

#### Example usage
Here is an example of how to use LocresExporter:
```
from locresexporter import LocresExporter

LOCRES_PAK_PATH = "C:\\Riot Games\\VALORANT\\live\\ShooterGame\\Content\\Paks\\en_US_Text-WindowsClient.pak"

exporter = LocresExporter("en_US", "en-US")
exporter.export_locres(LOCRES_PAK_PATH)
```
The first time this script is run, it will exit after generating `locres_config.json`.
Subsequent runs will continue exiting until the [configuration file](#config-file) is filled out correctly.
Once it is, the script will execute properly and the exported JSON will be in the output path (`output_path` in the config) 

#### Archiving
LocresExporter features an archival feature that allows the user to automatically archive 
every `Game.locres` file exported. The first time a script that uses LocresExporter
is run with `archive=True`, a new config file will be generated within the installation path 
of LocresExporter (shown by the script upon generation).

That configuration can be identical to the one in your project folder, but in order to not overwrite `Game.locres`
from other versions, it is recommended that the filename of the path in `output_path` be `Game-{pak_language}-{game_version}.json`

## Standalone usage
TODO