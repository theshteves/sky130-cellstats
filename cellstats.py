#!/usr/bin/env python3
#
# Mapping of sky130 hd cells to number of sites and number of transistors
# (each site has a width of 460 nm and a height of 2720 nm)

import mmap
import re

# Cells stored as "bytes" objects to speed up RegEx search
# (mmap'd files also prefer raw "bytes" comparisons)
_CELL_PATTERN = re.compile(rb'sky130_\w+')
_FILLER_CELLS = {
    b'sky130_ef_sc_hd__decap_12': (12, 2),
    b'sky130_ef_sc_hd__fakediode_2': (2, 0),
    b'sky130_fd_sc_hd__diode_2': (2, 0),
    b'sky130_fd_sc_hd__fill_1': (1, 0),
    b'sky130_fd_sc_hd__fill_2': (2, 0),
    b'sky130_fd_sc_hd__fill_4': (4, 0),
    b'sky130_fd_sc_hd__fill_8': (8, 0),
    b'sky130_ef_sc_hd__fill_8': (8, 0),
    b'sky130_ef_sc_hd__fill_12': (12, 0),
    b'sky130_fd_sc_hd__decap_3': (3, 2),
    b'sky130_fd_sc_hd__decap_4': (4, 2),
    b'sky130_fd_sc_hd__decap_6': (6, 2),
    b'sky130_fd_sc_hd__decap_8': (8, 2),
    b'sky130_fd_sc_hd__decap_12': (12, 2),
    b'sky130_fd_sc_hd__macro_sparecell': (29, 0),
    b'sky130_fd_sc_hd__tapvgnd2_1': (1, 0),
    b'sky130_fd_sc_hd__tapvgnd_1': (1, 0),
    b'sky130_fd_sc_hd__tapvpwrvgnd_1': (1, 0),
    b'sky130_fd_sc_hd__tap_1': (1, 0),
    b'sky130_fd_sc_hd__tap_2': (2, 0),
}
_REGULAR_CELLS = {
    b'sky130_fd_sc_hd__a2bb2oi_1': (7, 10),
    b'sky130_fd_sc_hd__a2bb2oi_2': (12, 10),
    b'sky130_fd_sc_hd__a2bb2oi_4': (21, 10),
    b'sky130_fd_sc_hd__a2bb2o_1': (8, 12),
    b'sky130_fd_sc_hd__a2bb2o_2': (9, 12),
    b'sky130_fd_sc_hd__a2bb2o_4': (16, 12),
    b'sky130_fd_sc_hd__a21boi_0': (6, 8),
    b'sky130_fd_sc_hd__a21boi_1': (6, 8),
    b'sky130_fd_sc_hd__a21boi_2': (9, 8),
    b'sky130_fd_sc_hd__a21boi_4': (15, 8),
    b'sky130_fd_sc_hd__a21bo_1': (8, 10),
    b'sky130_fd_sc_hd__a21bo_2': (8, 10),
    b'sky130_fd_sc_hd__a21bo_4': (13, 10),
    b'sky130_fd_sc_hd__a21oi_1': (4, 6),
    b'sky130_fd_sc_hd__a21oi_2': (7, 6),
    b'sky130_fd_sc_hd__a21oi_4': (13, 6),
    b'sky130_fd_sc_hd__a21o_1': (6, 8),
    b'sky130_fd_sc_hd__a21o_2': (7, 8),
    b'sky130_fd_sc_hd__a21o_4': (12, 8),
    b'sky130_fd_sc_hd__a22oi_1': (6, 8),
    b'sky130_fd_sc_hd__a22oi_2': (10, 8),
    b'sky130_fd_sc_hd__a22oi_4': (17, 8),
    b'sky130_fd_sc_hd__a22o_1': (7, 10),
    b'sky130_fd_sc_hd__a22o_2': (8, 10),
    b'sky130_fd_sc_hd__a22o_4': (14, 10),
    b'sky130_fd_sc_hd__a31oi_1': (5, 8),
    b'sky130_fd_sc_hd__a31oi_2': (10, 8),
    b'sky130_fd_sc_hd__a31oi_4': (17, 8),
    b'sky130_fd_sc_hd__a31o_1': (7, 10),
    b'sky130_fd_sc_hd__a31o_2': (7, 10),
    b'sky130_fd_sc_hd__a31o_4': (14, 10),
    b'sky130_fd_sc_hd__a32oi_1': (7, 10),
    b'sky130_fd_sc_hd__a32oi_2': (13, 10),
    b'sky130_fd_sc_hd__a32oi_4': (22, 10),
    b'sky130_fd_sc_hd__a32o_1': (8, 12),
    b'sky130_fd_sc_hd__a32o_2': (9, 12),
    b'sky130_fd_sc_hd__a32o_4': (17, 12),
    b'sky130_fd_sc_hd__a41oi_1': (7, 10),
    b'sky130_fd_sc_hd__a41oi_2': (13, 10),
    b'sky130_fd_sc_hd__a41oi_4': (22, 10),
    b'sky130_fd_sc_hd__a41o_1': (8, 12),
    b'sky130_fd_sc_hd__a41o_2': (9, 12),
    b'sky130_fd_sc_hd__a41o_4': (17, 12),
    b'sky130_fd_sc_hd__a211oi_1': (6, 8),
    b'sky130_fd_sc_hd__a211oi_2': (10, 8),
    b'sky130_fd_sc_hd__a211oi_4': (16, 8),
    b'sky130_fd_sc_hd__a211o_1': (7, 10),
    b'sky130_fd_sc_hd__a211o_2': (8, 10),
    b'sky130_fd_sc_hd__a211o_4': (14, 10),
    b'sky130_fd_sc_hd__a221oi_1': (7, 10),
    b'sky130_fd_sc_hd__a221oi_2': (12, 10),
    b'sky130_fd_sc_hd__a221oi_4': (21, 10),
    b'sky130_fd_sc_hd__a221o_1': (8, 12),
    b'sky130_fd_sc_hd__a221o_2': (9, 12),
    b'sky130_fd_sc_hd__a221o_4': (17, 12),
    b'sky130_fd_sc_hd__a222oi_1': (8, 12),
    b'sky130_fd_sc_hd__a311oi_1': (7, 10),
    b'sky130_fd_sc_hd__a311oi_2': (12, 10),
    b'sky130_fd_sc_hd__a311oi_4': (21, 10),
    b'sky130_fd_sc_hd__a311o_1': (8, 12),
    b'sky130_fd_sc_hd__a311o_2': (9, 12),
    b'sky130_fd_sc_hd__a311o_4': (16, 12),
    b'sky130_fd_sc_hd__a2111oi_0': (7, 10),
    b'sky130_fd_sc_hd__a2111oi_1': (8, 10),
    b'sky130_fd_sc_hd__a2111oi_2': (12, 10),
    b'sky130_fd_sc_hd__a2111oi_4': (22, 10),
    b'sky130_fd_sc_hd__a2111o_1': (9, 12),
    b'sky130_fd_sc_hd__a2111o_2': (10, 12),
    b'sky130_fd_sc_hd__a2111o_4': (17, 12),
    b'sky130_fd_sc_hd__and2b_1': (6, 8),
    b'sky130_fd_sc_hd__and2b_2': (7, 8),
    b'sky130_fd_sc_hd__and2b_4': (8, 8),
    b'sky130_fd_sc_hd__and2_0': (5, 6),
    b'sky130_fd_sc_hd__and2_1': (5, 6),
    b'sky130_fd_sc_hd__and2_2': (6, 6),
    b'sky130_fd_sc_hd__and2_4': (7, 6),
    b'sky130_fd_sc_hd__and3b_1': (7, 10),
    b'sky130_fd_sc_hd__and3b_2': (8, 10),
    b'sky130_fd_sc_hd__and3b_4': (10, 10),
    b'sky130_fd_sc_hd__and3_1': (5, 8),
    b'sky130_fd_sc_hd__and3_2': (6, 8),
    b'sky130_fd_sc_hd__and3_4': (9, 8),
    b'sky130_fd_sc_hd__and4bb_1': (10, 14),
    b'sky130_fd_sc_hd__and4bb_2': (10, 14),
    b'sky130_fd_sc_hd__and4bb_4': (13, 14),
    b'sky130_fd_sc_hd__and4b_1': (8, 12),
    b'sky130_fd_sc_hd__and4b_2': (9, 12),
    b'sky130_fd_sc_hd__and4b_4': (11, 12),
    b'sky130_fd_sc_hd__and4_1': (7, 10),
    b'sky130_fd_sc_hd__and4_2': (8, 10),
    b'sky130_fd_sc_hd__and4_4': (9, 10),
    b'sky130_fd_sc_hd__bufbuf_8': (15, 8),
    b'sky130_fd_sc_hd__bufbuf_16': (26, 8),
    b'sky130_fd_sc_hd__bufinv_8': (14, 6),
    b'sky130_fd_sc_hd__bufinv_16': (24, 6),
    b'sky130_fd_sc_hd__buf_1': (3, 4),
    b'sky130_fd_sc_hd__buf_2': (4, 4),
    b'sky130_fd_sc_hd__buf_4': (6, 4),
    b'sky130_fd_sc_hd__buf_6': (9, 4),
    b'sky130_fd_sc_hd__buf_8': (12, 4),
    b'sky130_fd_sc_hd__buf_12': (16, 4),
    b'sky130_fd_sc_hd__buf_16': (22, 4),
    b'sky130_fd_sc_hd__clkbuf_1': (3, 4),
    b'sky130_fd_sc_hd__clkbuf_2': (4, 4),
    b'sky130_fd_sc_hd__clkbuf_4': (6, 4),
    b'sky130_fd_sc_hd__clkbuf_8': (11, 4),
    b'sky130_fd_sc_hd__clkbuf_16': (20, 4),
    b'sky130_fd_sc_hd__clkdlybuf4s15_1': (8, 8),
    b'sky130_fd_sc_hd__clkdlybuf4s15_2': (9, 8),
    b'sky130_fd_sc_hd__clkdlybuf4s18_1': (8, 8),
    b'sky130_fd_sc_hd__clkdlybuf4s18_2': (8, 8),
    b'sky130_fd_sc_hd__clkdlybuf4s25_1': (8, 8),
    b'sky130_fd_sc_hd__clkdlybuf4s25_2': (8, 8),
    b'sky130_fd_sc_hd__clkdlybuf4s50_1': (8, 8),
    b'sky130_fd_sc_hd__clkdlybuf4s50_2': (9, 8),
    b'sky130_fd_sc_hd__clkinvlp_2': (4, 3),
    b'sky130_fd_sc_hd__clkinvlp_4': (6, 5),
    b'sky130_fd_sc_hd__clkinv_1': (3, 2),
    b'sky130_fd_sc_hd__clkinv_2': (4, 2),
    b'sky130_fd_sc_hd__clkinv_4': (7, 2),
    b'sky130_fd_sc_hd__clkinv_8': (13, 2),
    b'sky130_fd_sc_hd__clkinv_16': (24, 2),
    b'sky130_fd_sc_hd__conb_1': (3, 0),
    b'sky130_fd_sc_hd__dfbbn_1': (26, 40),
    b'sky130_fd_sc_hd__dfbbn_2': (28, 40),
    b'sky130_fd_sc_hd__dfbbp_1': (26, 40),
    b'sky130_fd_sc_hd__dfrbp_1': (23, 32),
    b'sky130_fd_sc_hd__dfrbp_2': (24, 32),
    b'sky130_fd_sc_hd__dfrtn_1': (20, 28),
    b'sky130_fd_sc_hd__dfrtp_1': (20, 28),
    b'sky130_fd_sc_hd__dfrtp_2': (21, 28),
    b'sky130_fd_sc_hd__dfrtp_4': (23, 28),
    b'sky130_fd_sc_hd__dfsbp_1': (23, 34),
    b'sky130_fd_sc_hd__dfsbp_2': (24, 34),
    b'sky130_fd_sc_hd__dfstp_1': (21, 32),
    b'sky130_fd_sc_hd__dfstp_2': (21, 32),
    b'sky130_fd_sc_hd__dfstp_4': (24, 32),
    b'sky130_fd_sc_hd__dfxbp_1': (19, 28),
    b'sky130_fd_sc_hd__dfxbp_2': (21, 28),
    b'sky130_fd_sc_hd__dfxtp_1': (16, 24),
    b'sky130_fd_sc_hd__dfxtp_2': (17, 24),
    b'sky130_fd_sc_hd__dfxtp_4': (19, 24),
    b'sky130_fd_sc_hd__dlclkp_1': (14, 20),
    b'sky130_fd_sc_hd__dlclkp_2': (15, 20),
    b'sky130_fd_sc_hd__dlclkp_4': (17, 20),
    b'sky130_fd_sc_hd__dlrbn_1': (17, 24),
    b'sky130_fd_sc_hd__dlrbn_2': (18, 24),
    b'sky130_fd_sc_hd__dlrbp_1': (17, 24),
    b'sky130_fd_sc_hd__dlrbp_2': (18, 24),
    b'sky130_fd_sc_hd__dlrtn_1': (14, 20),
    b'sky130_fd_sc_hd__dlrtn_2': (14, 20),
    b'sky130_fd_sc_hd__dlrtn_4': (16, 20),
    b'sky130_fd_sc_hd__dlrtp_1': (13, 20),
    b'sky130_fd_sc_hd__dlrtp_2': (14, 20),
    b'sky130_fd_sc_hd__dlrtp_4': (16, 20),
    b'sky130_fd_sc_hd__dlxbn_1': (15, 22),
    b'sky130_fd_sc_hd__dlxbn_2': (17, 22),
    b'sky130_fd_sc_hd__dlxbp_1': (15, 22),
    b'sky130_fd_sc_hd__dlxtn_1': (12, 18),
    b'sky130_fd_sc_hd__dlxtn_2': (13, 18),
    b'sky130_fd_sc_hd__dlxtn_4': (15, 18),
    b'sky130_fd_sc_hd__dlxtp_1': (12, 18),
    b'sky130_fd_sc_hd__dlygate4sd1_1': (7, 8),
    b'sky130_fd_sc_hd__dlygate4sd2_1': (7, 8),
    b'sky130_fd_sc_hd__dlygate4sd3_1': (8, 8),
    b'sky130_fd_sc_hd__dlymetal6s2s_1': (10, 12),
    b'sky130_fd_sc_hd__dlymetal6s4s_1': (10, 12),
    b'sky130_fd_sc_hd__dlymetal6s6s_1': (10, 12),
    b'sky130_fd_sc_hd__ebufn_1': (8, 8),
    b'sky130_fd_sc_hd__ebufn_2': (9, 8),
    b'sky130_fd_sc_hd__ebufn_4': (13, 8),
    b'sky130_fd_sc_hd__ebufn_8': (21, 8),
    b'sky130_fd_sc_hd__edfxbp_1': (26, 36),
    b'sky130_fd_sc_hd__edfxtp_1': (24, 34),
    b'sky130_fd_sc_hd__einvn_0': (4, 6),
    b'sky130_fd_sc_hd__einvn_1': (5, 6),
    b'sky130_fd_sc_hd__einvn_2': (7, 6),
    b'sky130_fd_sc_hd__einvn_4': (11, 6),
    b'sky130_fd_sc_hd__einvn_8': (18, 6),
    b'sky130_fd_sc_hd__einvp_1': (5, 6),
    b'sky130_fd_sc_hd__einvp_2': (7, 6),
    b'sky130_fd_sc_hd__einvp_4': (11, 6),
    b'sky130_fd_sc_hd__einvp_8': (18, 6),
    b'sky130_fd_sc_hd__fahcin_1': (27, 32),
    b'sky130_fd_sc_hd__fahcon_1': (27, 32),
    b'sky130_fd_sc_hd__fah_1': (27, 32),
    b'sky130_fd_sc_hd__fa_1': (16, 28),
    b'sky130_fd_sc_hd__fa_2': (18, 28),
    b'sky130_fd_sc_hd__fa_4': (22, 28),
    b'sky130_fd_sc_hd__ha_1': (10, 14),
    b'sky130_fd_sc_hd__ha_2': (12, 14),
    b'sky130_fd_sc_hd__ha_4': (20, 14),
    b'sky130_fd_sc_hd__inv_1': (3, 2),
    b'sky130_fd_sc_hd__inv_2': (3, 2),
    b'sky130_fd_sc_hd__inv_4': (5, 2),
    b'sky130_fd_sc_hd__inv_6': (7, 2),
    b'sky130_fd_sc_hd__inv_8': (9, 2),
    b'sky130_fd_sc_hd__inv_12': (13, 2),
    b'sky130_fd_sc_hd__inv_16': (16, 2),
    b'sky130_fd_sc_hd__lpflow_bleeder_1': (6, 5),
    b'sky130_fd_sc_hd__lpflow_clkbufkapwr_1': (3, 4),
    b'sky130_fd_sc_hd__lpflow_clkbufkapwr_2': (4, 4),
    b'sky130_fd_sc_hd__lpflow_clkbufkapwr_4': (6, 4),
    b'sky130_fd_sc_hd__lpflow_clkbufkapwr_8': (11, 4),
    b'sky130_fd_sc_hd__lpflow_clkbufkapwr_16': (20, 4),
    b'sky130_fd_sc_hd__lpflow_clkinvkapwr_1': (3, 2),
    b'sky130_fd_sc_hd__lpflow_clkinvkapwr_2': (4, 2),
    b'sky130_fd_sc_hd__lpflow_clkinvkapwr_4': (7, 2),
    b'sky130_fd_sc_hd__lpflow_clkinvkapwr_8': (13, 2),
    b'sky130_fd_sc_hd__lpflow_clkinvkapwr_16': (24, 2),
    b'sky130_fd_sc_hd__lpflow_decapkapwr_3': (3, 2),
    b'sky130_fd_sc_hd__lpflow_decapkapwr_4': (4, 2),
    b'sky130_fd_sc_hd__lpflow_decapkapwr_6': (6, 2),
    b'sky130_fd_sc_hd__lpflow_decapkapwr_8': (8, 2),
    b'sky130_fd_sc_hd__lpflow_decapkapwr_12': (12, 2),
    b'sky130_fd_sc_hd__lpflow_inputiso0n_1': (5, 6),
    b'sky130_fd_sc_hd__lpflow_inputiso0p_1': (6, 8),
    b'sky130_fd_sc_hd__lpflow_inputiso1n_1': (6, 8),
    b'sky130_fd_sc_hd__lpflow_inputiso1p_1': (5, 6),
    b'sky130_fd_sc_hd__lpflow_inputisolatch_1': (11, 16),
    b'sky130_fd_sc_hd__lpflow_isobufsrckapwr_16': (31, 10),
    b'sky130_fd_sc_hd__lpflow_isobufsrc_1': (5, 6),
    b'sky130_fd_sc_hd__lpflow_isobufsrc_2': (7, 6),
    b'sky130_fd_sc_hd__lpflow_isobufsrc_4': (11, 6),
    b'sky130_fd_sc_hd__lpflow_isobufsrc_8': (19, 6),
    b'sky130_fd_sc_hd__lpflow_isobufsrc_16': (36, 6),
    b'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_1': (28, 16),
    b'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_2': (28, 18),
    b'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_4': (32, 22),
    b'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_4': (32, 10),
    b'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_1': (28, 16),
    b'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_2': (28, 18),
    b'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_4': (32, 22),
    b'sky130_fd_sc_hd__maj3_1': (8, 14),
    b'sky130_fd_sc_hd__maj3_2': (9, 14),
    b'sky130_fd_sc_hd__maj3_4': (11, 14),
    b'sky130_fd_sc_hd__mux2i_1': (8, 10),
    b'sky130_fd_sc_hd__mux2i_2': (11, 10),
    b'sky130_fd_sc_hd__mux2i_4': (18, 10),
    b'sky130_fd_sc_hd__mux2_1': (9, 12),
    b'sky130_fd_sc_hd__mux2_2': (9, 12),
    b'sky130_fd_sc_hd__mux2_4': (12, 12),
    b'sky130_fd_sc_hd__mux2_8': (21, 12),
    b'sky130_fd_sc_hd__mux4_1': (21, 26),
    b'sky130_fd_sc_hd__mux4_2': (18, 26),
    b'sky130_fd_sc_hd__mux4_4': (20, 26),
    b'sky130_fd_sc_hd__nand2b_1': (5, 6),
    b'sky130_fd_sc_hd__nand2b_2': (7, 6),
    b'sky130_fd_sc_hd__nand2b_4': (11, 6),
    b'sky130_fd_sc_hd__nand2_1': (3, 4),
    b'sky130_fd_sc_hd__nand2_2': (5, 4),
    b'sky130_fd_sc_hd__nand2_4': (9, 4),
    b'sky130_fd_sc_hd__nand2_8': (16, 4),
    b'sky130_fd_sc_hd__nand3b_1': (6, 8),
    b'sky130_fd_sc_hd__nand3b_2': (9, 8),
    b'sky130_fd_sc_hd__nand3b_4': (16, 8),
    b'sky130_fd_sc_hd__nand3_1': (4, 6),
    b'sky130_fd_sc_hd__nand3_2': (8, 6),
    b'sky130_fd_sc_hd__nand3_4': (14, 6),
    b'sky130_fd_sc_hd__nand4bb_1': (9, 12),
    b'sky130_fd_sc_hd__nand4bb_2': (13, 12),
    b'sky130_fd_sc_hd__nand4bb_4': (22, 12),
    b'sky130_fd_sc_hd__nand4b_1': (7, 10),
    b'sky130_fd_sc_hd__nand4b_2': (12, 10),
    b'sky130_fd_sc_hd__nand4b_4': (19, 10),
    b'sky130_fd_sc_hd__nand4_1': (5, 8),
    b'sky130_fd_sc_hd__nand4_2': (10, 8),
    b'sky130_fd_sc_hd__nand4_4': (17, 8),
    b'sky130_fd_sc_hd__nor2b_1': (5, 6),
    b'sky130_fd_sc_hd__nor2b_2': (7, 6),
    b'sky130_fd_sc_hd__nor2b_4': (11, 6),
    b'sky130_fd_sc_hd__nor2_1': (3, 4),
    b'sky130_fd_sc_hd__nor2_2': (5, 4),
    b'sky130_fd_sc_hd__nor2_4': (9, 4),
    b'sky130_fd_sc_hd__nor2_8': (16, 4),
    b'sky130_fd_sc_hd__nor3b_1': (6, 8),
    b'sky130_fd_sc_hd__nor3b_2': (10, 8),
    b'sky130_fd_sc_hd__nor3b_4': (15, 8),
    b'sky130_fd_sc_hd__nor3_1': (4, 6),
    b'sky130_fd_sc_hd__nor3_2': (8, 6),
    b'sky130_fd_sc_hd__nor3_4': (13, 6),
    b'sky130_fd_sc_hd__nor4bb_1': (8, 12),
    b'sky130_fd_sc_hd__nor4bb_2': (13, 12),
    b'sky130_fd_sc_hd__nor4bb_4': (20, 12),
    b'sky130_fd_sc_hd__nor4b_1': (7, 10),
    b'sky130_fd_sc_hd__nor4b_2': (12, 10),
    b'sky130_fd_sc_hd__nor4b_4': (19, 10),
    b'sky130_fd_sc_hd__nor4_1': (5, 8),
    b'sky130_fd_sc_hd__nor4_2': (10, 8),
    b'sky130_fd_sc_hd__nor4_4': (17, 8),
    b'sky130_fd_sc_hd__o2bb2ai_1': (7, 10),
    b'sky130_fd_sc_hd__o2bb2ai_2': (12, 10),
    b'sky130_fd_sc_hd__o2bb2ai_4': (22, 10),
    b'sky130_fd_sc_hd__o2bb2a_1': (8, 12),
    b'sky130_fd_sc_hd__o2bb2a_2': (9, 12),
    b'sky130_fd_sc_hd__o2bb2a_4': (16, 12),
    b'sky130_fd_sc_hd__o21ai_0': (4, 6),
    b'sky130_fd_sc_hd__o21ai_1': (4, 6),
    b'sky130_fd_sc_hd__o21ai_2': (7, 6),
    b'sky130_fd_sc_hd__o21ai_4': (13, 6),
    b'sky130_fd_sc_hd__o21a_1': (6, 8),
    b'sky130_fd_sc_hd__o21a_2': (7, 8),
    b'sky130_fd_sc_hd__o21a_4': (12, 8),
    b'sky130_fd_sc_hd__o21bai_1': (6, 8),
    b'sky130_fd_sc_hd__o21bai_2': (9, 8),
    b'sky130_fd_sc_hd__o21bai_4': (15, 8),
    b'sky130_fd_sc_hd__o21ba_1': (8, 10),
    b'sky130_fd_sc_hd__o21ba_2': (8, 10),
    b'sky130_fd_sc_hd__o21ba_4': (13, 10),
    b'sky130_fd_sc_hd__o22ai_1': (5, 8),
    b'sky130_fd_sc_hd__o22ai_2': (10, 8),
    b'sky130_fd_sc_hd__o22ai_4': (16, 8),
    b'sky130_fd_sc_hd__o22a_1': (7, 10),
    b'sky130_fd_sc_hd__o22a_2': (8, 10),
    b'sky130_fd_sc_hd__o22a_4': (14, 10),
    b'sky130_fd_sc_hd__o31ai_1': (6, 8),
    b'sky130_fd_sc_hd__o31ai_2': (10, 8),
    b'sky130_fd_sc_hd__o31ai_4': (17, 8),
    b'sky130_fd_sc_hd__o31a_1': (7, 10),
    b'sky130_fd_sc_hd__o31a_2': (8, 10),
    b'sky130_fd_sc_hd__o31a_4': (14, 10),
    b'sky130_fd_sc_hd__o32ai_1': (7, 10),
    b'sky130_fd_sc_hd__o32ai_2': (13, 10),
    b'sky130_fd_sc_hd__o32ai_4': (22, 10),
    b'sky130_fd_sc_hd__o32a_1': (8, 12),
    b'sky130_fd_sc_hd__o32a_2': (9, 12),
    b'sky130_fd_sc_hd__o32a_4': (18, 12),
    b'sky130_fd_sc_hd__o41ai_1': (7, 10),
    b'sky130_fd_sc_hd__o41ai_2': (13, 10),
    b'sky130_fd_sc_hd__o41ai_4': (22, 10),
    b'sky130_fd_sc_hd__o41a_1': (9, 12),
    b'sky130_fd_sc_hd__o41a_2': (10, 12),
    b'sky130_fd_sc_hd__o41a_4': (17, 12),
    b'sky130_fd_sc_hd__o211ai_1': (6, 8),
    b'sky130_fd_sc_hd__o211ai_2': (10, 8),
    b'sky130_fd_sc_hd__o211ai_4': (17, 8),
    b'sky130_fd_sc_hd__o211a_1': (8, 10),
    b'sky130_fd_sc_hd__o211a_2': (8, 10),
    b'sky130_fd_sc_hd__o211a_4': (14, 10),
    b'sky130_fd_sc_hd__o221ai_1': (7, 10),
    b'sky130_fd_sc_hd__o221ai_2': (12, 10),
    b'sky130_fd_sc_hd__o221ai_4': (21, 10),
    b'sky130_fd_sc_hd__o221a_1': (9, 12),
    b'sky130_fd_sc_hd__o221a_2': (9, 12),
    b'sky130_fd_sc_hd__o221a_4': (16, 12),
    b'sky130_fd_sc_hd__o311ai_0': (7, 10),
    b'sky130_fd_sc_hd__o311ai_1': (7, 10),
    b'sky130_fd_sc_hd__o311ai_2': (13, 10),
    b'sky130_fd_sc_hd__o311ai_4': (21, 10),
    b'sky130_fd_sc_hd__o311a_1': (8, 12),
    b'sky130_fd_sc_hd__o311a_2': (9, 12),
    b'sky130_fd_sc_hd__o311a_4': (17, 12),
    b'sky130_fd_sc_hd__o2111ai_1': (7, 10),
    b'sky130_fd_sc_hd__o2111ai_2': (12, 10),
    b'sky130_fd_sc_hd__o2111ai_4': (21, 10),
    b'sky130_fd_sc_hd__o2111a_1': (9, 12),
    b'sky130_fd_sc_hd__o2111a_2': (10, 12),
    b'sky130_fd_sc_hd__o2111a_4': (16, 12),
    b'sky130_fd_sc_hd__or2b_1': (6, 8),
    b'sky130_fd_sc_hd__or2b_2': (7, 8),
    b'sky130_fd_sc_hd__or2b_4': (9, 8),
    b'sky130_fd_sc_hd__or2_0': (5, 6),
    b'sky130_fd_sc_hd__or2_1': (5, 6),
    b'sky130_fd_sc_hd__or2_2': (5, 6),
    b'sky130_fd_sc_hd__or2_4': (7, 6),
    b'sky130_fd_sc_hd__or3b_1': (7, 10),
    b'sky130_fd_sc_hd__or3b_2': (7, 10),
    b'sky130_fd_sc_hd__or3b_4': (9, 10),
    b'sky130_fd_sc_hd__or3_1': (5, 8),
    b'sky130_fd_sc_hd__or3_2': (6, 8),
    b'sky130_fd_sc_hd__or3_4': (9, 8),
    b'sky130_fd_sc_hd__or4bb_1': (9, 14),
    b'sky130_fd_sc_hd__or4bb_2': (10, 14),
    b'sky130_fd_sc_hd__or4bb_4': (12, 14),
    b'sky130_fd_sc_hd__or4b_1': (8, 12),
    b'sky130_fd_sc_hd__or4b_2': (8, 12),
    b'sky130_fd_sc_hd__or4b_4': (11, 12),
    b'sky130_fd_sc_hd__or4_1': (6, 10),
    b'sky130_fd_sc_hd__or4_2': (7, 10),
    b'sky130_fd_sc_hd__or4_4': (9, 10),
    b'sky130_fd_sc_hd__probec_p_8': (12, 4),
    b'sky130_fd_sc_hd__probe_p_8': (12, 4),
    b'sky130_fd_sc_hd__sdfbbn_1': (31, 48),
    b'sky130_fd_sc_hd__sdfbbn_2': (33, 48),
    b'sky130_fd_sc_hd__sdfbbp_1': (31, 48),
    b'sky130_fd_sc_hd__sdfrbp_1': (28, 40),
    b'sky130_fd_sc_hd__sdfrbp_2': (29, 40),
    b'sky130_fd_sc_hd__sdfrtn_1': (25, 36),
    b'sky130_fd_sc_hd__sdfrtp_1': (25, 36),
    b'sky130_fd_sc_hd__sdfrtp_2': (26, 36),
    b'sky130_fd_sc_hd__sdfrtp_4': (28, 36),
    b'sky130_fd_sc_hd__sdfsbp_1': (29, 42),
    b'sky130_fd_sc_hd__sdfsbp_2': (31, 42),
    b'sky130_fd_sc_hd__sdfstp_1': (27, 40),
    b'sky130_fd_sc_hd__sdfstp_2': (28, 40),
    b'sky130_fd_sc_hd__sdfstp_4': (30, 40),
    b'sky130_fd_sc_hd__sdfxbp_1': (24, 36),
    b'sky130_fd_sc_hd__sdfxbp_2': (26, 36),
    b'sky130_fd_sc_hd__sdfxtp_1': (21, 32),
    b'sky130_fd_sc_hd__sdfxtp_2': (22, 32),
    b'sky130_fd_sc_hd__sdfxtp_4': (24, 32),
    b'sky130_fd_sc_hd__sdlclkp_1': (15, 22),
    b'sky130_fd_sc_hd__sdlclkp_2': (16, 22),
    b'sky130_fd_sc_hd__sdlclkp_4': (18, 22),
    b'sky130_fd_sc_hd__sedfxbp_1': (31, 44),
    b'sky130_fd_sc_hd__sedfxbp_2': (33, 44),
    b'sky130_fd_sc_hd__sedfxtp_1': (29, 42),
    b'sky130_fd_sc_hd__sedfxtp_2': (30, 42),
    b'sky130_fd_sc_hd__sedfxtp_4': (32, 42),
    b'sky130_fd_sc_hd__xnor2_1': (7, 10),
    b'sky130_fd_sc_hd__xnor2_2': (13, 10),
    b'sky130_fd_sc_hd__xnor2_4': (22, 10),
    b'sky130_fd_sc_hd__xnor3_1': (18, 22),
    b'sky130_fd_sc_hd__xnor3_2': (19, 22),
    b'sky130_fd_sc_hd__xnor3_4': (21, 22),
    b'sky130_fd_sc_hd__xor2_1': (7, 10),
    b'sky130_fd_sc_hd__xor2_2': (13, 10),
    b'sky130_fd_sc_hd__xor2_4': (22, 10),
    b'sky130_fd_sc_hd__xor3_1': (19, 22),
    b'sky130_fd_sc_hd__xor3_2': (20, 22),
    b'sky130_fd_sc_hd__xor3_4': (22, 22),
}


def get_sky130_cell_statistics_from_file(filename, verbose=False):
    '''Count Skywater 130nm cells, sites, & transistors in file (with fillers seperately)'''

    global _CELL_PATTERN, _FILLER_CELLS, _REGULAR_CELLS
    file_statistics = {
        'filename': filename,
        'cells': 0,
        'sites': 0,
        'transistors': 0,
        'cells_with_filler': 0,
        'sites_with_filler': 0,
        'transistors_with_filler': 0,
    }

    with open(filename, 'rb') as file:
        # Reduce SLOW file I/O when scaning large files
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmfile:

            for cell in _CELL_PATTERN.findall(mmfile):
                is_filler = cell in _FILLER_CELLS
                sites, transistors = _FILLER_CELLS[cell] if is_filler else _REGULAR_CELLS[cell]
                if verbose:
                    print(f'{filename}:  {cell}  => ({"Filler" if is_filler else "Regular"}, {sites}, {transistors})')

                file_statistics['cells_with_filler'] += 1
                file_statistics['sites_with_filler'] += sites
                file_statistics['transistors_with_filler'] += transistors
                if not is_filler:
                    file_statistics['cells'] += 1
                    file_statistics['sites'] += sites
                    file_statistics['transistors'] += transistors

    return file_statistics


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Report Skywater 130nm usage statistics')
    parser.add_argument('filenames', nargs='+', help='1+ file(s) to parse (for example, "gate-level.v")')
    parser.add_argument('-v', '--verbose', action='store_true', help='Use verbose output')
    args = parser.parse_args()

    print('file,cells,sites,transistors,cells_with_fill,sites_with_fill,transistors_with_fill')
    for filename in args.filenames:
        file_statistics = get_sky130_cell_statistics_from_file(filename, args.verbose)

        print(','.join(
            str(statistic)
            for statistic in file_statistics.values()
        ))
