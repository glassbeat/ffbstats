from turbogears import controllers, expose, flash, paginate, identity, \
     redirect, url, widgets
from turbogears.toolbox.catwalk import CatWalk
from ffbstats import model
from cherrypy import request, response
from pkg_resources import resource_filename
from ffbstats.lib.populator import generate_teams
import fpformat

# widgets import
from turbogears.widgets import PaginateDataGrid

# model import
from ffbstats.model import Game, Team, Week

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
        PaginateDataGrid.Column('total_total_points',
                                'total_total_points',
                                'TRP',
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
        PaginateDataGrid.Column(name='Points',
                                getter=lambda self: get_points(self),
                                title='P'),
        PaginateDataGrid.Column(name='opponent',
                                getter=lambda self: get_opponent(self),
                                title='Opponent')
    ])

# change the css file for the widgets
teams_datagrid.css = [widgets.CSSLink('ffbstats', 'css/team_dg.css')]
week_datagrid.css = [widgets.CSSLink('ffbstats', 'css/week.css')]

# controllers
class Root(controllers.RootController):
    catwalk = CatWalk(model)
    
    @expose(template="ffbstats.templates.teams")
    @paginate('data',
              limit=20,
              default_order=('name', '-efficiency', '-total_points',
                                     '-total_possible_points',
                                     '-total_total_points',
                                     '-wins', '-losses', '-optimal_wins',
                                     '-optimal_losses'))
    # @identity.require(identity.in_group("admin"))
    def index(self):
        teams = Team.select()
        return dict(data=teams, datagrid=teams_datagrid)
    
    def viewteam(self, team=None):
        return dict()
    
    @expose(template="ffbstats.templates.week")
    @paginate('data',
              limit=20,)
    def week(self, num=None):
        if num == None:
            return dict(weeks="Please select a week")
        data = Team.select().filter(Game.q.weekID==num)
        return dict(data=data, datagrid=week_datagrid, num=num)
    
    @expose()
    def populate(self):
        if Team.select().count():
            flash("The tables are already populated.")
        else:
            for team in generate_teams():
                Team(**team)
            flash("The tables have been populated now.")
        redirect("/")
    
    # Identity methods
    @expose(template="ffbstats.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise redirect(forward_url)

        forward_url=None
        previous_url= request.path

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= request.headers.get("Referer", "/")
            
        response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")
