import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from datetime import timedelta


class preprocessing():

    def __init__(self,path) -> None:
        """ Preprocessing class for data cleaning and feature engineering
        Args:
            path (_type_): directory of the data
        """        
        self.path = path
        self.date_i = 'Fecha-I'
        self.date_o = 'Fecha-O'


    def read_data(self):
        data = pd.read_csv(self.path)
        return data
    
    def validate(self, df,date_col):
        try:
            df[date_col] = df[date_col].astype(str).apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
            )
            print("The date format is correct")

        except ValueError:
            raise ValueError( 
                "The date format is incorrect, should be  YYYY-MM-DD HH:MM:SS"
            )
        return df
    ## Feature Engineering

    def get_high_seasson(self,df):
        """ Function to get high season depending on the date of the reservation

        Args:
            df (_type_): dataframe with the date column

        Returns:
            _type_: dataframe with the high season feature
        """        
        range_season1 = ((df[self.date_i].dt.month == 12) & (df[self.date_i].dt.day >= 15)) | ((df[self.date_i].dt.month == 1) | (df[self.date_i].dt.month == 2) | ((df[self.date_i].dt.month == 3) & (df[self.date_i].dt.day <= 3)))
        range_season2 = ((df[self.date_i].dt.month == 7) & (df[self.date_i].dt.day >= 15) & (df[self.date_i].dt.day <= 31))
        range_season3 = ((df[self.date_i].dt.month == 9) & (df[self.date_i].dt.day >= 11) & (df[self.date_i].dt.day <= 30))
    
        df.loc[range_season1 | range_season2 | range_season3,'high_season'] = 1 # high season
        df.high_season = df.high_season.fillna(0) # low season
        
        #This function is used to create a new column in the dataframe, but its inneficient because read three times the dataframe, so we can
        # fix this using chining or pipelines in pandas. For time reasons we will not fix this.
        self.synthetic_features['high_season'] = df.high_season
        return df
    
    def get_min_diff(self,df):

        """Function to get the difference between the date of the reservation and the date of the check in

        Returns:
            _type_: DataFrame-> dataframe with the min_diff feature
        """                
        df['min_diff'] = (df['Fecha-O']-df['Fecha-I'])/timedelta(minutes=1)
        self.synthetic_features['min_diff'] = df['min_diff']
        return df
    
    def get_period_day(self,df):
        
        """Function to get the period of the day depending on the date of the reservation

        Returns:
            _type_: DataFrame with the new columns named 'period_day'
        """        
        df.loc[((df['Fecha-I'].dt.hour>=5 )& (df['Fecha-I'].dt.hour<12)),'period_day'] = 'morning'
        df.loc[((df['Fecha-I'].dt.hour>=12 )& (df['Fecha-I'].dt.hour<19)),'period_day'] = 'afternoon'
        df.loc[((df['Fecha-I'].dt.hour>=19 )| (df['Fecha-I'].dt.hour<5)),'period_day'] = 'night'
        self.synthetic_features['period_day'] = df['period_day']
        return df
    
    def get_delay_15(self,df):
        """Function to get if a flight had delay more than 15 minutes"""
        df['delay_15'] = np.where(df['min_diff'].astype(float) > 15, 1, 0)
        self.synthetic_features['delay_15'] = np.where(df['min_diff'].astype(float) > 15, 1, 0)
        return df

    def pipeline(self):
        self.df = self.read_data() # read data
        self.synthetic_features = pd.DataFrame() # create empty dataframe
        self.df = self.validate(self.df,self.date_i) # validate date format
        self.df = self.validate(self.df,self.date_o) # validate date format
        self.df = self.get_high_seasson(self.df) # get high season
        self.df = self.get_min_diff(self.df) # get difference between dates in minutes
        self.df = self.get_period_day(self.df) # get period day
        self.df = self.get_delay_15(self.df) # get delay 15
        self.synthetic_features.to_csv('./synthetic_features.csv',index=False) # save synthetic features


