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
        args.add_argument("limit", type=float, help="limit of the card")
        args.add_argument("status", type=str, help="state of the card")
        return args

    def get(self, number):
        logic = CardLogic()
        result = logic.getCardByNumber(number)
        if len(result) == 0:
            return {}
        result['balance'] = float(str(result['balance']))
        return result, 200

    def post(self):
        card = self.card_put_args.parse_args()
        cardDict = self.logic.getCardByNumber(card['number'])

        if cardDict != {}:
            
            if cardDict['status'] == "Activa":
                if cardDict['name'] == card['name']:
                    
                    if cardDict['date'] == card['date']:

                        code = card['code']
                        salt = cardDict['salt'].encode("utf-8")
                        strCode = code.encode("utf-8")
                        hashPassword = bcrypt.hashpw(strCode, salt)
                        dbPassword = cardDict['code'].encode("utf-8")

                        if hashPassword == dbPassword:
                            responseCode = self.logic.updateCardBalance(card)
                        else:
                            responseCode = "05" #Error de código
                    else:
                        responseCode = "54" #Error de fecha
                else:
                    responseCode = "08" #Error de nombre
            else:
                if cardDict['status'] == "Robada":
                    responseCode = "43"
                elif cardDict['status'] == "Perdida":
                    responseCode = "41"
                elif cardDict['status'] == "Inactiva":
                    responseCode = "54"
                else:
                    responseCode = "QA"
        else:
            responseCode = "14" #Error Numero Tarjeta
        #cardDict['balance'] = float(str(cardDict['balance']))
        return {"response": responseCode}

    def put(self):
        card = self.card_put_args.parse_args()
        rows = self.logic.insertCard(card)
        return {"rowsAffected": rows}

    def patch(self):
        data = self.card_put_args.parse_args()
        rows = self.logic.updateCardBalance(data)
        return {"rowsAffected": rows}