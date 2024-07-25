from pathlib import Path

import pandas
from datetime import datetime


def create_deg_report(ss1_fname, ss2_fname, ss1_sname, ss2_sname):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ss1_df = pandas.read_excel(ss1_fname, sheet_name=ss1_sname)
    ss2_df = pandas.read_excel(ss2_fname, sheet_name=ss2_sname)

    ss1_gene_set = set(ss1_df["Genes"].unique())
    ss2_gene_set = set(ss2_df["Genes"].unique())

    ss1_unique_genes = ss1_gene_set.difference(ss2_gene_set)
    ss2_unique_genes = ss2_gene_set.difference(ss1_gene_set)
    common_genes = ss1_gene_set.intersection(ss2_gene_set)

    ss1_unique_genes_df = ss1_df[ss1_df.Genes.isin(ss1_unique_genes)]
    ss2_unique_genes_df = ss2_df[ss2_df.Genes.isin(ss2_unique_genes)]

    ss1_common_genes_df = ss1_df[ss1_df.Genes.isin(common_genes)]
    ss1_common_genes_df = ss1_common_genes_df.copy()
    ss1_common_genes_df.loc[:, "Source SS"] = ss1_fname
    ss2_common_genes_df = ss2_df[ss2_df.Genes.isin(common_genes)]
    ss2_common_genes_df = ss2_common_genes_df.copy()
    ss2_common_genes_df.loc[:, "Source SS"] = ss2_fname
    common_genes_df = pandas.concat([ss1_common_genes_df, ss2_common_genes_df], ignore_index=True).sort_values(
        by='Genes')

    ss1_fbasename = Path(ss1_fname).stem
    ss2_fbasename = Path(ss2_fname).stem
    with pandas.ExcelWriter(f'deg_report-{timestamp}.xlsx') as outfile:
        ss1_unique_genes_df.to_excel(outfile, sheet_name=f'{ss1_fbasename} Unique', index=False)
        ss2_unique_genes_df.to_excel(outfile, sheet_name=f'{ss2_fbasename} Unique', index=False)
        common_genes_df.to_excel(outfile, sheet_name='Common Genes', index=False)

    with open(f'{ss1_fbasename}_unique_genes-{timestamp}.txt', 'w') as outfile:
        outfile.write(f"Genes unique to {ss1_fname}:")
        {outfile.write(f"\n{gene_name}") for gene_name in ss1_unique_genes}

    with open(f'{ss2_fbasename}_unique_genes-{timestamp}.txt', 'w') as outfile:
        outfile.write(f"Genes unique to {ss2_fname}:")
        {outfile.write(f"\n{gene_name}") for gene_name in ss2_unique_genes}

    with open(f'common_genes-{timestamp}.txt', 'w') as outfile:
        outfile.write(f"Genes common to {ss1_fname} and {ss2_fname}:")
        {outfile.write(f"\n{gene_name}") for gene_name in common_genes}


if __name__ == '__main__':
    ss1_fname = input("Please provide the file name of spreadsheet #1: ").strip()
    ss1_sname = input(f"Please provide the sheet name containing the genes within {ss1_fname}: ").strip()
    ss2_fname = input("Please provide the file name of spreadsheet #2: ").strip()
    ss2_sname = input(f"Please provide the sheet name containing the genes within {ss2_fname}: ").strip()
    print("Generating report...")
    create_deg_report(ss1_fname=ss1_fname, ss1_sname=ss1_sname,
                      ss2_fname=ss2_fname, ss2_sname=ss2_sname)
    print("\nDone!")