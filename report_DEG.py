from pathlib import Path

import pandas
from datetime import datetime


def create_deg_report(ss1_fname, ss2_fname, ss1_sname, ss2_sname, ss1_exp_lvl_col_name, ss2_exp_lvl_col_name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # read in both excel workbooks to dataframes
    ss1_df = pandas.read_excel(ss1_fname, sheet_name=ss1_sname)
    ss2_df = pandas.read_excel(ss2_fname, sheet_name=ss2_sname)

    # find the genes unique to each ss
    ss1_unique_genes = ss1_df[~ss1_df.Genes.isin(ss2_df.Genes)]
    ss2_unique_genes = ss2_df[~ss2_df.Genes.isin(ss1_df.Genes)]
    ss1_common_genes = ss1_df[ss1_df.Genes.isin(ss2_df.Genes)]
    ss2_common_genes = ss2_df[ss2_df.Genes.isin(ss1_df.Genes)]

    # find upregulated and downregulated genes
    ss1_upregulated_genes = ss1_common_genes[ss1_common_genes[ss1_exp_lvl_col_name] > 0]
    ss1_downregulated_genes = ss1_common_genes[ss1_common_genes[ss1_exp_lvl_col_name] < 0]
    ss2_upregulated_genes = ss2_common_genes[ss2_common_genes[ss2_exp_lvl_col_name] > 0]
    ss2_downregulated_genes = ss2_common_genes[ss2_common_genes[ss2_exp_lvl_col_name] < 0]

    # get the base file names to use as a column name suffix if necessary
    ss1_fbasename = Path(ss1_fname).stem
    ss2_fbasename = Path(ss2_fname).stem

    # find the common up and down regulated genes
    common_upregulated_genes = pandas.merge(
        left=ss1_upregulated_genes, right=ss2_upregulated_genes, on=['Genes'],
        suffixes=(f"_{ss1_fbasename}", f"_{ss2_fbasename}"), how='inner'
    )

    def reorder_columns(df):
        leading_columns = ['Genes', ss1_exp_lvl_col_name, ss2_exp_lvl_col_name]
        return df[leading_columns + [col for col in common_upregulated_genes.columns if col not in leading_columns]]

    common_upregulated_genes = reorder_columns(common_upregulated_genes)

    common_downregulated_genes = pandas.merge(
        left=ss1_downregulated_genes, right=ss2_downregulated_genes, on=['Genes'],
        suffixes=(f"_{ss1_fbasename}", f"_{ss2_fbasename}"), how='inner'
    )
    common_downregulated_genes = reorder_columns(common_downregulated_genes)

    # find the inversely up and down regulated genes
    inversely_regulated_genes_ss1_up = pandas.merge(
        left=ss1_upregulated_genes, right=ss2_downregulated_genes, on=['Genes'],
        suffixes=(f"_{ss1_fbasename}", f"_{ss2_fbasename}"), how='inner'
    )
    inversely_regulated_genes_ss2_up = pandas.merge(
        left=ss1_downregulated_genes, right=ss2_upregulated_genes, on=['Genes'],
        suffixes=(f"_{ss1_fbasename}", f"_{ss2_fbasename}"), how='inner'
    )
    # combine the inversely regulated gene DFs for convenience
    inversely_regulated_genes = pandas.concat([inversely_regulated_genes_ss1_up,
                                               inversely_regulated_genes_ss2_up],
                                              ignore_index=True)
    inversely_regulated_genes = reorder_columns(inversely_regulated_genes)

    # create a new Excel file with different tabs for the different categories
    with pandas.ExcelWriter(f'deg_report-{timestamp}.xlsx') as outfile:
        ss1_unique_genes.to_excel(outfile, sheet_name=f'{ss1_fbasename} Unique', index=False)
        ss2_unique_genes.to_excel(outfile, sheet_name=f'{ss2_fbasename} Unique', index=False)
        common_upregulated_genes.to_excel(outfile, sheet_name='Upregulated Genes', index=False)
        common_downregulated_genes.to_excel(outfile, sheet_name='Downregulated Genes', index=False)
        inversely_regulated_genes.to_excel(outfile, sheet_name='Inversely Regulated Genes', index=False)


if __name__ == '__main__':
    # todo: change these values to match your excel files!!!
    ss1_fname = "MultivsUni.xlsx"
    ss1_sname = "master file"
    ss1_exp_lvl_col_name = "diffexpr-Day1_MC_vs_WT"
    ss2_fname = "RLS1MtvsWt.xlsx"
    ss2_sname = "RLS1_TAP_TA_GO"
    ss2_exp_lvl_col_name = "diffexpr-TAP_day1_MtvsWT_sig-results"

    print("Generating report...")
    create_deg_report(ss1_fname=ss1_fname, ss1_sname=ss1_sname,
                      ss2_fname=ss2_fname, ss2_sname=ss2_sname,
                      ss1_exp_lvl_col_name=ss1_exp_lvl_col_name,
                      ss2_exp_lvl_col_name=ss2_exp_lvl_col_name)
    print("\nDone!")
