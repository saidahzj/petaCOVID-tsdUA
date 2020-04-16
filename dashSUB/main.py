

import pandas as pd  # provides interface for interacting with tabular data
import geopandas as gpd  # combines the capabilities of pandas and shapely for geospatial operations
from shapely.geometry import Point, Polygon, MultiPolygon  # for manipulating text data into geospatial shapes
from shapely import wkt  # stands for "well known text," allows for interchange across GIS programs
import rtree  # supports geospatial join
import os
import descartes
import csv
import json

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer


root_path = os.getcwd()
#print(root_path)
puds = gpd.read_file(root_path+'\input\Kelurahan_Surabaya_2017.shp', crs = {'init' :'epsg:4326'})#[['name','geometry']]

#puds.rename(columns = {'name' : 'Kelurahan'}, inplace= True)
#puds.sample()
#print(puds[['is_in_muni','name']])



#puds.info()
#puds.to_csv(root_path+'\kelurahansub.csv', index = False, header = True)
#puds.plot(column='name', legend=True, figsize=(16,8))


datafile = root_path+'\input\covid7aprsub.csv'
#Read csv file using pandas
df = pd.read_csv(datafile, names = ['Tanggal','Wilayah','Kecamatan','Kelurahan','Konfirmasi','Konfirmasi Sembuh','Konfirmasi Meninggal','PDP','PDP Sembuh','PDP Meninggal','ODP','ODP Dipantau','ODP Selesai Dipantau'], skiprows = 1)
#print(df.head())
#df.info()


#Ini bisa dikasih input tanggal dropdown
#df[df['Kelurahan'].isnull()]
pilihantanggal = '07-04-20'
df_tanggal = df[df['Tanggal'] == pilihantanggal]
print(df_tanggal)
#print(df['Konfirmasi'].max())

mergeset = puds.merge(df_tanggal, left_on= 'is_in_muni', right_on='Kecamatan')

print(mergeset[['Kecamatan','Kelurahan', 'Konfirmasi' ,'geometry']])
mergeset.info()


#ubah GEOjson.
merged_json = json.loads(mergeset.to_json())
json_data = json.dumps(merged_json)


#Oper data GEOJson ke parser
geosource = GeoJSONDataSource(geojson = json_data)
#ganti palet, acuan ke brewerDOC
palette = brewer['YlOrRd'][6]
#Reverse color order -> Semakin parah semakin gelap
palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 5)
#Define custom tick labels for color bar.
tick_labels = {'0': '0', '1': '1', '2':'2', '3':'3', '4':'4', '5':'5'}
#Create color bar.
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
#Create figure object.
p = figure(title = 'Konfirmasi Positif COVID-19 Per Kelurahan di Surabaya', plot_height = 600 , plot_width = 950, toolbar_location = None)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
#Add patch renderer to figure. #field bisa disesuaikan input mau odp pdp atau konfirm
p.patches('xs','ys', source = geosource,fill_color = {'field' :'Konfirmasi', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify figure layout.
p.add_layout(color_bar, 'below')



show(p)

