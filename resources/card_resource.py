import bcrypt
from flask_restful import Resource, reqparse
from logic.card_logic import CardLogic
import bcrypt


class Card(Resource):
    def __init__(self):
        self.card_put_args = self.createParser()
        self.logic = CardLogic()

    def createParser(self):
        args = reqparse.RequestParser()
        args.add_argument("name", type=str, help="name of the client")
        args.add_argument("number", type=str, help="number of the card")
        args.add_argument("date", type=str, help="date of the card")
        args.add_argument("code", type=str, help="code of the card")
        args.add_argument("salt", type=str, help="salt of the card")
        args.add_argument("balance", type=float, help="balance of the card")
        return args

    def post(self):
        card = self.card_put_args.parse_args()
        cardDict = self.logic.getCardByNumber(card['number'])

        if cardDict != {}:
            
            if cardDict['name'] == card['name']:
                
                if cardDict['date'] == card['date']:

                    code = card['code']
                    salt = cardDict['salt'].encode("utf-8")
                    strCode = code.encode("utf-8")
                    hashPassword = bcrypt.hashpw(strCode, salt)
                    dbPassword = cardDict['code'].encode("utf-8")

                    if hashPassword == dbPassword:
                        state = True
                        #balance = cardDict['balance']
                    else:
                        state = "Error de código"
                else:
                    state = "Error de fecha"
            else:
                state = "Error de nombre"
        else:
            state = "Error Numero Tarjeta"

        return {"Response": state}

    def put(self):
        card = self.card_put_args.parse_args()
        rows = self.logic.insertCard(card)
        return {"rowsAffected": rows}

    def patch(self):
        data = self.card_put_args.parse_args()
        rows = self.logic.updateCardBalance(data)
        return {"rowsAffected": rows}