import os
import re
import csv
import json
import shutil
import subprocess

from configloader import ConfigLoader
from versionutils import get_game_version

# Paths and filenames constants
PACKAGE_ROOT = os.path.join(__file__, "..")
LOCRES_CONFIG = "locres_config.json"
validators = {
    "quickbms_path": ConfigLoader.validate_file,
    "ut4_path": ConfigLoader.validate_file,
    "ut4_old_path": ConfigLoader.validate_file,
    "ul_path": ConfigLoader.validate_file,
    "aes_path": ConfigLoader.validate_file,
    "valorant_path": ConfigLoader.validate_folder,
    "working_path": ConfigLoader.validate_not_empty,
    "output_path": ConfigLoader.validate_nothing
}

RELATIVE_LOCRES_PAK = "\\ShooterGame\\Content\\Paks\\{pak_language}_Text-WindowsClient.pak"
RELATIVE_GAME_EXE = "\\ShooterGame\\Binaries\\Win64\\VALORANT-Win64-Shipping.exe"
RELATIVE_LOCRES = "\\ShooterGame\\Content\\Localization\\Game\\{folder_language}\\Game.locres"
RELATIVE_CSV = "\\ShooterGame\\Content\\Localization\\Game\\{folder_language}\\Game.csv"

DEFAULT_LANGUAGE = "en-US"


class LocresExporter:
    # Wrapper class for the exporting configuration
    def __init__(self, pak_language: str, folder_language: str, game_path: str = None, encoding="utf-8"):
        self.config = ConfigLoader(LOCRES_CONFIG, validators)
        self.pak_language = pak_language
        self.folder_language = folder_language
        self.valorant_exe = game_path if game_path else self.config["valorant_path"] + RELATIVE_GAME_EXE
        self.encoding = encoding

    def __get_aes_key(self) -> bytes:
        # Read the AES key from the provided raw text file
        with open(self.config["aes_path"], "rt") as aes_file:
            return str.encode(aes_file.read())

    def __apply_language_to_path(self, path: str) -> str:
        return path.replace("{pak_language}", self.pak_language) \
            .replace("{folder_language}", self.folder_language)

    def __apply_game_version_to_path(self, path: str) -> str:
        # Replace {game_version} keyword with current version
        client_version = get_game_version(self.valorant_exe)
        return path.replace("{game_version}", client_version["branch"] + "-" + client_version["version"])

    def export_locres(self, locres_pak_path: str, json_path: str = None, force_overwrite: bool = False,
                      sort_keys: bool = False, archive: bool = False) -> dict:
        self.extract_locres(locres_pak_path)
        self.locres_to_csv()
        return self.csv_to_json(json_path, force_overwrite, sort_keys, archive)

    def extract_locres(self, locres_pak_path: str):
        locres_pak_path = self.__apply_language_to_path(locres_pak_path)
        # Execute QuickBMS command, redirecting input to the pipe
        exporter_process = subprocess.Popen([self.config["quickbms_path"], self.config["ut4_path"],
                                             locres_pak_path, self.config["working_path"]],
                                            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        # Pass the AES key to the pipe
        exporter_process.communicate(self.__get_aes_key())
        exporter_process.wait()
        locres_path = self.__apply_language_to_path(self.config["working_path"] + RELATIVE_LOCRES)
        if not os.path.isfile(locres_path):
            self.__export_locres_old(locres_pak_path, locres_path)

    def __export_locres_old(self, locres_pak_path: str, locres_path: str):
        # Execute QuickBMS command, redirecting input to the pipe
        exporter_process = subprocess.Popen([self.config["quickbms_path"], self.config["ut4_old_path"],
                                             locres_pak_path, self.config["working_path"]],
                                            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        # Pass the AES key to the pipe
        exporter_process.communicate(self.__get_aes_key())
        exporter_process.wait()
        os.rename(self.config["working_path"] + "\\Game.locres", locres_path)

    def locres_to_csv(self, csv_path: str = None):
        # Run UnrealLocres
        locres_path = self.__apply_language_to_path(self.config["working_path"] + RELATIVE_LOCRES)
        working_csv_path = self.__apply_language_to_path(self.config["working_path"] + RELATIVE_CSV)
        parser_process = subprocess.Popen([self.config["ul_path"], "export", locres_path, "-o", working_csv_path],
                                          stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        parser_process.wait()
        os.remove(locres_path)
        if csv_path:
            shutil.copy(working_csv_path, csv_path)

    def csv_to_json(self, json_path: str = None, force_overwrite: bool = False,
                    sort_keys: bool = False, archive: bool = False):
        # Parse the CSV file to JSON
        csv_path = self.config["working_path"] + RELATIVE_CSV
        csv_path = self.__apply_language_to_path(csv_path)
        json_dict = {}
        with open(csv_path, "rt", encoding="utf-8") as csv_locres:
            # Open the CSV file and create a temporary dictionary
            csv_read = csv.DictReader(csv_locres, delimiter=",")
            for index, line in enumerate(csv_read):
                # Begin recursion to place the line being read
                LocresExporter.__add_child(json_dict, line["key"].replace("KAY/O", "KAYO").split("/"), line["source"])

            # Dump the temporary dictionary
            self.__begin_json_parse_dump(json_path, json_dict, force_overwrite, sort_keys)
            if archive:
                self.__archive_json(json_dict)
        # Remove CSV file
        os.remove(csv_path)
        return json_dict

    @staticmethod
    def __add_child(curr_dict: dict, remaining_childs: list, child_contents: list):
        # If this is the last key in the path to the contents
        if len(remaining_childs) == 1:
            curr_dict[remaining_childs[0]] = child_contents
        # There are superkeys left to complete the path to the contents
        else:
            # Get or create the path currently being completed
            next_dict = curr_dict.get(remaining_childs[0], {})
            # Assign the reference to the next dictionary in case it did not exist
            curr_dict[remaining_childs[0]] = next_dict
            # Continue the recursion with one less remaining superkey
            LocresExporter.__add_child(next_dict, remaining_childs[1:], child_contents)

    def __begin_json_parse_dump(self, json_path: str, json_dict: dict, force_overwrite: bool, sort_keys: bool):
        json_path = json_path if json_path else self.config["output_path"]
        json_path = self.__apply_game_version_to_path(self.__apply_language_to_path(json_path))
        # Try to dump the temporary dictionary
        # If the file exists check for overwriting
        if os.path.exists(json_path):
            # If file is not forcibly overwritten
            if not force_overwrite:
                print("[WARN] Target '" + json_path + "' already exists,")
                overwrite = input("       Overwrite it? (y/n) ")
            # If file is forcibly overwritten
            else:
                overwrite = "y"
            # If overwriting the file
            if overwrite.lower() == "y" or overwrite.lower() == "yes":
                LocresExporter.__dump_json_parse(json_path, json_dict, "wt", sort_keys=sort_keys)
        # File does not exist
        else:
            LocresExporter.__dump_json_parse(json_path, json_dict, "xt", sort_keys=sort_keys)

    def __archive_json(self, json_dict: dict):
        json_paths = ConfigLoader(PACKAGE_ROOT + "\\" + LOCRES_CONFIG, validators)
        json_path = self.__apply_game_version_to_path(self.__apply_language_to_path(json_paths["output_path"]))
        write_type = "wt" if os.path.exists(json_path) else "xt"
        LocresExporter.__dump_json_parse(json_path, json_dict, write_type, self.encoding)

    @staticmethod
    def __dump_json_parse(json_path: str, json_dict: dict, write_type: str, encoding: str, sort_keys: bool = False):
        # Dump the temporary dictionary
        with open(json_path, write_type, encoding=encoding) as json_locres:
            if sort_keys:
                for outer_key, values in json_dict.items():
                    convert = lambda text: int(text) if text.isdigit() else text.lower()
                    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
                    json_dict[outer_key] = {key: values[key] for key in sorted(values, key=alphanum_key)}
            json.dump(json_dict, json_locres, indent=4, ensure_ascii=False)


def __select_language():
    language = input(f"[INPUT] Select language (default is '{DEFAULT_LANGUAGE}'):\n        ")
    if language == "":
        print(f"        Empty selection, using '{DEFAULT_LANGUAGE}'")
        language = DEFAULT_LANGUAGE
    return language.replace("-", "_"), language.replace("_", "-")


def __main():
    pak_language, folder_language = __select_language()
    exporter = LocresExporter(pak_language, folder_language)
    print("[QuickBMS] Exporting Locres")
    locres_pak = exporter.config["valorant_path"] + RELATIVE_LOCRES_PAK
    exporter.extract_locres(locres_pak)
    print("[UnrealLocres] Converting Locres to CSV")
    exporter.locres_to_csv()
    print("Converting CSV to JSON")
    exporter.csv_to_json(sort_keys=True)
    print("Done")


if __name__ == "__main__":
    __main()
