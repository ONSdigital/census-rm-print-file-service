from app.constants import PackCode, Dataset, Supplier, PrintTemplate, ActionType
from config import Config

PACK_CODE_TO_DESCRIPTION = {
    PackCode.P_IC_ICL1: 'Initial contact pack for English households',
    PackCode.P_IC_ICL2B: 'Initial contact pack for Welsh households',
    PackCode.P_IC_ICL4: 'ICL with UAC HH (Post Out) Addressed Northern Ireland',

    PackCode.P_IC_H1: 'Household Questionnaire for England',
    PackCode.P_IC_H2: 'Household Questionnaire for Wales',
    PackCode.P_IC_H4: 'Household Questionnaire for Northern Ireland',

    PackCode.P_OR_H1: 'Household Questionnaire for England',
    PackCode.P_OR_H2: 'Household Questionnaire for Wales (in English)',
    PackCode.P_OR_H2W: 'Household Questionnaire for Wales (in Welsh)',
    PackCode.P_OR_H4: 'Household Questionnaire for Northern Ireland (in English)',

    PackCode.P_OR_HC1: 'Household Continuation for England',
    PackCode.P_OR_HC2: 'Household Continuation for Wales (in English)',
    PackCode.P_OR_HC2W: 'Household Continuation for Wales (in Welsh)',
    PackCode.P_OR_HC4: 'Continuation Questionnaire for Northern Ireland (English)',

    PackCode.P_RL_1RL1_1: "R1a England-1st reminder, UAC first households,  haven't launched EQ - batch x",
    PackCode.P_RL_1RL2B_1: "R1a Wales-1st reminder, UAC first households,  haven't launched EQ - batch x",
    PackCode.P_RL_1RL4: "R1b NI - first reminder, haven't launched EQ",
    PackCode.P_RL_2RL4: 'R1B NI - reminder 3 letter',
    PackCode.P_RL_2RL1: "R2a England-2nd reminder, UAC first households,  haven't launched EQ - batch x",

    PackCode.P_RL_1RL1B: "RPF1 England -First reminder going to paper first households,  haven't launched EQ",
    PackCode.P_RL_1RL2BB: "RPF1 Wales -First reminder going to paper first households, haven't launched EQ",
    PackCode.P_RL_1RL4A: 'R1a NI - first reminder, have launched EQ',
    PackCode.P_RL_2RL2B: "R2a Wales- 2nd reminder, UAC first households,  haven't launched EQ - batch x",
    PackCode.P_RL_3RL1: 'R3 - England   Third reminder letter going to anyone except those getting RP1/2/3',
    PackCode.P_RL_3RL2B: 'R3 - Wales   Third reminder letter going to anyone except those getting RP1/2/3',

    PackCode.P_RD_RNP41: 'RDR1 - England   Response-driven reminder 1 going to worst performing areas',
    PackCode.P_RD_RNP42B: 'RDR1 - Wales   Response-driven reminder 1 going to worst performing areas',
    PackCode.P_RD_RNP51: 'RDR2 - England   Response-driven reminder 2 going to worst performing areas',
    PackCode.P_RD_RNP52B: 'RDR2 - Wales   Response-driven reminder 2 going to worst performing areas',

    PackCode.P_RL_1RL1A: 'RU1 England- First reminder going to those who have launched EQ',
    PackCode.P_RL_1RL2BA: 'RU1 Wales- First reminder going to those who have launched EQ',
    PackCode.P_RL_2RL1A: 'RU2 England- First reminder going to those who have launched EQ',
    PackCode.P_RL_2RL2BA: 'RU2 Wales- First reminder going to those who have launched EQ',

    PackCode.P_RL_1IRL1: 'IRL England - going to those who have requested an individual form via eQ only',
    PackCode.P_RL_1IRL2B: 'IRL Wales - going to those who have requested an individual form via eQ only',

    PackCode.P_LP_HL1: 'Household Questionnaire (Large Print) for England',
    PackCode.P_LP_HL2: 'Household Questionnaire (Large Print) for Wales (in English)',
    PackCode.P_LP_HL2W: 'Household Questionnaire (Large Print) for Wales (in Welsh)',
    PackCode.P_LP_HL4: 'Household Questionnaire (Large Print) for Northern Ireland (in English)',

    PackCode.P_LP_ILP1: 'Individual Questionnaire (Large Print) for England',
    PackCode.P_LP_ILP2: 'Individual Questionnaire (Large Print) for Wales ( in English)',
    PackCode.P_LP_ILP2W: 'Individual Questionnaire (Large Print) for Wales ( in Welsh)',
    PackCode.P_LP_IL4: 'Individual Questionnaire (Large Print) for Northern Ireland',

    PackCode.P_TB_TBALB1: 'Translation Booklet for England - Albanian',
    PackCode.P_TB_TBAMH1: 'Translation Booklet for England - Amharic',
    PackCode.P_TB_TBARA1: 'Translation Booklet for England - Arabic',
    PackCode.P_TB_TBARA2: 'Translation Booklet for Wales - Arabic',
    PackCode.P_TB_TBARA4: 'Translation Booklet for Northern Ireland - Arabic',
    PackCode.P_TB_TBARM1: 'Translation Booklet for England - Armenian',
    PackCode.P_TB_TBBEN1: 'Translation Booklet for England - Bengali',
    PackCode.P_TB_TBBEN2: 'Translation Booklet for Wales - Bengali',
    PackCode.P_TB_TBBOS1: 'Translation Booklet for England - Bosnian',
    PackCode.P_TB_TBBUL1: 'Translation Booklet for England - Bulgarian',
    PackCode.P_TB_TBBUL2: 'Translation Booklet for Wales - Bulgarian',
    PackCode.P_TB_TBBUL4: 'Translation Booklet for Northern Ireland - Bulgarian',
    PackCode.P_TB_TBBUR1: 'Translation Booklet for England - Burmese',
    PackCode.P_TB_TBCAN1: 'Translation Booklet for England - Cantonese',
    PackCode.P_TB_TBCAN2: 'Translation Booklet for Wales - Cantonese',
    PackCode.P_TB_TBCAN4: 'Translation Booklet for Northern Ireland - Cantonese',
    PackCode.P_TB_TBCZE1: 'Translation Booklet for England - Czech',
    PackCode.P_TB_TBCZE4: 'Translation Booklet for Northern Ireland - Czech',
    PackCode.P_TB_TBFAR1: 'Translation Booklet for England - Farsi',
    PackCode.P_TB_TBFAR2: 'Translation Booklet for Wales - Farsi',
    PackCode.P_TB_TBFRE1: 'Translation Booklet for England - French',
    PackCode.P_TB_TBGER1: 'Translation Booklet for England - German',
    PackCode.P_TB_TBGRE1: 'Translation Booklet for England - Greek',
    PackCode.P_TB_TBGRE2: 'Translation Booklet for Wales - Greek',
    PackCode.P_TB_TBGUJ1: 'Translation Booklet for England - Gujarati',
    PackCode.P_TB_TBPAN1: 'Translation Booklet for England - Punjabi',
    PackCode.P_TB_TBPAN2: 'Translation Booklet for Wales - Punjabi',
    PackCode.P_TB_TBHEB1: 'Translation Booklet for England - Hebrew',
    PackCode.P_TB_TBHIN1: 'Translation Booklet for England - Hindi',
    PackCode.P_TB_TBHUN1: 'Translation Booklet for England - Hungarian',
    PackCode.P_TB_TBHUN4: 'Translation Booklet for Northern Ireland - Hungarian',
    PackCode.P_TB_TBIRI4: 'Translation Booklet for Northern Ireland - Irish',
    PackCode.P_TB_TBITA1: 'Translation Booklet for England - Italian',
    PackCode.P_TB_TBITA2: 'Translation Booklet for Wales - Italian',
    PackCode.P_TB_TBJAP1: 'Translation Booklet for England - Japanese',
    PackCode.P_TB_TBKOR1: 'Translation Booklet for England - Korean',
    PackCode.P_TB_TBKUR1: 'Translation Booklet for England - Kurdish',
    PackCode.P_TB_TBKUR2: 'Translation Booklet for Wales - Kurdish',
    PackCode.P_TB_TBLAT1: 'Translation Booklet for England - Latvian',
    PackCode.P_TB_TBLAT2: 'Translation Booklet for Wales - Latvian',
    PackCode.P_TB_TBLAT4: 'Translation Booklet for Northern Ireland - Latvian',
    PackCode.P_TB_TBLIN1: 'Translation Booklet for England - Lingala',
    PackCode.P_TB_TBLIT1: 'Translation Booklet for England - Lithuanian',
    PackCode.P_TB_TBLIT4: 'Translation Booklet for Northern Ireland - Lithuanian',
    PackCode.P_TB_TBMAL1: 'Translation Booklet for England - Malayalam',
    PackCode.P_TB_TBMAL2: 'Translation Booklet for Wales - Malayalam',
    PackCode.P_TB_TBMAN1: 'Translation Booklet for England - Mandarin Chinese',
    PackCode.P_TB_TBMAN2: 'Translation Booklet for Wales - Mandarin Chinese',
    PackCode.P_TB_TBMAN4: 'Translation Booklet for Northern Ireland - Mandarin Chinese',
    PackCode.P_TB_TBNEP1: 'Translation Booklet for England - Nepali',
    PackCode.P_TB_TBPAS1: 'Translation Booklet for England - Pashto',
    PackCode.P_TB_TBPAS2: 'Translation Booklet for Wales - Pashto',
    PackCode.P_TB_TBPOL1: 'Translation Booklet for England - Polish',
    PackCode.P_TB_TBPOL2: 'Translation Booklet for Wales - Polish',
    PackCode.P_TB_TBPOL4: 'Translation Booklet for Northern Ireland - Polish',
    PackCode.P_TB_TBPOR1: 'Translation Booklet for England - Portuguese',
    PackCode.P_TB_TBPOR2: 'Translation Booklet for Wales - Portuguese',
    PackCode.P_TB_TBPOR4: 'Translation Booklet for Northern Ireland - Portuguese',
    PackCode.P_TB_TBPOT1: 'Translation Booklet for England - Potwari',
    PackCode.P_TB_TBROM1: 'Translation Booklet for England - Romanian',
    PackCode.P_TB_TBROM4: 'Translation Booklet for Northern Ireland - Romanian',
    PackCode.P_TB_TBRUS1: 'Translation Booklet for England - Russian',
    PackCode.P_TB_TBRUS2: 'Translation Booklet for Wales - Russian',
    PackCode.P_TB_TBRUS4: 'Translation Booklet for Northern Ireland - Russian',
    PackCode.P_TB_TBSLE1: 'Translation Booklet for England - Slovenian',
    PackCode.P_TB_TBSLO1: 'Translation Booklet for England - Slovakian',
    PackCode.P_TB_TBSLO4: 'Translation Booklet for Northern Ireland - Slovakian',
    PackCode.P_TB_TBSOM1: 'Translation Booklet for England - Somali',
    PackCode.P_TB_TBSOM4: 'Translation Booklet for Northern Ireland - Somali',
    PackCode.P_TB_TBSPA1: 'Translation Booklet for England - Spanish',
    PackCode.P_TB_TBSPA2: 'Translation Booklet for Wales - Spanish',
    PackCode.P_TB_TBSWA1: 'Translation Booklet for England - Swahili',
    PackCode.P_TB_TBSWA2: 'Translation Booklet for Wales - Swahili',
    PackCode.P_TB_TBTAG1: 'Translation Booklet for England - Tagalog',
    PackCode.P_TB_TBTAM1: 'Translation Booklet for England - Tamil',
    PackCode.P_TB_TBTHA1: 'Translation Booklet for England - Thai',
    PackCode.P_TB_TBTHA2: 'Translation Booklet for Wales - Thai',
    PackCode.P_TB_TBTET4: 'Translation Booklet for Northern Ireland - Tetum',
    PackCode.P_TB_TBTIG1: 'Translation Booklet for England - Tigrinya',
    PackCode.P_TB_TBTUR1: 'Translation Booklet for England - Turkish',
    PackCode.P_TB_TBUKR1: 'Translation Booklet for England - Ukrainian',
    PackCode.P_TB_TBULS4: 'Translation Booklet for Northern Ireland - Ulster-Scots',
    PackCode.P_TB_TBURD1: 'Translation Booklet for England - Urdu',
    PackCode.P_TB_TBVIE1: 'Translation Booklet for England - Vietnamese',
    PackCode.P_TB_TBYSH1: 'Translation Booklet for England - Yiddish',

    PackCode.P_OR_I1: 'Individual Questionnaire for England',
    PackCode.P_OR_I2: 'Individual Questionnaire for Wales (in English)',
    PackCode.P_OR_I2W: 'Individual Questionnaire for Wales (in Welsh)',
    PackCode.P_OR_I4: 'Individual Questionnaire for Northern Ireland (in English)',

    PackCode.P_QU_H1: 'RP1 - England Paper questionnaire going to HtC willingness 4&5',
    PackCode.P_QU_H2: 'RP1 - Wales Paper questionnaire going to HtC willingness 4&5',
    PackCode.P_QU_H4: 'Reminder 2 NI PQ',

    PackCode.D_CE1A_ICLCR1: 'CE1 Packs (Hand Delivery) Addressed England',
    PackCode.D_CE1A_ICLCR2B: 'CE1 Packs (Hand Delivery) Addressed Wales',
    PackCode.D_ICA_ICLR1: 'ICL with UAC Individual (Hand Delivery)  Addressed England',
    PackCode.D_ICA_ICLR2B: 'ICL with UAC Individual (Hand Delivery) Addressed Wales',
    PackCode.D_CE4A_ICLR4: 'ICL with UAC Individual Resident (Hand Delivery) Addressed',
    PackCode.D_CE4A_ICLS4: 'ICL with UAC Individual Student (Hand Delivery) Addressed',

    PackCode.P_ICCE_ICL1: 'ICL with UAC HH (Post Out) Addressed England',
    PackCode.P_ICCE_ICL2B: 'ICL with UAC HH (Post Out) Addressed Wales',

    PackCode.D_FDCE_I4: 'Individual Questionnaire for NI (Hand delivery) Addressed',
    PackCode.D_FDCE_I1: 'Individual Questionnaire for England (Hand delivery) Addressed',
    PackCode.D_FDCE_I2: 'Individual Questionnaire for Wales (Hand delivery) Addressed',
    PackCode.D_FDCE_H1: 'Household Questionnaire for England (Hand delivery) Addressed',
    PackCode.D_FDCE_H2: 'Household Questionnaire for Wales (Hand delivery) Addressed',

    PackCode.P_UAC_UACHHP1: 'Household Unique Access Code for England via paper',
    PackCode.P_UAC_UACHHP2B: 'Household Unique Access Code for Wales (English/Welsh - Bilingual) via paper',
    PackCode.P_UAC_UACHHP4: 'Household Unique Access Code for Northern Ireland via paper',

    PackCode.P_ER_ILER1: 'Information leaflet (Easy Read) for England',
    PackCode.P_ER_ILER2B: 'Information leaflet (Easy Read) for Wales (English/Welsh - Bilingual)',

    PackCode.P_UAC_UACIP1: 'Individual Unique Access Code for England via paper',
    PackCode.P_UAC_UACIP2B: 'Individual Unique Access Code for Wales (English/Welsh - Bilingual) via paper',
    PackCode.P_UAC_UACIP4: 'Individual Unique Access Code for Northern Ireland via paper',
    PackCode.P_UAC_UACIPA1: 'Individual Unique Access Code for England via paper - Request from EQ',
    PackCode.P_UAC_UACIPA2B: 'Individual Unique Access Code for Wales (English/Welsh - Bilingual) via paper - Request'
                             ' from EQ',
    PackCode.P_UAC_UACIPA4: 'Individual Unique Access Code for Northern Ireland via paper - Request from EQ',

    PackCode.P_UAC_UACCEP1: 'UAC provided to Communal Establishment manager in England via paper',
    PackCode.P_UAC_UACCEP2B: 'UAC provided to Communal Establishment manager in Wales via paper (Bilingual)',

    PackCode.P_NC_NCLTA1: 'Non Compliance Warning Letter 1 England',
    PackCode.P_NC_NCLTA2B: 'Non Compliance Warning Letter 1 Wales'
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
    PackCode.P_OR_HC1: Dataset.QM3_4,
    PackCode.P_OR_HC2: Dataset.QM3_4,
    PackCode.P_OR_HC2W: Dataset.QM3_4,
    PackCode.P_OR_HC4: Dataset.QM3_4,

    PackCode.P_RL_1RL1_1: Dataset.PPD1_2,
    PackCode.P_RL_1RL2B_1: Dataset.PPD1_2,
    PackCode.P_RL_1RL1A: Dataset.PPD1_2,
    PackCode.P_RL_1RL2BA: Dataset.PPD1_2,
    PackCode.P_RL_2RL1A: Dataset.PPD1_2,
    PackCode.P_RL_2RL2B: Dataset.PPD1_2,
    PackCode.P_RL_2RL2BA: Dataset.PPD1_2,
    PackCode.P_RL_1RL4: Dataset.PPD1_2,

    PackCode.P_RL_2RL1: Dataset.PPD1_2,
    PackCode.P_RL_2RL4: Dataset.PPD1_2,
    PackCode.P_RL_3RL1: Dataset.PPD1_2,
    PackCode.P_RL_3RL2B: Dataset.PPD1_2,

    PackCode.P_RD_RNP41: Dataset.PPD1_2,
    PackCode.P_RD_RNP42B: Dataset.PPD1_2,
    PackCode.P_RD_RNP51: Dataset.PPD1_2,
    PackCode.P_RD_RNP52B: Dataset.PPD1_2,

    PackCode.P_RL_1RL1B: Dataset.PPD1_2,
    PackCode.P_RL_1RL2BB: Dataset.PPD1_2,
    PackCode.P_RL_1RL4A: Dataset.PPD1_2,

    PackCode.P_RL_1IRL1: Dataset.PPD1_2,
    PackCode.P_RL_1IRL2B: Dataset.PPD1_2,

    PackCode.P_LP_HL1: Dataset.PPD1_3,
    PackCode.P_LP_HL2: Dataset.PPD1_3,
    PackCode.P_LP_HL2W: Dataset.PPD1_3,
    PackCode.P_LP_HL4: Dataset.PPD1_3,

    PackCode.P_LP_ILP1: Dataset.PPD1_3,
    PackCode.P_LP_ILP2: Dataset.PPD1_3,
    PackCode.P_LP_ILP2W: Dataset.PPD1_3,
    PackCode.P_LP_IL4: Dataset.PPD1_3,

    PackCode.P_TB_TBALB1: Dataset.PPD1_3,
    PackCode.P_TB_TBAMH1: Dataset.PPD1_3,
    PackCode.P_TB_TBARA1: Dataset.PPD1_3,
    PackCode.P_TB_TBARA2: Dataset.PPD1_3,
    PackCode.P_TB_TBARA4: Dataset.PPD1_3,
    PackCode.P_TB_TBARM1: Dataset.PPD1_3,
    PackCode.P_TB_TBBEN1: Dataset.PPD1_3,
    PackCode.P_TB_TBBEN2: Dataset.PPD1_3,
    PackCode.P_TB_TBBOS1: Dataset.PPD1_3,
    PackCode.P_TB_TBBUL1: Dataset.PPD1_3,
    PackCode.P_TB_TBBUL2: Dataset.PPD1_3,
    PackCode.P_TB_TBBUL4: Dataset.PPD1_3,
    PackCode.P_TB_TBBUR1: Dataset.PPD1_3,
    PackCode.P_TB_TBCAN1: Dataset.PPD1_3,
    PackCode.P_TB_TBCAN2: Dataset.PPD1_3,
    PackCode.P_TB_TBCAN4: Dataset.PPD1_3,
    PackCode.P_TB_TBCZE1: Dataset.PPD1_3,
    PackCode.P_TB_TBCZE4: Dataset.PPD1_3,
    PackCode.P_TB_TBFAR1: Dataset.PPD1_3,
    PackCode.P_TB_TBFAR2: Dataset.PPD1_3,
    PackCode.P_TB_TBFRE1: Dataset.PPD1_3,
    PackCode.P_TB_TBGER1: Dataset.PPD1_3,
    PackCode.P_TB_TBGRE1: Dataset.PPD1_3,
    PackCode.P_TB_TBGRE2: Dataset.PPD1_3,
    PackCode.P_TB_TBGUJ1: Dataset.PPD1_3,
    PackCode.P_TB_TBPAN1: Dataset.PPD1_3,
    PackCode.P_TB_TBPAN2: Dataset.PPD1_3,
    PackCode.P_TB_TBHEB1: Dataset.PPD1_3,
    PackCode.P_TB_TBHIN1: Dataset.PPD1_3,
    PackCode.P_TB_TBHUN1: Dataset.PPD1_3,
    PackCode.P_TB_TBHUN4: Dataset.PPD1_3,
    PackCode.P_TB_TBIRI4: Dataset.PPD1_3,
    PackCode.P_TB_TBITA1: Dataset.PPD1_3,
    PackCode.P_TB_TBITA2: Dataset.PPD1_3,
    PackCode.P_TB_TBJAP1: Dataset.PPD1_3,
    PackCode.P_TB_TBKOR1: Dataset.PPD1_3,
    PackCode.P_TB_TBKUR1: Dataset.PPD1_3,
    PackCode.P_TB_TBKUR2: Dataset.PPD1_3,
    PackCode.P_TB_TBLAT1: Dataset.PPD1_3,
    PackCode.P_TB_TBLAT2: Dataset.PPD1_3,
    PackCode.P_TB_TBLAT4: Dataset.PPD1_3,
    PackCode.P_TB_TBLIN1: Dataset.PPD1_3,
    PackCode.P_TB_TBLIT1: Dataset.PPD1_3,
    PackCode.P_TB_TBLIT4: Dataset.PPD1_3,
    PackCode.P_TB_TBMAL1: Dataset.PPD1_3,
    PackCode.P_TB_TBMAL2: Dataset.PPD1_3,
    PackCode.P_TB_TBMAN1: Dataset.PPD1_3,
    PackCode.P_TB_TBMAN2: Dataset.PPD1_3,
    PackCode.P_TB_TBMAN4: Dataset.PPD1_3,
    PackCode.P_TB_TBNEP1: Dataset.PPD1_3,
    PackCode.P_TB_TBPAS1: Dataset.PPD1_3,
    PackCode.P_TB_TBPAS2: Dataset.PPD1_3,
    PackCode.P_TB_TBPOL1: Dataset.PPD1_3,
    PackCode.P_TB_TBPOL2: Dataset.PPD1_3,
    PackCode.P_TB_TBPOL4: Dataset.PPD1_3,
    PackCode.P_TB_TBPOR1: Dataset.PPD1_3,
    PackCode.P_TB_TBPOR2: Dataset.PPD1_3,
    PackCode.P_TB_TBPOR4: Dataset.PPD1_3,
    PackCode.P_TB_TBPOT1: Dataset.PPD1_3,
    PackCode.P_TB_TBROM1: Dataset.PPD1_3,
    PackCode.P_TB_TBROM4: Dataset.PPD1_3,
    PackCode.P_TB_TBRUS1: Dataset.PPD1_3,
    PackCode.P_TB_TBRUS2: Dataset.PPD1_3,
    PackCode.P_TB_TBRUS4: Dataset.PPD1_3,
    PackCode.P_TB_TBSLE1: Dataset.PPD1_3,
    PackCode.P_TB_TBSLO1: Dataset.PPD1_3,
    PackCode.P_TB_TBSLO4: Dataset.PPD1_3,
    PackCode.P_TB_TBSOM1: Dataset.PPD1_3,
    PackCode.P_TB_TBSOM4: Dataset.PPD1_3,
    PackCode.P_TB_TBSPA1: Dataset.PPD1_3,
    PackCode.P_TB_TBSPA2: Dataset.PPD1_3,
    PackCode.P_TB_TBSWA1: Dataset.PPD1_3,
    PackCode.P_TB_TBSWA2: Dataset.PPD1_3,
    PackCode.P_TB_TBTAG1: Dataset.PPD1_3,
    PackCode.P_TB_TBTAM1: Dataset.PPD1_3,
    PackCode.P_TB_TBTHA1: Dataset.PPD1_3,
    PackCode.P_TB_TBTHA2: Dataset.PPD1_3,
    PackCode.P_TB_TBTET4: Dataset.PPD1_3,
    PackCode.P_TB_TBTIG1: Dataset.PPD1_3,
    PackCode.P_TB_TBTUR1: Dataset.PPD1_3,
    PackCode.P_TB_TBUKR1: Dataset.PPD1_3,
    PackCode.P_TB_TBULS4: Dataset.PPD1_3,
    PackCode.P_TB_TBURD1: Dataset.PPD1_3,
    PackCode.P_TB_TBVIE1: Dataset.PPD1_3,
    PackCode.P_TB_TBYSH1: Dataset.PPD1_3,

    PackCode.P_ER_ILER1: Dataset.PPD1_3,
    PackCode.P_ER_ILER2B: Dataset.PPD1_3,

    PackCode.P_OR_I1: Dataset.QM3_4,
    PackCode.P_OR_I2: Dataset.QM3_4,
    PackCode.P_OR_I2W: Dataset.QM3_4,
    PackCode.P_OR_I4: Dataset.QM3_4,

    PackCode.P_QU_H1: Dataset.QM3_3,
    PackCode.P_QU_H2: Dataset.QM3_3,
    PackCode.P_QU_H4: Dataset.QM3_3,

    PackCode.D_CE1A_ICLCR1: Dataset.PPD1_7,
    PackCode.D_CE1A_ICLCR2B: Dataset.PPD1_7,
    PackCode.D_ICA_ICLR1: Dataset.PPD1_7,
    PackCode.D_ICA_ICLR2B: Dataset.PPD1_7,
    PackCode.D_CE4A_ICLR4: Dataset.PPD1_7,
    PackCode.D_CE4A_ICLS4: Dataset.PPD1_7,
    PackCode.P_ICCE_ICL1: Dataset.PPD1_7,
    PackCode.P_ICCE_ICL2B: Dataset.PPD1_7,

    PackCode.D_FDCE_I4: Dataset.QM3_2,
    PackCode.D_FDCE_I1: Dataset.QM3_2,
    PackCode.D_FDCE_I2: Dataset.QM3_2,
    PackCode.D_FDCE_H1: Dataset.QM3_2,
    PackCode.D_FDCE_H2: Dataset.QM3_2,

    PackCode.P_UAC_UACHHP1: Dataset.PPD1_3,
    PackCode.P_UAC_UACHHP2B: Dataset.PPD1_3,
    PackCode.P_UAC_UACHHP4: Dataset.PPD1_3,
    PackCode.P_UAC_UACIP1: Dataset.PPD1_3,
    PackCode.P_UAC_UACIP2B: Dataset.PPD1_3,
    PackCode.P_UAC_UACIP4: Dataset.PPD1_3,
    PackCode.P_UAC_UACIPA1: Dataset.PPD1_3,
    PackCode.P_UAC_UACIPA2B: Dataset.PPD1_3,
    PackCode.P_UAC_UACIPA4: Dataset.PPD1_3,
    PackCode.P_UAC_UACCEP1: Dataset.PPD1_3,
    PackCode.P_UAC_UACCEP2B: Dataset.PPD1_3,

    PackCode.P_NC_NCLTA1: Dataset.PPD1_8,
    PackCode.P_NC_NCLTA2B: Dataset.PPD1_8,
}

DATASET_TO_SUPPLIER = {
    Dataset.QM3_2: Supplier.QM,
    Dataset.QM3_3: Supplier.QM,
    Dataset.QM3_4: Supplier.QM,
    Dataset.PPD1_1: Supplier.PPO,  # Initial Contact Letter Addresses
    Dataset.PPD1_2: Supplier.PPO,  # Reminder Letter Addresses
    Dataset.PPD1_3: Supplier.PPO,  # Fulfilment Request for Supplementary Printed Materials
    Dataset.PPD1_6: Supplier.PPO,  # Unaddressed Initial Contact Materials
    Dataset.PPD1_7: Supplier.PPO,  # Initial Contact Addresses (CE/SPG)
    Dataset.PPD1_8: Supplier.PPO  # Non Compliance Letter Addresses
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

    ActionType.P_RL_1RL1_1: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL4: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL2B_1: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL1A: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL2BA: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_2RL1A: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_2RL2BA: PrintTemplate.PPO_LETTER_TEMPLATE,

    ActionType.P_RL_2RL1: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_2RL4: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_2RL2B: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_3RL1: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_3RL2B: PrintTemplate.PPO_LETTER_TEMPLATE,

    ActionType.P_RD_RNP41: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RD_RNP42B: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RD_RNP51: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RD_RNP52B: PrintTemplate.PPO_LETTER_TEMPLATE,

    ActionType.P_RL_1RL1B: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL2BB: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1RL4A: PrintTemplate.PPO_LETTER_TEMPLATE,

    ActionType.P_RL_1IRL1: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_RL_1IRL2B: PrintTemplate.PPO_LETTER_TEMPLATE,

    ActionType.P_QU_H1: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.P_QU_H2: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.P_QU_H4: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,

    ActionType.CE1_IC01: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.CE1_IC02: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.CE_IC03: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.CE_IC04: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.CE_IC05: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.CE_IC06: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.CE_IC08: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.CE_IC09: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.CE_IC10: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,

    ActionType.SPG_IC11: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.SPG_IC12: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.SPG_IC13: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.SPG_IC14: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,

    ActionType.P_LP_HLX: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_LP_ILX: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_OR_IX: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.P_TB_TBX: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_UAC_HX: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_ER_IL: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_UAC_IX: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_OR_HX: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
    ActionType.P_UAC_CX: PrintTemplate.PPO_LETTER_TEMPLATE,

    ActionType.P_NC_NCLTA1: PrintTemplate.PPO_LETTER_TEMPLATE,
    ActionType.P_NC_NCLTA2B: PrintTemplate.PPO_LETTER_TEMPLATE,
}

SUPPLIER_TO_PRINT_TEMPLATE = {
    Supplier.PPO: PrintTemplate.PPO_LETTER_TEMPLATE,
    Supplier.QM: PrintTemplate.QM_QUESTIONNAIRE_TEMPLATE,
}
