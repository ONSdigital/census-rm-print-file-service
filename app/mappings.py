from app.constants import PackCode, Dataset, Supplier, PrintTemplate, ActionType
from config import Config

PACK_CODE_TO_DESCRIPTION = {
    PackCode.P_IC_ICL1: 'Initial contact letter households - England',
    PackCode.P_IC_ICL2B: 'Initial contact letter households - Wales',
    PackCode.P_IC_ICL4: 'Initial contact letter households - Northern Ireland',
    PackCode.P_IC_H1: 'Initial contact questionnaire households - England',
    PackCode.P_IC_H2: 'Initial contact questionnaire households - Wales',
    PackCode.P_IC_H4: 'Initial contact questionnaire households - Northern Ireland',
    PackCode.P_OR_H1: 'Household Questionnaire for England',
    PackCode.P_OR_H2: 'Household Questionnaire for Wales (English)',
    PackCode.P_OR_H2W: 'Household Questionnaire for Wales (Welsh)',
    PackCode.P_OR_H4: 'Household Questionnaire for Northern Ireland (English)',
    PackCode.P_LP_HL1: 'Household Questionnaire Large Print pack for England',
    PackCode.P_LP_HL2: 'Household Questionnaire Large Print pack for Wales (English)',
    PackCode.P_LP_HL2W: 'Household Questionnaire Large Print pack for Wales (Welsh)',
    PackCode.P_LP_HL4: 'Household Questionnaire Large Print pack for Northern Ireland',
    PackCode.P_TB_TBARA1: 'Translation Booklet for England & Wales - Arabic',
    PackCode.P_TB_TBBEN1: 'Translation Booklet for England & Wales - Bengali',
    PackCode.P_TB_TBCAN1: 'Translation Booklet for England & Wales - Cantonese',
    PackCode.P_TB_TBCAN4: 'Translation Booklet for Northern Ireland - Cantonese',
    PackCode.P_TB_TBFRE1: 'Translation Booklet for England & Wales - French',
    PackCode.P_TB_TBGUJ1: 'Translation Booklet for England & Wales - Gujarati',
    PackCode.P_TB_TBGUR1: 'Translation Booklet for England & Wales - Panjabi – Gurmukhi	',
    PackCode.P_TB_TBIRI4: 'Translation Booklet for Northern Ireland - Irish',
    PackCode.P_TB_TBITA1: 'Translation Booklet for England & Wales - Italian',
    PackCode.P_TB_TBKUR1: 'Translation Booklet for England & Wales - Kurdish',
    PackCode.P_TB_TBLIT1: 'Translation Booklet for England & Wales - Lithuanian',
    PackCode.T_PB_TBLIT4: 'Translation Booklet for Northern Ireland - Lithuanian',
    PackCode.P_TB_TBMAN1: 'Translation Booklet for England & Wales - Mandarin Chinese',
    PackCode.P_TB_TBMAN4: 'Translation Booklet for Northern Ireland - Mandarin',
    PackCode.P_TB_TBPOL1: 'Translation Booklet for England & Wales - Polish',
    PackCode.P_TB_TBPOL4: 'Translation Booklet for Northern Ireland - Polish',
    PackCode.P_TB_TBPOR1: 'Translation Booklet for England & Wales - Portuguese',
    PackCode.P_TB_TBRUS1: 'Translation Booklet for England & Wales - Russian',
    PackCode.P_TB_TBSOM1: 'Translation Booklet for England & Wales - Somali',
    PackCode.P_TB_TBSPA1: 'Translation Booklet for England & Wales - Spanish',
    PackCode.P_TB_TBTUR1: 'Translation Booklet for England & Wales - Turkish',
    PackCode.P_TB_TBULS4: 'Translation Booklet for Northern Ireland - Ulster-Scots',
    PackCode.P_TB_TBURD1: 'Translation Booklet for England & Wales - Urdu',
    PackCode.P_TB_TBVIE1: 'Translation Booklet for England & Wales - Vietnamese',
    PackCode.P_TB_TBYSH1: 'Translation Booklet for England & Wales - Yiddish',

}

PACK_CODE_TO_DATASET = {
    PackCode.P_IC_ICL1: Dataset.PPD1_1,
    PackCode.P_IC_ICL2B: Dataset.PPD1_1,
    PackCode.P_IC_ICL4: Dataset.PPD1_1,
    PackCode.P_IC_H1: Dataset.QM3_2,
    PackCode.P_IC_H2: Dataset.QM3_2,
    PackCode.P_IC_H4: Dataset.QM3_2,
    PackCode.P_OR_H1: Dataset.QM3_4,
    PackCode.P_OR_H2: Dataset.QM3_4,
    PackCode.P_OR_H2W: Dataset.QM3_4,
    PackCode.P_OR_H4: Dataset.QM3_4,
    PackCode.P_LP_HL1: Dataset.PPD1_3,
    PackCode.P_LP_HL2: Dataset.PPD1_3,
    PackCode.P_LP_HL2W: Dataset.PPD1_3,
    PackCode.P_LP_HL4: Dataset.PPD1_3,
    PackCode.P_TB_TBARA1: Dataset.PPD1_3,
    PackCode.P_TB_TBBEN1: Dataset.PPD1_3,
    PackCode.P_TB_TBCAN1: Dataset.PPD1_3,
    PackCode.P_TB_TBCAN4: Dataset.PPD1_3,
    PackCode.P_TB_TBFRE1: Dataset.PPD1_3,
    PackCode.P_TB_TBGUJ1: Dataset.PPD1_3,
    PackCode.P_TB_TBGUR1: Dataset.PPD1_3,
    PackCode.P_TB_TBIRI4: Dataset.PPD1_3,
    PackCode.P_TB_TBITA1: Dataset.PPD1_3,
    PackCode.P_TB_TBKUR1: Dataset.PPD1_3,
    PackCode.P_TB_TBLIT1: Dataset.PPD1_3,
    PackCode.T_PB_TBLIT4: Dataset.PPD1_3,
    PackCode.P_TB_TBMAN1: Dataset.PPD1_3,
    PackCode.P_TB_TBMAN4: Dataset.PPD1_3,
    PackCode.P_TB_TBPOL1: Dataset.PPD1_3,
    PackCode.P_TB_TBPOL4: Dataset.PPD1_3,
    PackCode.P_TB_TBPOR1: Dataset.PPD1_3,
    PackCode.P_TB_TBRUS1: Dataset.PPD1_3,
    PackCode.P_TB_TBSOM1: Dataset.PPD1_3,
    PackCode.P_TB_TBSPA1: Dataset.PPD1_3,
    PackCode.P_TB_TBTUR1: Dataset.PPD1_3,
    PackCode.P_TB_TBULS4: Dataset.PPD1_3,
    PackCode.P_TB_TBVIE1: Dataset.PPD1_3,
    PackCode.P_TB_TBYSH1: Dataset.PPD1_3,
}

DATASET_TO_SUPPLIER = {
    Dataset.QM3_2: Supplier.QM,
    Dataset.QM3_4: Supplier.QM,
    Dataset.PPD1_1: Supplier.PPO,
    Dataset.PPD1_3: Supplier.PPO
}

SUPPLIER_TO_SFTP_DIRECTORY = {
    Supplier.QM: Config.SFTP_QM_DIRECTORY,
    Supplier.PPO: Config.SFTP_PPO_DIRECTORY,
}

SUPPLIER_TO_KEY_PATH = {
    Supplier.QM: Config.QM_SUPPLIER_PUBLIC_KEY_PATH,
    Supplier.PPO: Config.PPO_SUPPLIER_PUBLIC_KEY_PATH,
}

ACTION_TYPE_TO_PRINT_TEMPLATE = {
    ActionType.ICL1E: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.ICL2W: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.ICL4N: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.ICHHQE: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.ICHHQW: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.ICHHQN: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.P_OR_HX: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.P_LP_HX: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_TB_TBX: PrintTemplate.PPO_LETTER_TEMPLATE

}

SUPPLIER_TO_PRINT_TEMPLATE = {
    Supplier.PPO: PrintTemplate.PPO_LETTER_TEMPLATE,
    Supplier.QM: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
}
