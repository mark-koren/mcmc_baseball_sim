import numpy as np
import pandas as pd
import pdb
from scipy.stats import beta
import time
from os import listdir
import os
import shutil
from os.path import isfile, join
import wget
import copy
from zipfile import ZipFile
import progressbar

from player import Player
from team import Team
from game import Game
from league import League

BEVENT_COLUMN_NAMES = [
    'game_id',
    'visiting_team',
    'inning',
    'batting_team',
    'outs',
    'balls',
    'strikes',
    'pitch_sequence',
    'vis_score',
    'home_score',
    'batter',
    'batter_hand',
    'res_batter',
    'res_batter_hand',
    'pitcher',
    'pitcher_hand',
    'res_pitcher',
    'res_pitcher_hand',
    'catcher',
    'first_base',
    'second_base',
    'third_base',
    'shortstop',
    'left_field',
    'center_field',
    'right_field',
    'first_runner',
    'second_runner',
    'third_runner',
    'event_text',
    'leadoff_flag',
    'pinchhit_flag',
    'defensive_position',
    'lineup_position',
    'event_type',
    'batter_event_flag',
    'ab_flag',
    'hit_value',
    'sh_flag',
    'sf_flag',
    'outs_on_play',
    'double_play_flag',
    'triple_play_flag',
    'rbi_on_play',
    'wild_pitch_flag',
    'passed_ball_flag',
    'fielded_by',
    'batted_ball_type',
    'bunt_flag',
    'foul_flag',
    'hit_location',
    'num_errors',
    '1st_error_player',
    '1st_error_type',
    '2nd_error_player',
    '2nd_error_type',
    '3rd_error_player',
    '3rd_error_type',
    'batter_dest',
    'runner_on_1st_dest',
    'runner_on_2nd_dest',
    'runner_on_3rd_dest',
    'play_on_batter',
    'play_on_runner_on_1st',
    'play_on_runner_on_2nd',
    'play_on_runner_on_3rd',
    'sb_for_runner_on_1st_flag',
    'sb_for_runner_on_2nd_flag',
    'sb_for_runner_on_3rd_flag',
    'cs_for_runner_on_1st_flag',
    'cs_for_runner_on_2nd_flag',
    'cs_for_runner_on_3rd_flag',
    'po_for_runner_on_1st_flag',
    'po_for_runner_on_2nd_flag',
    'po_for_runner_on_3rd_flag',
    'responsible_pitcher_for_runner_on_1st',
    'responsible_pitcher_for_runner_on_2nd',
    'responsible_pitcher_for_runner_on_3rd',
    'new_game_flag',
    'end_game_flag',
    'pinch_runner_on_1st',
    'pinch_runner_on_2nd',
    'pinch_runner_on_3rd',
    'runner_removed_for_pinch_runner_on_1st',
    'runner_removed_for_pinch_runner_on_2nd',
    'runner_removed_for_pinch_runner_on_3rd',
    'batter_removed_for_pinch_hitter',
    'position_of_batter_removed_for_pinch_hitter',
    'fielder_with_first_putout',
    'fielder_with_second_putout',
    'fielder_with_third_putout',
    'fielder_with_first_assist',
    'fielder_with_second_assist',
    'fielder_with_third_assist',
    'fielder_with_fourth_assist',
    'fielder_with_fifth_assist',
    'event_num'
]

BGAME_COLUMN_NAMES = [
    'game_id',
    'date',
    'game_number',
    'day_of_week',
    'start_time',
    'dh_used_flag',
    'day_night_flag',
    'visiting_team',
    'home_team',
    'game_site',
    'vis_starting_pitcher',
    'home_starting_pitcher',
    'home_plate_umpire',
    'first_base_umpire',
    'second_base_umpire',
    'third_base_umpire',
    'left_field_umpire',
    'right_field_umpire',
    'attendance',
    'ps_scorer',
    'translator',
    'inputter',
    'input_time',
    'edit_time',
    'how_scored',
    'pitches_entered',
    'temperature',
    'wind_direction',
    'wind_speed',
    'field_condition',
    'precipitation',
    'sky',
    'time_of_game',
    'number_of_innings',
    'visitor_final_score',
    'home_final_score',
    'visitor_hits',
    'home_hits',
    'visitor_errors',
    'home_errors',
    'visitor_left_on_base',
    'home_left_on_base',
    'winning_pitcher',
    'losing_pitcher',
    'save_for',
    'gw_rbi',
    'visitor_batter_1',
    'visitor_position_1',
    'visitor_batter_2',
    'visitor_position_2',
    'visitor_batter_3',
    'visitor_position_3',
    'visitor_batter_4',
    'visitor_position_4',
    'visitor_batter_5',
    'visitor_position_5',
    'visitor_batter_6',
    'visitor_position_6',
    'visitor_batter_7',
    'visitor_position_7',
    'visitor_batter_8',
    'visitor_position_8',
    'visitor_batter_9',
    'visitor_position_9',
    'home_batter_1',
    'home_position_1',
    'home_batter_2',
    'home_position_2',
    'home_batter_3',
    'home_position_3',
    'home_batter_4',
    'home_position_4',
    'home_batter_5',
    'home_position_5',
    'home_batter_6',
    'home_position_6',
    'home_batter_7',
    'home_position_7',
    'home_batter_8',
    'home_position_8',
    'home_batter_9',
    'home_position_9',
    'visitor_finishing_pitcher',
    'home_finishing_pitcher',
    'name_of_official_scorer'
]
ROS_COLUMN_NAMES = [
    'player_id',
    'first_name',
    'last_name',
    'batter_hand',
    'pitcher_hand',
    'team',
    'primary_position'
]


def load_retrosheet_as_df(df_name, path, column_names, index_col=None):
    # General helper to load a retrosheet file into a pandas dataframe
    return pd.read_csv(join(path, df_name), names=column_names, index_col=index_col)


def load_retrosheet_bev_as_df(df_name, path='./data/retrosheet_pbp'):
    # Helper function to load a BEV file into a pandas dataframe
    return load_retrosheet_as_df(df_name=df_name, path=path, column_names=BEVENT_COLUMN_NAMES)


def load_retrosheet_bga_as_df(df_name, path='./data/retrosheet_pbp'):
    # Helper function to load a BGA file into a pandas dataframe
    return load_retrosheet_as_df(df_name=df_name, path=path, column_names=BGAME_COLUMN_NAMES, index_col='game_id')


def load_retrosheet_ros_as_df(df_name, path='./data/retrosheet_pbp'):
    # Helper function to load a ROS file into a pandas dataframe
    return load_retrosheet_as_df(df_name=df_name, path=path, column_names=ROS_COLUMN_NAMES)


def get_parse_build_retrosheet_years(path, start_year=2018, end_year=2019, get_data=True, parse_data=True,
                                     build_df=True, keep_data=False):
    cwd = os.getcwd()

    # Download and unzip the bevent tool
    if parse_data and not os.path.isfile('BEVENT.EXE'):
        url = 'https://www.retrosheet.org/bevent19.zip'
        zipped_filename = wget.download(url)
        with ZipFile(zipped_filename, 'r') as zipObj:
            zipObj.extractall()
        os.remove(zipped_filename)

    # Download and unzip the bgame tool
    if parse_data and not os.path.isfile('BGAME.EXE'):
        url = 'https://www.retrosheet.org/bgame19.zip'
        zipped_filename = wget.download(url)
        with ZipFile(zipped_filename, 'r') as zipObj:
            zipObj.extractall()
        os.remove(zipped_filename)

    years = np.arange(end_year - start_year + 1) + start_year
    for year in years:

        year_path = join(path, str(year))
        if not os.path.isdir(year_path):
            os.mkdir(year_path)

        if get_data:
            # Download the zipfile from retrosheet.org
            url = 'https://www.retrosheet.org/events/' + str(year) + 'eve.zip'
            zipped_filename = wget.download(url)
            # Unzip the data to a new folder
            with ZipFile(zipped_filename, 'r') as zipObj:
                zipObj.extractall(year_path)
            os.remove(zipped_filename)

        if parse_data:
            # Move bevent to folder and run
            shutil.move(join(cwd, 'BEVENT.EXE'), join(year_path, 'BEVENT.EXE'))
            os.chdir(year_path)
            bevent_cmd = 'wine bevent -f 0-96 -y ' + str(year) + ' ' + str(year) + '*.EV* > ' + str(year) + 'MLB.BEV'
            os.system(bevent_cmd)
            shutil.move(join(year_path, 'BEVENT.EXE'), join(cwd, 'BEVENT.EXE'))
            os.chdir(cwd)

            # Move bgame to folder and run
            shutil.move(join(cwd, 'BGAME.EXE'), join(year_path, 'BGAME.EXE'))
            os.chdir(year_path)
            bgame_cmd = 'wine bgame  -y ' + str(year) + ' ' + str(year) + '*.EV* > ' + str(year) + 'MLB.BGA'
            os.system(bgame_cmd)
            shutil.move(join(year_path, 'BGAME.EXE'), join(cwd, 'BGAME.EXE'))
            os.chdir(cwd)

            # Combine the ROS files
            combine_ros_files(path=year_path, out_filename=str(year) + 'MLB.ROS')
        if build_df:
            # Build and save the batter and pitcher databases
            # print('Building batter df for year %d' % (year))
            # batter_df = build_batter_year_df(path=year_path, df_name=str(year) + 'MLB.BEV',
            #                                  rosname=str(year) + 'MLB.ROS')
            # batter_df = batter_df.set_index('player_id')
            # batter_df.to_csv(join(path, str(year) + '_batter.csv'))
            # print('Building pitcher df for year %d' % (year))
            # pitcher_df = build_pitcher_year_df(path=year_path, df_name=str(year) + 'MLB.BEV',
            #                                    ros_name=str(year) + 'MLB.ROS')
            # pitcher_df = pitcher_df.set_index('player_id')
            # pitcher_df.to_csv(join(path, str(year) + '_pitcher.csv'))
            #
            # print('Building pitcher fatigue df for year %d' % (year))
            # fatigue_df = build_pitcher_year_fatigue_df(path=year_path, df_bev_name=str(year) + 'MLB.BEV',
            #                                            df_bga_name=str(year) + 'MLB.BGA', ros_name=str(year) + 'MLB.ROS')
            # league_sum = fatigue_df.sum()
            # league_sum['player_id'] = 'LEAGUE'
            # league_sum['team_id'] = 'LEAGUE'
            # fatigue_df = fatigue_df.append(league_sum, ignore_index=True)
            # fatigue_df.to_csv(join(path, str(year) + '_fatigue.csv'))

            print('Building team df for year %d' % (year))
            team_df = build_team_year_df(path=year_path, df_name=str(year) + 'MLB.BEV',
                                         team_filename='TEAM' + str(year))
            team_df = team_df.set_index('team_id')
            team_df.loc['LEAGUE'] = team_df.sum()
            team_df.to_csv(join(path, str(year) + '_team.csv'))

        # Clean up
        if not keep_data:
            shutil.rmtree(year_path)

    # Delete bevent and bgame
    if not keep_data:
        os.remove(join(cwd, 'BEVENT.EXE'))
        os.remove(join(cwd, 'BGAME.EXE'))


def combine_ros_files(path, out_filename='all.ROS'):
    list_of_filepaths = [join(path, f) for f in listdir(path) if
                         (isfile(join(path, f)) and f.lower().endswith('.ros'))]

    players = []
    lines = []
    for file in list_of_filepaths:
        with open(file, 'r') as f:
            for line in f.readlines():
                player = line.split(',')[0]
                if player not in players:
                    players.append(player)
                    lines.append(line)

    with open(join(path, out_filename), 'w') as f:
        f.writelines(lines)


def get_batter_stats(df):
    data = {'single': 0,
            'double': 0,
            'triple': 0,
            'homerun': 0,
            'walk': 0,
            'hbp':0,
            'error':0,
            'out': 0,
            'productive_out': 0}

    for at_bat in df.itertuples(False):
        if at_bat.event_type == 20:
            data['single'] = data['single'] + 1
        elif at_bat.event_type == 21:
            data['double'] = data['double'] + 1
        elif at_bat.event_type == 22:
            data['triple'] = data['triple'] + 1
        elif at_bat.event_type == 23:
            data['homerun'] = data['homerun'] + 1
        elif at_bat.event_type == 14 or at_bat.event_type == 15:
            data['walk'] = data['walk'] + 1
        elif at_bat.event_type == 16:
            data['hbp'] = data['hbp'] + 1
        elif at_bat.event_type == 18:
            data['error'] = data['error'] + 1
        elif at_bat.event_type == 2 or at_bat.event_type == 3:
            data['out'] = data['out'] + 1

            try:
                productive_out = False
                if isinstance(at_bat.first_runner, str) and at_bat.runner_on_1st_dest > 1:
                    productive_out = True
                elif isinstance(at_bat.second_runner, str) and at_bat.runner_on_2nd_dest > 2:
                    productive_out = True
                elif isinstance(at_bat.third_runner, str) and at_bat.runner_on_3rd_dest > 3:
                    productive_out = True
                if productive_out:
                    data['productive_out'] = data['productive_out'] + 1
            except:
                import pdb;
                pdb.set_trace()

    return data


def get_runner_stats(df_1st, df_2nd):
    data = {'s31st_success': 0,
            's31st_fail': 0,
            'dh1st_success': 0,
            'dh1st_fail': 0,
            'sh2nd_success': 0,
            'sh2nd_fail': 0,
            }

    for at_bat in df_1st.itertuples(False):
        if at_bat.event_type == 20:
            # Single with runner on 1st
            if at_bat.runner_on_1st_dest == 3:
                data['s31st_success'] = data['s31st_success'] + 1
            if at_bat.runner_on_1st_dest == 2:
                data['s31st_fail'] = data['s31st_fail'] + 1
        elif at_bat.event_type == 21:
            # Double with runner on 1st
            if at_bat.runner_on_1st_dest == 4:
                data['dh1st_success'] = data['dh1st_success'] + 1
            if at_bat.runner_on_1st_dest == 3:
                data['dh1st_fail'] = data['dh1st_fail'] + 1

    for at_bat in df_2nd.itertuples(False):
        if at_bat.event_type == 20:
            # Single with runner on 2nd
            if at_bat.runner_on_2nd_dest == 4:
                data['sh2nd_success'] = data['sh2nd_success'] + 1
            if at_bat.runner_on_2nd_dest == 3:
                data['sh2nd_fail'] = data['sh2nd_fail'] + 1

    return data


def build_batter_year_df(path, df_name, rosname):
    df = load_retrosheet_bev_as_df(df_name=df_name, path=path)
    data_list = []
    num_lines = sum(1 for line in open(join(path, rosname)))
    with open(join(path, rosname), 'r') as f:
        bar = progressbar.ProgressBar(maxval=num_lines + 1,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for counter, line in enumerate(f.readlines()):
            bar.update(counter)
            player_id = line.split(',')[0]

            df_player_batting = df[df.loc[:, 'batter'].str.contains(player_id)]
            df_player_batting_v_l = df_player_batting[df_player_batting.loc[:, 'pitcher_hand'].str.contains('L')]
            data_v_l = get_batter_stats(df_player_batting_v_l)
            df_player_batting_v_r = df_player_batting[df_player_batting.loc[:, 'pitcher_hand'].str.contains('R')]
            data_v_r = get_batter_stats(df_player_batting_v_r)

            df_no_na = df[df.loc[:, 'first_runner'].notna()]
            df_player_on_1st = df_no_na[df_no_na.loc[:, 'first_runner'].str.contains(player_id)]
            df_no_na = df[df.loc[:, 'second_runner'].notna()]
            df_player_on_2nd = df_no_na[df_no_na.loc[:, 'second_runner'].str.contains(player_id)]
            data_running = get_runner_stats(df_player_on_1st, df_player_on_2nd)

            data_list.append({'player_id': player_id,
                              'first_name': line.split(',')[1],
                              'last_name': line.split(',')[2],
                              'batter_hand': line.split(',')[3],
                              'pitcher_hand': line.split(',')[4],
                              'single_v_left': data_v_l['single'],
                              'double_v_left': data_v_l['double'],
                              'triple_v_left': data_v_l['triple'],
                              'homerun_v_left': data_v_l['homerun'],
                              'walk_v_left': data_v_l['walk'],
                              'hbp_v_left': data_v_l['hbp'],
                              'error_v_left': data_v_l['error'],
                              'out_v_left': data_v_l['out'],
                              'productive_out_v_left': data_v_l['productive_out'],
                              'single_v_right': data_v_r['single'],
                              'double_v_right': data_v_r['double'],
                              'triple_v_right': data_v_r['triple'],
                              'homerun_v_right': data_v_r['homerun'],
                              'walk_v_right': data_v_r['walk'],
                              'hbp_v_right': data_v_r['hbp'],
                              'error_v_right': data_v_r['error'],
                              'out_v_right': data_v_r['out'],
                              'productive_out_v_right': data_v_r['productive_out'],
                              's31st_success': data_running['s31st_success'],
                              's31st_fail': data_running['s31st_fail'],
                              'dh1st_success': data_running['dh1st_success'],
                              'dh1st_fail': data_running['dh1st_fail'],
                              'sh2nd_success': data_running['sh2nd_success'],
                              'sh2nd_fail': data_running['sh2nd_fail'],
                              })

    batter_df = pd.DataFrame(data_list)
    bar.finish()
    return batter_df


def build_pitcher_year_df(path, df_name, ros_name):
    df = load_retrosheet_bev_as_df(df_name=df_name, path=path)
    data_list = []
    num_lines = sum(1 for line in open(join(path, ros_name)))
    with open(join(path, ros_name), 'r') as f:
        bar = progressbar.ProgressBar(maxval=num_lines + 1,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for counter, line in enumerate(f.readlines()):
            bar.update(counter)
            player_id = line.split(',')[0]

            df_player_pitching = df[df.loc[:, 'pitcher'].str.contains(player_id)]
            df_player_pitching_v_l = df_player_pitching[df_player_pitching.loc[:, 'batter_hand'].str.contains('L')]
            data_v_l = get_batter_stats(df_player_pitching_v_l)
            df_player_pitching_v_r = df_player_pitching[df_player_pitching.loc[:, 'batter_hand'].str.contains('R')]
            data_v_r = get_batter_stats(df_player_pitching_v_r)

            df_player_pitching_runner_on_1st = df_player_pitching[df_player_pitching.loc[:, 'first_runner'].notna()]
            df_player_pitching_runner_on_2nd = df_player_pitching[df_player_pitching.loc[:, 'first_runner'].notna()]
            data_running = get_runner_stats(df_player_pitching_runner_on_1st, df_player_pitching_runner_on_2nd)

            data_list.append({'player_id': player_id,
                              'first_name': line.split(',')[1],
                              'last_name': line.split(',')[2],
                              'batter_hand': line.split(',')[3],
                              'pitcher_hand': line.split(',')[4],
                              'single_v_left': data_v_l['single'],
                              'double_v_left': data_v_l['double'],
                              'triple_v_left': data_v_l['triple'],
                              'homerun_v_left': data_v_l['homerun'],
                              'walk_v_left': data_v_l['walk'],
                              'hbp_v_left': data_v_l['hbp'],
                              'error_v_left': data_v_l['error'],
                              'out_v_left': data_v_l['out'],
                              'productive_out_v_left': data_v_l['productive_out'],
                              'single_v_right': data_v_r['single'],
                              'double_v_right': data_v_r['double'],
                              'triple_v_right': data_v_r['triple'],
                              'homerun_v_right': data_v_r['homerun'],
                              'walk_v_right': data_v_r['walk'],
                              'hbp_v_right': data_v_r['hbp'],
                              'error_v_right': data_v_r['error'],
                              'out_v_right': data_v_r['out'],
                              'productive_out_v_right': data_v_r['productive_out'],
                              's31st_success': data_running['s31st_success'],
                              's31st_fail': data_running['s31st_fail'],
                              'dh1st_success': data_running['dh1st_success'],
                              'dh1st_fail': data_running['dh1st_fail'],
                              'sh2nd_success': data_running['sh2nd_success'],
                              'sh2nd_fail': data_running['sh2nd_fail'],
                              })

    pitcher_df = pd.DataFrame(data_list)
    bar.finish()
    return pitcher_df


def build_team_year_df(path, df_name, team_filename):
    df = load_retrosheet_bev_as_df(df_name=df_name, path=path)
    data_list = []
    num_lines = sum(1 for line in open(join(path, team_filename)))
    with open(join(path, team_filename), 'r') as f:
        bar = progressbar.ProgressBar(maxval=num_lines + 1,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for counter, line in enumerate(f.readlines()):
            bar.update(counter)
            team_id = line.split(',')[0]

            # TODO: Build fielding/league stats for 4 batter hand/pitcher hand permutations
            # import pdb; pdb.set_trace()
            df_team_fielding = df.loc[
                ((df.loc[:, 'game_id'].str.contains(team_id)) & (df.loc[:, 'batting_team'] == 0)) |
                ((df.loc[:, 'visiting_team'].str.contains(team_id)) & (df.loc[:, 'batting_team'] == 1))]

            df_team_fielding_l = df_team_fielding[df_team_fielding.loc[:, 'pitcher_hand'].str.contains('L')]
            df_team_fielding_r = df_team_fielding[df_team_fielding.loc[:, 'pitcher_hand'].str.contains('R')]

            df_team_fielding_l_v_l = df_team_fielding_l[df_team_fielding_l.loc[:, 'batter_hand'].str.contains('L')]
            df_team_fielding_l_v_r = df_team_fielding_l[df_team_fielding_l.loc[:, 'batter_hand'].str.contains('R') |
                                                        df_team_fielding_l.loc[:, 'batter_hand'].str.contains('B')]

            df_team_fielding_r_v_r = df_team_fielding_r[df_team_fielding_r.loc[:, 'batter_hand'].str.contains('R')]
            df_team_fielding_r_v_l = df_team_fielding_r[df_team_fielding_r.loc[:, 'batter_hand'].str.contains('L') |
                                                        df_team_fielding_r.loc[:, 'batter_hand'].str.contains('B')]

            data_l_v_l = get_batter_stats(df_team_fielding_l_v_l)
            data_l_v_r = get_batter_stats(df_team_fielding_l_v_r)
            data_r_v_r = get_batter_stats(df_team_fielding_r_v_r)
            data_r_v_l = get_batter_stats(df_team_fielding_r_v_l)
            data = get_batter_stats(df_team_fielding)

            df_player_on_1st = df_team_fielding[df_team_fielding.loc[:, 'first_runner'].notna()]
            df_player_on_2nd = df_team_fielding[df_team_fielding.loc[:, 'second_runner'].notna()]
            data_running = get_runner_stats(df_player_on_1st, df_player_on_2nd)

            data_list.append({'team_id': team_id,
                              'single': data['single'],
                              'double': data['double'],
                              'triple': data['triple'],
                              'homerun': data['homerun'],
                              'walk': data['walk'],
                              'hbp': data['hbp'],
                              'error': data['error'],
                              'out': data['out'],
                              'productive_out': data['productive_out'],
                              's31st_success': data_running['s31st_success'],
                              's31st_fail': data_running['s31st_fail'],
                              'dh1st_success': data_running['dh1st_success'],
                              'dh1st_fail': data_running['dh1st_fail'],
                              'sh2nd_success': data_running['sh2nd_success'],
                              'sh2nd_fail': data_running['sh2nd_fail'],
                              'single_l_v_l': data_l_v_l['single'],
                              'double_l_v_l': data_l_v_l['double'],
                              'triple_l_v_l': data_l_v_l['triple'],
                              'homerun_l_v_l': data_l_v_l['homerun'],
                              'walk_l_v_l': data_l_v_l['walk'],
                              'hbp_l_v_l': data_l_v_l['hbp'],
                              'error_l_v_l': data_l_v_l['error'],
                              'out_l_v_l': data_l_v_l['out'],
                              'single_l_v_r': data_l_v_r['single'],
                              'double_l_v_r': data_l_v_r['double'],
                              'triple_l_v_r': data_l_v_r['triple'],
                              'homerun_l_v_r': data_l_v_r['homerun'],
                              'walk_l_v_r': data_l_v_r['walk'],
                              'hbp_l_v_r': data_l_v_r['hbp'],
                              'error_l_v_r': data_l_v_r['error'],
                              'out_l_v_r': data_l_v_r['out'],
                              'single_r_v_l': data_r_v_l['single'],
                              'double_r_v_l': data_r_v_l['double'],
                              'triple_r_v_l': data_r_v_l['triple'],
                              'homerun_r_v_l': data_r_v_l['homerun'],
                              'walk_r_v_l': data_r_v_l['walk'],
                              'hbp_r_v_l': data_r_v_l['hbp'],
                              'error_r_v_l': data_r_v_l['error'],
                              'out_r_v_l': data_r_v_l['out'],
                              'single_r_v_r': data_r_v_r['single'],
                              'double_r_v_r': data_r_v_r['double'],
                              'triple_r_v_r': data_r_v_r['triple'],
                              'homerun_r_v_r': data_r_v_r['homerun'],
                              'walk_r_v_r': data_r_v_r['walk'],
                              'hbp_r_v_r': data_r_v_r['hbp'],
                              'error_r_v_r': data_r_v_r['error'],
                              'out_r_v_r': data_r_v_r['out'],
                              })

    team_df = pd.DataFrame(data_list)
    bar.finish()
    return team_df

def get_fatigue_stats(df_bev, df_bga, player_id):
    team_rows = {}
    game_id_list = df_bev.loc[:,'game_id'].unique()
    for game_id in game_id_list:
        df_game = df_bev[df_bev.loc[:,'game_id'] == game_id]

        if df_bga.loc[game_id, 'vis_starting_pitcher'] == player_id or df_bga.loc[game_id, 'home_starting_pitcher'] == player_id:
            role = 'sp'
        else:
            role = 'rp'

        game_row = df_game.iloc[0,:]

        if game_row['batting_team'] == 0:
#             Pitching for home team
            team_id = game_id[0:3]
        else:
            team_id = game_row['visiting_team']

        if team_id in team_rows.keys():
            data = team_rows[team_id]
        else:
            data = {'player_id':player_id,
                    'team_id':team_id,
                    'bf_as_sp_success_1':0,
                    'bf_as_sp_fail_1': 0,
                    'bf_as_rp_success_1': 0,
                    'bf_as_rp_fail_1': 0,
                    'bf_as_sp_success_2': 0,
                    'bf_as_sp_fail_2': 0,
                    'bf_as_rp_success_2': 0,
                    'bf_as_rp_fail_2': 0,
                    'bf_as_sp_success_3': 0,
                    'bf_as_sp_fail_3': 0,
                    'bf_as_rp_success_3': 0,
                    'bf_as_rp_fail_3': 0,
                    'bf_as_sp_success_4': 0,
                    'bf_as_sp_fail_4': 0,
                    'bf_as_rp_success_4': 0,
                    'bf_as_rp_fail_4': 0,
                    'bf_as_sp_success_5': 0,
                    'bf_as_sp_fail_5': 0,
                    'bf_as_rp_success_5': 0,
                    'bf_as_rp_fail_5': 0,
                    'bf_as_sp_success_6': 0,
                    'bf_as_sp_fail_6': 0,
                    'bf_as_rp_success_6': 0,
                    'bf_as_rp_fail_6': 0,
                    'bf_as_sp_success_7': 0,
                    'bf_as_sp_fail_7': 0,
                    'bf_as_rp_success_7': 0,
                    'bf_as_rp_fail_7': 0,
                    'bf_as_sp_success_8': 0,
                    'bf_as_sp_fail_8': 0,
                    'bf_as_rp_success_8': 0,
                    'bf_as_rp_fail_8': 0,
                    'bf_as_sp_success_9': 0,
                    'bf_as_sp_fail_9': 0,
                    'bf_as_rp_success_9': 0,
                    'bf_as_rp_fail_9': 0,
                    'bf_as_sp_success_10': 0,
                    'bf_as_sp_fail_10': 0,
                    'bf_as_rp_success_10': 0,
                    'bf_as_rp_fail_10': 0,
                    'bf_as_sp_success_11': 0,
                    'bf_as_sp_fail_11': 0,
                    'bf_as_rp_success_11': 0,
                    'bf_as_rp_fail_11': 0,
                    'bf_as_sp_success_12': 0,
                    'bf_as_sp_fail_12': 0,
                    'bf_as_rp_success_12': 0,
                    'bf_as_rp_fail_12': 0,
                    'bf_as_sp_success_13': 0,
                    'bf_as_sp_fail_13': 0,
                    'bf_as_rp_success_13': 0,
                    'bf_as_rp_fail_13': 0,
                    'bf_as_sp_success_14': 0,
                    'bf_as_sp_fail_14': 0,
                    'bf_as_rp_success_14': 0,
                    'bf_as_rp_fail_14': 0,
                    'bf_as_sp_success_15': 0,
                    'bf_as_sp_fail_15': 0,
                    'bf_as_rp_success_15': 0,
                    'bf_as_rp_fail_15': 0,
                    'bf_as_sp_success_16': 0,
                    'bf_as_sp_fail_16': 0,
                    'bf_as_rp_success_16': 0,
                    'bf_as_rp_fail_16': 0,
                    'bf_as_sp_success_17': 0,
                    'bf_as_sp_fail_17': 0,
                    'bf_as_rp_success_17': 0,
                    'bf_as_rp_fail_17': 0,
                    'bf_as_sp_success_18': 0,
                    'bf_as_sp_fail_18': 0,
                    'bf_as_rp_success_18': 0,
                    'bf_as_rp_fail_18': 0,
                    'bf_as_sp_success_19': 0,
                    'bf_as_sp_fail_19': 0,
                    'bf_as_rp_success_19': 0,
                    'bf_as_rp_fail_19': 0,
                    'bf_as_sp_success_20': 0,
                    'bf_as_sp_fail_20': 0,
                    'bf_as_rp_success_20': 0,
                    'bf_as_rp_fail_20': 0,
                    'bf_as_sp_success_21': 0,
                    'bf_as_sp_fail_21': 0,
                    'bf_as_rp_success_21': 0,
                    'bf_as_rp_fail_21': 0,
                    'bf_as_sp_success_22': 0,
                    'bf_as_sp_fail_22': 0,
                    'bf_as_rp_success_22': 0,
                    'bf_as_rp_fail_22': 0,
                    'bf_as_sp_success_23': 0,
                    'bf_as_sp_fail_23': 0,
                    'bf_as_rp_success_23': 0,
                    'bf_as_rp_fail_23': 0,
                    'bf_as_sp_success_24': 0,
                    'bf_as_sp_fail_24': 0,
                    'bf_as_rp_success_24': 0,
                    'bf_as_rp_fail_24': 0,
                    'bf_as_sp_success_25': 0,
                    'bf_as_sp_fail_25': 0,
                    'bf_as_rp_success_25': 0,
                    'bf_as_rp_fail_25': 0,
                    'bf_as_sp_success_26': 0,
                    'bf_as_sp_fail_26': 0,
                    'bf_as_rp_success_26': 0,
                    'bf_as_rp_fail_26': 0,
                    'bf_as_sp_success_27': 0,
                    'bf_as_sp_fail_27': 0,
                    'bf_as_rp_success_27': 0,
                    'bf_as_rp_fail_27': 0,
                    'bf_as_sp_success_28': 0,
                    'bf_as_sp_fail_28': 0,
                    'bf_as_rp_success_28': 0,
                    'bf_as_rp_fail_28': 0,
                    'bf_as_sp_success_29': 0,
                    'bf_as_sp_fail_29': 0,
                    'bf_as_rp_success_29': 0,
                    'bf_as_rp_fail_29': 0,
                    'bf_as_sp_success_30': 0,
                    'bf_as_sp_fail_30': 0,
                    'bf_as_rp_success_30': 0,
                    'bf_as_rp_fail_30': 0,
                    'bf_as_sp_success_31': 0,
                    'bf_as_sp_fail_31': 0,
                    'bf_as_rp_success_31': 0,
                    'bf_as_rp_fail_31': 0,
                    'bf_as_sp_success_32': 0,
                    'bf_as_sp_fail_32': 0,
                    'bf_as_rp_success_32': 0,
                    'bf_as_rp_fail_32': 0,
                    'bf_as_sp_success_33': 0,
                    'bf_as_sp_fail_33': 0,
                    'bf_as_rp_success_33': 0,
                    'bf_as_rp_fail_33': 0,
                    'bf_as_sp_success_34': 0,
                    'bf_as_sp_fail_34': 0,
                    'bf_as_rp_success_34': 0,
                    'bf_as_rp_fail_34': 0,
                    'bf_as_sp_success_35': 0,
                    'bf_as_sp_fail_35': 0,
                    'bf_as_rp_success_35': 0,
                    'bf_as_rp_fail_35': 0,
                    'bf_as_sp_success_36': 0,
                    'bf_as_sp_fail_36': 0,
                    'bf_as_rp_success_36': 0,
                    'bf_as_rp_fail_36': 0,
                    }

        batters_faced = 0
        for row in df_game.itertuples():
            if row.batter_event_flag == 'T':
                batters_faced += 1
                if batters_faced > 1 and batters_faced <= 36:
                    data['bf_as_' + role + '_success_' + str(batters_faced - 1)] += 1
        if batters_faced > 0 and batters_faced <= 36:
            data['bf_as_' + role + '_fail_' + str(batters_faced)] += 1

        team_rows[team_id] = data
    return team_rows



def build_pitcher_year_fatigue_df(path, df_bev_name, df_bga_name, ros_name):
    df_bev = load_retrosheet_bev_as_df(df_name=df_bev_name, path=path)
    df_bga = load_retrosheet_bga_as_df(df_name=df_bga_name, path=path)
    data_list = []
    num_lines = sum(1 for line in open(join(path, ros_name)))
    with open(join(path, ros_name), 'r') as f:
        bar = progressbar.ProgressBar(maxval=num_lines + 1,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for counter, line in enumerate(f.readlines()):
            bar.update(counter)
            player_id = line.split(',')[0]

            df_player_pitching = df_bev[df_bev.loc[:, 'pitcher'].str.contains(player_id)]
            data_dict = get_fatigue_stats(df_player_pitching, df_bga, player_id)

            for key in data_dict.keys():
                data_list.append(data_dict[key])

    pitcher_df = pd.DataFrame(data_list)
    bar.finish()
    return pitcher_df

def adjust_for_prior(num_event, num_chances, min_chances, prior_prob):
    return ((num_event + prior_prob * max([0, min_chances - num_chances])) /
            (num_chances + max([0, min_chances - num_chances])))

def build_player_stats_from_row(player, player_row, minimum_atbats=50, league_prior = None):
    if league_prior is None:
        league_prior = {'single': (42039 - 8531 - 785 - 6776) / 166651,
                        'double': 8531 / 166651,
                        'triple': 785 / 166651,
                        'homerun': 6776 / 166651,
                        'walk': 15895 / 166651,
                        'hbp': 2898 / 166651,
                        }
        league_prior['out'] = 1 - (league_prior['single'] +
                                   league_prior['double'] +
                                   league_prior['triple'] +
                                   league_prior['homerun'] +
                                   league_prior['walk'])
    
    atbats_v_left = (player_row['single_v_left'] +
                     player_row['double_v_left'] +
                     player_row['triple_v_left'] +
                     player_row['homerun_v_left'] +
                     player_row['walk_v_left'] +
                     player_row['out_v_left'])

    player.single_v_left = adjust_for_prior(player_row['single_v_left'], atbats_v_left, minimum_atbats, league_prior['single'])
    player.double_v_left = adjust_for_prior(player_row['double_v_left'], atbats_v_left, minimum_atbats, league_prior['double'])
    player.triple_v_left = adjust_for_prior(player_row['triple_v_left'], atbats_v_left, minimum_atbats, league_prior['triple'])
    player.homerun_v_left = adjust_for_prior(player_row['homerun_v_left'], atbats_v_left, minimum_atbats, league_prior['homerun'])
    player.walk_v_left = adjust_for_prior(player_row['walk_v_left'], atbats_v_left, minimum_atbats, league_prior['walk'])
    player.hbp_v_left = adjust_for_prior(player_row['hbp_v_left'], atbats_v_left, minimum_atbats,
                                          league_prior['hbp'])
    player.out_v_left = adjust_for_prior(player_row['out_v_left'], atbats_v_left, minimum_atbats, league_prior['out'])
    player.productive_out_v_left = player_row['productive_out_v_left'] / player_row['out_v_left']



    atbats_v_right = (player_row['single_v_right'] +
                      player_row['double_v_right'] +
                      player_row['triple_v_right'] +
                      player_row['homerun_v_right'] +
                      player_row['walk_v_right'] +
                      player_row['out_v_right'])

    player.single_v_right = adjust_for_prior(player_row['single_v_right'], atbats_v_right, minimum_atbats, league_prior['single'])
    player.double_v_right = adjust_for_prior(player_row['double_v_right'], atbats_v_right, minimum_atbats, league_prior['double'])
    player.triple_v_right = adjust_for_prior(player_row['triple_v_right'], atbats_v_right, minimum_atbats, league_prior['triple'])
    player.homerun_v_right = adjust_for_prior(player_row['homerun_v_right'], atbats_v_right, minimum_atbats, league_prior['homerun'])
    player.walk_v_right = adjust_for_prior(player_row['walk_v_right'], atbats_v_right, minimum_atbats, league_prior['walk'])
    player.hbp_v_right = adjust_for_prior(player_row['hbp_v_right'], atbats_v_right, minimum_atbats,
                                           league_prior['hbp'])
    player.out_v_right = adjust_for_prior(player_row['out_v_right'], atbats_v_right, minimum_atbats, league_prior['out'])
    player.productive_out_v_right = player_row['productive_out_v_right'] / player_row['out_v_right']

    player.s31st = player_row['s31st_success'] / (player_row['s31st_success'] + player_row['s31st_fail'])
    player.dh1st = player_row['dh1st_success'] / (player_row['dh1st_success'] + player_row['dh1st_fail'])
    player.sh2nd = player_row['sh2nd_success'] / (player_row['sh2nd_success'] + player_row['sh2nd_fail'])

    return player


def build_player_from_retrosheet_data(player_id, df_batters, df_pitchers):
    batter_row = df_batters.loc[player_id]
    pitcher_row = df_pitchers.loc[player_id]

    player = Player()

    player.player_id = player_id
    player.name = batter_row['first_name'] + ' ' + batter_row['last_name']
    player.batter_hand = batter_row['batter_hand']
    player.pitcher_hand = batter_row['pitcher_hand']

    player.as_batter = build_player_stats_from_row(player.as_batter, batter_row)
    player.as_pitcher = build_player_stats_from_row(player.as_pitcher, pitcher_row)

    return player


def build_team_from_retrosheet(team_name, ros_path, ros_filename, df_batters, df_pitchers, df_fatigue,
                               starting_pitcher=None,
                               batting_order=None,
                               existing_player_dict=None):
    if existing_player_dict is None:
        existing_player_dict = {}

    team = Team()
    team.name = team_name

    df_ros = load_retrosheet_ros_as_df(df_name=ros_filename, path=ros_path)
    for row in df_ros.itertuples():
        # Check if player was already built. Use if so, otherwise build and add
        player_id = row.player_id
        if player_id in existing_player_dict.keys():
            player = existing_player_dict[player_id]
        else:
            player = build_player_from_retrosheet_data(player_id=row.player_id, df_batters=df_batters,
                                                       df_pitchers=df_pitchers)
            existing_player_dict[player_id] = player
        team.players[player.player_id] = copy.deepcopy(player)

    # if batting_order is None:
    #     batting_order = [player_id for player_id in team.players.keys()][0:9]
    # team.order = batting_order
    #
    # if starting_pitcher is None:
    #     starting_pitcher = batting_order[0]
    # team.pitcher = team.players[starting_pitcher]

    # TODO: Get team fielding stats (unused in simulation currently)

    df_team_fatigue = df_fatigue[df_fatigue.loc[:, 'team_id'] == team_name]
    player_id_list = df_team_fatigue.loc[:, 'player_id'].unique()

    total_rp_bf = 0

    for player_id in player_id_list:
        df_player_fatigue = df_team_fatigue[df_fatigue.loc[:, 'player_id'] == player_id]
        df_league_fatigue = df_team_fatigue[df_fatigue.loc[:, 'player_id'] == player_id]
        bf_as_rp = df_player_fatigue.bf_as_rp_success_1.item() + df_player_fatigue.bf_as_rp_fail_1.item()
        if bf_as_rp >= 25:
            # Filter out pitchers who normally did not throw in relief
            total_rp_bf += bf_as_rp
            team.bullpen[player_id] = bf_as_rp
        player = team.players[player_id]
        for i in range(1,36):

            player.chance_of_substitution_as_rp.append(
                ((1 + df_league_fatigue['bf_as_rp_fail_' + str(i)].item()) /
                 (1 + df_league_fatigue['bf_as_rp_success_' + str(i)].item() +
                  df_league_fatigue['bf_as_rp_fail_' + str(i)].item())))

            player.chance_of_substitution_as_sp.append(
                ((1 + df_league_fatigue['bf_as_sp_fail_' + str(i)].item()) /
                 (1 + df_league_fatigue['bf_as_sp_success_' + str(i)].item() +
                  df_league_fatigue['bf_as_sp_fail_' + str(i)].item())))

    for player_id in team.bullpen.keys():
        team.bullpen[player_id] = team.bullpen[player_id] / total_rp_bf
    return team


def build_teams_from_game_id(game_id, df_bga, df_batters, df_pitchers, df_fatigue, ros_path, existing_team_dict=None, existing_player_dict=None):
    if existing_team_dict is None:
        existing_team_dict = {}
    if existing_player_dict is None:
        existing_player_dict = {}
    # Get Teams from BGA
    game_bga_data = df_bga.loc[game_id]
    vis_team_name = game_bga_data['visiting_team']
    home_team_name = game_bga_data['home_team']
    # Get rosters from ROS files
    # TODO: Build database of each team's 25 man roster by date (could keep fatigue data there too)
    game_year = game_id[3:7]
    vis_ros_filename = vis_team_name + game_year + '.ROS'
    home_ros_filename = home_team_name + game_year + '.ROS'
    # Build players on roster
    vis_team_order = [game_bga_data['visitor_batter_1'],
                      game_bga_data['visitor_batter_2'],
                      game_bga_data['visitor_batter_3'],
                      game_bga_data['visitor_batter_4'],
                      game_bga_data['visitor_batter_5'],
                      game_bga_data['visitor_batter_6'],
                      game_bga_data['visitor_batter_7'],
                      game_bga_data['visitor_batter_8'],
                      game_bga_data['visitor_batter_9']]

    home_team_order = [game_bga_data['home_batter_1'],
                       game_bga_data['home_batter_2'],
                       game_bga_data['home_batter_3'],
                       game_bga_data['home_batter_4'],
                       game_bga_data['home_batter_5'],
                       game_bga_data['home_batter_6'],
                       game_bga_data['home_batter_7'],
                       game_bga_data['home_batter_8'],
                       game_bga_data['home_batter_9']]

    if vis_team_name not in existing_team_dict.keys():
        vis_team = build_team_from_retrosheet(team_name=vis_team_name, ros_path=ros_path, ros_filename=vis_ros_filename,
                                              df_batters=df_batters, df_pitchers=df_pitchers, df_fatigue=df_fatigue,
                                              starting_pitcher=game_bga_data['vis_starting_pitcher'],
                                              batting_order=vis_team_order, existing_player_dict=existing_player_dict)
        existing_team_dict[vis_team_name] = vis_team

    if home_team_name not in existing_team_dict.keys():
        home_team = build_team_from_retrosheet(team_name=home_team_name, ros_path=ros_path, ros_filename=home_ros_filename,
                                               df_batters=df_batters, df_pitchers=df_pitchers, df_fatigue=df_fatigue,
                                               starting_pitcher=game_bga_data['home_starting_pitcher'],
                                               batting_order=home_team_order, existing_player_dict=existing_player_dict)
        existing_team_dict[home_team_name] = home_team

    vis_team = copy.deepcopy(existing_team_dict[vis_team_name])
    vis_team.order = vis_team_order
    vis_team.pitcher = vis_team.players[game_bga_data['vis_starting_pitcher']]

    home_team = copy.deepcopy(existing_team_dict[home_team_name])
    home_team.order = home_team_order
    home_team.pitcher = home_team.players[game_bga_data['home_starting_pitcher']]

    # Get fatigue history from some database (need to build it)
    return vis_team, home_team


def build_league_from_game_id(df_teams):
    league_data = df_teams.loc['LEAGUE']
    league_atbats = league_data['single'] + league_data['double'] + league_data['triple'] + league_data['homerun'] + \
                    league_data['walk'] + league_data['hbp'] + league_data['error'] + league_data['out']
    league = League(single=league_data['single'] / league_atbats,
                    double=league_data['double'] / league_atbats,
                    triple=league_data['triple'] / league_atbats,
                    homerun=league_data['homerun'] / league_atbats,
                    walk=league_data['walk'] / league_atbats,
                    name='League')

    league.error = league_data['error'] / league_atbats
    
    league_atbats_l_v_l = (league_data['single_l_v_l'] + 
                           league_data['double_l_v_l'] + 
                           league_data['triple_l_v_l'] + 
                           league_data['homerun_l_v_l'] + 
                           league_data['walk_l_v_l'] + 
                           league_data['out_l_v_l'])
    
    league.single_l_v_l = league_data['single_l_v_l'] / league_atbats_l_v_l
    league.double_l_v_l = league_data['double_l_v_l'] / league_atbats_l_v_l
    league.triple_l_v_l = league_data['triple_l_v_l'] / league_atbats_l_v_l
    league.homerun_l_v_l = league_data['homerun_l_v_l'] / league_atbats_l_v_l
    league.walk_l_v_l = league_data['walk_l_v_l'] / league_atbats_l_v_l
    league.out_l_v_l = 1 - (
            league.single_l_v_l + league.double_l_v_l + league.triple_l_v_l + league.homerun_l_v_l + league.walk_l_v_l)

    league_atbats_l_v_r = (league_data['single_l_v_r'] +
                           league_data['double_l_v_r'] +
                           league_data['triple_l_v_r'] +
                           league_data['homerun_l_v_r'] +
                           league_data['walk_l_v_r'] +
                           league_data['out_l_v_r'])

    league.single_l_v_r = league_data['single_l_v_r'] / league_atbats_l_v_r
    league.double_l_v_r = league_data['double_l_v_r'] / league_atbats_l_v_r
    league.triple_l_v_r = league_data['triple_l_v_r'] / league_atbats_l_v_r
    league.homerun_l_v_r = league_data['homerun_l_v_r'] / league_atbats_l_v_r
    league.walk_l_v_r = league_data['walk_l_v_r'] / league_atbats_l_v_r
    league.out_l_v_r = 1 - (
            league.single_l_v_r + league.double_l_v_r + league.triple_l_v_r + league.homerun_l_v_r + league.walk_l_v_r)

    league_atbats_r_v_l = (league_data['single_r_v_l'] +
                           league_data['double_r_v_l'] +
                           league_data['triple_r_v_l'] +
                           league_data['homerun_r_v_l'] +
                           league_data['walk_r_v_l'] +
                           league_data['out_r_v_l'])

    league.single_r_v_l = league_data['single_r_v_l'] / league_atbats_r_v_l
    league.double_r_v_l = league_data['double_r_v_l'] / league_atbats_r_v_l
    league.triple_r_v_l = league_data['triple_r_v_l'] / league_atbats_r_v_l
    league.homerun_r_v_l = league_data['homerun_r_v_l'] / league_atbats_r_v_l
    league.walk_r_v_l = league_data['walk_r_v_l'] / league_atbats_r_v_l
    league.out_r_v_l = 1 - (
            league.single_r_v_l + league.double_r_v_l + league.triple_r_v_l + league.homerun_r_v_l + league.walk_r_v_l)

    league_atbats_r_v_r = (league_data['single_r_v_r'] +
                           league_data['double_r_v_r'] +
                           league_data['triple_r_v_r'] +
                           league_data['homerun_r_v_r'] +
                           league_data['walk_r_v_r'] +
                           league_data['out_r_v_r'])

    league.single_r_v_r = league_data['single_r_v_r'] / league_atbats_r_v_r
    league.double_r_v_r = league_data['double_r_v_r'] / league_atbats_r_v_r
    league.triple_r_v_r = league_data['triple_r_v_r'] / league_atbats_r_v_r
    league.homerun_r_v_r = league_data['homerun_r_v_r'] / league_atbats_r_v_r
    league.walk_r_v_r = league_data['walk_r_v_r'] / league_atbats_r_v_r
    league.out_r_v_r = 1 - (
            league.single_r_v_r + league.double_r_v_r + league.triple_r_v_r + league.homerun_r_v_r + league.walk_r_v_r)

    return league


def game_from_game_id(game_id, event_num, df_bev, df_bga, df_batters, df_pitchers, df_teams, df_fatigue, ros_path, eva_path, existing_league_dict=None, existing_team_dict=None, existing_player_dict=None):
    if existing_league_dict is None:
        existing_league_dict = {}
    game = Game()

    game.away_team, game.home_team = build_teams_from_game_id(game_id, df_bga, df_batters, df_pitchers, df_fatigue, ros_path, existing_team_dict, existing_player_dict)
    league_year = game_id[3:7]
    if league_year not in existing_league_dict.keys():
        existing_league_dict[league_year] = build_league_from_game_id(df_teams=df_teams)
    game.league = copy.deepcopy(existing_league_dict[league_year])

    df_game = df_bev[df_bev['game_id'] == game_id]
    game_state_row = df_game[df_game['event_num'] == event_num].index[0]

    df_game_state = df_bev.iloc[game_state_row]

    game.top_half = not df_game_state['batting_team']

    if not pd.isnull(df_game_state['first_runner']):
        game.first_base = df_game_state['first_runner']
    if not pd.isnull(df_game_state['second_runner']):
        game.second_base = df_game_state['second_runner']
    if not pd.isnull(df_game_state['third_runner']):
        game.third_base = df_game_state['third_runner']

    game.inning = df_game_state['inning']
    game.outs = df_game_state['outs']
    # game_state = np.zeros((2, game.inning))
    game_state = np.zeros((2, np.max([9, game.inning])))

    runs = 0
    for row in df_game.itertuples():
        inning = row.inning
        top_half = not row.batting_team

        if top_half:
            batting_team = game.away_team
            pitching_team = game.home_team
            # game.away_team.index = (row.lineup_position - 1)
        else:
            batting_team = game.home_team
            pitching_team = game.away_team
        batting_team.index = (row.lineup_position - 1)

        if row.event_num == event_num:
            break

        if top_half:
            score = row.vis_score
        else:
            score = row.home_score

        runs = score - np.sum(game_state[int(not top_half), :(inning - 1)])
        game_state[int(not top_half), (inning - 1)] = runs
    #     TODO: Check for substitutions
    #  Check for pinch hitters
    # if not pd.isnull(row.batter_removed_for_pinch_hitter):
    #     batting_team.order[batting_team.order.index(row.batter_removed_for_pinch_hitter)] = row.batter

    # if '.' in row.pitch_sequence:
    #     num_nonbatter_events_handled = 0
    #     while num_nonbatter_events_handled < row.pitch_sequence.find('.'):
    #         # TODO: Check for non-batter events (SBs, WPs, PBs, balks, and whatever else (need to build list))
    #         # TODO: No wait none of these matter for getting game state correct
    #         # TODO: No wait if they still count as '.'s then we need to handle them to ensure not missing subs
    #         # Check for pitcher substitutions
    #         if row.pitcher != pitching_team.pitcher:
    #             if pitching_team.pitcher in pitching_team.order:
    #                 pitching_team.order[pitching_team.order.index(pitching_team.pitcher)] = row.pitcher
    #             pitching_team.pitcher = pitching_team.players[row.pitcher]
    #             num_nonbatter_events_handled += 1
    #             # TODO: Do I need to check for the batting team changing pitcher?
    #         # Check for pinch runners
    #         if not pd.isnull(row.runner_removed_for_pinch_runner_on_1st):
    #             batting_team.order[batting_team.order.index(row.runner_removed_for_pinch_runner_on_1st)] = row.first_runner
    #             num_nonbatter_events_handled += 1
    #         if not pd.isnull(row.runner_removed_for_pinch_runner_on_2nd):
    #             batting_team.order[batting_team.order.index(row.runner_removed_for_pinch_runner_on_1st)] = row.second_runner
    #             num_nonbatter_events_handled += 1
    #         if not pd.isnull(row.runner_removed_for_pinch_runner_on_3rd):
    #             batting_team.order[batting_team.order.index(row.runner_removed_for_pinch_runner_on_1st)] = row.third_runner
    #             num_nonbatter_events_handled += 1
    #         # TODO: Check for Non-DH fielder substitutions (can't do without position dict)
    #         # TODO: Check for all other substitutions
    #         pdb.set_trace()
    # TODO: Check for substitutions
    # ANA201904050
    #  2019ANA.EVA
    eva_filename = game_id[3:7] + game_id[0:3] + '.EV'
    for filename in os.listdir(eva_path):
        if eva_filename in filename:
            eva_filename = filename
            break
    # eva_filename = game_id[3:7] + game_id[0:3] + '.EVA'
    with open(join(eva_path, eva_filename), 'r') as f:
        line = f.readline()
        # Skip to correct game
        while game_id not in line:
            line = f.readline()
        # Skip to plays
        while 'play' not in line:
            line = f.readline()

        while True:
            split_line = line.split(',')
            if split_line[0] == 'data' or split_line[0] == 'id':
                raise Exception('ERROR: Reached end of game in EVA file without stopping!')
            elif split_line[0] == 'play':
                # Check if target game state has been reached
                if (int(split_line[1]) == game.inning and
                        int(split_line[2]) == int(not game.top_half) and
                        split_line[3] == batting_team.order[batting_team.index] and
                        split_line[6].rstrip() == row.event_text
                ):
                    break
            elif split_line[0] == 'sub':
                sub_batting_order = int(split_line[4])
                sub_id = split_line[1]
                if int(split_line[3]) == 0:
                    # Visiting team substitution
                    team = game.away_team
                else:
                    team = game.home_team

                if sub_batting_order == 0:
                    # non-batting pitcher sub
                    team.pitcher = team.players[sub_id]
                else:
                    team.order[sub_batting_order - 1] = sub_id

            line = f.readline()

    game.game = game_state
    game.runs = runs

    return game

def season_from_team_id(team_id, df_bev):
    home_game_id_list = df_bev.loc[:,'game_id'].str.contains(team_id).unique()
    away_game_id_list = df_bev.loc[:, 'visiting team'].str.contains(team_id).unique()


if __name__ == '__main__':
    get_parse_build_retrosheet_years(path='/home/mark/Research/mcmc_baseball_sim/data/retrosheet_pbp',
                                     start_year=2019,
                                     end_year=2019,
                                     get_data=False,
                                     parse_data=False,
                                     build_df=True,
                                     keep_data=True)
