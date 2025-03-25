import re
import sys

def parse_hisat2_log(file_path):
    with open(file_path, 'r') as f:
        text = f.read()

    patterns = {
        "Total Reads": r"^(\d+) reads",
        "Overall Alignment Rate": r"^(\d+\.\d+)% overall alignment rate",
        "Concordant Unique Pairs": r"(\d+) \([\d\.]+%\) aligned concordantly exactly 1 time",
        "Concordant Multi-mapped": r"(\d+) \([\d\.]+%\) aligned concordantly >1 times",
        "Non-Concordant Pairs": r"(\d+) \([\d\.]+%\) aligned concordantly 0 times",
        "Discordant Alignments": r"^\s+(\d+) \([\d\.]+%\) aligned discordantly 1 time",
        "Unaligned Pairs Total": r"\s+(\d+) pairs aligned 0 times concordantly or discordantly",
        "Single-end Unaligned": r"^\s+(\d+) \([\d\.]+%\) aligned 0 times",
        "Single-end Unique": r"^\s+(\d+) \([\d\.]+%\) aligned exactly 1 time",
        "Single-end Multi": r"^\s+(\d+) \([\d\.]+%\) aligned >1 times"
    }

    summary = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        summary[key] = float(match.group(1)) if match else "NA"
    total_reads = summary.get("Total Reads", 0)
    print("{:<35} {:>15}".format("Metric", "Value"))
    print("-" * 55)
    for key, value in summary.items():
        if key == "Total Reads":
            print("{:<35} {:>15}".format(key, int(value)))
        elif key == "Overall Alignment Rate":
            print("{:<35} {:>14.2f}%".format(key, value))
        else:
            print("{:<35} {:>14.2f}%".format(key, value/total_reads * 100))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_hisat2_log.py <hisat2_log.txt>")
        sys.exit(1)

    parse_hisat2_log(sys.argv[1])

