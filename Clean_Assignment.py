import pandas as pd


def read_in_file(path,number_of_assignment,each_score,weight):

    result_name = ["R" + str(x) for x in range(1,number_of_assignment+1)]
    score_name = ["S" + str(x) for x in range(1, number_of_assignment + 1)]

    df = pd.read_csv(path)
    df = df.fillna(0)

    df_with_score = df.copy()
    df_with_score = add_score_column(number_of_assignment, each_score, df_with_score)
    df_calculate_score = calculate_score(number_of_assignment, df_with_score)


    list_find_min = find_min(number_of_assignment, df)

    df_find_min = find_min_column(list_find_min, df)
    print(df_find_min)

    find_result, df_calculate_score = result(df_find_min, df_calculate_score,result_name,score_name, weight)

    path_name = ("/").join(path.split('/')[:-1])+'/Result.csv'
    path_name_1 = ("/").join(path.split('/')[:-1]) + '/Result_1.csv'
    find_result.to_csv(path_name)
    df_calculate_score.to_csv(path_name_1)


def add_score_column(number_of_assignment, each_score, df):
    for i in range(1,number_of_assignment+1):
        df["S"+str(i)] = each_score[i-1]
    return df


def calculate_score(number_of_assignment,df):
    for i in range(1,number_of_assignment+1):
        df["R"+str(i)] = df["A"+str(i)]*df["S"+str(i)]
    return df


def find_min(number_of_assignment, df,skipna=False):
    minValuesObj = df.min(axis=1)
    #print(minValuesObj.tolist())
    return minValuesObj.tolist()


def find_min_column(list_find_min, df):
    for i,r in df.iterrows():
        for x in df.columns:
            if df.at[i, x] ==  list_find_min[i]:
                df.at[i, 'Min'] = x
    return df['Min'].tolist()


def result(df_find_min, df_calculate_score,result_name, score_name,weight):
    for i,r in df_calculate_score.iterrows():
        result_name_copy = result_name.copy()
        result_name_copy.remove("R"+df_find_min[i][1:])
        score_name_copy = score_name.copy()
        score_name_copy.remove("S"+ df_find_min[i][1:])
        #print(assignment_name_copy)
        #print(df_calculate_score.loc[i, assignment_name])
        df_calculate_score.at[i,'Score'] = df_calculate_score.loc[i, result_name_copy].sum()
        df_calculate_score.at[i,'total'] = df_calculate_score.loc[i,score_name_copy].sum()
        df_calculate_score.at[i, 'Result'] = round(df_calculate_score.at[i,'Score']/df_calculate_score.at[i,'total']*weight, 2)
    df_sub = df_calculate_score[['Last name', 'First name', 'Score', 'total', 'Result']]
    return df_sub, df_calculate_score



path = "/Users/xinyue/Documents/college/TA_Work/Econ 360 Fall 2019/Assignment/Detailed_Homework_Results.csv"
number_of_assignment = 8
each_score = [18,39,49,16,20,40,22,35]
weight = 25
read_in_file(path,number_of_assignment,each_score,weight)