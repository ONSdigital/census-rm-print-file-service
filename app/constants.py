from enum import Enum


class ActionType(Enum):
    # Initial contact letters
    ICL1E = 'ICL1E'
    ICL2W = 'ICL2W'
    ICL4N = 'ICL4N'

    # Initial contact letter CE/SPG
    CE1_IC01 = 'CE1_IC01'
    CE1_IC02 = 'CE1_IC02'

    # Individual addressed initial contact letters for CE Estabs
    CE_IC03 = 'CE_IC03'
    CE_IC04 = 'CE_IC04'

    # Individual addressed initial contact letters for CE Units
    CE_IC03_1 = 'CE_IC03_1'
    CE_IC04_1 = 'CE_IC04_1'

    # Individual addressed initial contact letters for SPGs
    SPG_IC11 = 'SPG_IC11'
    SPG_IC12 = 'SPG_IC12'

    # Initial contact individual CE questionnaire
    CE_IC09 = 'CE_IC09'
    CE_IC10 = 'CE_IC10'

    # Initial contact household questionnaires
    ICHHQE = 'ICHHQE'
    ICHHQW = 'ICHHQW'
    ICHHQN = 'ICHHQN'

    # On request questionnaire fulfilments
    P_OR_HX = 'P_OR_HX'

    # On request individual fulfilment questionaires
    P_OR_IX = 'P_OR_IX'

    # Large print fulfilments
    P_LP_HLX = 'P_LP_HLX'

    # Translation booklet fulfilments
    P_TB_TBX = 'P_TB_TBX'

    # Reminder letters
    P_RL_1RL1_1 = 'P_RL_1RL1_1'
    P_RL_1RL2B_1 = 'P_RL_1RL2B_1'
    P_RL_1RL4 = 'P_RL_1RL4'
    P_RL_1RL1_2 = 'P_RL_1RL1_2'
    P_RL_1RL2B_2 = 'P_RL_1RL2B_2'
    P_RL_2RL1_3a = 'P_RL_2RL1_3a'
    P_RL_2RL2B_3a = 'P_RL_2RL2B_3a'

    # Reminder Questionnaires
    P_QU_H1 = 'P_QU_H1'
    P_QU_H2 = 'P_QU_H2'
    P_QU_H4 = 'P_QU_H4'

    # Response driven reminders
    P_RD_2RL1_1 = 'P_RD_2RL1_1'
    P_RD_2RL2B_1 = 'P_RD_2RL2B_1'
    P_RD_2RL1_2 = 'P_RD_2RL1_2'
    P_RD_2RL2B_2 = 'P_RD_2RL2B_2'
    P_RD_2RL1_3 = 'P_RD_2RL1_3'
    P_RD_2RL2B_3 = 'P_RD_2RL2B_3'


class PackCode(Enum):
    # Initial contact letters
    P_IC_ICL1 = 'P_IC_ICL1'
    P_IC_ICL2B = 'P_IC_ICL2B'
    P_IC_ICL4 = 'P_IC_ICL4'

    # Initial contact letter CE/SPG
    D_CE1A_ICLCR1 = 'D_CE1A_ICLCR1'
    D_CE1A_ICLCR2B = 'D_CE1A_ICLCR2B'

    # Individual addressed initial contact letters for CE Estabs and Units
    D_ICA_ICLR1 = 'D_ICA_ICLR1'
    D_ICA_ICLR2B = 'D_ICA_ICLR2B'

    # Individual addressed initial contact letters for SPGs
    P_ICCE_ICL1 = 'P_ICCE_ICL1'
    P_ICCE_ICL2B = 'P_ICCE_ICL2B'

    # Initial contact individual questionnaires
    D_FDCE_I1 = 'D_FDCE_I1'
    D_FDCE_I2 = 'D_FDCE_I2'

    # Initial contact questionnaires
    P_IC_H1 = 'P_IC_H1'
    P_IC_H2 = 'P_IC_H2'
    P_IC_H4 = 'P_IC_H4'

    # Reminder letters
    P_RL_1RL1_1 = 'P_RL_1RL1_1'
    P_RL_1RL2B_1 = 'P_RL_1RL2B_1'
    P_RL_1RL4 = 'P_RL_1RL4'
    P_RL_1RL1_2 = 'P_RL_1RL1_2'
    P_RL_1RL2B_2 = 'P_RL_1RL2B_2'
    P_RL_2RL1_3a = 'P_RL_2RL1_3a'
    P_RL_2RL2B_3a = 'P_RL_2RL2B_3a'

    # Reminder Questionnaires
    P_QU_H1 = "P_QU_H1"
    P_QU_H2 = "P_QU_H2"
    P_QU_H4 = "P_QU_H4"

    # On request questionnaire fulfilments
    P_OR_H1 = 'P_OR_H1'
    P_OR_H2 = 'P_OR_H2'
    P_OR_H2W = 'P_OR_H2W'
    P_OR_H4 = 'P_OR_H4'

    # On request continuation questionnaire fulfilments
    P_OR_HC1 = 'P_OR_HC1'
    P_OR_HC2 = 'P_OR_HC2'
    P_OR_HC2W = 'P_OR_HC2W'
    P_OR_HC4 = 'P_OR_HC4'

    # On request individual questionnaire fulfilments
    P_OR_I1 = 'P_OR_I1'
    P_OR_I2 = 'P_OR_I2'
    P_OR_I2W = 'P_OR_I2W'
    P_OR_I4 = 'P_OR_I4'

    # Large print fulfilments
    P_LP_HL1 = "P_LP_HL1"
    P_LP_HL2 = "P_LP_HL2"
    P_LP_HL2W = "P_LP_HL2W"
    P_LP_HL4 = "P_LP_HL4"

    # Translation booklet fulfilments
    P_TB_TBARA1 = "P_TB_TBARA1"
    P_TB_TBBEN1 = "P_TB_TBBEN1"
    P_TB_TBCAN1 = "P_TB_TBCAN1"
    P_TB_TBCAN4 = "P_TB_TBCAN4"
    P_TB_TBFRE1 = "P_TB_TBFRE1"
    P_TB_TBGUJ1 = "P_TB_TBGUJ1"
    P_TB_TBGUR1 = "P_TB_TBGUR1"
    P_TB_TBIRI4 = "P_TB_TBIRI4"
    P_TB_TBITA1 = "P_TB_TBITA1"
    P_TB_TBKUR1 = "P_TB_TBKUR1"
    P_TB_TBLIT1 = "P_TB_TBLIT1"
    P_TB_TBLIT4 = "P_TB_TBLIT4"
    P_TB_TBMAN1 = "P_TB_TBMAN1"
    P_TB_TBMAN4 = "P_TB_TBMAN4"
    P_TB_TBPOL1 = "P_TB_TBPOL1"
    P_TB_TBPOL4 = "P_TB_TBPOL4"
    P_TB_TBPOR1 = "P_TB_TBPOR1"
    P_TB_TBRUS1 = "P_TB_TBRUS1"
    P_TB_TBSOM1 = "P_TB_TBSOM1"
    P_TB_TBSPA1 = "P_TB_TBSPA1"
    P_TB_TBTUR1 = "P_TB_TBTUR1"
    P_TB_TBULS4 = "P_TB_TBULS4"
    P_TB_TBURD1 = "P_TB_TBURD1"
    P_TB_TBVIE1 = "P_TB_TBVIE1"
    P_TB_TBYSH1 = "P_TB_TBYSH1"

    P_RD_2RL1_1 = 'P_RD_2RL1_1'
    P_RD_2RL2B_1 = 'P_RD_2RL2B_1'
    P_RD_2RL1_2 = 'P_RD_2RL1_2'
    P_RD_2RL2B_2 = 'P_RD_2RL2B_2'
    P_RD_2RL1_3 = 'P_RD_2RL1_3'
    P_RD_2RL2B_3 = 'P_RD_2RL2B_3'


class Dataset(Enum):
    QM3_2 = 'QM3.2'
    QM3_3 = 'QM3.3'
    QM3_4 = 'QM3.4'
    PPD1_1 = 'PPD1.1'
    PPD1_2 = 'PPD1.2'
    PPD1_3 = 'PPD1.3'


class Supplier(Enum):
    QM = 'QM'
    PPO = 'PPO'


class PrintTemplate:
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
                           'packCode',
                           'qid',
                           'organisationName',
                           'fieldCoordinatorId',
                           'fieldOfficerId')

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
                                 'packCode',
                                 'organisationName',
                                 'fieldOfficerId')
