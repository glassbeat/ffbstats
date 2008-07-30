import turbogears as tg
from turbogears import controllers, expose, flash, paginate, identity, \
     redirect, url, widgets
from turbogears.toolbox.catwalk import CatWalk
from ffbstats import model
from cherrypy import request, response
from ffbstats.lib.populator import generate_teams
from ffbstats.lib.datagrids import week_datagrid, teams_datagrid
# model import
from ffbstats.model import Game, Team, Week

# controllers
class Root(controllers.RootController):
    catwalk = CatWalk(model)
    
    @expose(template="ffbstats.templates.teams")
    @paginate('data', limit=20,
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
    @paginate('data', limit=20,)
    def week(self, num=None):
        if num == None:
            flash("Please select a week")
            redirect(tg.url("/"))
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
