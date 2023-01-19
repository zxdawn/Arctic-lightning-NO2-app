import streamlit as st
from PIL import Image

# decrease pad to page top
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

st.title(':orange[Data Sources]')

st.markdown('### Plotted Data')
st.markdown('The NetCDF data plotted in the "Quickview" Page is hosted on \
            [GitHub](https://github.com/zxdawn/Arctic-lightning-NO2/blob/main/data/S5P_LNO2_grid_product.nc). \
            Here are some links of related source codes: \
            [s5p_lno2_grid_product.py](https://github.com/zxdawn/S5P-LNO2/blob/main/main/s5p_lno2_grid_product.py) \
            and [streamlit app](https://github.com/zxdawn/Arctic-lightning-NO2-app).')

st.markdown('### TROPOMI Data')
st.markdown('The TROPOMI NO$_2$ L2 data used in this study is the [PAL](https://data-portal.s5p-pal.com/) version.')
st.markdown('> This dataset has been generated due to a switch in the processor version of the NO2 processor \
                    during early December 2020 introducing a discontinuity in the time series of the Sentinel-5P NO2 data. \
                To harmonize this data record the latest operational processor (version 02.03.01) was used to \
                    reprocess the data from the beginning of the mission until mid November 2021 \
                    (aligning with the operational deployment of the V02.03.01 processor). \
                The reprocessing consisted of a regeneration of the FRESCO and AAI input products, \
                    followed by a reprocessing of the NO2 product itself using these new inputs. \
                Only the final NO2 products are made available via the S5P-PAL data portal.')

st.markdown('### TROPOMI Lightning NO$_2$ Data')
st.markdown('We also uploaded the original TROPOMI lightning NO$_2$ data \
            ([2019](https://doi.org/10.5281/zenodo.7547817), \
             [2020](https://doi.org/10.5281/zenodo.7547819), \
             [2021](https://doi.org/10.5281/zenodo.7547825)) to Zenodo. \
            Because these files include the VAISALA GLD360 lightning data, users need to apply for access on the page.')

