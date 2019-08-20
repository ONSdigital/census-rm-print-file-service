from enum import Enum


class ActionType(Enum):
    ICL1E = 'ICL1E'
    ICL2W = 'ICL2W'
    ICL4N = 'ICL4N'
    ICHHQE = 'ICHHQE'
    ICHHQW = 'ICHHQW'
    ICHHQN = 'ICHHQN'
    P_OR_HX = 'P_OR_HX'
    P_RL_1RL1_1 = 'P_RL_1RL1_1'
    P_RL_1RL2B_1 = 'P_RL_1RL2B_1'
    P_RL_1RL4 = 'P_RL_1RL4'
    P_RL_1RL1_2 = 'P_RL_1RL1_2'
    P_RL_1RL2B_2 = 'P_RL_1RL2B_2'
    P_RL_2RL1_3a = 'P_RL_2RL1_3a'
    P_RL_2RL2B_3a = 'P_RL_2RL2B_3a'


class PackCode(Enum):
    P_IC_ICL1 = 'P_IC_ICL1'
    P_IC_ICL2B = 'P_IC_ICL2B'
    P_IC_ICL4 = 'P_IC_ICL4'
    P_IC_H1 = 'P_IC_H1'
    P_IC_H2 = 'P_IC_H2'
    P_IC_H4 = 'P_IC_H4'
    P_OR_H1 = 'P_OR_H1'
    P_OR_H2 = 'P_OR_H2'
    P_OR_H2W = 'P_OR_H2W'
    P_OR_H4 = 'P_OR_H4'
    P_RL_1RL1_1 = 'P_RL_1RL1_1'
    P_RL_1RL2B_1 = 'P_RL_1RL2B_1'
    P_RL_1RL4 = 'P_RL_1RL4'
    P_RL_1RL1_2 = 'P_RL_1RL1_2'
    P_RL_1RL2B_2 = 'P_RL_1RL2B_2'
    P_RL_2RL1_3a = 'P_RL_2RL1_3a'
    P_RL_2RL2B_3a = 'P_RL_2RL2B_3a'


class Dataset(Enum):
    QM3_2 = 'QM3.2'
    QM3_4 = 'QM3.4'
    PPD1_1 = 'PPD1.1'
    PPD1_2 = 'PPD1.2'


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
