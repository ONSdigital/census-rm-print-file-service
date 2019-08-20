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
    PackCode.P_RL_1RL1_1: '1st Reminder, Letter - for England addresses',
    PackCode.P_RL_1RL1_2: '2nd Reminder, Letter - for England addresses',
    PackCode.P_RL_1RL2B_1: '1st Reminder, Letter - for Wales addresses (bilingual Welsh and English)',
    PackCode.P_RL_1RL2B_2: '2nd Reminder, Letter - for Wales addresses (bilingual Welsh and English)',
    PackCode.P_RL_1RL4: '1st Reminder, Letter - for Ireland addresses',
    PackCode.P_RL_2RL1_3a: '3rd Reminder, Letter - for England addresses',
    PackCode.P_RL_2RL2B_3a: '3rd Reminder, Letter - for Wales addresses	'
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
    PackCode.P_RL_1RL1_1: Dataset.PPD1_2,
    PackCode.P_RL_1RL1_2: Dataset.PPD1_2,
    PackCode.P_RL_1RL2B_1: Dataset.PPD1_2,
    PackCode.P_RL_1RL2B_2: Dataset.PPD1_2,
    PackCode.P_RL_1RL4: Dataset.PPD1_2,
    PackCode.P_RL_2RL1_3a: Dataset.PPD1_2,
    PackCode.P_RL_2RL2B_3a: Dataset.PPD1_2,
}

DATASET_TO_SUPPLIER = {
    Dataset.QM3_2: Supplier.QM,
    Dataset.QM3_4: Supplier.QM,
    Dataset.PPD1_1: Supplier.PPO,
    Dataset.PPD1_2: Supplier.PPO
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
    ActionType.P_RL_1RL1_1: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL1_2: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL4: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_2RL1_3a: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL2B_1: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL2B_2: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_2RL2B_3a: PrintTemplate.PPO_LETTER_TEMPLATE,
}

SUPPLIER_TO_PRINT_TEMPLATE = {
    Supplier.PPO: PrintTemplate.PPO_LETTER_TEMPLATE,
    Supplier.QM: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
}
