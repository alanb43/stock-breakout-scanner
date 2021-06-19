# Stock Squeeze Scanner

Very simple to use squeeze scanner, detect squeezes within data retrieved from the price_retriever script.

To use: 

1. Install requirements
```console
$ pip3 install -r requirements.txt
```
2. Create sub-directory "datasets"
3. Update symbols.csv with desired symbols (currently have QTEC etf holdings)
5. Update price_retriever with desired time-frame for data, then run
```console
$ python3 price_retriever.py
```
4. Run squeeze_scanner
```console
$ python3 squeeze_scanner.py
```
5. Analyze the resulting output / graphs!


Notes:
* You may want to update lines 48 / 51 of squeeze_scanner with different indices 
    * currently scanning to see if in a squeeze or if coming out of a squeeze in the past 3 days
* You may want to add other / more specific conditions to squeeze_scanner for the graph function to be called, especially if handling many stocks
* Bollinger Bands:
    * upper/lower bands are 2 std dev above/below the sma, middle band is the sma
    * default sma calculation is the 20 day moving average
    * Potential Method 1
        * When we (price) exceed upper band, expect a reversal to sma/middle band, sellpoint / short
        * When we (price) go under lower band, expect reversal back upward, buypoint / long
    * Method 2
        * When we (price) exceed upper band, we ride the strong momentum and we ride along the top of upper BB
* Keltner's Channels:
    * Instead of bands tracking the stddev's from the sma, we'll have them be a multiple of the average
    * true range (ATR) above/below the middle line/channel, which we'll use the 20 day sma for (though the official definition uses the 20 day Exponential MA)
* When Bollinger Bands are within Keltner Channels (squeezed), low volatility is indicated. We then are looking for a breakout