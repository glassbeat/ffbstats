from pkg_resources import resource_filename
from turbogears import widgets
from turbogears.widgets import PaginateDataGrid
import fpformat

# datagrids
# find 'static' directory in package 'ffbstats'
static_dir = resource_filename('ffbstats', 'static')
# register directory under name 'ffbstats'
widgets.register_static_directory('ffbstats', static_dir)

# datagrid for index page
teams_datagrid = PaginateDataGrid(name='team_list',
                                  template="ffbstats.templates.datagrid",
    fields = [
        PaginateDataGrid.Column('name',
                                'name',
                                'Name',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('owner',
                                'owner',
                                'Owner',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('total_points',
                                'total_points',
                                'P',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('total_possible_points',
                                'total_possible_points',
                                'OP',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('efficiency',
                                lambda teams: (
                                    "".join([str(fpformat.fix(
                                        (teams.efficiency * 100), 2)), "%"])), 
                                'Efficiency',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('wins',
                                'wins',
                                'W',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('losses',
                                'losses',
                                'L',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('optimal_wins',
                                'optimal_wins',
                                'OW',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('optimal_losses',
                                'optimal_losses',
                                'OL',
                                options=dict(sortable=True)),
    ])

# datagrid and functions for week view page.
def get_opponent(team):
    if team.games.count():
        if team.id == team.games[0].opponent1ID:
            return team.games[0].opponent2.name
        else:
            return team.games[0].opponent1.name
    else:
        return "TBD"

def get_points(team):
    if team.games.count():
        if team.id == team.games[0].opponent1ID:
            return team.games[0].opp1_score
        else:
            return team.games[0].opp2_score
    else:
        return 0
    
def get_possible_points(team):
    if team.games.count():
        if team.id == team.games[0].opponent1ID:
            return team.games[0].opp1_possible_score
        else:
            return team.games[0].opp2_possible_score
    else:
        return 0
    
def get_opponent_points(team):
    if team.games.count():
        if team.id == team.games[0].opponent1ID:
            return team.games[0].opp2_score
        else:
            return team.games[0].opp1_score
    else:
        return 0
    
def get_opponent_possible_points(team):
    if team.games.count():
        if team.id == team.games[0].opponent1ID:
            return team.games[0].opp2_possible_score
        else:
            return team.games[0].opp1_possible_score
    else:
        return 0

week_datagrid = PaginateDataGrid(name='team_list',
                                 template='ffbstats.templates.datagrid',
    fields=[
        PaginateDataGrid.Column(name='name',
                                getter='name',
                                title='Name',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column(name='owner',
                                getter='owner',
                                title='Owner',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column(name='points',
                                getter=lambda self: get_points(self),
                                title='P'),
        PaginateDataGrid.Column(name='optimal_points',
                                getter=lambda self: get_possible_points(self),
                                title='OP'),
        PaginateDataGrid.Column(name='opponent',
                                getter=lambda self: get_opponent(self),
                                title='Opponent'),
        PaginateDataGrid.Column(name='opponent_points',
                                getter=lambda self: get_opponent_points(self),
                                title='P'),
        PaginateDataGrid.Column(name='opponent_possible_points',
                                getter=lambda self: get_opponent_possible_points(self),
                                title='OP'),
        
    ])

# change the css file for the widgets
teams_datagrid.css = [widgets.CSSLink('ffbstats', 'css/team_dg.css')]
week_datagrid.css = [widgets.CSSLink('ffbstats', 'css/week.css')]
