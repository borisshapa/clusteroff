import argparse
import csv
import json
import random
import sys


def _configure_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path", type=str, default="data/en.openfoodfacts.org.products.csv"
    )
    parser.add_argument("--columns-path", type=str, default="configs/columns.json")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--save-to", type=str, default="data/products-1k.csv")
    return parser


def main(data_path: str, columns_path: str, limit: int, save_to: str):
    csv.field_size_limit(sys.maxsize)

    with open(columns_path, "r", encoding="utf-8") as columns_file:
        columns = json.load(columns_file)["nutriments"]

    data = []
    with open(data_path, "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter="\t")
        header = next(csvreader)
        feature_column_index = [header.index(col) for col in columns]

        for row in csvreader:
            skip = False
            for col_index in feature_column_index:
                if row[col_index] == "":
                    skip = True
                    break
            if skip:
                continue

            data.append(row)

        random.shuffle(data)
        data = data[:limit]

        with open(save_to, "w", encoding="utf-8") as csv_result:
            csv_writer = csv.writer(csv_result, delimiter="\t")
            csv_writer.writerow(header)
            csv_writer.writerows(data)


if __name__ == "__main__":
    args = _configure_parser().parse_args()
    main(**vars(args))
