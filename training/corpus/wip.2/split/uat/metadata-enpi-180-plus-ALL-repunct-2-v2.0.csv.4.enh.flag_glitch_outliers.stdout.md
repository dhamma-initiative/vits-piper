======================================================================
      SUTTAPLAYER PĀLI AUDIO QA: GLITCH OUTLIER DETECTOR             
======================================================================
📂 QA Report Input  : ./build/4.enh/metadata/report_qa_analytics.csv
🎯 Density Threshold: 2.50 glitches / sec
======================================================================

📊 Summary Analytics:
  • Total files analyzed       : 1052
  • Flagged outliers (≥ 2.50/s) : 6 (0.6%)
  • Mean glitch density (corpus): 1.286 glitches/sec
  • Max glitch density observed : 3.261 glitches/sec

--- TOP FLAGGED OUTLIERS FOR RE-SYNTHESIS ---
                file_name  duration_s  f0_glitch_jumps  glitches_per_sec
 KN_StNp_StNp4_4_0011.wav        1.84                6          3.260870
KN_Thag_thag6_13_0005.wav        1.41                4          2.836879
       AN_AN4_99_0008.wav        5.89               16          2.716469
         MN_MN18_0075.wav        1.48                4          2.702703
         MN_MN55_0005.wav        3.86               10          2.590674
     KN_Ud_ud1_7_0006.wav        3.48                9          2.586207

✅ Saved flagged outlier list (6 rows) to:
   ./build/4.enh/metadata/flag_glitch_outliers.csv
