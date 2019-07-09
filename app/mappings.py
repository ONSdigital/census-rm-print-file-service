from config import Config

QM_SUPPLIER = 'QM'
PPD_SUPPLIER = 'PPD'

PRODUCTPACK_CODE_TO_DESCRIPTION = {
    'P_IC_ICL1': 'Initial contact letter households - England',
    'P_IC_ICL2': 'Initial contact letter households - Wales',
    'P_IC_ICL4': 'Initial contact letter households - Northern Ireland',
    'P_IC_H1': 'Initial contact questionnaire households - England',
    'P_IC_H2': 'Initial contact questionnaire households - Wales',
    'P_IC_H4': 'Initial contact questionnaire households - Northern Ireland'
}

PACK_CODE_TO_SUPPLIER = {
    'P_IC_ICL1': PPD_SUPPLIER,
    'P_IC_ICL2': PPD_SUPPLIER,
    'P_IC_ICL4': PPD_SUPPLIER,
    'P_IC_H1': QM_SUPPLIER,
    'P_IC_H2': QM_SUPPLIER,
    'P_IC_H4': QM_SUPPLIER
}

SUPPLIER_TO_DATASET = {
    QM_SUPPLIER: 'QM3.2',
    PPD_SUPPLIER: 'PPD1.1'
}

SUPPLIER_TO_SFTP_DIRECTORY = {
    QM_SUPPLIER: Config.SFTP_QM_DIRECTORY,
    PPD_SUPPLIER: Config.SFTP_PPO_DIRECTORY
}

SUPPLIER_TO_KEY_PATH = {
    QM_SUPPLIER: Config.QM_SUPPLIER_PUBLIC_KEY_PATH,
    PPD_SUPPLIER: Config.PPD_SUPPLIER_PUBLIC_KEY_PATH
}
