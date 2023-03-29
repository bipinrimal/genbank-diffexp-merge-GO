import argparse
from Bio import SeqIO
import pandas as pd

# # Create an argument parser to specify the input and output files
parser = argparse.ArgumentParser(description="Merge genbank and differential expression data")
parser.add_argument("-gb", "--genbank", type=str, required=True, help="Path to genbank file")
parser.add_argument("-i", "--diffexp", type=str, required=True, help="Path to differential expression file")
parser.add_argument("-o", "--output", type=str, required=True, help="Path to output file")
args = parser.parse_args()

# Parse the genbank file and extract relevant information
genbank_data = {}
for record in SeqIO.parse(args.genbank, "genbank"):
    for feature in record.features:
        if feature.type == "CDS":
            locus_tag = feature.qualifiers.get("locus_tag", [""])[0]
            gene = feature.qualifiers.get("gene", [""])[0]
            refseq = feature.qualifiers.get("sequence:RefSeq", [""])[0]
            go_process = feature.qualifiers.get("GO_process", [""])[0]
            go_component = feature.qualifiers.get("GO_component", [""])[0]
            go_function = feature.qualifiers.get("GO_function", [""])[0]
            genbank_data[locus_tag] = {
                "gene": gene,
                "refseq": refseq,
                "go_process": go_process,
                "go_component": go_component,
                "go_function": go_function,
            }

# Load the differential expression file into a pandas DataFrame
diff_exp_data = pd.read_csv(args.diffexp)

# Merge the genbank and differential expression data based on locus_tag/gene_id
merged_data = pd.merge(diff_exp_data, pd.DataFrame.from_dict(genbank_data, orient="index"), left_on="gene_id", right_index=True, how="left")

# Create new columns for GO_process, GO_component, and GO_function and fill with genbank data
merged_data["GO_process"] = merged_data["go_process"]
merged_data["GO_component"] = merged_data["go_component"]
merged_data["GO_function"] = merged_data["go_function"]

# Drop unnecessary columns
merged_data.drop(["go_process", "go_component", "go_function"], axis=1, inplace=True)

# Write merged data to a new file
merged_data.to_csv(args.output, index=False)
