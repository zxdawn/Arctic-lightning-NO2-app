import streamlit as st
from PIL import Image

# decrease pad to page top
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

st.title(':orange[Contact]')

st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

st.info('The arctic-lightning-no2 website is maintained by [Xin Zhang](https://dreambooker.site/about/). \
         \n \
         \n If you meet any problem or wanna communicate, \
         please feel free to [drop an email](mailto:xinzhang1215@gmail.com) \
         or submit issues on the [GitHub page](https://github.com/zxdawn/Arctic-lightning-NO2-app/issues).')

st.image('https://github.com/zxdawn/zxdawn/blob/main/imgs/cloud.jpg?raw=true')