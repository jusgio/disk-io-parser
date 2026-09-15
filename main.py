from pathlib import Path

import json
import pandas as pd
import typer


app = typer.Typer()


@app.command()
def parse_io_log(json_file: Path):
    print(f"Processing {json_file}")

    io_entries = []

    with open(json_file, mode="r", encoding="utf-8") as f:
        for line in f:
            io_entry = json.loads(line)

            host = io_entry["sysstat"]["hosts"][0]
            statistics = host["statistics"][0]
            for disk in statistics["disk"]:
                if not disk["disk_device"].startswith("loop"):
                    io_entries.append({
                        "hostname": host["nodename"],
                        "timestamp": statistics["timestamp"],
                        **disk
                    })

    io_df = pd.DataFrame(io_entries)
    io_df["timestamp"] = pd.to_datetime(io_df["timestamp"])

    sda_df = io_df[io_df["disk_device"] == "sda"]
    sda_df = sda_df.set_index("timestamp")
    dm0_df = io_df[io_df["disk_device"] == "dm-0"]
    dm0_df = dm0_df.set_index("timestamp")

    print(sda_df)
    print(dm0_df)


if __name__ == "__main__":
    app()