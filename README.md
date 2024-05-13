
# Booth-Badge-Scanner

Booth-Badge-Scanner is a Python tool designed to extract VCARD information from QR codes found in images. This tool is capable of processing images from various sources, including local files, URLs, directories, and files containing lists of paths or URLs.

## Features

- Supports reading images from local paths, URLs, directories, and files containing lists of paths or URLs.
- Efficiently decodes QR codes to extract VCARD information.
- Outputs VCARD data in both human-readable format and CSV format.
- Handles faulty or incomplete QR code data by providing raw QR data.

## Installation

Clone the repository to your local machine:

\`\`\`bash
git clone https://github.com/javier/booth-badge-scanner.git
cd booth-badge-scanner
\`\`\`

Ensure you have Python 3.x installed, and install the required dependencies:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage

### Basic Command

\`\`\`bash
python booth-badge-scanner.py <source> [--csv]
\`\`\`

- `<source>` can be a URL, a local file path, a directory, or a file containing a list of URLs or file paths.
- \`--csv\` is an optional argument to output the results in CSV format.

### Examples

1. **Scan a single image file**:

\`\`\`bash
python booth-badge-scanner.py /path/to/image.jpg
\`\`\`

2. **Scan all images in a directory**:

\`\`\`bash
python booth-badge-scanner.py /path/to/directory --csv
\`\`\`

3. **Scan from a list of image URLs or paths specified in a text file**:

\`\`\`bash
python booth-badge-scanner.py /path/to/file.txt --csv
\`\`\`

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with any enhancements or fixes.

## License

Distributed under the Apache 2.0 License. See \`LICENSE\` for more information.
