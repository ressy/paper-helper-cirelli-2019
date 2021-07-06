#!/usr/bin/env python

import re
import sys
from csv import DictReader, DictWriter

def convert(tableS1_in, alleles_csv_out):
    with open(tableS1_in) as f_in, open(alleles_csv_out, "wt") as f_out:
        reader = DictReader(f_in)
        rows_out = []
        for row in reader:
            gene = re.sub(r"\.a$", "", re.sub(r"^LJI\.Rh_", "", row["Sequence.ID"]))
            gene = re.sub(r"\.", "-", gene)
            family = re.sub("-.*", "", gene)
            segment = family[0:4]
            locus = segment[0:3]
            rm_na = lambda txt: re.sub("^NA$", "", txt)
            rows_out.append({
                "Allele": row["Sequence.ID"],
                "Gene": gene,
                "Family": family,
                "Segment": segment,
                "Locus": locus,
                "FunctionalAnnotation": row["Functional.Annotation"],
                "Contig": row["Rh.Contig.Name"],
                "AnnotationType": row["Annotation.Type"],
                "IMGT": rm_na(row["IMGT"]),
                "NCBI": rm_na(row["NCBI"]),
                "RepSeq": rm_na(row["RepSeq"]),
                "Seq": row["V.Region.Sequence"]}) # yes, this does include D and J too
        writer = DictWriter(f_out, fieldnames=rows_out[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows_out)

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
