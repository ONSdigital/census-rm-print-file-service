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

    # Individual addressed initial contact letters CE (Northern Ireland)
    CE_IC05 = 'CE_IC05'
    CE_IC06 = 'CE_IC06'

    # Initial contact individual CE questionnaire
    CE_IC08 = 'CE_IC08'
    CE_IC09 = 'CE_IC09'
    CE_IC10 = 'CE_IC10'

    # Initial contact letters for SPGs
    SPG_IC11 = 'SPG_IC11'
    SPG_IC12 = 'SPG_IC12'

    # Initial contact SPG questionnaires
    SPG_IC13 = 'SPG_IC13'
    SPG_IC14 = 'SPG_IC14'

    # Initial contact household questionnaires
    ICHHQE = 'ICHHQE'
    ICHHQW = 'ICHHQW'
    ICHHQN = 'ICHHQN'

    # On request questionnaire fulfilments
    P_OR_HX = 'P_OR_HX'

    # On request individual fulfilment questionnaires
    P_OR_IX = 'P_OR_IX'

    # Large print fulfilments Household questionnaire fulfilments
    P_LP_HLX = 'P_LP_HLX'

    # Large print individual questionnaire fulfilments
    P_LP_ILX = 'P_LP_ILX'

    # Translation booklet fulfilments
    P_TB_TBX = 'P_TB_TBX'

    # Individual UAC print fulfilments
    P_UAC_IX = 'P_UAC_IX'

    # Reminder letters
    P_RL_1RL1_1 = 'P_RL_1RL1_1'
    P_RL_1RL2B_1 = 'P_RL_1RL2B_1'
    P_RL_1RL4 = 'P_RL_1RL4'
    P_RL_1RL1_2 = 'P_RL_1RL1_2'
    P_RL_1RL2B_2 = 'P_RL_1RL2B_2'
    P_RL_2RL1 = 'P_RL_2RL1'
    P_RL_2RL2B = 'P_RL_2RL2B'
    P_RL_2RL1_3a = 'P_RL_2RL1_3a'
    P_RL_2RL2B_3a = 'P_RL_2RL2B_3a'

    # Reminder letters for paper first households
    P_RL_1RL1B = 'P_RL_1RL1B'
    P_RL_1RL2BB = 'P_RL_1RL2BB'
    P_RL_1RL4A = 'P_RL_1RL4A'
    P_RL_2RL4 = 'P_RL_2RL4'
    P_RL_3RL1 = 'P_RL_3RL1'
    P_RL_3RL2B = 'P_RL_3RL2B'

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

    # Response driven reminders, for RH launched surveys
    P_RL_1RL1A = 'P_RL_1RL1A'
    P_RL_1RL2BA = 'P_RL_1RL2BA'
    P_RL_2RL1A = 'P_RL_2RL1A'
    P_RL_2RL2BA = 'P_RL_2RL2BA'

    # Individual response reminders
    P_RL_1IRL1 = 'P_RL_1IRL1'
    P_RL_1IRL2B = 'P_RL_1IRL2B'

    # Household Unique Access Codes via paper
    P_UAC_HX = 'P_UAC_HX'

    # Information leaflet
    P_ER_IL = 'P_ER_IL'


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
    D_CE4A_ICLR4 = 'D_CE4A_ICLR4'
    D_CE4A_ICLS4 = 'D_CE4A_ICLS4'

    # Initial contact individual questionnaires
    D_FDCE_I4 = 'D_FDCE_I4'
    D_FDCE_I1 = 'D_FDCE_I1'
    D_FDCE_I2 = 'D_FDCE_I2'

    # Initial contact letters for SPGs
    P_ICCE_ICL1 = 'P_ICCE_ICL1'
    P_ICCE_ICL2B = 'P_ICCE_ICL2B'

    # Initial contact SPG questionnaires
    D_FDCE_H1 = 'D_FDCE_H1'
    D_FDCE_H2 = 'D_FDCE_H2'

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
    P_RL_2RL1 = 'P_RL_2RL1'
    P_RL_2RL2B = 'P_RL_2RL2B'
    P_RL_2RL1_3a = 'P_RL_2RL1_3a'
    P_RL_2RL2B_3a = 'P_RL_2RL2B_3a'

    P_RL_2RL4 = 'P_RL_2RL4'
    P_RL_3RL1 = 'P_RL_3RL1'
    P_RL_3RL2B = 'P_RL_3RL2B'

    # Reminder letters for paper first households
    P_RL_1RL1B = 'P_RL_1RL1B'
    P_RL_1RL2BB = 'P_RL_1RL2BB'
    P_RL_1RL4A = 'P_RL_1RL4A'

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

    # Individual UAC print fulfilments
    P_UAC_UACIP1 = 'P_UAC_UACIP1'
    P_UAC_UACIP2B = 'P_UAC_UACIP2B'
    P_UAC_UACIP4 = 'P_UAC_UACIP4'

    # Large print Household questionnaire fulfilments
    P_LP_HL1 = "P_LP_HL1"
    P_LP_HL2 = "P_LP_HL2"
    P_LP_HL2W = "P_LP_HL2W"
    P_LP_HL4 = "P_LP_HL4"

    # Large print individual questionnaire fulfilments
    P_LP_ILP1 = "P_LP_ILP1"
    P_LP_ILP2 = "P_LP_ILP2"
    P_LP_ILP2W = "P_LP_ILP2W"
    P_LP_IL4 = "P_LP_IL4"

    # Translation booklet fulfilments
    P_TB_TBALB1 = "P_TB_TBALB1"
    P_TB_TBAMH1 = "P_TB_TBAMH1"
    P_TB_TBARA1 = "P_TB_TBARA1"
    P_TB_TBARA2 = "P_TB_TBARA2"
    P_TB_TBARA4 = "P_TB_TBARA4"
    P_TB_TBARM1 = "P_TB_TBARM1"
    P_TB_TBBEN1 = "P_TB_TBBEN1"
    P_TB_TBBEN2 = "P_TB_TBBEN2"
    P_TB_TBBOS1 = "P_TB_TBBOS1"
    P_TB_TBBUL1 = "P_TB_TBBUL1"
    P_TB_TBBUL2 = "P_TB_TBBUL2"
    P_TB_TBBUL4 = "P_TB_TBBUL4"
    P_TB_TBBUR1 = "P_TB_TBBUR1"
    P_TB_TBCAN1 = "P_TB_TBCAN1"
    P_TB_TBCAN2 = "P_TB_TBCAN2"
    P_TB_TBCAN4 = "P_TB_TBCAN4"
    P_TB_TBCZE1 = "P_TB_TBCZE1"
    P_TB_TBCZE4 = "P_TB_TBCZE4"
    P_TB_TBFAR1 = "P_TB_TBFAR1"
    P_TB_TBFAR2 = "P_TB_TBFAR2"
    P_TB_TBFRE1 = "P_TB_TBFRE1"
    P_TB_TBGER1 = "P_TB_TBGER1"
    P_TB_TBGRE1 = "P_TB_TBGRE1"
    P_TB_TBGRE2 = "P_TB_TBGRE2"
    P_TB_TBGUJ1 = "P_TB_TBGUJ1"
    P_TB_TBPAN1 = "P_TB_TBPAN1"
    P_TB_TBPAN2 = "P_TB_TBPAN2"
    P_TB_TBHEB1 = "P_TB_TBHEB1"
    P_TB_TBHIN1 = "P_TB_TBHIN1"
    P_TB_TBHUN1 = "P_TB_TBHUN1"
    P_TB_TBHUN4 = "P_TB_TBHUN4"
    P_TB_TBIRI4 = "P_TB_TBIRI4"
    P_TB_TBITA1 = "P_TB_TBITA1"
    P_TB_TBITA2 = "P_TB_TBITA2"
    P_TB_TBJAP1 = "P_TB_TBJAP1"
    P_TB_TBKOR1 = "P_TB_TBKOR1"
    P_TB_TBKUR1 = "P_TB_TBKUR1"
    P_TB_TBKUR2 = "P_TB_TBKUR2"
    P_TB_TBLAT1 = "P_TB_TBLAT1"
    P_TB_TBLAT2 = "P_TB_TBLAT2"
    P_TB_TBLAT4 = "P_TB_TBLAT4"
    P_TB_TBLIN1 = "P_TB_TBLIN1"
    P_TB_TBLIT1 = "P_TB_TBLIT1"
    P_TB_TBLIT4 = "P_TB_TBLIT4"
    P_TB_TBMAL1 = "P_TB_TBMAL1"
    P_TB_TBMAL2 = "P_TB_TBMAL2"
    P_TB_TBMAN1 = "P_TB_TBMAN1"
    P_TB_TBMAN2 = "P_TB_TBMAN2"
    P_TB_TBMAN4 = "P_TB_TBMAN4"
    P_TB_TBNEP1 = "P_TB_TBNEP1"
    P_TB_TBPAS1 = "P_TB_TBPAS1"
    P_TB_TBPAS2 = "P_TB_TBPAS2"
    P_TB_TBPOL1 = "P_TB_TBPOL1"
    P_TB_TBPOL2 = "P_TB_TBPOL2"
    P_TB_TBPOL4 = "P_TB_TBPOL4"
    P_TB_TBPOR1 = "P_TB_TBPOR1"
    P_TB_TBPOR2 = "P_TB_TBPOR2"
    P_TB_TBPOR4 = "P_TB_TBPOR4"
    P_TB_TBPOT1 = "P_TB_TBPOT1"
    P_TB_TBROM1 = "P_TB_TBROM1"
    P_TB_TBROM4 = "P_TB_TBROM4"
    P_TB_TBRUS1 = "P_TB_TBRUS1"
    P_TB_TBRUS2 = "P_TB_TBRUS2"
    P_TB_TBRUS4 = "P_TB_TBRUS4"
    P_TB_TBSLE1 = "P_TB_TBSLE1"
    P_TB_TBSLO1 = "P_TB_TBSLO1"
    P_TB_TBSLO4 = "P_TB_TBSLO4"
    P_TB_TBSOM1 = "P_TB_TBSOM1"
    P_TB_TBSOM4 = "P_TB_TBSOM4"
    P_TB_TBSPA1 = "P_TB_TBSPA1"
    P_TB_TBSPA2 = "P_TB_TBSPA2"
    P_TB_TBSWA1 = "P_TB_TBSWA1"
    P_TB_TBSWA2 = "P_TB_TBSWA2"
    P_TB_TBTAG1 = "P_TB_TBTAG1"
    P_TB_TBTAM1 = "P_TB_TBTAM1"
    P_TB_TBTHA1 = "P_TB_TBTHA1"
    P_TB_TBTHA2 = "P_TB_TBTHA2"
    P_TB_TBTET4 = "P_TB_TBTET4"
    P_TB_TBTIG1 = "P_TB_TBTIG1"
    P_TB_TBTUR1 = "P_TB_TBTUR1"
    P_TB_TBUKR1 = "P_TB_TBUKR1"
    P_TB_TBULS4 = "P_TB_TBULS4"
    P_TB_TBURD1 = "P_TB_TBURD1"
    P_TB_TBVIE1 = "P_TB_TBVIE1"
    P_TB_TBYSH1 = "P_TB_TBYSH1"

    # Reminders
    P_RD_2RL1_1 = 'P_RD_2RL1_1'
    P_RD_2RL2B_1 = 'P_RD_2RL2B_1'
    P_RD_2RL1_2 = 'P_RD_2RL1_2'
    P_RD_2RL2B_2 = 'P_RD_2RL2B_2'
    P_RD_2RL1_3 = 'P_RD_2RL1_3'
    P_RD_2RL2B_3 = 'P_RD_2RL2B_3'

    # Reminders for survey already started
    P_RL_1RL1A = 'P_RL_1RL1A'
    P_RL_1RL2BA = 'P_RL_1RL2BA'
    P_RL_2RL1A = 'P_RL_2RL1A'
    P_RL_2RL2BA = 'P_RL_2RL2BA'

    # Individual response reminders
    P_RL_1IRL1 = 'P_RL_1IRL1'
    P_RL_1IRL2B = 'P_RL_1IRL2B'

    # Household Unique Access Codes via paper
    P_UAC_UACHHP1 = 'P_UAC_UACHHP1'
    P_UAC_UACHHP2B = 'P_UAC_UACHHP2B'
    P_UAC_UACHHP4 = 'P_UAC_UACHHP4'

    # Information leaflet
    P_ER_ILER1 = 'P_ER_ILER1'
    P_ER_ILER2B = 'P_ER_ILER2B'


class Dataset(Enum):
    QM3_2 = 'QM3.2'
    QM3_3 = 'QM3.3'
    QM3_4 = 'QM3.4'
    PPD1_1 = 'PPD1.1'
    PPD1_2 = 'PPD1.2'
    PPD1_3 = 'PPD1.3'
    PPD1_6 = 'PPD1.6'
    PPD1_7 = 'PPD1.7'
    PPD1_8 = 'PPD1.8'


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


class PrintFileSorting:
    SORTING_KEY = ['fieldOfficerId', 'organisationName']
    PACKCODES_TO_SORT = {PackCode.D_CE1A_ICLCR1, PackCode.D_CE1A_ICLCR2B, PackCode.D_ICA_ICLR1, PackCode.D_ICA_ICLR1,
                         PackCode.D_ICA_ICLR2B, PackCode.D_ICA_ICLR2B, PackCode.D_FDCE_I1, PackCode.D_FDCE_I2,
                         PackCode.D_FDCE_I4, PackCode.D_CE4A_ICLR4, PackCode.D_CE4A_ICLS4,
                         PackCode.D_FDCE_H1, PackCode.D_FDCE_H2}
