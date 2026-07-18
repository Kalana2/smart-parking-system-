#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="${1:-videos}"
OUTPUT_FILE="${OUTPUT_DIR}/sample.mp4"
URLS=(
	"https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/car-detection.mp4"
	"https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/face-demographics-walking.mp4"
)

if [ -f "$OUTPUT_FILE" ]; then
	echo "✓ Sample video already exists at ${OUTPUT_FILE}"
	exit 0
fi

mkdir -p "$OUTPUT_DIR"

for url in "${URLS[@]}"; do
	echo "Downloading ${url} ..."
	if command -v wget &>/dev/null; then
		wget -q --show-progress "$url" -O "$OUTPUT_FILE" && {
			echo "✓ Saved to ${OUTPUT_FILE} ($(du -h "$OUTPUT_FILE" | cut -f1))"
			exit 0
		}
	elif command -v curl &>/dev/null; then
		curl -fL "$url" -o "$OUTPUT_FILE" && {
			echo "✓ Saved to ${OUTPUT_FILE} ($(du -h "$OUTPUT_FILE" | cut -f1))"
			exit 0
		}
	fi
done

echo "Failed to download sample video." >&2
exit 1
