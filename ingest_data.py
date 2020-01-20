import csv
from itertools import accumulate
from itertools import zip_longest as izip_longest
from pathlib import Path
import requests
import typing


FIELD_NAMES = ("name", "width", "datatype")
DATATYPE_TO_OBJECT_MAPPING = {
    "BOOLEAN": bool,
    "INTEGER": int,
    "TEXT": str,
}


class PerformanceDataParser(object):

    def __init__(self, schema_file: str):
    
        self.API_URL = "https://jsonplaceholder.typicode.com/posts"
        self.metric_names = []
        self.field_widths = []
        self.field_converter = {}

        self._parse_schema_file(schema_file)
        self.parse = self._make_data_parser()

    def _parse_schema_file(self, schema_file: str):

        try:
            with open(schema_file) as f:
                reader = csv.DictReader(f, fieldnames=FIELD_NAMES)
                for idx, row in enumerate(reader):
                    self.metric_names.append(row["name"])
                    self.field_widths.append(int(row["width"]))
                    self.field_converter[idx] = DATATYPE_TO_OBJECT_MAPPING[row["datatype"]]
        except FileNotFoundError as e:
            e.args(f"Could not find schema file: {schema_file}")
            raise

    def ingest(self, data_file: str):

        try:
            with open(data_file) as f:
                for idx, row in enumerate(f):
                    metrics_data = self.parse(row)
                    self._push_to_api(dict(zip(self.metric_names, metrics_data)))
        except FileNotFoundError:
            e.args(f"Failed to ingest data, could not find data file: {schema_file}")
            raise

    def _push_to_api(self, data: typing.Dict):
        print(f"Sending the following data to the API: {data}")
        response = requests.post(self.API_URL, json=data)

        if response.status_code == requests.codes.created:
            print(f"Data sent successfully, response status code: {response.status_code}")
        else:
            print(
                "And error ocurrer while sending the data to the API, "
                f"reponse: {response.json()}")

    def _make_data_parser(self):

        cuts = tuple(cut for cut in accumulate(abs(fw) for fw in self.field_widths))
        fields = tuple(izip_longest((0,) + cuts, cuts))[:-1]  # ignore the last one
        
        parser = lambda line: tuple(
            self.field_converter[idx](line[i:j])
            for idx, (i, j) in enumerate(fields)
        )

        return parser


if __name__ == "__main__":

    schema_directory = Path('schemas/')
    data_directory = Path('data/')

    existing_schema_files_set = set(entry.name[:-4] for entry in schema_directory.iterdir() if entry.is_file())
    existing_data_files_set = set(entry.name[:-4] for entry in data_directory.iterdir() if entry.is_file())

    filenames_to_ingest_set = existing_schema_files_set & existing_data_files_set
    files_to_process_count = len(filenames_to_ingest_set)

    print(f"Starting processing {files_to_process_count}")

    for filename in filenames_to_ingest_set:
        print(f"Reading schema file: {filename}.csv")
        parser = PerformanceDataParser(schema_directory.joinpath(f"{filename}.csv"))
        
        print(f"Ingesting data...")
        parser.ingest(data_directory.joinpath(f"{filename}.txt"))
    
    print(f"Finished processing {files_to_process_count}")
