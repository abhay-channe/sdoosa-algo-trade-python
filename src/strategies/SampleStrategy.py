import logging

from strategies.BaseStrategy import BaseStrategy
from utils.Utils import Utils
from trademgmt.Trade import Trade

# Each strategy has to be derived from BaseStrategy
class SampleStrategy(BaseStrategy):
  __instance = None

  @staticmethod
  def getInstance(): # singleton class
    if SampleStrategy.__instance == None:
      SampleStrategy.__instance = SampleStrategy()
    return SampleStrategy.__instance

  def __init__(self):
    if SampleStrategy.__instance != None:
      raise Exception("This class is a singleton!")
    # Call Base class constructor
    BaseStrategy.__init__(self, "SAMPLE")
    # Initialize all the properties specific to this strategy
    self.productType = "MIS"
    self.symbols = ["SBIN", "INFY", "TATASTEEL", "RELIANCE", "HDFCBANK", "CIPLA"]
    self.slPercentage = 1.1
    self.targetPerncetage = 2.2
    self.startTimestamp = Utils.getTimeOfToDay(9, 30, 0) # When to start the strategy. Default is Market start time
    self.stopTimestamp = Utils.getTimeOfToDay(12, 30, 0) # This is not square off timestamp. This is the timestamp after which no new trades will be placed under this strategy but existing trades continue to be active.
    self.squareOfTimestamp = Utils.getTimeOfToDay(15, 0, 0) # Square off time
    self.capital = 3000 # Capital to trade (This is the margin you allocate from your broker account for this strategy)
    self.leverage = 3 # 2x, 3x Etc
    self.maxTradesPerDay = 3 # Max number of trades per day under this strategy
    self.isFnO = False # Does this strategy trade in FnO or not
    self.capitalPerSet = 0 # Applicable if isFnO is True (1 set means 1CE/1PE or 2CE/2PE etc based on your strategy logic)

  def process(self):
    # This is a sample strategy with the following logic:
    # 1. If current market price > 0.5% from previous day close then create LONG trade
    # 2. If current market price < 0.5% from previous day close then create SHORT trade
    for symbol in self.symbols:
      quote = self.getQuote(symbol)
      if quote == None:
        logging.error('%s: Could not get quote for %s', self.getName(), symbol)
        continue
      longBreakoutPrice = Utils.roundToNSEPrice(quote.close + quote.close * 0.5 / 100)
      shortBreakoutPrice = Utils.roundToNSEPrice(quote.close - quote.close * 0.5 / 100)
      cmp = quote.lastTradedPrice
      logging.info('%s: %s => long = %f, short = %f, CMP = %f', self.getName(), symbol, longBreakoutPrice, shortBreakoutPrice, cmp)
      
      direction = None
      breakoutPrice = 0
      if cmp > longBreakoutPrice:
        direction = 'LONG'
        breakoutPrice = longBreakoutPrice
      elif cmp < shortBreakoutPrice:
        direction = 'SHORT'
        breakoutPrice = shortBreakoutPrice
      if direction == None:
        continue

      if symbol not in self.tradesCreatedSymbols:
        self.generateTrade(symbol, direction, breakoutPrice)


  def generateTrade(self, tradingSymbol, direction, breakoutPrice):
    trade = Trade(tradingSymbol)
    trade.strategy = self.getName()
    trade.direction = direction
    trade.productType = self.productType
    trade.placeMarketOrder = True
    trade.requestedEntry = breakoutPrice
    trade.qty = int(self.calculateCapitalPerTrade() / breakoutPrice)
    if direction == 'LONG':
      trade.stopLoss = Utils.roundToNSEPrice(breakoutPrice - breakoutPrice * self.slPercentage / 100)
    else:
      trade.stopLoss = Utils.roundToNSEPrice(breakoutPrice + breakoutPrice * self.slPercentage / 100)

    if direction == 'LONG':
      trade.target = Utils.roundToNSEPrice(breakoutPrice + breakoutPrice * self.targetPerncetage / 100)
    else:
      trade.target = Utils.roundToNSEPrice(breakoutPrice - breakoutPrice * self.targetPerncetage / 100)

    # currently just printing the details
    trade.printTrade()

    # add symbol to created list so that the trade will not be created again for the same symbol
    self.tradesCreatedSymbols.append(tradingSymbol)