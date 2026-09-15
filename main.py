from pathlib import Path

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import typer


app = typer.Typer()


@app.command()
def plot_disk_io(json_file: Path):
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

    physical_df = io_df[io_df["disk_device"].isin(["sda", "nvme0n1"])]
    physical_df = physical_df.set_index("timestamp")
    start_time = physical_df.index.min()
    end_time = physical_df.index.max()

    # Seperate dataframe with 5-minute resampling to improve the readability of the graphs  
    plot_df = (physical_df.resample("5min").mean(numeric_only=True))

    # === Disk I/O metrics summary ===
    summary = physical_df[
        ["util", "aqu-sz", "w_await", "r_await", "wkB/s", "rkB/s"]
    ].agg(["mean", "max"]).round(2)
    print(f"{physical_df['hostname'].iloc[0].upper()} summary ({start_time:%Y-%m-%d %H:%M} - {end_time:%Y-%m-%d %H:%M}):")
    print(summary)

    # === Disk performance graph ===
    fig_perf, axes_perf = plt.subplots(2, 2, figsize=(18, 10), sharex=True)
    fig_perf.suptitle(
        f"{physical_df['hostname'].iloc[0].upper()} Disk performance from iostat logs "
        f"({start_time:%Y-%m-%d %H:%M} - {end_time:%Y-%m-%d %H:%M})",
        fontsize=16,
        fontweight="bold"
    )
    axes_perf[0, 0].plot(plot_df.index, plot_df["util"])
    axes_perf[0, 0].set_title("Disk utilization")
    axes_perf[0, 0].set_ylabel("%")
    axes_perf[0, 1].plot(plot_df.index, plot_df["aqu-sz"])
    axes_perf[0, 1].set_title("Outstanding I/O requests")  
    axes_perf[0, 1].set_ylabel("Requests")
    axes_perf[1, 0].plot(plot_df.index, plot_df["w_await"])
    axes_perf[1, 0].set_title("Write wait time")
    axes_perf[1, 0].set_ylabel("ms")
    axes_perf[1, 1].plot(plot_df.index, plot_df["r_await"])
    axes_perf[1, 1].set_title("Read wait time")
    axes_perf[1, 1].set_ylabel("ms")
    # Format dates correctly in x-axis
    for ax in axes_perf.flatten():
        ax.xaxis.set_major_locator(
            mdates.HourLocator(interval=1)
        )
        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%H:%M")
        )
        ax.grid(True, alpha=0.3)
    fig_perf.autofmt_xdate()

    # === Disk throughput graph ===
    fig_thr, ax_thr = plt.subplots(figsize=(18, 10))
    ax_thr.set_title(
        f"{physical_df['hostname'].iloc[0].upper()} Disk throughput from iostat logs "
        f"({start_time:%Y-%m-%d %H:%M} - {end_time:%Y-%m-%d %H:%M})",
        fontsize=16,
        fontweight="bold"
    )
    ax_thr.plot(plot_df.index, plot_df["wkB/s"], label="Write Throughput")
    ax_thr.plot(plot_df.index, plot_df["rkB/s"], label="Read Throughput")
    ax_thr.set_ylabel("kB/s")
    ax_thr.legend()
    ax_thr.grid(True, alpha=0.3)
    # Format dates correctly in x-axis
    ax_thr.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax_thr.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    plt.show()


if __name__ == "__main__":
    app()