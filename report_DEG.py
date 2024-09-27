import pandas
from datetime import datetime
import re


def parse_gene_number(gene_text):
    gene_number_re = re.compile(r"g\d+")
    m = re.search(gene_number_re, gene_text)
    if m:
        return m.group(0)
    else:
        return None


class DegDataObj:
    GENE_COL_NAME = "extracted_common_gene_id"

    def __init__(self, wb_fp, ss_name, short_uniq_id, gene_col_name, expr_lvl_col_name):
        self.wb_fp = wb_fp
        self.df = pandas.read_excel(wb_fp, sheet_name=ss_name)
        self.id = short_uniq_id
        self.expr_lvl_col_name = f"{expr_lvl_col_name}_{self.id}"
        self.df.rename(columns={expr_lvl_col_name: self.expr_lvl_col_name}, inplace=True)
        self.df[DegDataObj.GENE_COL_NAME] = self.df[gene_col_name].apply(lambda x: parse_gene_number(x))

    def get_gene_col(self):
        return self.df[DegDataObj.GENE_COL_NAME]


def get_unique_genes(deg_obj1: DegDataObj, deg_obj2: DegDataObj):
    return deg_obj1.df[~deg_obj1.get_gene_col().isin(deg_obj2.get_gene_col())]


def __get_common_genes_df_from_1st_deg_obj(deg_obj1: DegDataObj, deg_obj2: DegDataObj):
    return deg_obj1.df[deg_obj1.get_gene_col().isin(deg_obj2.get_gene_col())]


def get_upregulated_genes(deg_obj: DegDataObj):
    return deg_obj.df[deg_obj.df[deg_obj.expr_lvl_col_name] > 0]


def get_downregulated_genes(deg_obj: DegDataObj):
    return deg_obj.df[deg_obj.df[deg_obj.expr_lvl_col_name] < 0]


def __merge_deg_df_records(deg_obj1, df1, deg_obj2, df2):
    merged_dfs = pandas.merge(
        left=df1, right=df2, on=DegDataObj.GENE_COL_NAME,
        suffixes=(f"_{deg_obj1.id}", f"_{deg_obj2.id}"), how='inner'
    )
    leading_columns = [DegDataObj.GENE_COL_NAME, deg_obj1.expr_lvl_col_name, deg_obj2.expr_lvl_col_name]
    return merged_dfs[leading_columns + [col for col in merged_dfs.columns if col not in leading_columns]]


def find_commonly_upregulated_genes(deg_obj1: DegDataObj, deg_obj2: DegDataObj):
    up_reg1 = get_upregulated_genes(deg_obj1)
    up_reg2 = get_upregulated_genes(deg_obj2)
    return __merge_deg_df_records(deg_obj1, up_reg1, deg_obj2, up_reg2)


def find_commonly_downregulated_genes(deg_obj1: DegDataObj, deg_obj2: DegDataObj):
    down_reg1 = get_downregulated_genes(deg_obj1)
    down_reg2 = get_downregulated_genes(deg_obj2)
    return __merge_deg_df_records(deg_obj1, down_reg1, deg_obj2, down_reg2)


def find_inversely_regulated_genes(deg_obj1: DegDataObj, deg_obj2: DegDataObj):
    up_reg1 = get_upregulated_genes(deg_obj1)
    down_reg2 = get_downregulated_genes(deg_obj2)
    up1_down2 = __merge_deg_df_records(deg_obj1, up_reg1, deg_obj2, down_reg2)

    down_reg1 = get_downregulated_genes(deg_obj1)
    up_reg2 = get_upregulated_genes(deg_obj2)
    down1_up2 = __merge_deg_df_records(deg_obj1, down_reg1, deg_obj2, up_reg2)

    return pandas.concat([up1_down2, down1_up2], ignore_index=True)


def report_common_and_inverse_gn_reg(deg_obj1: DegDataObj, deg_obj2: DegDataObj):
    if deg_obj1.id == deg_obj2.id:
        return "No file created... IDs provided were not unique"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    uniq_gns1 = get_unique_genes(deg_obj1, deg_obj2)
    uniq_gns2 = get_unique_genes(deg_obj2, deg_obj1)
    common_up_reg_gns = find_commonly_upregulated_genes(deg_obj1, deg_obj2)
    common_down_reg_gns = find_commonly_downregulated_genes(deg_obj1, deg_obj2)
    inverse_reg_gns = find_inversely_regulated_genes(deg_obj1, deg_obj2)

    out_fname = f'Output/{deg_obj1.id}-vs-{deg_obj2.id}_deg_report-{timestamp}.xlsx'

    # create a new Excel file with different tabs for the different categories
    with pandas.ExcelWriter(out_fname) as outfile:
        uniq_gns1.to_excel(outfile, sheet_name=f'{deg_obj1.id} Unique', index=False)
        uniq_gns2.to_excel(outfile, sheet_name=f'{deg_obj2.id} Unique', index=False)
        common_up_reg_gns.to_excel(outfile, sheet_name='Upregulated Genes', index=False)
        common_down_reg_gns.to_excel(outfile, sheet_name='Downregulated Genes', index=False)
        inverse_reg_gns.to_excel(outfile, sheet_name='Inversely Regulated Genes', index=False)

    return out_fname


def generate_report_with_printed_statuses(deg_obj1: DegDataObj, deg_obj2: DegDataObj):
    print(f"Working on {deg_obj1.id} vs {deg_obj2.id}...")
    print(report_common_and_inverse_gn_reg(deg_obj1, deg_obj2))
    print("")


if __name__ == '__main__':
    input_folder = "Input"
    rls_deg = DegDataObj(f"{input_folder}/RLS1MtvsWt.xlsx", "RLS1_TAP_TA_GO", "rls1Mut", "Genes",
                         "diffexpr-TAP_day1_MtvsWT_sig-results")
    exp_mt_deg = DegDataObj(f"{input_folder}/MultivsUni.xlsx", "master file", "ExpMult", "Genes",
                            "diffexpr-Day1_MC_vs_WT")
    salt_time_course_deg = DegDataObj(f"{input_folder}/SaltTimeCourseZhang2022; DifExpression analysis.xlsx", "Sheet1",
                                      "SaltTC",
                                      "GeneID", "SinglecellVSCellgroups_LogFold")
    predation_deg = DegDataObj(f"{input_folder}/MulticellularityBernardes2022; DifExpression analysis.xlsx", "Sheet1",
                               "Predation",
                               "GeneID", "SinglecellVSCellgroups_LogFold")
    generate_report_with_printed_statuses(rls_deg, exp_mt_deg)
    generate_report_with_printed_statuses(rls_deg, salt_time_course_deg)
    generate_report_with_printed_statuses(rls_deg, predation_deg)
    generate_report_with_printed_statuses(exp_mt_deg, salt_time_course_deg)
    generate_report_with_printed_statuses(exp_mt_deg, predation_deg)
    generate_report_with_printed_statuses(salt_time_course_deg, predation_deg)

