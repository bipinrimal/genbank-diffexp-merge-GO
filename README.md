# Genbank and Differential Expression Data Merge

This script parses a genbank file and a differential gene expression file, and merges them based on locus_tag/gene_id to create a new file with additional columns for GO_process, GO_component, and GO_function.

## Usage

To run the script, you'll need to have the following dependencies installed:

- Biopython
- pandas

You can run the script with the following command:
`python merge_data.py -gb genbank_file.gb -i differential_expression.csv -o merged_data.csv`


Replace `genbank_file.gb`, `differential_expression.csv`, and `merged_data.csv` with the actual file names and paths on your system.

Note: It assumes that the `locus_tag` in genbank matches with `gene_id` in the differential gene expression file
## License

This script is released under the MIT License. See the LICENSE file for more information.
