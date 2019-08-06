from config import Config

PPO_LETTER_TEMPLATE = ('uac',
                       'caseRef',
                       'title',
                       'forename',
                       'surname',
                       'addressLine1',
                       'addressLine2',
                       'addressLine3',
                       'townName',
                       'postcode',
                       'packCode')

QM_QUESTIONNAIRE_TEMPLATE = ('uac',
                             'qid',
                             'uacWales',
                             'qidWales',
                             'fieldCoordinatorId',
                             'title',
                             'forename',
                             'surname',
                             'addressLine1',
                             'addressLine2',
                             'addressLine3',
                             'townName',
                             'postcode',
                             'packCode')

QM_SUPPLIER = 'QM'
PPO_SUPPLIER = 'PPO'

QM3_2_DATASET = 'QM3.2'
QM3_4_DATASET = 'QM3.4'
PPD1_1_DATASET = 'PPD1.1'

PRODUCTPACK_CODE_TO_DESCRIPTION = {
    'P_IC_ICL1': 'Initial contact letter households - England',
    'P_IC_ICL2B': 'Initial contact letter households - Wales',
    'P_IC_ICL4': 'Initial contact letter households - Northern Ireland',
    'P_IC_H1': 'Initial contact questionnaire households - England',
    'P_IC_H2': 'Initial contact questionnaire households - Wales',
    'P_IC_H4': 'Initial contact questionnaire households - Northern Ireland',
    'P_OR_H1': 'Household Questionnaire for England',
    'P_OR_H2': 'Household Questionnaire for Wales (English)',
    'P_OR_H2W': 'Household Questionnaire for Wales (Welsh)',
    'P_OR_H4': 'Household Questionnaire for Northern Ireland (English)'
}

PACK_CODE_TO_DATASET = {
    'P_IC_ICL1': PPD1_1_DATASET,
    'P_IC_ICL2B': PPD1_1_DATASET,
    'P_IC_ICL4': PPD1_1_DATASET,
    'P_IC_H1': QM3_2_DATASET,
    'P_IC_H2': QM3_2_DATASET,
    'P_IC_H4': QM3_2_DATASET,
    'P_OR_H1': QM3_4_DATASET,
    'P_OR_H2': QM3_4_DATASET,
    'P_OR_H2W': QM3_4_DATASET,
    'P_OR_H4': QM3_4_DATASET
}

DATASET_TO_SUPPLIER = {
    QM3_2_DATASET: QM_SUPPLIER,
    QM3_4_DATASET: QM_SUPPLIER,
    PPD1_1_DATASET: PPO_SUPPLIER
}

SUPPLIER_TO_SFTP_DIRECTORY = {
    QM_SUPPLIER: Config.SFTP_QM_DIRECTORY,
    PPO_SUPPLIER: Config.SFTP_PPO_DIRECTORY
}

SUPPLIER_TO_KEY_PATH = {
    QM_SUPPLIER: Config.QM_SUPPLIER_PUBLIC_KEY_PATH,
    PPO_SUPPLIER: Config.PPO_SUPPLIER_PUBLIC_KEY_PATH
}

ACTION_TYPE_TO_PRINT_TEMPLATE = {
    'ICL1E': PPO_LETTER_TEMPLATE,
    'ICL2W': PPO_LETTER_TEMPLATE,
    'ICL4N': PPO_LETTER_TEMPLATE,
    'ICHHQE': QM_QUESTIONNAIRE_TEMPLATE,
    'ICHHQW': QM_QUESTIONNAIRE_TEMPLATE,
    'ICHHQN': QM_QUESTIONNAIRE_TEMPLATE,
    'P_OR_H1': QM_QUESTIONNAIRE_TEMPLATE,
    'P_OR_H2': QM_QUESTIONNAIRE_TEMPLATE,
    'P_OR_H2W': QM_QUESTIONNAIRE_TEMPLATE,
    'P_OR_H4': QM_QUESTIONNAIRE_TEMPLATE,
}

SUPPLIER_TO_PRINT_TEMPLATE = {
    PPO_SUPPLIER: PPO_LETTER_TEMPLATE,
    QM_SUPPLIER: QM_QUESTIONNAIRE_TEMPLATE
}
