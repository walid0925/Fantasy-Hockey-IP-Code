import argparse
import numpy as np
import pandas as pd

def main():
    dk_df = pd.read_csv(args.dkfile)

    gdf = dk_df[dk_df['Position']=='G']
    gdf = gdf[['Name', 'Salary', 'TeamAbbrev', 'Game Info']]

    sdf = dk_df[dk_df['Position']!='G']
    sdf = sdf[['Name', 'Salary', 'TeamAbbrev', 'Game Info']]

    def split_names(df):
        """
        Split the player names into first and last
        """
        firstlast = df['Name'].str.split(' ', n=1, expand=True)
        df['First Name'] = firstlast[0]
        df['Last Name'] = firstlast[1]
        df = df.drop('Name', axis=1)
        return df

    def get_opponent(x):
        """
        get opponent for one row of the df
        """
        a_b = x['Game Info'].split(' ')[0].split('@')
        opponent = [t for t in a_b if t != x['TeamAbbrev']]
        return opponent


    gdf['Opponent'] = gdf.apply(get_opponent, axis=1, result_type='expand')
    gdf.drop(['Game Info'], axis=1, inplace=True)
    sdf['Opponent'] = sdf.apply(get_opponent, axis=1, result_type='expand')
    sdf.drop(['Game Info'], axis=1, inplace=True)

    gdf = split_names(gdf)
    sdf = split_names(sdf)

    gdf = gdf.rename(columns={'TeamAbbrev': 'Team'})
    sdf = sdf.rename(columns={'TeamAbbrev': 'Team'})

    cols = ['First Name', 'Last Name', 'Salary', 'Team', 'Opponent']
    gdf = gdf[cols]
    sdf = sdf[cols]

    gdf.to_csv(args.gkoutfile, index=False)
    sdf.to_csv(args.skoutfile, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dkfile',
        type=str,
        help='path to DK csv file'
    )
    parser.add_argument(
        '--gkoutfile',
        type=str,
        help='path to output goalie csv'
    )
    parser.add_argument(
        '--skoutfile',
        type=str,
        help='path to output skaters csv'
    )

    args = parser.parse_args()
    main()
