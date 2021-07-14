from core.pyba_logic import PybaLogic
import bcrypt


class CardLogic(PybaLogic):
    def __init__(self):
        super().__init__()

    # get
    def getCardByNumber(self, number):
        database = self.createDatabaseObj()
        sql = f"SELECT * FROM thebank.products where number= '{number}';"
        result = database.executeQuery(sql)
        if len(result) != 0:
            return result[0]
        else:
            return {}

    # put
    def insertCard(self, card):
        database = self.createDatabaseObj()

        strBalance = card['balance']
        fBalance = float(strBalance)

        code = card['code']
        salt = bcrypt.gensalt(rounds=14)
        strSalt = salt.decode("utf-8")
        encCode = code.encode("utf-8")
        hashCode = bcrypt.hashpw(encCode, salt)
        strCode = hashCode.decode("utf-8")

        sql = (
            f"INSERT INTO `thebank`.`products`"
            + f"(`id`,`name`,`number`,`date`,`code`,`salt`,`balance`) "
            + f"VALUES(0,'{card['name']}','{card['number']}','{card['date']}','{strCode}','{card['status']}' "
            + f"'{strSalt}',{fBalance});"
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    # patch
    def updateCard(self, number, card):
        database = self.createDatabaseObj()

        code = card['Code']
        salt = bcrypt.gensalt(rounds=14)
        strSalt = salt.decode("utf-8")
        encCode = code.encode("utf-8")
        hashCode = bcrypt.hashpw(encCode, salt)
        strCode = hashCode.decode("utf-8")

        sql = (
            f"UPDATE `thebank`.`products` "
            + f"SET `name` = '{card['name']}',`date` = '{card['date']}',`code` = '{strCode}',"
            + f"`salt` = {strSalt},`balance` = {card['balance']},`status` = {card['status']},`limit` = {card['limit']} "
            + f"WHERE `number` = {number};"
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def updateCardBalance(self, data):
        database = self.createDatabaseObj()
        sql = f"SELECT * FROM thebank.products where number={data['number']};"
        result = database.executeQuery(sql)
        if len(result) != 0:
            cardDict = result[0]
            actualBalance = cardDict['balance']
            print(actualBalance)

        cardDigits = cardDict['number']
        cardType = cardDigits[0:4]

        if cardType == "7000": #Crédito
            newBalance = float(cardDict['balance']) + float(data['balance'])
            if newBalance > float(cardDict['limit']):
                return "61" #Excede el limite
        elif cardType == "6000": #Débito
            newBalance = float(cardDict['balance']) - data['balance']
            if newBalance < 0:
                return "51" #Saldo insuficiente
        else:
            return "QY" #Tipo de Tarjeta Invalido

        sql = (
            f"UPDATE `thebank`.`products` "
            + f"SET `balance` = {newBalance} "
            + f"WHERE `number` = {data['number']};"
        )
        rows = database.executeNonQueryRows(sql)
        return "00" #OK!
