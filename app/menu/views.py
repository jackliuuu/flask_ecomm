from flask import request
from app.menu import menu,menu_api
from app import models
from database.database import db
from flask_restful import Resource


class Menu(Resource):
    def get(self):
        type_ =request.args.get('type')
        menu_list = []
        if type_ == 'list':
            mu = models.Menu.query.filter(models.Menu.level !=0 ).all()
            for m in mu:
                menu_list.append(m.to_dict())
        else:
            mu = models.Menu.query.filter(models.Menu.level == 1).all()
            print('mu: ',mu)
            for m in mu:
                print('m: ',m)
                first_mu = m.to_dict()
                for sm in m.children:
                    print('sm:',sm)
                    second_dict = sm.to_dict()
                    second_dict['children'] == sm.get_child_list()
                    first_mu['children'].append(second_dict)
                menu_list.append(first_mu)
            return menu_list
menu_api.add_resource(Menu,'/menu')

