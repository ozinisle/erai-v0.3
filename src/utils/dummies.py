def getSampleDataFrame():
    
    # Import pandas library 
    import pandas as pd 

    # initialize list of lists 
    data1 = [[1,'chokalingam', 10], [2,'samy', 15], [3,'raja', 14], [4,'pandi', 14], [5,'palani', 14]] 
    data2 = [[4,'rajapandi', 14], [5,'palani muthu', 14],[20,'Sathappan', 10], [21,'Veilmuthu', 15], [23,'velraj', 14], [24,'balamurugan', 14], [25,'chinnathambi', 14]] 

    # Create the pandas DataFrame 
    df1 = pd.DataFrame(data1, columns = ['#','Name', 'Age']) 
    df2 = pd.DataFrame(data2, columns = ['#','Name', 'Age']) 

    # print dataframe. 
    return df1,df2 