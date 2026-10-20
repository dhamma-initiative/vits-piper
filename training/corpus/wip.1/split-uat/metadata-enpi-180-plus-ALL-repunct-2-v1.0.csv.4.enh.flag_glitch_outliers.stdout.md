======================================================================
      SUTTAPLAYER PĀLI AUDIO QA: GLITCH OUTLIER DETECTOR             
======================================================================
📂 QA Report Input  : ./build.wip.1/4.enh/metadata/report_qa_analytics.csv
🎯 Density Threshold: 2.50 glitches / sec
======================================================================

📊 Summary Analytics:
  • Total files analyzed       : 1154
  • Flagged outliers (≥ 2.50/s) : 17 (1.5%)
  • Mean glitch density (corpus): 1.327 glitches/sec
  • Max glitch density observed : 3.636 glitches/sec

--- TOP FLAGGED OUTLIERS FOR RE-SYNTHESIS ---
            file_name  duration_s  f0_glitch_jumps  glitches_per_sec
   AN_AN3_42_0005.wav        1.65                6          3.636364
   SN_SN44_1_0018.wav        1.99                7          3.517588
  SN_SN22_80_0030.wav        1.15                4          3.478261
   SN_SN21_8_0005.wav        2.06                7          3.398058
   SN_SN21_1_0013.wav        4.77               15          3.144654
 KN_Khp_khp7_0011.wav        4.65               14          3.010753
KN_Iti_iti78_0003.wav        5.35               16          2.990654
   AN_AN6_63_0099.wav        4.04               12          2.970297
    SN_SN6_2_0029.wav        2.42                7          2.892562
  AN_AN10_92_0013.wav        5.14               14          2.723735
   SN_SN21_9_0006.wav        1.85                5          2.702703
  SN_SN22_95_0034.wav        2.96                8          2.702703
KN_Iti_iti79_0009.wav        3.14                8          2.547771
  AN_AN5_162_0010.wav        2.36                6          2.542373
  AN_AN3_103_0014.wav        5.12               13          2.539062
  SN_SN22_55_0022.wav       11.43               29          2.537183
   AN_AN4_99_0012.wav        6.32               16          2.531646

✅ Saved flagged outlier list (17 rows) to:
   ./build.wip.1/4.enh/metadata/flag_glitch_outliers.csv
