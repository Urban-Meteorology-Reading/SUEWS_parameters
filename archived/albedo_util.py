import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import supy as sp
import os
from shutil import copyfile
import geopandas as gpd
import pickle
pd.options.mode.chained_assignment = None
from IPython.display import clear_output

def generate_array_dif(attrs_site, attr,level):
    dar = [0.75,0.5,.25]
    dar[level] = attrs_site[attr].values[0]
    return dar


def generate_array_same(attrs_site, attr):
    a = attrs_site[attr].values[0]
    return [a, a, a]


def modify_attr(df_state_init, df, name):

    all_attrs = pd.read_csv('all_attrs.csv')
    attrs_site = all_attrs[all_attrs.site == name]
    df_state_init.loc[:, 'emissionsmethod'] = 0

    if attrs_site.land.values[0] == 'DecTr':
        ar = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
        level = 1
        df_state_init.albmin_dectr=attrs_site['albmin'].values[0]
        df_state_init.albmax_dectr=attrs_site['albmax'].values[0]
        df_state_init.albdectr_id=df_state_init.albmin_dectr
        df_state_init.loc[:, 'dectreeh'] = attrs_site.height.values[0]

    elif attrs_site.land.values[0] == 'EveTr':
        ar = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
        level = 0
        df_state_init.albmin_evetr=attrs_site['albmin'].values[0]
        df_state_init.albmax_evetr=attrs_site['albmax'].values[0]
        df_state_init.albevetr_id=df_state_init.albmin_evetr
        df_state_init.loc[:, 'evetreeh'] = attrs_site.height.values[0]

    elif attrs_site.land.values[0] == 'Grass':
        ar = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
        level = 2
        df_state_init.albmin_grass=attrs_site['albmin'].values[0]
        df_state_init.albmax_grass=attrs_site['albmax'].values[0]
        df_state_init.loc[:,'roughlenmommethod']=1
        df_state_init.albgrass_id=df_state_init.albmin_grass
        df_state_init.loc[:,'z0m_in']=attrs_site.height.values[0]*.1
        df_state_init.loc[:,'zdm_in']=attrs_site.height.values[0]*.7

    else:
        print('The land cover type is not found! using the default one')

    df_state_init.loc[:, 'sfr'] = ar
    df_state_init.loc[:, 'lat'] = df.Latitude.values[0].values[0]
    df_state_init.loc[:, 'lng'] = df.Longitude.values[0].values[0]
    df_state_init.loc[:, 'z'] = attrs_site.meas.values[0]
    df_state_init.loc[:, 'laimin'] = generate_array_dif(attrs_site, 'laimin',level)
    df_state_init.loc[:, 'laimax'] = generate_array_dif(attrs_site, 'laimax',level)
    df_state_init.loc[:, 'gddfull'] = generate_array_same(attrs_site, 'gddfull')
    df_state_init.loc[:, 'sddfull'] = generate_array_same(attrs_site, 'sddfull')
    df_state_init.loc[:, 'basete'] = generate_array_same(attrs_site, 'basete')
    df_state_init.loc[:, 'baset'] = generate_array_same(attrs_site, 'baset')
    df_state_init.lai_id = df_state_init.loc[:, 'laimin']
    
    

    return df_state_init,level



def func_parse_date(year, doy, hour, min):
        dt = pd.to_datetime(' '.join(
            [str(k) for k in [year, doy, hour, min]]),
            format='%Y %j %H %M')
        return dt


def read_plot(years,name,multiple_run=0,botyl=False,topyl=False):

    for year in years:
        print(name+'-'+str(year))
        df=pd.read_csv('data_csv_zip_clean/'+name+'_clean.csv.gz')
        df.time=pd.to_datetime(df.time)
        df=df.set_index(['time'])


        period_start=str(year)+'-01-01'
        period_end=str(year+1)+'-01-01'
        df_period=df[(df.index>=period_start) & (df.index<period_end)]



        df_period=df_period[df_period.SWIN>5]
        df_period=df_period[(df_period.index.hour <=14) & (df_period.index.hour >=10)]
        alb_raw=df_period['SWOUT']/df_period['SWIN']
        alb_raw=alb_raw.resample('1D').mean()
        alb=alb_raw[(alb_raw>0) & (alb_raw<1)]


        alb_avg_day=pd.DataFrame(alb,columns=['alb'])



        a=alb_avg_day.index.strftime('%j')
        alb_avg_day['DOY']=[int(b) for b in a]


        copyfile("./runs/data/"+name+"_"+str(year)+"_data_60.txt", "runs/run/input/Kc_2012_data_60.txt")
        df_forcing=pd.read_csv('runs/run'+'/Input/'+'kc'+'_'+'2012'+'_data_60.txt',sep=' ',
                                        parse_dates={'datetime': [0, 1, 2, 3]},
                                        keep_date_col=True,
                                        date_parser=func_parse_date)


        
        df_forcing.loc[:,'snow']=.8
        rol=df_forcing.Tair.rolling(5).mean()
        snowdetected=1
        for i in range(len(df_forcing)):

            if snowdetected==1:
                if rol.iloc[i]>=5:
                    df_forcing.loc[df_forcing.iloc[i].name,'snow']=0
                    snowdetected=0
                else:
                    df_forcing.loc[df_forcing.iloc[i].name,'snow']=0.8
            else:
                df_forcing.loc[df_forcing.iloc[i].name,'snow']=0


            if (df_forcing.iloc[i].Tair<0) and (df_forcing.iloc[i].rain>0):
                df_forcing.loc[df_forcing.iloc[i].name,'snow']=0.8
                snowdetected=1
                

        all_sites_info =  pd.read_csv('site_info.csv')
        site_info=all_sites_info[all_sites_info['Site Id'] == name]
        df = pd.DataFrame(
            {'Site': [name],
            'Latitude': [site_info['Latitude (degrees)']],
            'Longitude': [site_info['Longitude (degrees)']]})

        

        path_runcontrol = Path('runs/run'+'/') / 'RunControl.nml'
        df_state_init = sp.init_supy(path_runcontrol)


        df_state_init,level=modify_attr(df_state_init, df, name)

        if level==1:
            attrs=[
                df_state_init.albmin_dectr,
                df_state_init.albmax_dectr
                ]
        elif level==0:
            attrs=[
                df_state_init.albmin_evetr,
                df_state_init.albmax_evetr
                ]
        elif level ==2:
            attrs=[
                df_state_init.albmin_grass,
                df_state_init.albmax_grass
                ]

        with open('albedo/'+name+'-attrs_albedo','wb') as f:
            pickle.dump(attrs, f)
        
        grid = df_state_init.index[0]
        df_forcing_run = sp.load_forcing_grid(path_runcontrol, grid)
    
        if multiple_run == 0:
            df_output, df_state_final = sp.run_supy(df_forcing_run, df_state_init, save_state=False)

        if multiple_run == 1:
            error=20
            for i in range(10):

                if (error <= 0.1):
                    break
                df_output, df_state_final = sp.run_supy(df_forcing_run, df_state_init,save_state=False)
                final_state = df_state_final[df_state_init.columns.levels[0]].iloc[1]
                df_state_init.iloc[0] = final_state
                soilstore_before = df_state_final.soilstore_id.iloc[0]
                soilstore_after = df_state_final.soilstore_id.iloc[1]
                diff_soil = sum(abs(soilstore_after-soilstore_before))
                error = 100*diff_soil/soilstore_before.mean()
                print(error) 

        df_output_2=df_output.SUEWS.loc[grid]
        df_output_2=df_output_2[df_output_2.index.year>=year]
   
        alb_model=pd.DataFrame(df_output_2.AlbBulk)
        a=alb_model.index.strftime('%j')
        alb_model['DOY']=[int(b) for b in a]


        Tair=df_forcing_run.Tair.resample('1d', closed='left',label='right').mean()
        Tair=pd.DataFrame(Tair)
        a=Tair.index.strftime('%j')
        Tair['DOY']=[int(b) for b in a]

        lai=df_output_2.LAI
        lai=lai.resample('1d', closed='left',label='right').mean()
        lai=pd.DataFrame(lai)
        a=lai.index.strftime('%j')
        lai['DOY']=[int(b) for b in a]

        snow=df_forcing.snow
        snow.index=df_forcing.datetime
        snow=snow.resample('1D').mean()
        snow=pd.DataFrame(snow)
        a=snow.index.strftime('%j')
        snow['DOY']=[int(b) for b in a]

        rain=df_forcing_run.rain
        rain=rain.resample('1d', closed='left',label='right').sum()
        rain=pd.DataFrame(rain)
        a=rain.index.strftime('%j')
        rain['DOY']=[int(b) for b in a]

        SMD=df_output_2.SMD
        SMD=SMD.resample('1d', closed='left',label='right').mean()
        SMD=pd.DataFrame(SMD)
        a=SMD.index.strftime('%j')
        SMD['DOY']=[int(b) for b in a]

        out={'obs':{'x':alb_avg_day.DOY,'y':alb_avg_day.alb},
            'model':{'x':alb_model.DOY,'y':alb_model.AlbBulk},
            'Tair':{'x':Tair.DOY,'y':Tair.Tair},
            'lai':{'x':lai.DOY,'y':lai.LAI},
            'snow':{'x':snow.DOY,'y':snow.snow},
            'rain':{'x':rain.DOY,'y':rain.rain},
            'smd':{'x':SMD.DOY,'y':SMD.SMD},
            }
        with open('output/'+name+'-'+str(year),'wb') as f:
            pickle.dump(out, f)

        clear_output()
    fig,axs=plt.subplots(len(years),1,figsize=(5,5))
    counter=-1
    for year in years:
        counter += 1
        try:
            ax=axs[counter]
        except:
            ax=axs
        with open('output/'+name+'-'+str(year),'rb') as f:
            out=pickle.load(f)
        ax.scatter(out['obs']['x'],out['obs']['y'],color='r',label='Obs')
        ax.plot(out['model']['x'],out['model']['y'],color='k',label='Model')
        ax.legend()
        if topyl!=False:
            ax.set_ylim(top=topyl)
        if botyl!=False:
            ax.set_ylim(bottom=botyl)         
        ax.set_title(name+'-'+str(year))
    plt.savefig('figs/'+name+'-albedo.png',dpi=300,bbox_inches = 'tight',pad_inches = 0.01)