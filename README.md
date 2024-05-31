# algorithm-backtest-app

Things to potentially do in backend in the future in no apparent order:

- [ ] add options for slippage, setting fees etc
- [ ] add more indicators
- [ ] add the option to chose partial or whole shares
- [ ] add the option to save algorithm using mongo db
- [ ] if performance sucks change dataframes to dictionaries to make searches faster

App will consist of a python backend, and a reactjs frontend.

Very very ealy in development.

PERSONAL NOTE:
Anything to do with years passed or anywhere in code where there is 365 or 365.25...
composer uses 252 becuase there are 252 trading days in year. If you want exact same values as composer
use 252. 365 and years passed makes more sense in my opinion. Lets say there are 12 trading days a year, once
a month. Even though there is not a trading day everyday you are still holding the asset and the price is still
changing everyday even if you cant trade on that day. Hence, for things like calculating annualized return
the time period makes sense to be 365 not 255 becuase the price of the asset changes every day. Your annualized return should take into account days that are not trading days becuase you are still holding the asset on those days and the price is still changing.
