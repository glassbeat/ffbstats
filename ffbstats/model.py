from datetime import datetime
from turbogears.database import PackageHub
from sqlobject import *
from turbogears import identity

hub = PackageHub('ffbstats')
__connection__ = hub

class Team(SQLObject):
    name = StringCol(length=40, alternateID=True)
    owner = StringCol(length=40)
    scores = SQLMultipleJoin('Score')
    
    def _get_games(self):
        games = Game.select().filter(Score.q.team == self.id).distinct()
        return games
    
    # get the total points this team has scored in every game
    def _get_total_points(self):
        return self.scores.sum('score')
    
    # get the total possible points this team could've scored in every game
    def _get_total_possible_points(self):
        return self.scores.sum('optimal_score')
    
    def _get_wins(self):
        Game.select(Game.q.id).filter(Score.q.team == self.id)
    def _get_losses(self):
        pass
    
    def _get_optimal_wins(self):
        pass
    
    def _get_optimal_losses(self):
        pass
    
    def _get_efficiency(self):
        result = 0
        if self.total_possible_points > 0:
            result = float(self.total_points) / float(self.total_possible_points)
        else:
            result = 0
        return result
    
class Game(SQLObject):
    week = ForeignKey('Week', default=None)
    scores = SQLMultipleJoin('Score')
class Score(SQLObject):
    score = IntCol()
    optimal_score = IntCol()
    team = ForeignKey('Team', default=None)
    game = ForeignKey('Game', default=None)

#TODO: Could I make a Score table that is related to the game and team table so that
#I can have just opponents instead of opponent1, opponent2? Look into this more.
#class Score(SQLObject):
#    pass
    
class Week(SQLObject):
    week_num = IntCol(default=None)
    games = SQLMultipleJoin('Game', joinColumn='week_id')
    comments = UnicodeCol(default=None)
    data_entered = BoolCol()
    
# identity models.
class Visit(SQLObject):
    """
    A visit to your site
    """
    class sqlmeta:
        table = 'visit'

    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()

    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)


class VisitIdentity(SQLObject):
    """
    A Visit that is link to a User object
    """
    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    user_id = IntCol()


class Group(SQLObject):
    """
    An ultra-simple group definition.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_group'

    group_name = UnicodeCol(length=16, alternateID=True,
                            alternateMethodName='by_group_name')
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)

    # collection of all users belonging to this group
    users = RelatedJoin('User', intermediateTable='user_group',
                        joinColumn='group_id', otherColumn='user_id')

    # collection of all permissions for this group
    permissions = RelatedJoin('Permission', joinColumn='group_id',
                              intermediateTable='group_permission',
                              otherColumn='permission_id')


class User(SQLObject):
    """
    Reasonably basic User definition.
    Probably would want additional attributes.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_user'

    user_name = UnicodeCol(length=16, alternateID=True,
                           alternateMethodName='by_user_name')
    email_address = UnicodeCol(length=255, alternateID=True,
                               alternateMethodName='by_email_address')
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)

    # groups this user belongs to
    groups = RelatedJoin('Group', intermediateTable='user_group',
                         joinColumn='user_id', otherColumn='group_id')

    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    def _set_password(self, cleartext_password):
        "Runs cleartext_password through the hash algorithm before saving."
        password_hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(password_hash)

    def set_password_raw(self, password):
        "Saves the password as-is to the database."
        self._SO_set_password(password)


class Permission(SQLObject):
    """
    A relationship that determines what each Group can do
    """
    permission_name = UnicodeCol(length=16, alternateID=True,
                                 alternateMethodName='by_permission_name')
    description = UnicodeCol(length=255)

    groups = RelatedJoin('Group',
                         intermediateTable='group_permission',
                         joinColumn='permission_id',
                         otherColumn='group_id')
