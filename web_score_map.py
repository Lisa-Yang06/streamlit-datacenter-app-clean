import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.features import GeoJsonTooltip
import branca.colormap as cm
import sys

state_name_to_fips = {
    "Alabama": "01",
    "Alaska": "02",
    "Arizona": "04",
    "Arkansas": "05",
    "California": "06",
    "Colorado": "08",
    "Connecticut": "09",
    "Delaware": "10",
    "District of Columbia": "11",
    "Florida": "12",
    "Georgia": "13",
    "Hawaii": "15",
    "Idaho": "16",
    "Illinois": "17",
    "Indiana": "18",
    "Iowa": "19",
    "Kansas": "20",
    "Kentucky": "21",
    "Louisiana": "22",
    "Maine": "23",
    "Maryland": "24",
    "Massachusetts": "25",
    "Michigan": "26",
    "Minnesota": "27",
    "Mississippi": "28",
    "Missouri": "29",
    "Montana": "30",
    "Nebraska": "31",
    "Nevada": "32",
    "New Hampshire": "33",
    "New Jersey": "34",
    "New Mexico": "35",
    "New York": "36",
    "North Carolina": "37",
    "North Dakota": "38",
    "Ohio": "39",
    "Oklahoma": "40",
    "Oregon": "41",
    "Pennsylvania": "42",
    "Rhode Island": "44",
    "South Carolina": "45",
    "South Dakota": "46",
    "Tennessee": "47",
    "Texas": "48",
    "Utah": "49",
    "Vermont": "50",
    "Virginia": "51",
    "Washington": "53",
    "West Virginia": "54",
    "Wisconsin": "55",
    "Wyoming": "56",
    "Puerto Rico": "72"
}

fips_to_state_abbr = {
    "01": "AL",  # Alabama
    "02": "AK",  # Alaska
    "04": "AZ",  # Arizona
    "05": "AR",  # Arkansas
    "06": "CA",  # California
    "08": "CO",  # Colorado
    "09": "CT",  # Connecticut
    "10": "DE",  # Delaware
    "11": "DC",  # District of Columbia
    "12": "FL",  # Florida
    "13": "GA",  # Georgia
    "15": "HI",  # Hawaii
    "16": "ID",  # Idaho
    "17": "IL",  # Illinois
    "18": "IN",  # Indiana
    "19": "IA",  # Iowa
    "20": "KS",  # Kansas
    "21": "KY",  # Kentucky
    "22": "LA",  # Louisiana
    "23": "ME",  # Maine
    "24": "MD",  # Maryland
    "25": "MA",  # Massachusetts
    "26": "MI",  # Michigan
    "27": "MN",  # Minnesota
    "28": "MS",  # Mississippi
    "29": "MO",  # Missouri
    "30": "MT",  # Montana
    "31": "NE",  # Nebraska
    "32": "NV",  # Nevada
    "33": "NH",  # New Hampshire
    "34": "NJ",  # New Jersey
    "35": "NM",  # New Mexico
    "36": "NY",  # New York
    "37": "NC",  # North Carolina
    "38": "ND",  # North Dakota
    "39": "OH",  # Ohio
    "40": "OK",  # Oklahoma
    "41": "OR",  # Oregon
    "42": "PA",  # Pennsylvania
    "44": "RI",  # Rhode Island
    "45": "SC",  # South Carolina
    "46": "SD",  # South Dakota
    "47": "TN",  # Tennessee
    "48": "TX",  # Texas
    "49": "UT",  # Utah
    "50": "VT",  # Vermont
    "51": "VA",  # Virginia
    "53": "WA",  # Washington
    "54": "WV",  # West Virginia
    "55": "WI",  # Wisconsin
    "56": "WY",  # Wyoming
    "72": "PR"   # Puerto Rico
}


# 页面配置
st.set_page_config(page_title="Core Variable Score Map", layout="wide")
st.title("🗺️ Interactive County-Level Environmental Friendliness Map")

# 读取数据函数
@st.cache_data
def load_data():
    counties = gpd.read_file("/Users/yuxuanyang/Library/CloudStorage/OneDrive-Emory/AI.X/us_map/tl_2024_us_county/tl_2024_us_county.shp")
    counties["GEOID"] = counties["GEOID"].astype(str).str.zfill(5)
    counties["STATE"] = counties["STATEFP"].map(fips_to_state_abbr)

    score_df = pd.read_csv("/Users/yuxuanyang/Library/CloudStorage/OneDrive-Emory/AI.X/env_RESULTS/data/MERGED.csv")
    score_df["GEOID"] = score_df["GEOID"].astype(str).str.zfill(5)

    merged = counties.merge(score_df, on="GEOID", how="left")
    merged["geometry"] = merged["geometry"].simplify(tolerance=0.01, preserve_topology=True)
    return merged

# 加载合并数据
map_df = load_data()

page = st.sidebar.radio("Navigation", ["About",
                                       "Map by Overall Score", 
                                        "Map by Four Core Variables Score", 
                                        "Custom Variable Average",
                                        "Weighted Score Map (Profitability vs. Environment)"])
if page == "About":
    st.title("About this Dashboard")
    st.markdown("""
    Welcome to the **Data Center Environmental Suitability Dashboard**.
                
    This tool visualizes environmental indicators that influence the tolerance of U.S. counties to data center impacts, including:
    - Climate (Temperature and Precipitation)
    - Biodiversity (Birds, Mammals, and Reptiles Population)
    - Water & Carbon footprint of a hypothetical 1MW Data Center Placed Within Each County
    - Water Seasonal Variability, Water Stress Index, Baseline Water Stress
    - Forest & Shrub Proportion
    - Population Density
    - Wind Speed
    - Dustiness (Whether Tolerable to Light Pollution)
    
    Among all the variables, we identified four core variables, which are ***carbon footprint, water footprint, population density, and shrub proportion***.
                
    You can:
    - Explore pre-computed overall score (16 variables) and core score (4 core variables) for each county.
    - Customize your own weighted averages for each county using selected variables.
                """)

if page == "Map by Overall Score":
    # 创建 Folium 地图
    m = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles="CartoDB positron")

    # 定义颜色渐变（绿色系）
    score_min, score_max = map_df["SUM"].min(), map_df["SUM"].max()
    colormap = cm.linear.YlGn_09.scale(score_min, score_max)
    colormap.caption = "Overall Score"
    colormap.add_to(m)

    # 设置 tooltip
    tooltip = GeoJsonTooltip(
        fields=["NAME", "STATE", "SUM"],
        aliases=["County", "State", "Score"],
        localize=True
    )

    # 添加 GeoJson 图层，颜色渐变按 SUM 值填充
    folium.GeoJson(
        map_df,
        name="Overall Score",
        tooltip=tooltip,
        style_function=lambda feature: {
            "fillColor": colormap(feature["properties"]["SUM"]) if feature["properties"]["SUM"] is not None else "#cccccc",
            "color": "black",
            "weight": 0.2,
            "fillOpacity": 0.7,
        }
    ).add_to(m)

    # 🔍 添加可选县用于高亮显示
    available_counties = map_df[map_df["SUM"].notna()][["NAME", "STATE", "GEOID"]].drop_duplicates()
    available_counties["display_name"] = available_counties["NAME"] + ", " + available_counties["STATE"]

    selected_county = st.selectbox("🔍 Highlight a County", ["None"] + sorted(available_counties["display_name"]), key = "highlight_overall")

    if selected_county != "None":
        selected_geoid = available_counties[available_counties["display_name"] == selected_county]["GEOID"].values[0]
        highlight_geo = map_df[map_df["GEOID"] == selected_geoid]

        # 添加红色边界图层
        folium.GeoJson(
            highlight_geo,
            name="Highlighted County",
            style_function=lambda feature: {
                "fillColor": "none",
                "color": "red",
                "weight": 1,
                "fillOpacity": 0,
            },
            tooltip=GeoJsonTooltip(
                fields=["NAME", "STATE"],
                aliases=["County", "State"],
                localize=True
            )
        ).add_to(m)

    # 展示地图
    st_data = st_folium(m, width=1000, height=650)

    # 点击显示详情
    if st_data and st_data.get("last_active_drawing"):
        props = st_data["last_active_drawing"]["properties"]
        st.subheader(f"📍 {props['NAME']}, {props['STATE']}")
        st.write(f"**Overall Score**: {props['SUM']}")


elif page == "Map by Four Core Variables Score":
    m = folium.Map(location = [39.5, -98.35], zoom_start = 4, titles = "CartoDB positron")
    tooltip = GeoJsonTooltip(
        fields = ["NAME", "STATE", "four_SUM"],
        aliases = ["County", "State", "Score"],
        localize = True
    )
    
    score_min = map_df["four_SUM"].min()
    score_max = map_df["four_SUM"].max()
    colormap = cm.linear.YlGn_09.scale(score_min, score_max)
    colormap.caption = "Four Core Variable Score"

    folium.GeoJson(
        map_df,
        name="Core Score",
        tooltip=tooltip,
        style_function=lambda feature: {
            "fillColor": (
            colormap(feature["properties"]["four_SUM"])
            if feature["properties"]["four_SUM"] is not None
            else "#cccccc"
        ),

            "color": "black",
            "weight": 0.2,
            "fillOpacity": 0.6,
        }
    ).add_to(m)

        # 🔍 添加可选县用于高亮显示
    available_counties = map_df[map_df["SUM"].notna()][["NAME", "STATE", "GEOID"]].drop_duplicates()
    available_counties["display_name"] = available_counties["NAME"] + ", " + available_counties["STATE"]

    selected_county = st.selectbox("🔍 Highlight a County", ["None"] + sorted(available_counties["display_name"]), key = "highlight_4_core")

    if selected_county != "None":
        selected_geoid = available_counties[available_counties["display_name"] == selected_county]["GEOID"].values[0]
        highlight_geo = map_df[map_df["GEOID"] == selected_geoid]

        # 添加红色边界图层
        folium.GeoJson(
            highlight_geo,
            name="Highlighted County",
            style_function=lambda feature: {
                "fillColor": "none",
                "color": "red",
                "weight": 1,
                "fillOpacity": 0,
            },
            tooltip=GeoJsonTooltip(
                fields=["NAME", "STATE"],
                aliases=["County", "State"],
                localize=True
            )
        ).add_to(m)

    colormap.add_to(m)
    st_data = st_folium(m, width=1000, height=650)

    if st_data and st_data.get("last_active_drawing"):
        props = st_data["last_active_drawing"]["properties"]
        st.subheader(f"📍 {props['NAME']}, {props['STATE']}")
        st.write(f"**4 Variables Core Score**: {props['fore_SUM']}")

elif page == "Custom Variable Average":
    if "custom_map_generated" not in st.session_state:
        st.session_state.custom_map_generated = False

    ui_var_dict = {
        "Temperature": "Normal_temp",
        "Precipitation": "Normalized precip",
        "Population Density": "pop_den_norm",
        "Forest Proportion": "Normalized_sqrt_forest",
        "Shrub Proportion": "Normalized_log_shrub",
        "Dustiness": "dustiness_binary",
        "Birds Population": "Normal_bird",
        "Mammals Population": "Normal_mammal",
        "Reptile Population": "Normal_reptile",
        "Wind Speed": "Normal_wind",
        "Carbon Footprint": "Normal_CF",
        "Water Footprint": "Normal_WF",
        "Water Scarcity Footprint": "Normal_WSF",
        "Baseline Water Stress": "BWS_norm",
        "Water Seasonal Variability": "SV_norm",
        "Water Stress Index": "WSV_norm"
    }

    numeric_cols = list(ui_var_dict.keys())
    available_counties = map_df[map_df["SUM"].notna()][["NAME", "STATE", "GEOID"]].drop_duplicates()
    available_counties["display_name"] = available_counties["NAME"] + ", " + available_counties["STATE"]

    # ⬆️ 放到顶部的两栏
    col1, col2 = st.columns([2, 2])
    with col1:
        selected_keys = st.multiselect("📊 Select variables to calculate average", numeric_cols)
    with col2:
        selected_county = st.selectbox("🔍 Highlight a County", ["None"] + sorted(available_counties["display_name"]), key="highlight_customized")

    generate = st.button("Generate Customized Map")
    reset = st.button("Reset Map")

    if reset:
        st.session_state.custom_map_generated = False

    if selected_keys and generate:
        st.session_state.custom_map_generated = True
        st.session_state.selected_var = [ui_var_dict[var] for var in selected_keys]

    if st.session_state.custom_map_generated:
        selected_var = st.session_state.selected_var
        map_df["custom_avg"] = map_df[selected_var].mean(axis=1, skipna=True)
        m = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles="CartoDB positron")

        colormap = cm.linear.YlGn_09.scale(map_df["custom_avg"].min(), map_df["custom_avg"].max())
        colormap.caption = "Average of Selected Variables"

        tooltip = GeoJsonTooltip(
            fields=["NAME", "STATE", "custom_avg"],
            aliases=["County", "State", "Average"],
            localize=True
        )

        folium.GeoJson(
            map_df,
            name="Custom Avg",
            tooltip=tooltip,
            style_function=lambda feature: {
                "fillColor": colormap(feature["properties"]["custom_avg"]) if feature["properties"]["custom_avg"] is not None else "#cccccc",
                "color": "black",
                "weight": 0.2,
                "fillOpacity": 0.6,
            }
        ).add_to(m)

        # ➕ 高亮县的边界
        if selected_county != "None":
            selected_geoid = available_counties[available_counties["display_name"] == selected_county]["GEOID"].values[0]
            highlight_geo = map_df[map_df["GEOID"] == selected_geoid]

            folium.GeoJson(
                highlight_geo,
                name="Highlighted County",
                style_function=lambda feature: {
                    "fillColor": "none",
                    "color": "red",
                    "weight": 1.5,
                    "fillOpacity": 0,
                },
                tooltip=GeoJsonTooltip(
                    fields=["NAME", "STATE"],
                    aliases=["County", "State"],
                    localize=True
                )
            ).add_to(m)

        colormap.add_to(m)
        st_data = st_folium(m, width=1000, height=650)

        if st_data and st_data.get("last_active_drawing"):
            props = st_data["last_active_drawing"]["properties"]
            st.subheader(f"📍 {props['NAME']}, {props['STATE']}")
            st.write(f"**Custom Average**: {props['custom_avg']:.2f}")


elif page == "Weighted Score Map (Profitability vs. Environment)":
    # === 读取两个模型预测的分数 ===
    @st.cache_data
    def load_weighted_data():
        env_df = pd.read_csv("/Users/yuxuanyang/Library/CloudStorage/OneDrive-Emory/AI.X/RF_all_GEOID_scores.csv")
        env_df.rename(columns={"env_score": "env_score"}, inplace=True)
        env_df["GEOID"] = env_df["GEOID"].astype(str).str.zfill(5)

        prof_df = pd.read_csv("/Users/yuxuanyang/Library/CloudStorage/OneDrive-Emory/AI.X/RF_predicted_profitability.csv")
        prof_df.rename(columns={"predicted_profitability": "prof_score"}, inplace=True)
        prof_df["GEOID"] = prof_df["GEOID"].astype(str).str.zfill(5)

        merged = env_df.merge(prof_df, on="GEOID", how="inner")
        return merged

    score_df = load_weighted_data()

    # 合并到原始地图 dataframe
    map_weight = map_df.merge(score_df, on="GEOID", how="left")

    # 滑块选择权重
    env_weight = st.slider("🧮 Environmental Weight (Profitability = 1 - Environmental)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    map_weight["weighted_score"] = env_weight * map_weight["env_score"] + (1 - env_weight) * map_weight["prof_score"]

    # 绘制地图
    m = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles="CartoDB positron")

    # 设置颜色映射
    score_min = map_weight["weighted_score"].min()
    score_max = map_weight["weighted_score"].max()
    colormap = cm.linear.YlGnBu_09.scale(score_min, score_max)
    colormap.caption = "Weighted Score"
    colormap.add_to(m)

    # Tooltip
    tooltip = GeoJsonTooltip(
        fields=["NAME", "STATE", "weighted_score"],
        aliases=["County", "State", "Weighted Score"],
        localize=True
    )

    # 添加 GeoJSON 图层
    folium.GeoJson(
        map_weight,
        name="Weighted Score",
        tooltip=tooltip,
        style_function=lambda feature: {
            "fillColor": colormap(feature["properties"]["weighted_score"]) if feature["properties"]["weighted_score"] is not None else "#cccccc",
            "color": "black",
            "weight": 0.2,
            "fillOpacity": 0.7,
        }
    ).add_to(m)

    # 高亮选中县
    available_counties = map_weight[map_weight["weighted_score"].notna()][["NAME", "STATE", "GEOID"]].drop_duplicates()
    available_counties["display_name"] = available_counties["NAME"] + ", " + available_counties["STATE"]

    selected_county = st.selectbox("🔍 Highlight a County", ["None"] + sorted(available_counties["display_name"]), key="highlight_weighted")

    if selected_county != "None":
        selected_geoid = available_counties[available_counties["display_name"] == selected_county]["GEOID"].values[0]
        highlight_geo = map_weight[map_weight["GEOID"] == selected_geoid]

        folium.GeoJson(
            highlight_geo,
            name="Highlighted County",
            style_function=lambda feature: {
                "fillColor": "none",
                "color": "red",
                "weight": 1.2,
                "fillOpacity": 0,
            },
            tooltip=GeoJsonTooltip(
                fields=["NAME", "STATE"],
                aliases=["County", "State"],
                localize=True
            )
        ).add_to(m)

    st_data = st_folium(m, width=1000, height=650)

    # 显示点击县的详细信息
    if st_data and st_data.get("last_active_drawing"):
        props = st_data["last_active_drawing"]["properties"]
        st.subheader(f"📍 {props['NAME']}, {props['STATE']}")
        st.write(f"**Weighted Score (env_weight={env_weight:.2f})**: {props['weighted_score']:.3f}")
