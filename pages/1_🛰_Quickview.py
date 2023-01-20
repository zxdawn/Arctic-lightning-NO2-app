import urllib
import xarray as xr
import streamlit as st
import plotly.express as px

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

# GITHUB_ROOT = "https://raw.githubusercontent.com/zxdawn/Arctic-lightning-NO2-app/data/"

@st.experimental_singleton
def read_data(filename):
    return xr.open_dataset(filename)

    # github_url = GITHUB_ROOT+'S5P_LNO2_grid_product.nc'
    # with urllib.request.urlopen(github_url) as open_file:  # type: ignore
    #     return xr.open_dataset(open_file)


class view_product:
    '''Plot the tropomi no2 with lightning images'''
    def __init__(self, filename):
        self.ds = read_data(filename)
    
    def set_page(self):
        # decrease pad to page top
        st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

        # application title
        st.title(':lightning_cloud: :orange[Lightning NO$_2$ in the Arctic]')

        font_css = """
        <style>
        button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
        font-size: 24px; font-weight: bold;
        }
        </style>
        """

        st.write(font_css, unsafe_allow_html=True)


    def set_slider(self):
        # get the case nums
        case_list = list(sorted(set([s.split('_')[0] for s in self.ds['orbit'].values])))

        # add slider of cases
        st.sidebar.success("Select case (Defalut is 11).")
        self.case_num = st.sidebar.slider('Case No.', min_value=0, max_value=int(case_list[-1])-1, value=11) # default: case 11

        self.plev = st.sidebar.selectbox('Pressure level (hPa) \n of lightning tracer', (300, 500, 700), index=2) # default: 700 hPa
        st.sidebar.info("Lightning tracer is released at the detected location \n\
                        and transported by horizontal advection, \n \
                        also known as isobaric forward trajectories.")

        # increase the font size of slider
        st.markdown(
            """<style>
        div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
            font-size: 20px; font-weight: bold; color: gray;
        }
            </style>
            """, unsafe_allow_html=True)
        

    def plot_data(self):
        orbit_list = list(filter(lambda x: x.startswith(f'{self.case_num:02}'), self.ds['orbit'].values))
        ds_sel = self.ds.loc[dict(orbit=orbit_list)]
        # drop nan values
        # ds_sel = ds_sel.where(~ds_sel['no2'].isnull(), drop=True)
        # this is much quicker
        ds_sel = ds_sel.dropna(dim='latitude', how='all').dropna(dim='longitude', how='all')

        # change units
        ds_sel['no2'] *= 1e6
        ds_sel['lno2'] *= 1e6
        ds_sel['cloud_pressure_crb'] /= 100
        no2_max = ds_sel['no2'].max().item()
        ds_sel['lightning_counts'] = ds_sel['lightning_counts'].sel(level=self.plev)
        ds_sel['lightning_counts'] = ds_sel['lightning_counts'].where(ds_sel['lightning_counts']>0, drop=True)

        # rename for title and convert Dataset to DataArray
        data = ds_sel[['no2', 'lno2', 'cloud_pressure_crb', 'lightning_counts']]\
                    .rename({'no2': 'NO2', 'lno2': 'Lightning NO2', 'cloud_pressure_crb': 'Cloud Pressure'}).to_array().transpose('orbit', ...)

        # animation
        fig = px.imshow(data.assign_coords({'variable': range(len(data['variable']))}),
                        animation_frame='orbit', facet_col='variable',
                        facet_col_wrap=2,
                        facet_col_spacing=0.05,
                        color_continuous_scale='Thermal', origin='lower',
                        labels={'color': 'value'},
                        width=950, height=700,
                        # zmin=0, zmax=no2_max
                        )
        fig.layout.font.size = 20

        # set variable back to string
        #   https://community.plotly.com/t/cant-set-strings-as-facet-col-in-px-imshow
        #   https://community.plotly.com/t/wrong-title-when-changing-facet-col-wrap-value
        for k in range(len(data['variable'])):
            fig.layout.annotations[k].update(text = ['Cloud Pressure', 'Lightning Counts', 'NO2', 'Lightning NO2'][k])

        # fig.for_each_xaxis(lambda axis: axis.title.update(font=dict(size=20)))
        # fig.update_xaxes(title_font=dict(size=20))

        # fig.update_layout(
        #     # title=f"Case '{self.case_num:02}'",
        #     # xaxis_title="Longitude",
        #     # yaxis_title="Latitude",
        #     # margin = dict(b=200),
        #     yaxis = dict(tickfont = dict(size=18)),
        #     xaxis = dict(tickfont = dict(size=18)),
        #     font=dict(size=20),
        #         coloraxis_colorbar=dict(title=r'Cloumn density (umol m<sup>2</sup>)'),
        # )

        fig.update_geos(fitbounds='locations')

        # update traces to use different coloraxis
        for i, t in enumerate(fig.data):
            t.update(coloraxis=f'coloraxis{i+1}')
        for fr in fig.frames:
            # update each of the traces in each of the animation frames
            for i, t in enumerate(fr.data):
                t.update(coloraxis=f'coloraxis{i+1}')

        # position / config all coloraxis
        fig.update_layout(
            coloraxis={'colorbar': {'x': -0.3,
                                    'len': 0.5,
                                    'y': 0.8,
                                    'title': r'umol m<sup>2</sup>',
                                    },
                        'cmin': 0,
                        'cmax': 30,
                        },
            coloraxis2={
                        'colorbar': {'x': 1.1,
                                    'len': 0.5,
                                    'y': 0.8,
                                    'title': r'umol m<sup>2</sup>'
                                    },
                        'cmin': 0,
                        'cmax': 30,
                        'colorscale': fig.layout['coloraxis']['colorscale'],
                        },
            coloraxis3={'colorbar': {'x': -0.3,
                                     'len': 0.5,
                                     'y': 0.3,
                                     'title': 'hPa'
                        },
                        'cmin': ds_sel['cloud_pressure_crb'].min().item(),
                        'cmax': ds_sel['cloud_pressure_crb'].max().item(),
                        # 'cmax': 700,
                        'colorscale': 'Ice_r',
                        },
            coloraxis4={'colorbar': {'x': 1.1,
                                     'len': 0.5,
                                     'y': 0.3,
                                     },
                        'cmin': ds_sel['lightning_counts'].min().item(),
                        'cmax': ds_sel['lightning_counts'].max().item(),
                        'colorscale': 'matter',
            },
        )

        fig.update_layout(updatemenus=[dict(type='buttons',
                        showactive=False,
                        y=1.3,
                        x=-0.15,
                        xanchor='left',
                        yanchor='bottom')
                                ])

        # position the slider (closer to the plot)
        fig['layout']['sliders'][0]['pad']=dict(r=100, t=-600,)

        st.plotly_chart(fig)#, theme="streamlit")



def main():
    filename = './data/S5P_LNO2_grid_product.nc'
    product = view_product(filename)
    product.set_page()
    product.set_slider()
    product.plot_data()


if __name__ == "__main__":
    main()