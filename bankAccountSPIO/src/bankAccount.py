'''
Created on Feb 25, 2014

@author: rafalb
'''
class bankAccountGeneral:
    def __init__(self, name, accountNumber):
        self._name, self._number = name, accountNumber    
   
class bankAccountROR(bankAccountGeneral):
    def __init__(self, name, accountNumber, initialAmount, debitFlag):
        bankAccountGeneral.__init__(self, name, accountNumber)
        self._balance = initialAmount
        self._debit = debitFlag
        self._history = []
        self._interestRate = interestRate2()
        
    def getNewAmount(self):
        newAmount = self._interestRate.getNewSaldo(self._balance)
        print 'newAmount %s' % newAmount 
        return(newAmount)
    
    def setNewInterestRate(self, newInterestRate):
        self._interestRate = newInterestRate
        
    def deposit(self, amount):
        self._balance += amount
        strAdd = 'operation: deposit, amount %s, balance: %s' % (amount, self._balance)
        self._history.append(strAdd)
        
    def withdraw(self, amount):
        success = False
        if (amount <= self._balance):
            self._balance -= amount
            success = True
        else:
            if (self._debit):
                self._balance -= amount
                success = True
                
        strAdd = 'operation: withdraw, amount %s, balance: %s' % (amount, self._balance)
        self._history.append(strAdd)
        return(success)      
                
    def setDebit(self, yesOrNo):
        self._debit = yesOrNo
        
    def writeInfo(self):
        strPrt = 'RORaccount: %s, %s, balance: %s, debitPossible? %s' % (self._name, self._number, self._balance, self._debit)
        print strPrt

    def getHistory(self):
        print "Number of entries: %s" % (len(self._history))
        for iii in range(len(self._history)):
            print self._history[iii]

class bankDeposit(bankAccountGeneral):
    def __init__(self, RORaccount, initialAmount, timeWindow, interestRate):
        bankAccountGeneral.__init__(self, RORaccount._name, RORaccount._number)
        self._initialAmount, self._timeWindow, self._interestRate = initialAmount, timeWindow, interestRate
        self._RORaccount = RORaccount
        
    def writeInfo(self):
        strPrt = 'depositAccount: %s, %s, initialAmount: %s, timeWindow %s, initerstRate %s' % (self._name, self._number, self._initialAmount, self._timeWindow, self._interestRate)
        print strPrt
        
    def getTimeWindow(self):
        return self._timeWindow

    def getInitialAmount(self):
        return self._initialAmount

    def getInteresRate(self):
        return self._interestRate

class bankLoan(bankAccountGeneral):
    def __init__(self, RORaccount, loanAmount, timeWindow, loanRate):
        bankAccountGeneral.__init__(self, RORaccount._name, RORaccount._number)
        self._loanAmount, self._timeWindow, self._loanRate = loanAmount, timeWindow, loanRate
        self._RORaccount = RORaccount
        
    def getLoanAmount(self):
        return float(self._loanAmount)
    
    def getTimeWindow(self):
        return float(self._timeWindow)
    
    def getLoanRate(self):
        return float(self._loanRate)

class Bank:
    def __init__(self):
        self._allAccounts = list()

    def getNumberOfAccounts(self):
        return (len(self._allAccounts))

    def printAllAcounts(self):
        for iii in range(len(self._allAccounts)):
            print "account: %s" % self._allAccounts[iii]
            
    def checkAccount(self, accountToBeChecked):
        taken = False
        for iii in range(len(self._allAccounts)):
            if (self._allAccounts[iii]==accountToBeChecked):
                taken = True
        return(taken)        
    
    def createRORaccount(self, name, initialAmount, debitFlag):
        #append only unique number
        #taken = self._allAccounts.checkAccount(self._number)
        #if (not taken):
        #    self._allAccounts._allAccounts.append(accountNumber)
        Acc = bankAccountROR(name, 12345678, initialAmount, debitFlag)
        
        return(Acc)

    def createBankDeposit(self, RORaccount, depositAmount, timeWindow, interestRate):
        success = RORaccount.withdraw(depositAmount)
        if (success):
            Acc = bankDeposit(RORaccount, depositAmount, timeWindow, interestRate)
        return(Acc)
    
    def removeBankDeposit(self, bankDeposit, monthsElapsed):
        if (monthsElapsed >= bankDeposit.getTimeWindow()):
            addedAmount = bankDeposit.getInitialAmount()*float(bankDeposit.getInteresRate())/100.0
        else:
            addedAmount = 0
            
        bankDeposit._RORaccount.deposit(addedAmount)
        
        del(bankDeposit)
        
    def createBankLoan(self, RORaccount, loanAmount, timeWindow, loanRate):
        RORaccount.deposit(loanAmount)
        #if (success):
        Acc = bankLoan(RORaccount, loanAmount, timeWindow, loanRate)
        return(Acc)
    
    def removeBankLoan(self, bankLoan, monthsElapsed):

        if (monthsElapsed == bankLoan.getTimeWindow()):
            additionalCharge = 1.0
        elif (monthsElapsed > bankLoan.getTimeWindow()):
            additionalCharge = 1 + (bankLoan.getTimeWindow()-monthsElapsed)/100.0
        else:
            additionalCharge = 1.01

        finalAmount = bankLoan.getLoanAmount()* ( additionalCharge*float(monthsElapsed)*bankLoan.getLoanRate()/1200.0 + 1.0)
        success = bankLoan._RORaccount.withdraw(finalAmount)
        if (not success):
            bankLoan._RORaccount.setDebit(True)
            bankLoan._RORaccount.withdraw(finalAmount)
            
        del(bankLoan)    

#
# State pattern design
#
class interestRate:
        
    def getNewSaldo(self, amount):
        return(amount*(1.0+self._rate/float(100.0)))
        
class interestRate1(interestRate):
    def __init__(self):
        self._rate = 5.0
        
class interestRate2(interestRate):
    def __init__(self):
        self._rate = 10.0
        
        
class debitWrapper:
    def __init__(self, RORaccount, maxDebit):
        self._RORaccount = RORaccount
        self._maxDebit = maxDebit
        self._currDebit = 0
        
    def writeInfo(self):
        self._RORaccount.writeInfo()

    def deposit(self, amount):
        if (self._currDebit > 0):
            tmp = self._currDebit - amount
            if (tmp > 0):
                self._currDebit = tmp
            else:
                self._currDebit = 0
                self._RORaccount.deposit(tmp)
        else:
            self._RORaccount.deposit(amount)
                
#    def getCurrDebit(self):


allAccounts1=Bank()
#Acc1 = allAccounts1.createRORaccount("Rafal Bachorz 1", 40000, False)
#Acc2 = allAccounts1.createRORaccount("Rafal Bachorz 2", 30000, False)
#Acc1.writeInfo()
#Acc2.writeInfo()
#Acc1.setDebit(True)
#success = Acc1.withdraw(100000)
#print success
#Acc1.writeInfo()

ROR1 = allAccounts1.createRORaccount("Rafal Bachorz 1", 40000, False)
ROR1.writeInfo()
DEP1 = allAccounts1.createBankDeposit(ROR1, 4000, 12, 6)
allAccounts1.removeBankDeposit(DEP1, 12)
ROR1.writeInfo()

ROR1debit = debitWrapper(ROR1, 1000)
ROR1debit.writeInfo()
ROR1debit.deposit(20)
ROR1debit.writeInfo()
#Acc3.writeInfo()
#Acc1.writeInfo()
#allAccounts1.removeBankDeposit(Acc3, 12)
#Acc1.writeInfo()
#Acc3 = allAccounts1.createBankLoan(Acc1, 200, 12, 6)
#Acc1.writeInfo()
#allAccounts1.removeBankLoan(Acc3, 12)
#Acc1.writeInfo()

#ZygaKonto = allAccounts1.createRORaccount("Zygmunt Solorz", 220, False)
#ZygaKonto.writeInfo()
#ZygaLoan = allAccounts1.createBankLoan(ZygaKonto, 200, 12, 6)
#ZygaKonto.writeInfo()
#allAccounts1.removeBankLoan(ZygaLoan,12)
#ZygaKonto.writeInfo()


#ZygmuntKonto = allAccounts1.createRORaccount("Zygmunt Solorz", 220, False)
#ZygmuntKonto.writeInfo()
#ZygmuntKonto.deposit(30)
#ZygmuntKonto.writeInfo()
#ZygmuntKonto.getNewAmount()


#print allAccounts1.getNumberOfAccounts()
#Acc1=bankAccountROR("Rafal Bachorz 1", 12345678, allAccounts1, 50000, False)
#Acc2=bankAccountROR("Rafal Bachorz 2", 12345679, allAccounts1, 50000, False)
#Acc3=bankAccountROR("Rafal Bachorz 3", 12345674, allAccounts1, 50000, False)
#Acc3.writeInfo()
#Acc3.setDebit(True)
#Acc3.writeInfo()

#print allAccounts1.getNumberOfAccounts()
#allAccounts1.printAllAcounts()
#print(allAccounts1.checkAccount(12345673))
#Acc1.deposit(100)
#Acc1.getHistory()
#Acc1.deposit(100)
#Acc1.withdraw(100)
#Acc1.getHistory()
#Acc1.writeInfo()
#Acc1.withdraw(50000)
#Acc1.writeInfo()

#Acc1.withdraw(101)
#Acc1.writeInfo()        

